"""Build local packages for the drawn Stata papers (../gold-set/stata/draw-stata.json).

Each package is downloaded from its pinned source into WORK/packages/<opaque name>, with the
rendered outputs the package's own code produces removed (same rule as the twins:
../gold-set/twins/strip_outputs.json). The opaque name hides which paper a folder holds. A manifest
of every kept and stripped file, with SHA-256, is written to ../gold-set/stata/packages/<S-xx>.json.

Sources:
- REPRO-Bench tasks: the replication_package folder at the pinned Hugging Face commit;
- I4R-243: the GitHub repository at the pinned commit plus the author-linked Dropbox data archive;
- SC-a2Yx: the original (version 1) do-files from OSF node zxdca and the data from node my6bg, not
  the SCORE reproduction project that also holds the human report.

Usage: python3 model-gating/benchmark/build_stata_packages.py [S-01 S-02 ...]
"""
import hashlib
import io
import json
import shutil
import sys
import tarfile
import urllib.parse
import time
import urllib.request
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
STATA = HERE.parent / "gold-set" / "stata"
WORK = Path("/tmp/scratch_bench_luna")
HF = "https://huggingface.co/api/datasets/chuxuan/REPRO-Bench/tree/{rev}/{path}?recursive=true"
HF_FILE = "https://huggingface.co/datasets/chuxuan/REPRO-Bench/resolve/{rev}/{path}"
HF_REV = "74958fba32daeacff51f2e1fd37be3916595648f"
# Outputs that shipped code renders: logs, Stata graphs, figures, knitted documents, LaTeX tables.
STRIP_EXT = {".log", ".smcl", ".gph", ".png", ".jpg", ".jpeg", ".eps", ".svg", ".html", ".htm",
             ".tex"}
I4R243 = {"repo": "stevebholt/waiting-time", "commit": "95e2eaec985dfbd7f2dfd5e05ebe768195e4e613",
          "data": "https://www.dropbox.com/sh/5z2pornijzv0bn8/AAABc-y5Rx8u8O7SRccTqtsda?dl=1"}
A2YX = {"code": "zxdca", "data": "my6bg"}


def opaque(stata_id, seed):
    return "pkg-" + hashlib.sha256(f"{seed}:{stata_id}".encode()).hexdigest()[:6]


def get(url, timeout=600):
    req = urllib.request.Request(url, headers={"User-Agent": "reprocrowd-benchmark"})
    for attempt in range(5):
        try:
            return urllib.request.urlopen(req, timeout=timeout)
        except Exception:
            if attempt == 4:
                raise
            time.sleep(10 * (attempt + 1))


def save(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with get(url) as resp, open(dest, "wb") as out:
        shutil.copyfileobj(resp, out, 1 << 20)


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def fetch_hf(task, out):
    prefix = f"{task}/replication_package"
    files = [e for e in json.load(get(HF.format(rev=HF_REV, path=urllib.parse.quote(prefix))))
             if e["type"] == "file"]
    for e in files:
        dest = out / e["path"][len(prefix) + 1:]
        if not dest.exists() or dest.stat().st_size != e["size"]:
            save(HF_FILE.format(rev=HF_REV, path=urllib.parse.quote(e["path"])), dest)
    return f"{HF_FILE.format(rev=HF_REV, path=prefix)} (Hugging Face commit {HF_REV})"


def fetch_i4r243(out):
    tgz = get(f"https://codeload.github.com/{I4R243['repo']}/tar.gz/{I4R243['commit']}").read()
    with tarfile.open(fileobj=io.BytesIO(tgz)) as tar:
        for m in tar.getmembers():
            if m.isfile():
                dest = out / m.name.split("/", 1)[1]
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(tar.extractfile(m).read())
    data = WORK / "downloads" / "i4r243-data.zip"
    if not data.exists():
        save(I4R243["data"], data)
    with zipfile.ZipFile(data) as z:
        for name in z.namelist():
            if not name.endswith("/") and not name.startswith("__MACOSX"):
                dest = out / "data" / Path(name).name
                if not dest.exists():
                    with z.open(name) as src, open(dest, "wb") as fh:
                        shutil.copyfileobj(src, fh, 1 << 20)
    return (f"https://github.com/{I4R243['repo']} at {I4R243['commit']}; data from the "
            "author-linked Dropbox archive named in the README")


def osf_files(node):
    url, files = f"https://api.osf.io/v2/nodes/{node}/files/osfstorage/", []
    while url:
        d = json.load(get(url))
        files += [f for f in d["data"] if f["attributes"]["kind"] == "file"]
        url = d["links"].get("next")
    return files


def fetch_a2yx(out):
    for node, sub in ((A2YX["code"], "code"), (A2YX["data"], "data")):
        for f in osf_files(node):
            dest = out / sub / f["attributes"]["name"]
            if not dest.exists():
                save(f"https://osf.io/download/{f['id']}/?version=1", dest)
    return f"OSF nodes {A2YX['code']} (do-files, version 1) and {A2YX['data']} (data)"


def build(entry, seed):
    out = WORK / "packages" / opaque(entry["stata_id"], seed)
    out.mkdir(parents=True, exist_ok=True)
    cid = entry["cand_id"]
    if cid.startswith("RB-"):
        source = fetch_hf(int(cid[3:]), out)
    elif cid == "I4R-243":
        source = fetch_i4r243(out)
    elif cid == "SC-a2Yx":
        source = fetch_a2yx(out)
    else:
        raise SystemExit(f"no fetcher for {cid}")
    kept, stripped = [], []
    for path in sorted(p for p in out.rglob("*") if p.is_file()):
        rel = str(path.relative_to(out))
        if path.suffix.lower() in STRIP_EXT:
            stripped.append({"path": rel, "sha256": sha256(path), "bytes": path.stat().st_size})
            path.unlink()
        else:
            kept.append({"path": rel, "sha256": sha256(path), "bytes": path.stat().st_size})
    manifest = {"stata_id": entry["stata_id"], "cand_id": cid, "package_dir": out.name,
                "source": source, "strip_rule": sorted(STRIP_EXT), "kept": kept,
                "stripped": stripped}
    (STATA / "packages").mkdir(exist_ok=True)
    (STATA / "packages" / f"{entry['stata_id']}.json").write_text(json.dumps(manifest, indent=1))
    print(f"{entry['stata_id']} {cid}: {len(kept)} files kept, {len(stripped)} stripped -> {out}")


def main(ids):
    draw = json.loads((STATA / "draw-stata.json").read_text())
    for entry in draw["drawn"]:
        if not ids or entry["stata_id"] in ids:
            build(entry, draw["seed"])


if __name__ == "__main__":
    main(sys.argv[1:])
