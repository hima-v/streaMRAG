"""Frame sampling with PyAV (the VLMs are given PIL frames, never raw video)."""
from __future__ import annotations

import av
from PIL import Image


def video_duration(path: str) -> float:
    with av.open(path) as c:
        if c.duration is not None:
            return c.duration / av.time_base
        s = c.streams.video[0]
        return float(s.duration * s.time_base)


def frames_at(path: str, times: list[float]) -> list[Image.Image]:
    """Decode the first frame at or after each timestamp (seconds)."""
    out: list[Image.Image] = []
    with av.open(path) as c:
        s = c.streams.video[0]
        s.thread_type = "AUTO"
        for t in sorted(times):
            c.seek(int(t / s.time_base), stream=s, backward=True)
            img = None
            for frame in c.decode(s):
                img = frame
                if frame.time is not None and frame.time >= t:
                    break
            if img is None:
                raise ValueError(f"No frame at t={t}s in {path}")
            out.append(img.to_image())
    return out


def frame_at(path: str, t: float) -> Image.Image:
    return frames_at(path, [t])[0]


def sample_times(duration: float, every_s: float | None = None, n: int | None = None,
                 start: float = 0.0) -> list[float]:
    """Either one timestamp every `every_s` seconds, or `n` evenly spaced timestamps."""
    if every_s:
        ts, t = [], start
        while t < duration:
            ts.append(round(t, 3))
            t += every_s
        return ts
    if n:
        step = duration / n
        return [round(start + step * (i + 0.5), 3) for i in range(n)]
    raise ValueError("Pass every_s or n")


def contact_sheet(images: list[Image.Image], labels: list[str] | None = None,
                  cols: int = 4, thumb: int = 320) -> Image.Image:
    """Grid of thumbnails with optional labels (used by the data viewer)."""
    from PIL import ImageDraw

    thumbs = []
    for im in images:
        im = im.copy()
        im.thumbnail((thumb, thumb))
        thumbs.append(im)
    cell_h = max((t.height for t in thumbs), default=thumb) + 20
    rows = max(1, (len(thumbs) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * thumb, rows * cell_h), "white")
    draw = ImageDraw.Draw(sheet)
    for i, im in enumerate(thumbs):
        x, y = (i % cols) * thumb, (i // cols) * cell_h
        sheet.paste(im, (x + (thumb - im.width) // 2, y))
        if labels:
            draw.text((x + 4, y + cell_h - 17), labels[i][:48], fill="black")
    return sheet
