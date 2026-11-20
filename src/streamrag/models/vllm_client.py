"""Optional: talk to a `vllm serve` endpoint (separate .venv-vllm) through its OpenAI API.

Example models.yaml entry:
  nemotron-vllm: {kind: vllm, hf_id: nvidia/NVIDIA-Nemotron-Nano-12B-v2-VL-BF16,
                  base_url: http://localhost:8000/v1}
"""
from __future__ import annotations

import base64
import io

from PIL import Image

from streamrag.models.base import VLM


def _data_url(im: Image.Image) -> str:
    buf = io.BytesIO()
    im.save(buf, format="JPEG", quality=90)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


class VLLMClient(VLM):
    def __init__(self, name: str, cfg: dict):
        from openai import OpenAI
        self.name, self.cfg = name, cfg
        self.client = OpenAI(base_url=cfg.get("base_url", "http://localhost:8000/v1"),
                             api_key=cfg.get("api_key", "EMPTY"))

    def generate(self, prompt, images=None, frames=None, system=None, max_new_tokens=256):
        content = [{"type": "image_url", "image_url": {"url": _data_url(im)}}
                   for im in (images or []) + (frames or [])]
        content.append({"type": "text", "text": prompt})
        msgs = ([{"role": "system", "content": system}] if system else []) + \
               [{"role": "user", "content": content}]
        r = self.client.chat.completions.create(model=self.cfg["hf_id"], messages=msgs,
                                                max_tokens=max_new_tokens, temperature=0)
        return r.choices[0].message.content.strip()
