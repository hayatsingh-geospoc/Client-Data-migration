"""Phase 1: list the contents of every archive in the Drive folder without downloading them.

Usage: python3 -I scripts/inventory.py [--refresh]
Outputs (reports/):
  inventory/<drive_id>.json   per-archive cache (resume: archives already cached are skipped)
  inventory_members.csv       one row per file inside each archive
  inventory.json / inventory.md  consolidated summary
"""
import csv
import json
import os
import subprocess
import sys
import zipfile
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from remote_zip import RcloneRangeFile, DRIVE_ARGS  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REMOTE = os.environ.get("LEADS_REMOTE", "clientdrive:1.2B Leads-sazag")
REPORTS = os.path.join(ROOT, "reports")
CACHE = os.path.join(REPORTS, "inventory")


def gib(n):
    return f"{n / 2**30:.2f}"


def list_drive():
    out = subprocess.run(["rclone", "lsjson", REMOTE, "-R", "--files-only", *DRIVE_ARGS],
                         capture_output=True, check=True)
    return json.loads(out.stdout)


def ext_of(name):
    base = name.rsplit("/", 1)[-1]
    return base.rsplit(".", 1)[-1].lower() if "." in base else ""


def inspect_archive(entry):
    f = RcloneRangeFile(f"{REMOTE}/{entry['Path']}", entry["Size"], chunk=2**20)
    result = {"archive": entry["Path"], "drive_id": entry["ID"], "size": entry["Size"],
              "modtime": entry["ModTime"], "status": "ok", "error": None, "members": []}
    try:
        with zipfile.ZipFile(f) as z:
            for i in z.infolist():
                result["members"].append({
                    "path": i.filename, "is_dir": i.is_dir(), "ext": "" if i.is_dir() else ext_of(i.filename),
                    "compressed": i.compress_size, "uncompressed": i.file_size,
                    "method": zipfile.compressor_names.get(i.compress_type, str(i.compress_type)),
                    "encrypted": bool(i.flag_bits & 0x1),
                    "macos_junk": i.filename.startswith("__MACOSX/") or i.filename.rsplit("/", 1)[-1].startswith("._"),
                })
    except zipfile.BadZipFile as e:
        result["status"], result["error"] = "not_a_zip", str(e)
    except Exception as e:  # network etc. -> not cached, retried next run
        result["status"], result["error"] = "error", repr(e)
    result["range_requests"], result["bytes_fetched"] = f.requests, f.bytes_fetched
    return result


def main():
    os.makedirs(CACHE, exist_ok=True)
    refresh = "--refresh" in sys.argv
    entries = sorted(list_drive(), key=lambda e: e["Size"])
    results = []
    for n, e in enumerate(entries, 1):
        cache = os.path.join(CACHE, f"{e['ID']}.json")
        if os.path.exists(cache) and not refresh:
            results.append(json.load(open(cache)))
            print(f"[{n}/{len(entries)}] cached  {e['Path']}")
            continue
        r = inspect_archive(e)
        files = [m for m in r["members"] if not m["is_dir"]]
        print(f"[{n}/{len(entries)}] {r['status']:9} {e['Path']}  files={len(files)} "
              f"fetched={r['bytes_fetched'] / 2**20:.1f}MB req={r['range_requests']}", flush=True)
        if r["status"] != "error":
            json.dump(r, open(cache, "w"), indent=1)
        results.append(r)

    with open(os.path.join(REPORTS, "inventory_members.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["archive", "member_path", "ext", "compressed_bytes", "uncompressed_bytes",
                    "method", "encrypted", "macos_junk"])
        for r in results:
            for m in r["members"]:
                if not m["is_dir"]:
                    w.writerow([r["archive"], m["path"], m["ext"], m["compressed"], m["uncompressed"],
                                m["method"], m["encrypted"], m["macos_junk"]])

    summary = []
    for r in results:
        files = [m for m in r["members"] if not m["is_dir"] and not m["macos_junk"]]
        summary.append({
            "archive": r["archive"], "status": r["status"], "error": r["error"],
            "zip_bytes": r["size"], "uncompressed_bytes": sum(m["uncompressed"] for m in files),
            "file_count": len(files), "ext_counts": dict(Counter(m["ext"] or "(none)" for m in files)),
            "nested_zips": [m["path"] for m in files if m["ext"] in ("zip", "gz", "7z", "rar", "tar")],
            "encrypted_files": sum(m["encrypted"] for m in files),
            "largest_file": max(files, key=lambda m: m["uncompressed"])["path"] if files else None,
            "largest_file_bytes": max((m["uncompressed"] for m in files), default=0),
        })
    json.dump(summary, open(os.path.join(REPORTS, "inventory.json"), "w"), indent=1)

    tot_z = sum(s["zip_bytes"] for s in summary)
    tot_u = sum(s["uncompressed_bytes"] for s in summary)
    lines = ["# Archive inventory (Phase 1)", "",
             f"Archives: {len(summary)} | Zipped: {gib(tot_z)} GiB | Uncompressed: {gib(tot_u)} GiB | "
             f"Files inside: {sum(s['file_count'] for s in summary)}", "",
             "| Archive | Status | Zip GiB | Unzipped GiB | Files | Types | Largest file (GiB) | Notes |",
             "|---|---|---:|---:|---:|---|---|---|"]
    for s in sorted(summary, key=lambda s: -s["zip_bytes"]):
        notes = []
        if s["nested_zips"]:
            notes.append(f"{len(s['nested_zips'])} nested archives")
        if s["encrypted_files"]:
            notes.append(f"{s['encrypted_files']} encrypted")
        if s["error"]:
            notes.append(s["error"][:80])
        types = ", ".join(f"{k}:{v}" for k, v in sorted(s["ext_counts"].items(), key=lambda kv: -kv[1]))
        largest = f"{(s['largest_file'] or '').rsplit('/', 1)[-1][:50]} ({gib(s['largest_file_bytes'])})"
        lines.append(f"| {s['archive']} | {s['status']} | {gib(s['zip_bytes'])} | {gib(s['uncompressed_bytes'])} | "
                     f"{s['file_count']} | {types} | {largest} | {'; '.join(notes)} |")
    open(os.path.join(REPORTS, "inventory.md"), "w").write("\n".join(lines) + "\n")
    print(f"\nTotal zipped {gib(tot_z)} GiB -> uncompressed {gib(tot_u)} GiB. Reports written to {REPORTS}")


if __name__ == "__main__":
    main()
