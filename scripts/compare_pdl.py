"""Phase 4b: is PeopleDataLabs_416M.json the same data as PeopleDataLabs_chunk_*.csv?

Reads only the first --sample-kb (compressed) of the JSON and of chunk_1.csv (plus the last chunk for row
counting), compares records by normalized LinkedIn URL and by full content, and prints counts only (no PII).

Usage: python3 -I scripts/compare_pdl.py     (needs scripts/serve_drive.sh running)
"""
import argparse
import ast
import csv
import hashlib
import io
import json
import os
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import profile_files as pf  # noqa: E402
from remote_zip import HttpRangeFile  # noqa: E402

ARCHIVE = "Copy of People Datalabs Database 415,821,844.zip"
FIELDS = ["a", "e", "liid", "linkedin", "n", "t"]


def norm_url(u):
    u = (u or "").strip().lower().split("?")[0].rstrip("/")
    for p in ("https://", "http://", "www."):
        u = u[len(p):] if u.startswith(p) else u
    return u


def as_list(v):
    """CSV stores lists as text like "['x', 'y']"; JSON has real lists. Normalize both."""
    if isinstance(v, list):
        return sorted(str(x) for x in v)
    if isinstance(v, str) and v.startswith("["):
        try:
            return sorted(str(x) for x in ast.literal_eval(v))
        except (ValueError, SyntaxError):
            return [v]
    return [] if v in (None, "") else [str(v)]


def fingerprint(rec):
    parts = [norm_url(rec.get("linkedin")), str(rec.get("liid") or ""), str(rec.get("n") or ""),
             str(rec.get("a") or ""), "|".join(as_list(rec.get("e"))), "|".join(as_list(rec.get("t")))]
    return hashlib.sha1("\x1f".join(parts).encode()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample-kb", type=int, default=2048)
    args = ap.parse_args()
    size = next(e["Size"] for e in json.load(open(os.path.join(pf.REPORTS, "drive_listing.json")))
                if e["Path"] == ARCHIVE)
    pf.ARCHIVE_SIZES[ARCHIVE] = size
    with zipfile.ZipFile(HttpRangeFile(ARCHIVE, size)) as z:
        infos = {i.filename.rsplit("/", 1)[-1]: i for i in z.infolist()}

    raw, _ = pf.fetch_member_head(ARCHIVE, infos["PeopleDataLabs_416M.json"], args.sample_kb * 1024)
    lines = raw.decode("utf-8", "replace").splitlines()[:-1]  # last line may be cut
    jrecs = []
    for ln in lines:
        try:
            jrecs.append(json.loads(ln))
        except ValueError:
            pass

    raw, _ = pf.fetch_member_head(ARCHIVE, infos["PeopleDataLabs_chunk_1.csv"], args.sample_kb * 1024)
    text = raw.decode("utf-8-sig", "replace")
    crecs = list(csv.DictReader(io.StringIO(text[:text.rfind("\n")], newline="")))[:-1]

    n = min(len(jrecs), len(crecs))
    same_pos_url = sum(norm_url(jrecs[i].get("linkedin")) == norm_url(crecs[i].get("linkedin")) for i in range(n))
    same_pos_all = sum(fingerprint(jrecs[i]) == fingerprint(crecs[i]) for i in range(n))
    ju = {norm_url(r.get("linkedin")) for r in jrecs}
    cu = {norm_url(r.get("linkedin")) for r in crecs}
    jf = {fingerprint(r) for r in jrecs}
    cf = {fingerprint(r) for r in crecs}

    print(f"JSON records read: {len(jrecs):,} | CSV chunk_1 records read: {len(crecs):,}")
    print(f"JSON keys: {sorted(set().union(*(r.keys() for r in jrecs[:1000])))} | CSV header: {list(crecs[0].keys())}")
    print(f"Same position, same LinkedIn URL: {same_pos_url:,}/{n:,}")
    print(f"Same position, identical record (all 6 fields): {same_pos_all:,}/{n:,}")
    print(f"LinkedIn URLs in both samples (any position): {len(ju & cu):,} of {len(ju):,} JSON / {len(cu):,} CSV")
    print(f"Identical records in both samples (any position): {len(jf & cf):,}")
    dup_in_json = len(jrecs) - len(jf)
    print(f"Repeated records inside the JSON sample itself: {dup_in_json:,}")
    for k in ("PeopleDataLabs_chunk_1.csv", "PeopleDataLabs_chunk_417.csv"):
        print(f"{k}: {infos[k].file_size / 2**20:.0f} MB uncompressed")


if __name__ == "__main__":
    main()
