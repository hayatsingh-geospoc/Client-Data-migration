"""Phase 2: profile the start of every data file inside every archive, without downloading archives.

For each file it fetches only the first --sample-kb of compressed bytes (one HTTP range request via
scripts/serve_drive.sh), decompresses in memory, and records encoding, delimiter, header, column types,
empties/placeholders, likely PII, malformed rows and masked sample values. Nothing is written to disk
except the reports.

Excel files must be fetched whole (xlsx is itself a zip), so they only run with --with-excel.
Nested archives (zip inside zip) are recorded as deferred.

Usage:
  scripts/serve_drive.sh &                  # start local read-only Drive server first
  .venv/bin/python -I scripts/profile_files.py [--archive TEXT] [--with-excel] [--workers 6]
Resumable: each profiled file is cached in reports/profile/<archive>/; rerun skips cached files.
"""
import argparse
import csv
import hashlib
import io
import json
import os
import re
import struct
import subprocess
import sys
import time
import zipfile
import zlib
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_zip import HttpRangeFile, http_range  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")
OUT = os.path.join(REPORTS, "profile")
ARCHIVE_SIZES = {}  # archive name -> bytes, filled in main()
LOCAL_ZIPS = {}  # archive name -> temp local copy (only while that archive is being profiled)
TMP = os.path.join(ROOT, "data", "tmp")
REMOTE = os.environ.get("LEADS_REMOTE", "clientdrive:1.2B Leads-sazag")

csv.field_size_limit(2**31 - 1)

PLACEHOLDERS = {"—", "–", "-", "--", "n/a", "na", "null", "none", "nan", "#n/a", "undefined", "nil", "?", "unknown", "0000-00-00"}
RE = {
    "email": re.compile(r"^[^@\s]+@[^@\s]+\.[a-z]{2,}$", re.I),
    "url": re.compile(r"^(https?://|www\.)\S+$", re.I),
    "date": re.compile(r"^(\d{4}-\d{1,2}-\d{1,2}([ T][\d:.]+Z?)?|\d{1,2}/\d{1,2}/\d{2,4}|\d{4}/\d{1,2}/\d{1,2})$"),
    "bool": re.compile(r"^(true|false|yes|no|y|n)$", re.I),
    "int": re.compile(r"^-?\d{1,18}$"),
    "float": re.compile(r"^-?(\d{1,3}(,\d{3})+|\d*)\.\d+$|^-?\d{1,3}(,\d{3})+$"),
    "phone": re.compile(r"^\+?[\d\s().-]{7,22}$"),
    "domain": re.compile(r"^[a-z0-9-]+(\.[a-z0-9-]+)*\.[a-z]{2,}$", re.I),
    "json": re.compile(r"^[\[{].*[\]}]$", re.S),
}
PII_HEADER = re.compile(r"e-?mail|phone|mobile|cell|tel\b|first.?name|last.?name|full.?name|person|contact.?name|"
                        r"address|street|zip|postal|birth|dob|gender|age\b|linkedin|facebook|twitter|instagram|ssn", re.I)
EMAIL_ANY = re.compile(r"([A-Za-z0-9])[A-Za-z0-9._%+-]*@")
PHONE_ANY = re.compile(r"\+?\d[\d\s().-]{6,}\d")
MASK_HEADER = re.compile(r"^n$|first.?name|last.?name|full.?name|person|contact.?name|address|street|birth|dob", re.I)


def classify(v):
    v = v.lstrip("'=\"")  # spreadsheet text markers like '+1 315-... or ="0123"
    for t in ("email", "url", "date", "bool", "int", "float"):
        if RE[t].match(v):
            return t
    if RE["phone"].match(v) and sum(ch.isdigit() for ch in v) >= 7:
        return "phone"
    if RE["domain"].match(v):
        return "domain"
    if RE["json"].match(v):
        return "json"
    return "text"


def mask(v, kind, header):
    if kind == "email":
        local, _, dom = v.partition("@")
        return f"{local[:1]}***@{dom}"
    if kind == "phone" or re.search(r"phone|mobile|cell|tel\b", header, re.I):
        return "***" + v[-2:]
    if MASK_HEADER.search(header):
        return v[:1] + "***"
    # Scrub emails / phone numbers embedded anywhere (lists like ['a@b.com'], odd headers like "e" or "t").
    v = EMAIL_ANY.sub(lambda m: m.group(1) + "***@", v)
    v = PHONE_ANY.sub(lambda m: "***" + m.group()[-2:] if sum(ch.isdigit() for ch in m.group()) >= 9 else m.group(), v)
    return v[:80]


def profile_table(header, rows, max_rows):
    """Column stats for a header + iterable of rows (lists of strings)."""
    ncols = len(header)
    width = Counter()
    cols = [{"non_empty": 0, "empty": 0, "placeholder": Counter(), "types": Counter(), "max_len": 0,
             "distinct": set(), "samples": []} for _ in range(ncols)]
    n = 0
    for row in rows:
        n += 1
        width[len(row)] += 1
        for i in range(min(ncols, len(row))):
            v = (row[i] or "").strip()
            c = cols[i]
            if not v:
                c["empty"] += 1
                continue
            if v.lower() in PLACEHOLDERS:
                c["placeholder"][v] += 1
                continue
            c["non_empty"] += 1
            c["max_len"] = max(c["max_len"], len(v))
            k = classify(v)
            c["types"][k] += 1
            if len(c["distinct"]) < 1000:
                c["distinct"].add(v)
            if len(c["samples"]) < 3 and v not in c["samples"]:
                c["samples"].append(v)
        if n >= max_rows:
            break
    out_cols = []
    for i, (h, c) in enumerate(zip(header, cols)):
        dominant = c["types"].most_common(1)[0][0] if c["types"] else "empty"
        if dominant == "int" and PII_HEADER.search(h or "") and re.search(r"phone|mobile|cell|tel", h or "", re.I):
            dominant = "phone"
        pii = bool(PII_HEADER.search(h or "")) or dominant in ("email", "phone")
        out_cols.append({
            "index": i, "header": h, "inferred_type": dominant, "type_votes": dict(c["types"]),
            "non_empty": c["non_empty"], "empty": c["empty"], "placeholders": dict(c["placeholder"]),
            "fill_pct": round(100 * c["non_empty"] / n, 1) if n else 0, "max_len": c["max_len"],
            "distinct_in_sample": len(c["distinct"]) if len(c["distinct"]) < 1000 else ">=1000",
            "pii_suspect": pii, "samples": [mask(s, classify(s), h or "") for s in c["samples"]],
        })
    malformed = sum(cnt for w, cnt in width.items() if w != ncols)
    return n, malformed, dict(width), out_cols


def schema_id(header):
    norm = "|".join(re.sub(r"\s+", " ", (h or "").strip().lower()) for h in header)
    return hashlib.sha1(norm.encode()).hexdigest()[:10]


def decode(raw, truncated):
    if truncated:  # cut at last newline so we never parse a half row / half utf-8 char
        cut = max(raw.rfind(b"\n"), raw.rfind(b"\r"))
        raw = raw[:cut + 1] if cut > 0 else raw
    bom = raw.startswith(b"\xef\xbb\xbf")
    for enc in ("utf-8-sig", "cp1252"):
        try:
            return raw.decode(enc), enc, bom, 0
        except UnicodeDecodeError:
            pass
    text = raw.decode("utf-8", errors="replace")
    return text, "utf-8 (with invalid bytes)", bom, text.count("�")


def fetch_member_head(archive, info, sample_bytes):
    """Decompressed first bytes of a zip member using one range request. Returns (bytes, truncated)."""
    want = min(sample_bytes, info.compress_size)
    end = min(info.header_offset + 30 + 4096 + want, ARCHIVE_SIZES[archive]) - 1
    if archive in LOCAL_ZIPS:
        with open(LOCAL_ZIPS[archive], "rb") as fh:
            fh.seek(info.header_offset)
            data = fh.read(end - info.header_offset + 1)
    else:
        data = http_range(archive, info.header_offset, end)
    if data[:4] != b"PK\x03\x04":
        raise ValueError("bad local header signature")
    name_len, extra_len = struct.unpack("<HH", data[26:30])
    start = 30 + name_len + extra_len
    payload = data[start:start + want]
    if info.compress_type == zipfile.ZIP_STORED:
        out = payload
    elif info.compress_type == zipfile.ZIP_DEFLATED:
        out = zlib.decompressobj(-15).decompress(payload)
    else:
        raise ValueError(f"unsupported compression {info.compress_type}")
    complete = want == info.compress_size
    if complete and zlib.crc32(out) != info.CRC:
        raise ValueError("CRC mismatch on full member")
    return out, not complete


def profile_delimited(raw, truncated, info, max_rows):
    text, enc, bom, bad = decode(raw, truncated)
    head = text[:65536]
    try:
        delim = csv.Sniffer().sniff(head, delimiters=",;\t|").delimiter
    except csv.Error:
        delim = ","
    # Sniffer sometimes picks "," for tab files (e.g. Apollo); trust the header line if it clearly disagrees.
    first_line = head.splitlines()[0] if head else ""
    counts = {d: first_line.count(d) for d in ",;\t|"}
    best = max(counts, key=counts.get)
    if counts[best] > counts.get(delim, 0):
        delim = best
    crlf = text.count("\r\n")
    cr, lf = text.count("\r") - crlf, text.count("\n") - crlf
    line_endings = "+".join(k for k, v in (("crlf", crlf), ("cr", cr), ("lf", lf)) if v) or "none"
    # newline="" lets csv handle \r, \n and \r\n row endings (old-Mac \r-only files otherwise fail)
    rows = list(csv.reader(io.StringIO(text, newline=""), delimiter=delim))
    if truncated and rows:
        rows.pop()  # last record may be cut mid-quote
    if not rows:
        return {"kind": "delimited", "status": "empty", "encoding": enc}
    header, body = rows[0], rows[1:]
    n, malformed, widths, cols = profile_table(header, body, max_rows)
    used = len(text.encode("utf-8"))
    est = n if not truncated else int(n * info.file_size / max(used, 1))
    return {"kind": "delimited", "status": "ok", "encoding": enc, "bom": bom, "invalid_chars": bad,
            "delimiter": delim, "line_endings": line_endings, "n_cols": len(header), "header": header, "schema_id": schema_id(header),
            "sample_rows": n, "complete_file": not truncated, "est_total_rows": est,
            "row_count_is_estimate": truncated, "malformed_rows_in_sample": malformed,
            "row_widths": widths, "columns": cols}


def flatten_keys(obj, prefix="", depth=0, out=None):
    out = {} if out is None else out
    for k, v in obj.items():
        key = f"{prefix}{k}"
        t = type(v).__name__ if v is not None else "null"
        if isinstance(v, (list, str, dict)) and not v:
            t = "empty"
        out[key] = t
        if isinstance(v, dict) and depth < 1:
            flatten_keys(v, key + ".", depth + 1, out)
    return out


def profile_json(raw, truncated, info, max_rows):
    text, enc, bom, bad = decode(raw, truncated)
    s = text.lstrip()
    if s.startswith("["):
        return {"kind": "json", "status": "json_array_needs_streaming_parser", "encoding": enc, "first_chars": s[:200]}
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if truncated and lines:
        lines.pop()
    keys, types, bad_lines, n = Counter(), defaultdict(Counter), 0, 0
    for ln in lines[:max_rows]:
        try:
            obj = json.loads(ln)
        except ValueError:
            bad_lines += 1
            continue
        n += 1
        for k, t in flatten_keys(obj).items():
            keys[k] += 1
            types[k][t] += 1
    used = len(text.encode("utf-8"))
    return {"kind": "ndjson", "status": "ok" if n else "unparsed", "encoding": enc, "sample_rows": n,
            "bad_lines": bad_lines, "est_total_rows": int(n * info.file_size / max(used, 1)) if truncated else n,
            "row_count_is_estimate": truncated,
            "fields": [{"key": k, "present_pct": round(100 * c / n, 1), "types": dict(types[k]),
                        "pii_suspect": bool(PII_HEADER.search(k))} for k, c in keys.most_common()]}


def profile_xlsx(archive, info, max_rows):
    import openpyxl
    raw, _ = fetch_member_head(archive, info, info.compress_size)
    wb = openpyxl.load_workbook(io.BytesIO(raw), read_only=True, data_only=True)
    sheets = []
    for ws in wb.worksheets:
        it = ws.iter_rows(values_only=True)
        header = next(it, None)
        if header is None:
            sheets.append({"sheet": ws.title, "status": "empty"})
            continue
        header = ["" if h is None else str(h) for h in header]
        rows = ([("" if v is None else str(v)) for v in r] for r in it)
        n, malformed, widths, cols = profile_table(header, rows, max_rows)
        sheets.append({"sheet": ws.title, "status": "ok", "reported_max_row": ws.max_row, "n_cols": len(header),
                       "header": header, "schema_id": schema_id(header), "sample_rows": n, "columns": cols})
    wb.close()
    return {"kind": "xlsx", "status": "ok", "sheets": sheets,
            "est_total_rows": sum((s.get("reported_max_row") or 1) - 1 for s in sheets if s["status"] == "ok")}


def profile_member(archive, info, args):
    name = info.filename
    base = name.rsplit("/", 1)[-1]
    ext = base.rsplit(".", 1)[-1].lower() if "." in base else ""
    rec = {"archive": archive, "member": name, "ext": ext, "compressed": info.compress_size,
           "uncompressed": info.file_size}
    t0 = time.time()
    try:
        if name.startswith("__MACOSX/") or base.startswith("._"):
            rec.update(kind="macos_junk", status="skipped")
        elif ext in ("zip", "7z", "rar", "gz"):
            rec.update(kind="nested_archive", status="deferred")
        elif ext in ("docx", "doc", "pdf"):
            rec.update(kind="document", status="skipped_non_data")
        elif ext in ("xlsx", "xlsm"):
            if not (args.with_excel or archive in LOCAL_ZIPS):
                rec.update(kind="xlsx", status="deferred_excel")
            else:
                rec.update(profile_xlsx(archive, info, args.max_rows))
        else:
            raw, truncated = fetch_member_head(archive, info, args.sample_kb * 1024)
            first = raw.lstrip()[:1]
            if ext == "json" or first in (b"{", b"["):
                rec.update(profile_json(raw, truncated, info, args.max_rows))
            else:
                rec.update(profile_delimited(raw, truncated, info, args.max_rows))
    except Exception as e:
        rec.update(status="error", error=repr(e)[:500])
    rec["seconds"] = round(time.time() - t0, 1)
    return rec


def download_chunked(archive, size, dest, chunk=64 * 2**20):
    """Sequential download in range chunks (each retried) so one stalled Drive connection can't hang the run."""
    with open(dest, "wb") as fh:
        for start in range(0, size, chunk):
            fh.write(http_range(archive, start, min(start + chunk, size) - 1))
            if (start // chunk) % 4 == 3:
                print(f"   downloaded {min(start + chunk, size) / 2**20:.0f}/{size / 2**20:.0f} MB", flush=True)
    if os.path.getsize(dest) != size:
        raise IOError(f"temp download size mismatch for {archive}")


def cache_path(archive, member):
    d = os.path.join(OUT, hashlib.sha1(archive.encode()).hexdigest()[:12])
    return os.path.join(d, hashlib.sha1(member.encode()).hexdigest()[:16] + ".json")


def remask(rec):
    """Re-apply current masking to cached samples (idempotent), so masking fixes reach old cache files."""
    for s in (rec.get("sheets") or [rec]):
        if "header" in s:
            # A "header" made of emails/phones/urls/numbers means the file has no header row (first row is data).
            kinds = [classify(h.strip()) for h in s["header"] if h and h.strip()]
            s["header_looks_like_data"] = sum(k in ("email", "phone", "url", "int", "float", "date") for k in kinds) >= 2
            s["header"] = [mask(h, classify(h), "") for h in s["header"]]
        for c in s.get("columns", []):
            c["header"] = mask(c["header"] or "", classify(c["header"] or ""), "")
            c["samples"] = [mask(v, classify(v), c["header"] or "") for v in c["samples"]]
    return rec


def write_reports():
    recs = []
    for root, _, files in os.walk(OUT):
        for f in files:
            if f.endswith(".json"):
                p = os.path.join(root, f)
                rec = remask(json.load(open(p)))
                json.dump(rec, open(p, "w"), indent=1)
                recs.append(rec)
    recs.sort(key=lambda r: (r["archive"], r["member"]))

    with open(os.path.join(REPORTS, "profile_files.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["archive", "member", "kind", "status", "encoding", "delimiter", "n_cols", "schema_id",
                    "sample_rows", "est_total_rows", "row_count_is_estimate", "malformed_rows_in_sample",
                    "pii_columns", "uncompressed_bytes", "error"])
        for r in recs:
            sheets = r.get("sheets") or [r]
            for s in sheets:
                pii = [c["header"] for c in s.get("columns", []) if c["pii_suspect"]] + \
                      [f["key"] for f in r.get("fields", []) if f["pii_suspect"]]
                w.writerow([r["archive"], r["member"] + (f" [{s['sheet']}]" if "sheet" in s else ""),
                            r.get("kind"), s.get("status", r.get("status")), r.get("encoding"), r.get("delimiter"),
                            s.get("n_cols"), s.get("schema_id"), s.get("sample_rows"),
                            s.get("reported_max_row", r.get("est_total_rows")) if "sheet" in s else r.get("est_total_rows"),
                            r.get("row_count_is_estimate"), r.get("malformed_rows_in_sample"),
                            "; ".join(pii), r["uncompressed"], r.get("error", "")])

    schemas = {}
    for r in recs:
        for s in (r.get("sheets") or [r]):
            sid = s.get("schema_id")
            if not sid:
                continue
            e = schemas.setdefault(sid, {"schema_id": sid, "header": s["header"], "n_cols": len(s["header"]),
                                          "files": 0, "archives": Counter(), "est_rows": 0, "example": r["member"],
                                          "columns": s.get("columns", [])})
            e["files"] += 1
            e["archives"][r["archive"]] += 1
            e["est_rows"] += (s.get("reported_max_row") or 1) - 1 if "sheet" in s else (r.get("est_total_rows") or 0)
    sch = sorted(schemas.values(), key=lambda e: -e["est_rows"])
    for e in sch:
        e["archives"] = dict(e["archives"])
    json.dump(sch, open(os.path.join(REPORTS, "schemas.json"), "w"), indent=1)

    status = Counter((r.get("kind"), r.get("status")) for r in recs)
    by_arch = defaultdict(lambda: {"files": 0, "schemas": set(), "est_rows": 0, "errors": 0, "deferred": 0,
                                   "pii": set(), "encodings": Counter(), "malformed": 0})
    for r in recs:
        a = by_arch[r["archive"]]
        a["files"] += 1
        a["est_rows"] += r.get("est_total_rows") or 0
        a["errors"] += r.get("status") == "error"
        a["deferred"] += str(r.get("status", "")).startswith("deferred")
        a["malformed"] += r.get("malformed_rows_in_sample") or 0
        if r.get("encoding"):
            a["encodings"][r["encoding"]] += 1
        for s in (r.get("sheets") or [r]):
            if s.get("schema_id"):
                a["schemas"].add(s["schema_id"])
            a["pii"].update(c["inferred_type"] if c["inferred_type"] in ("email", "phone") else "name/addr/social"
                            for c in s.get("columns", []) if c["pii_suspect"])
        if r.get("kind") == "ndjson":
            a["pii"].update(["(json fields)"] if any(f["pii_suspect"] for f in r["fields"]) else [])

    L = ["# Data profile (Phase 2, sampled)", "",
         "Row counts are **estimates** from a sample (bytes ratio) unless the whole file fit in the sample. "
         "Exact counts need a full streaming pass.", "",
         f"Files profiled: {len(recs)} | Distinct column layouts (schemas): {len(sch)}", "",
         "## Status", "", "| Kind | Status | Files |", "|---|---|---:|"]
    L += [f"| {k} | {s} | {n} |" for (k, s), n in status.most_common()]
    L += ["", "## Per archive", "",
          "| Archive | Files | Schemas | Est. rows | Encodings | Malformed rows (sample) | PII types | Errors | Deferred |",
          "|---|---:|---:|---:|---|---:|---|---:|---:|"]
    for name, a in sorted(by_arch.items(), key=lambda kv: -kv[1]["est_rows"]):
        L.append(f"| {name} | {a['files']} | {len(a['schemas'])} | {a['est_rows']:,} | "
                 f"{', '.join(f'{k}:{v}' for k, v in a['encodings'].items())} | {a['malformed']} | "
                 f"{', '.join(sorted(a['pii']))} | {a['errors']} | {a['deferred']} |")
    L += ["", "## Largest schemas (by estimated rows)", ""]
    for e in sch[:40]:
        L.append(f"- `{e['schema_id']}` — {e['n_cols']} cols, {e['files']} files, ~{e['est_rows']:,} rows, "
                 f"archives: {', '.join(a[8:40] for a in e['archives'])}  ")
        L.append(f"  columns: {', '.join(h[:30] for h in e['header'][:25])}{' …' if e['n_cols'] > 25 else ''}")
    errs = [r for r in recs if r.get("status") == "error"]
    if errs:
        L += ["", "## Errors", ""] + [f"- {r['archive']} / {r['member']}: {r['error'][:200]}" for r in errs[:50]]
    open(os.path.join(REPORTS, "profile.md"), "w").write("\n".join(L) + "\n")
    print(f"reports: profile.md, profile_files.csv, schemas.json ({len(recs)} files, {len(sch)} schemas)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", help="only archives whose name contains this text")
    ap.add_argument("--with-excel", action="store_true", help="also profile xlsx (downloads whole xlsx members)")
    ap.add_argument("--sample-kb", type=int, default=256, help="compressed KB to fetch per file")
    ap.add_argument("--max-rows", type=int, default=5000)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--local-min-files", type=int, default=50,
                    help="archives with at least this many files are temp-downloaded whole")
    ap.add_argument("--local-max-mb", type=int, default=1500, help="...if the archive is at most this big")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()
    if args.report_only:
        return write_reports()

    listing = json.load(open(os.path.join(REPORTS, "drive_listing.json")))
    archives = sorted((e for e in listing if not e["IsDir"]), key=lambda e: e["Size"])
    if args.archive:
        archives = [e for e in archives if args.archive.lower() in e["Path"].lower()]

    for e in archives:
        name = e["Path"]
        ARCHIVE_SIZES[name] = e["Size"]
        with zipfile.ZipFile(HttpRangeFile(name, e["Size"])) as z:
            infos = [i for i in z.infolist() if not i.is_dir()]
        # Many small files: one sequential download beats hundreds of slow (~20s) Drive range requests.
        local_ok = len(infos) >= args.local_min_files and e["Size"] <= args.local_max_mb * 2**20
        todo = []
        for i in infos:
            p = cache_path(name, i.filename)
            if os.path.exists(p):
                cached = json.load(open(p))
                if not ((args.with_excel or local_ok) and cached.get("status") == "deferred_excel"):
                    continue
            todo.append(i)
        print(f"== {name}: {len(infos)} files, {len(todo)} to profile", flush=True)
        if not todo:
            continue
        local = None
        try:
            if local_ok:
                os.makedirs(TMP, exist_ok=True)
                local = os.path.join(TMP, f"{e['ID']}.zip")
                print(f"   temp download {e['Size'] / 2**20:.0f} MB (deleted after profiling)", flush=True)
                try:
                    download_chunked(name, e["Size"], local)
                    LOCAL_ZIPS[name] = local
                except Exception as ex:
                    print(f"   temp download failed, falling back to remote reads: {ex!r}"[:300], flush=True)
            done = 0
            with ThreadPoolExecutor(args.workers) as ex:
                futs = {ex.submit(profile_member, name, i, args): i for i in todo}
                for f in as_completed(futs):
                    rec = f.result()
                    done += 1
                    if rec["status"] != "error":  # errors are retried on the next run
                        os.makedirs(os.path.dirname(cache_path(name, rec["member"])), exist_ok=True)
                        json.dump(rec, open(cache_path(name, rec["member"]), "w"), indent=1)
                    if rec["status"] == "error" or done % 50 == 0 or done == len(todo):
                        print(f"   [{done}/{len(todo)}] {rec['status']} {rec['member'][-60:]} "
                              f"{rec.get('error', '')[:120]}", flush=True)
        finally:
            LOCAL_ZIPS.pop(name, None)
            if local and os.path.exists(local):
                os.remove(local)
    write_reports()


if __name__ == "__main__":
    main()
