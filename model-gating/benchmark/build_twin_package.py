"""Rebuild a seeded twin's package outside the repository: download every input in the twin's
input_manifest.json, check its SHA-256, then apply twin.patch.

The result is the package a benchmark model receives. It contains no twin metadata, logs or
references, and nothing that names it a twin.

Usage: python3 model-gating/benchmark/build_twin_package.py T-02 /tmp/scratch_bench_luna/packages/T-02
"""
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

TWINS = Path(__file__).resolve().parents[1] / "gold-set" / "twins"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fetch(entry, dest):
    want = entry.get("lfs_sha256") or entry["sha256"]
    urls = [u for u in (entry.get("lfs_media_url"), entry.get("url")) if u]
    for url in urls:
        req = urllib.request.Request(url, headers={"User-Agent": "reprocrowd-benchmark"})
        with urllib.request.urlopen(req, timeout=300) as resp, open(dest, "wb") as out:
            while block := resp.read(1 << 20):
                out.write(block)
        if sha256(dest) in (want, entry["sha256"]):
            return
    raise SystemExit(f"hash mismatch for {entry['path']} from {urls}")


def main(twin_id, out_dir):
    out = Path(out_dir)
    manifest = json.loads((TWINS / twin_id / "input_manifest.json").read_text())
    for entry in manifest:
        dest = out / entry["path"]
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists() and sha256(dest) in (entry["sha256"], entry.get("lfs_sha256")):
            continue
        fetch(entry, dest)
    patch = (TWINS / twin_id / "twin.patch").read_bytes()
    res = subprocess.run(["patch", "-p1", "--forward", "-d", str(out)], input=patch,
                         capture_output=True)
    if res.returncode != 0 and b"previously applied" not in res.stdout:
        raise SystemExit(res.stdout.decode() + res.stderr.decode())
    for orig in out.rglob("*.orig"):
        orig.unlink()
    print(f"{twin_id}: {len(manifest)} inputs verified, patch applied in {out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
