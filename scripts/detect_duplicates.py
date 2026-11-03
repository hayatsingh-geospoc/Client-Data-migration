"""Phase 4a: find files that are exact copies of each other, across and within archives.

Uses the CRC-32 + uncompressed size stored in each ZIP's central directory (no file content is downloaded).
Same CRC + same size + size > 0 => almost certainly identical content. Nested archives (zip in zip) are not
included here (their directories are inside compressed data); they were compared by name + size in Phase 2.

Usage: python3 -I scripts/detect_duplicates.py      (needs scripts/serve_drive.sh running)
Outputs:
  reports/crc/<drive_id>.json      per-archive cache (resume)
  reports/file_duplicates.csv      one row per file that has at least one identical copy
  reports/file_duplicates.md       summary: archive pairs, bytes and estimated rows duplicated
"""
import csv
import json
import os
import sys
import zipfile
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_zip import HttpRangeFile  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")
CACHE = os.path.join(REPORTS, "crc")


def short(a):
    return a.replace("Copy of ", "").replace(".zip", "")


def load_dir(entry):
    path = os.path.join(CACHE, entry["ID"] + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    with zipfile.ZipFile(HttpRangeFile(entry["Path"], entry["Size"])) as z:
        files = [{"member": i.filename, "crc": f"{i.CRC:08x}", "size": i.file_size}
                 for i in z.infolist() if not i.is_dir()]
    json.dump(files, open(path, "w"))
    return files


def main():
    os.makedirs(CACHE, exist_ok=True)
    listing = [e for e in json.load(open(os.path.join(REPORTS, "drive_listing.json"))) if not e["IsDir"]]
    est = {}
    for r in csv.DictReader(open(os.path.join(REPORTS, "profile_files.csv"))):
        member = r["member"].split(" [")[0]  # xlsx rows carry " [sheet]"
        est[(r["archive"], member)] = est.get((r["archive"], member), 0) + int(r["est_total_rows"] or 0)

    groups = defaultdict(list)
    for n, e in enumerate(sorted(listing, key=lambda e: e["Size"]), 1):
        files = load_dir(e)
        print(f"[{n}/{len(listing)}] {short(e['Path'])}: {len(files)} files", flush=True)
        for f in files:
            name = f["member"].rsplit("/", 1)[-1]
            if f["size"] == 0 or f["member"].startswith("__MACOSX/") or name.startswith("._"):
                continue
            groups[(f["crc"], f["size"])].append((e["Path"], f["member"]))

    dups = {k: v for k, v in groups.items() if len(v) > 1}
    rows = []
    pair = defaultdict(lambda: {"files": 0, "bytes": 0, "rows": 0})
    within = Counter()
    extra_bytes = extra_rows = 0
    for gid, ((crc, size), members) in enumerate(sorted(dups.items(), key=lambda kv: -kv[0][1]), 1):
        keep = members[0]  # first copy counts as the original; the rest are redundant
        extra_bytes += size * (len(members) - 1)
        extra_rows += est.get(keep, 0) * (len(members) - 1)
        archives = sorted({a for a, _ in members})
        if len(archives) == 1:
            within[archives[0]] += len(members) - 1
        for i, a in enumerate(archives):
            for b in archives[i + 1:]:
                p = pair[(a, b)]
                p["files"] += 1
                p["bytes"] += size
                p["rows"] += est.get(keep, 0)
        for a, m in members:
            rows.append({"group": gid, "crc32": crc, "bytes": size, "copies": len(members),
                         "archive": a, "member": m, "est_rows": est.get((a, m), "")})

    with open(os.path.join(REPORTS, "file_duplicates.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["group", "crc32", "bytes", "copies", "archive", "member", "est_rows"])
        w.writeheader()
        w.writerows(rows)

    total_files = sum(len(v) for v in groups.values())
    total_bytes = sum(k[1] * len(v) for k, v in groups.items())
    L = ["# Exact file duplicates (Phase 4a)", "",
         "Based on CRC-32 + size from ZIP directories (no content downloaded). Same CRC and size => identical "
         "file with near certainty. Nested archives were checked separately by name + size (see profile.md).", "",
         f"Files checked: {total_files:,} ({total_bytes / 2**30:.1f} GiB uncompressed)", "",
         f"Duplicate groups: {len(dups):,} | redundant copies: {sum(len(v) - 1 for v in dups.values()):,} | "
         f"redundant data: {extra_bytes / 2**30:.2f} GiB | redundant rows (est.): ~{extra_rows:,}", "",
         "## Copies shared between archives", "",
         "| Archive A | Archive B | Identical files | GiB | Est. rows |", "|---|---|---:|---:|---:|"]
    for (a, b), p in sorted(pair.items(), key=lambda kv: -kv[1]["bytes"]):
        L.append(f"| {short(a)} | {short(b)} | {p['files']:,} | {p['bytes'] / 2**30:.2f} | {p['rows']:,} |")
    L += ["", "## Copies inside the same archive", "", "| Archive | Redundant copies |", "|---|---:|"]
    L += [f"| {short(a)} | {n:,} |" for a, n in within.most_common()]
    open(os.path.join(REPORTS, "file_duplicates.md"), "w").write("\n".join(L) + "\n")
    print(f"\n{len(dups)} duplicate groups, {extra_bytes / 2**30:.2f} GiB redundant -> reports/file_duplicates.md")


if __name__ == "__main__":
    main()
