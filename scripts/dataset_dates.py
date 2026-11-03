"""Estimate how recent each dataset is, and rank datasets newest-first (survivorship priority).

Evidence per archive (no file content downloaded):
  1. dates in file / folder / archive names  (Pitchbook 2025-09-14, crunchbase-2024-08-31, cafe_2023_07_17, Jan.2023)
  2. file modification times stored in the ZIP directory (when the export files were written)
  3. date-like columns in the profiled samples (Research Date, Last Updated, created_at, ...)

data_as_of = name date if any, else newest sampled row date, else median ZIP file time.
priority   = 1 for the newest dataset, 2 for the next, ... (ties: alphabetical).

Usage: python3 -I scripts/dataset_dates.py     (needs scripts/serve_drive.sh running for step 2)
Outputs: config/datasets.csv (seed for catalog.datasets), reports/dataset_dates.md
"""
import csv
import datetime as dt
import glob
import json
import os
import re
import statistics
import sys
import zipfile
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_zip import HttpRangeFile  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS = os.path.join(ROOT, "reports")
CACHE = os.path.join(REPORTS, "mtimes")
MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
# Only columns that say when the record was collected/refreshed. Not start/founded/created dates: those describe
# the person or company (job start, store creation), not the age of the data.
DATE_COL = re.compile(r"last ?updated|updated ?at|research ?date|vacuumed|scraped|last ?seen|as ?of|collected|last ?verified|verified ?at", re.I)


def short(a):
    return re.sub(r"\.zip$", "", a.replace("Copy of ", ""))


def safe_date(y, m, d):
    try:
        x = dt.date(int(y), int(m), int(d))
        return x if dt.date(2015, 1, 1) <= x <= dt.date.today() else None
    except ValueError:
        return None


def dates_in_name(text):
    out = []
    for y, m, d in re.findall(r"(20\d\d)[-_.](\d\d)[-_.](\d\d)", text):
        out.append(safe_date(y, m, d))
    for y, m, d in re.findall(r"(20\d\d)(\d\d)(\d\d)T\d{6}", text):
        out.append(safe_date(y, m, d))
    for mon, y in re.findall(r"\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[ .\-_]?(20\d\d)\b", text, re.I):
        out.append(safe_date(y, MONTHS[mon.lower()], 1))
    return [d for d in out if d]


def parse_sample_date(v):
    v = v.strip()
    m = re.match(r"^(20\d\d)-(\d{1,2})-(\d{1,2})", v)
    if m:
        return safe_date(*m.groups())
    m = re.match(r"^(\d{1,2})/(\d{1,2})/(20\d\d)", v)
    if m:
        return safe_date(m.group(3), m.group(1), m.group(2))
    return None


def zip_mtimes(entry):
    path = os.path.join(CACHE, entry["ID"] + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    with zipfile.ZipFile(HttpRangeFile(entry["Path"], entry["Size"])) as z:
        times = [list(i.date_time[:3]) for i in z.infolist()
                 if not i.is_dir() and not i.filename.startswith("__MACOSX/")
                 and not i.filename.rsplit("/", 1)[-1].startswith("._")]
    json.dump(times, open(path, "w"))
    return times


def main():
    os.makedirs(CACHE, exist_ok=True)
    listing = sorted((e for e in json.load(open(os.path.join(REPORTS, "drive_listing.json"))) if not e["IsDir"]),
                     key=lambda e: e["Size"])

    # row-level date columns from profiles (3 samples per column: weak but real evidence)
    row_dates = defaultdict(list)
    row_cols = defaultdict(Counter)
    for f in glob.glob(os.path.join(REPORTS, "profile", "*", "*.json")):
        r = json.load(open(f))
        top = r["archive"].split(" :: ")[0]
        for s in (r.get("sheets") or [r]):
            for c in s.get("columns", []):
                if DATE_COL.search(c.get("header") or ""):
                    ds = [d for d in (parse_sample_date(v) for v in c.get("samples", [])) if d]
                    if ds:
                        row_dates[top] += ds
                        row_cols[top][c["header"]] += 1

    # members per archive (for name dates)
    members = defaultdict(list)
    for r in csv.DictReader(open(os.path.join(REPORTS, "inventory_members.csv"))):
        if r["macos_junk"] == "False":
            members[r["archive"]].append(r["member_path"])

    # dataset kind from the column mapping (row-weighted)
    kind_rows = defaultdict(Counter)
    for r in csv.DictReader(open(os.path.join(REPORTS, "column_mapping.csv"))):
        if r["col_index"] == "0":
            for a in r["archives"].split(" | "):
                kind_rows[a.strip()][r["dataset_kind"]] += int(r["est_rows"] or 0)

    rows = []
    for n, e in enumerate(listing, 1):
        a = e["Path"]
        print(f"[{n}/{len(listing)}] {short(a)}", flush=True)
        name_ds = dates_in_name(a) + [d for p in members[a] for d in dates_in_name(p)]
        named_files = sum(1 for p in members[a] if dates_in_name(p))
        mt = [safe_date(*t) for t in zip_mtimes(e)]
        mt = sorted(d for d in mt if d)
        rd = sorted(row_dates.get(a, []))
        if name_ds:
            as_of, basis = max(name_ds), f"file/folder names ({named_files} of {len(members[a])} files dated)"
        elif rd:
            as_of, basis = rd[-1], "newest sampled row date (" + ", ".join(h for h, _ in row_cols[a].most_common(2)) + ")"
        elif mt:
            as_of, basis = mt[len(mt) // 2], "median file time inside the ZIP"
        else:
            as_of, basis = None, "no evidence"
        k = kind_rows.get(a.replace("Copy of ", "")[:45], Counter())
        kind = "person" if k.get("person", 0) >= k.get("company/other", 0) else "company"
        rows.append({
            "dataset": short(a), "archive": a, "dataset_kind": kind,
            "data_as_of": as_of.isoformat() if as_of else "", "date_basis": basis,
            "name_dates": f"{min(name_ds)} .. {max(name_ds)}" if name_ds else "",
            "zip_file_times": f"{mt[0]} .. {mt[-1]} (median {mt[len(mt) // 2]})" if mt else "",
            "sampled_row_dates": f"{rd[0]} .. {rd[-1]}" if rd else "",
        })

    rows.sort(key=lambda r: (r["data_as_of"] == "", [-int(x) for x in r["data_as_of"].split("-")] if r["data_as_of"] else [], r["dataset"]))
    for i, r in enumerate(rows, 1):
        r["priority"] = i

    os.makedirs(os.path.join(ROOT, "config"), exist_ok=True)
    cols = ["priority", "dataset", "dataset_kind", "data_as_of", "date_basis", "name_dates", "zip_file_times",
            "sampled_row_dates", "archive"]
    with open(os.path.join(ROOT, "config", "datasets.csv"), "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    L = ["# Dataset recency and ranking", "",
         "Survivorship rule (decided 2026-10-31): when sources disagree, the value from the dataset with the better "
         "(lower) priority wins; priority is assigned by how recent each dataset's data is.", "",
         "`data_as_of` = date in file/folder names if any, else newest sampled row date, else median file time "
         "inside the ZIP. ZIP file times show when the export files were written, which bounds how old the data "
         "is; they are not a guarantee of collection date.", "",
         "| Priority | Dataset | Kind | data_as_of | Basis | Name dates | ZIP file times | Sampled row dates |",
         "|---:|---|---|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['priority']} | {r['dataset']} | {r['dataset_kind']} | {r['data_as_of'] or '?'} | {r['date_basis']} | "
                 f"{r['name_dates']} | {r['zip_file_times']} | {r['sampled_row_dates']} |")
    open(os.path.join(REPORTS, "dataset_dates.md"), "w").write("\n".join(L) + "\n")
    print("wrote config/datasets.csv and reports/dataset_dates.md")


if __name__ == "__main__":
    main()
