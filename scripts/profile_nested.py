"""Phase 2b: profile archives nested inside archives (zip inside zip).

For each nested archive found by profile_files.py, the inner zip is streamed out of the outer
archive into data/tmp (CRC-checked by zipfile), profiled member by member with the same profiler,
then deleted. Inner files are cached under the pseudo-archive name "<outer> :: <inner path>".

Usage: .venv/bin/python -I scripts/profile_nested.py   (needs scripts/serve_drive.sh running)
"""
import hashlib
import json
import os
import shutil
import sys
import zipfile
from argparse import Namespace
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import profile_files as pf  # noqa: E402
from remote_zip import HttpRangeFile  # noqa: E402

ARGS = Namespace(with_excel=True, sample_kb=256, max_rows=5000)


def nested_entries():
    for root, _, files in os.walk(pf.OUT):
        for f in files:
            p = os.path.join(root, f)
            rec = json.load(open(p))
            if rec.get("kind") == "nested_archive":
                yield p, rec


def temp_path(name):
    return os.path.join(pf.TMP, "nested_" + hashlib.sha1(name.encode()).hexdigest()[:12] + ".zip")


def open_archive(name, listing, temps):
    """Drive archive -> range-read file; "<outer> :: <member>" -> member extracted to temp (recursive)."""
    if name in listing:
        return HttpRangeFile(name, listing[name]["Size"], chunk=16 * 2**20)
    parent, member = name.rsplit(" :: ", 1)
    path = temp_path(name)
    if not os.path.exists(path):
        extract_inner(parent, member, path, listing, temps)
        temps.append(path)
    return open(path, "rb")


def extract_inner(outer, member, dest, listing, temps):
    with zipfile.ZipFile(open_archive(outer, listing, temps)) as z, z.open(member) as fin, open(dest, "wb") as fout:
        shutil.copyfileobj(fin, fout, 4 * 2**20)  # zipfile raises BadZipFile on CRC mismatch


def main():
    listing = {e["Path"]: e for e in json.load(open(os.path.join(pf.REPORTS, "drive_listing.json")))}
    os.makedirs(pf.TMP, exist_ok=True)
    for cache_file, rec in nested_entries():
        if rec.get("status") == "expanded":
            continue
        outer, member = rec["archive"], rec["member"]
        pseudo = f"{outer} :: {member}"
        dest = temp_path(pseudo)
        temps = []
        print(f"== {pseudo} ({rec['uncompressed'] / 2**20:.0f} MB) extracting to temp", flush=True)
        try:
            extract_inner(outer, member, dest, listing, temps)
            pf.ARCHIVE_SIZES[pseudo] = os.path.getsize(dest)
            pf.LOCAL_ZIPS[pseudo] = dest
            with zipfile.ZipFile(dest) as z:
                infos = [i for i in z.infolist() if not i.is_dir()]
            todo = [i for i in infos if not os.path.exists(pf.cache_path(pseudo, i.filename))]
            print(f"   {len(infos)} inner files, {len(todo)} to profile", flush=True)
            errors = 0
            with ThreadPoolExecutor(6) as ex:
                for r in ex.map(lambda i: pf.profile_member(pseudo, i, ARGS), todo):
                    if r["status"] == "error":
                        errors += 1
                        print(f"   error {r['member'][-60:]} {r.get('error', '')[:150]}", flush=True)
                        continue
                    os.makedirs(os.path.dirname(pf.cache_path(pseudo, r["member"])), exist_ok=True)
                    json.dump(r, open(pf.cache_path(pseudo, r["member"]), "w"), indent=1)
            if not errors:
                rec.update(status="expanded", inner_files=len(infos), expanded_as=pseudo)
                json.dump(rec, open(cache_file, "w"), indent=1)
            print(f"   done, errors={errors}", flush=True)
        except Exception as e:
            print(f"   error {e!r}"[:300], flush=True)
        finally:
            pf.LOCAL_ZIPS.pop(pseudo, None)
            for p in [dest] + temps:
                if os.path.exists(p):
                    os.remove(p)
    pf.write_reports()


if __name__ == "__main__":
    main()
