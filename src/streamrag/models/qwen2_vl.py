"""Qwen2-VL (2B / 7B Instruct) via HF transformers + qwen_vl_utils."""
from __future__ import annotations

import torch
from PIL import Image
from qwen_vl_utils import process_vision_info
from transformers import AutoProcessor, Qwen2VLForConditionalGeneration

from streamrag.models.base import VLM, torch_dtype


class Qwen2VL(VLM):
    def __init__(self, name: str, cfg: dict):
        self.name, self.cfg = name, cfg
        self.model = Qwen2VLForConditionalGeneration.from_pretrained(
            cfg["hf_id"], torch_dtype=torch_dtype(cfg.get("dtype", "bfloat16")),
            attn_implementation=cfg.get("attn_implementation", "sdpa"),
            device_map=cfg.get("device_map", "cuda:0"),
        ).eval()
        self.processor = AutoProcessor.from_pretrained(
            cfg["hf_id"], max_pixels=cfg.get("max_pixels", 1280 * 28 * 28))
        self.device = next(self.model.parameters()).device

    @torch.inference_mode()
    def generate(self, prompt: str, images: list[Image.Image] | None = None,
                 frames: list[Image.Image] | None = None, system: str | None = None,
                 max_new_tokens: int = 256) -> str:
        content: list[dict] = [{"type": "image", "image": im} for im in images or []]
        if frames:
            if len(frames) % 2:            # Qwen2-VL groups frames in pairs
                frames = frames + frames[-1:]
            content.append({"type": "video", "video": list(frames), "fps": 1.0,
                            "max_pixels": self.cfg.get("video_max_pixels", 360 * 420)})
        content.append({"type": "text", "text": prompt})
        messages = ([{"role": "system", "content": system}] if system else []) + \
                   [{"role": "user", "content": content}]
        text = self.processor.apply_chat_template(messages, tokenize=False,
                                                  add_generation_prompt=True)
        image_inputs, video_inputs = process_vision_info(messages)
        inputs = self.processor(text=[text], images=image_inputs, videos=video_inputs,
                                padding=True, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        new = out[:, inputs.input_ids.shape[1]:]
        return self.processor.batch_decode(new, skip_special_tokens=True)[0].strip()
