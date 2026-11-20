"""Download / parsing helpers shared by dataset modules."""
from __future__ import annotations

import hashlib
import re
import zipfile
from pathlib import Path

import requests
from tqdm import tqdm


def http_download(url: str, dest: Path, md5: str | None = None, chunk: int = 1 << 20) -> Path:
    """Stream a URL to `dest` (skip if it exists and the md5 matches)."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and (md5 is None or file_md5(dest) == md5):
        return dest
    tmp = dest.with_suffix(dest.suffix + ".part")
    with requests.get(url, stream=True, timeout=60) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length", 0))
        with open(tmp, "wb") as f, tqdm(total=total, unit="B", unit_scale=True,
                                        desc=dest.name) as bar:
            for b in r.iter_content(chunk):
                f.write(b)
                bar.update(len(b))
    if md5 and (got := file_md5(tmp)) != md5:
        raise IOError(f"md5 mismatch for {dest.name}: {got} != {md5}")
    tmp.rename(dest)
    return dest


def file_md5(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def safe_extract(zf: zipfile.ZipFile, out: Path, members: list[str] | None = None) -> None:
    """Extract, refusing paths that escape `out` (zip-slip)."""
    out = out.resolve()
    for m in members or zf.namelist():
        target = (out / m).resolve()
        if not str(target).startswith(str(out)):
            raise IOError(f"Unsafe path in zip: {m}")
        zf.extract(m, out)


def hms_to_s(ts: str) -> float:
    """'HH:MM:SS,mmm' | 'MM:SS' | 'SS' -> seconds."""
    parts = ts.replace(",", ".").split(":")
    s = 0.0
    for p in parts:
        s = s * 60 + float(p)
    return s


_TAG = re.compile(r"<[^>]+>")
_SRT_TIME = re.compile(r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)")


def parse_srt(path: Path) -> list[tuple[float, float, str]]:
    """Return [(start_s, end_s, text)] from an .srt file."""
    out, block = [], []
    for line in list(path.read_text(encoding="utf-8", errors="replace").splitlines()) + [""]:
        if line.strip():
            block.append(line.strip())
            continue
        times = next((_SRT_TIME.search(b) for b in block if _SRT_TIME.search(b)), None)
        if times:
            idx = next(i for i, b in enumerate(block) if _SRT_TIME.search(b))
            text = _TAG.sub("", " ".join(block[idx + 1:])).strip()
            if text:
                out.append((hms_to_s(times.group(1)), hms_to_s(times.group(2)), text))
        block = []
    return out
