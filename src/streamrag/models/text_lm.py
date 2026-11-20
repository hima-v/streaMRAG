"""Small text-only LM (Qwen3-4B-Instruct-2507) used for atomic claim extraction."""
from __future__ import annotations

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from streamrag.models.base import TextLM, torch_dtype


class HFTextLM(TextLM):
    def __init__(self, name: str, cfg: dict):
        self.name, self.cfg = name, cfg
        self.tokenizer = AutoTokenizer.from_pretrained(cfg["hf_id"])
        self.model = AutoModelForCausalLM.from_pretrained(
            cfg["hf_id"], torch_dtype=torch_dtype(cfg.get("dtype", "bfloat16")),
            device_map=cfg.get("device_map", "cuda:0"),
        ).eval()

    @torch.inference_mode()
    def generate(self, prompt: str, system: str | None = None,
                 max_new_tokens: int = 256) -> str:
        messages = ([{"role": "system", "content": system}] if system else []) + \
                   [{"role": "user", "content": prompt}]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False,
                                                  add_generation_prompt=True)
        inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)
        out = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        return self.tokenizer.decode(out[0, inputs.input_ids.shape[1]:],
                                     skip_special_tokens=True).strip()
