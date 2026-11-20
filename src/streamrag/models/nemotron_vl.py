"""NVIDIA Nemotron-Nano-12B-v2-VL via HF transformers (trust_remote_code), 8-bit by default.

BF16 weights (~25 GB) do not fit a 24 GB card, so weights are quantized with bitsandbytes
while the vision tower and projector stay in BF16. Video = list of PIL frames we sample.
"""
from __future__ import annotations

import torch
from PIL import Image
from transformers import (AutoModelForCausalLM, AutoProcessor, AutoTokenizer,
                          BitsAndBytesConfig)

from streamrag.models.base import VLM


class NemotronVL(VLM):
    def __init__(self, name: str, cfg: dict):
        self.name, self.cfg = name, cfg
        hf_id = cfg["hf_id"]
        quant = cfg.get("quant", "int8")
        skip = cfg.get("skip_quant_modules") or None
        if quant == "int8":
            # threshold 6.0 = standard LLM.int8 outlier decomposition (best quality, ~7 tok/s);
            # 0.0 = pure int8 matmuls (~17 tok/s on the 24 GB reference GPU, small quality risk)
            qc = BitsAndBytesConfig(load_in_8bit=True, llm_int8_skip_modules=skip,
                                    llm_int8_threshold=cfg.get("int8_threshold", 6.0))
        elif quant == "nf4":
            qc = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                    bnb_4bit_compute_dtype=torch.bfloat16,
                                    llm_int8_skip_modules=skip)
        elif quant in (None, "none", "bf16"):
            qc = None
        else:
            raise ValueError(f"Unknown quant '{quant}'")
        self.model = AutoModelForCausalLM.from_pretrained(
            hf_id, trust_remote_code=True, torch_dtype=torch.bfloat16,
            quantization_config=qc, device_map=cfg.get("device_map", "cuda:0"),
        ).eval()
        self.tokenizer = AutoTokenizer.from_pretrained(hf_id, trust_remote_code=True)
        self.processor = AutoProcessor.from_pretrained(hf_id, trust_remote_code=True)
        names = {n for n, _ in self.model.named_modules()}
        for s in skip or []:
            if not any(n == s or n.endswith("." + s) or n.startswith(s + ".") for n in names):
                print(f"[nemotron] warning: skip_quant_modules entry '{s}' matches no module")
        self.model.video_pruning_rate = cfg.get("video_pruning_rate", 0.0)
        if cfg.get("fix_generation_cache", True):
            _fix_generation_cache(self.model.language_model)
        self.device = next(self.model.parameters()).device

    def _system(self, system: str | None) -> str:
        tag = "/think" if self.cfg.get("reasoning") else "/no_think"
        return f"{tag}\n{system}" if system else tag

    @torch.inference_mode()
    def generate(self, prompt: str, images: list[Image.Image] | None = None,
                 frames: list[Image.Image] | None = None, system: str | None = None,
                 max_new_tokens: int = 256) -> str:
        if images and frames:
            raise ValueError("Pass images or frames, not both")
        content: list[dict] = []
        if images:
            content += [{"type": "image", "image": ""} for _ in images]
        if frames:
            vcfg = self.cfg.get("video", {})
            frames = _clip_frames(frames, vcfg.get("min_frames", 8), vcfg.get("max_frames", 128))
            content.append({"type": "video", "video": ""})
        content.append({"type": "text", "text": prompt})
        messages = [{"role": "system", "content": self._system(system)},
                    {"role": "user", "content": content}]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False,
                                                  add_generation_prompt=True)
        kwargs: dict = {"text": [text], "return_tensors": "pt"}
        if images:
            kwargs["images"] = images
        if frames:
            kwargs["videos"] = frames
        inputs = self.processor(**kwargs).to(self.device)

        gen_kwargs = dict(input_ids=inputs.input_ids, attention_mask=inputs.attention_mask,
                          max_new_tokens=max_new_tokens, do_sample=False,
                          eos_token_id=self.tokenizer.eos_token_id)
        if images:
            gen_kwargs["pixel_values"] = inputs.pixel_values.to(torch.bfloat16)
        if frames:
            gen_kwargs["pixel_values_videos"] = inputs.pixel_values_videos.to(torch.bfloat16)
        out = self.model.generate(**gen_kwargs)
        new = out[:, inputs.input_ids.shape[1]:] if out.shape[1] > inputs.input_ids.shape[1] else out
        return self.processor.batch_decode(new, skip_special_tokens=True)[0].strip()


def _fix_generation_cache(lm) -> None:
    """Make HF generate() actually reuse the Mamba/attention cache.

    The remote NemotronH code's prepare_inputs_for_generation() reads/returns the cache as
    `past_key_values`, but forward() only accepts `cache_params` (the other name is swallowed
    by **kwargs), and generate() hands the returned cache back as `cache_params`. Net effect
    with transformers 4.53: every decode step starts a fresh cache and recomputes the full
    sequence (output is correct, decode is O(n^2): 16 tok/s at 30 ctx -> 4 tok/s at 800 ctx).
    """
    import functools
    import sys

    # The cache class's Mamba helpers were never exercised upstream; repair them.
    cache_cls = sys.modules[type(lm).__module__].HybridMambaAttentionDynamicCache
    if not getattr(cache_cls, "_streamrag_patched", False):
        orig_init = cache_cls.__init__

        def __init__(self, config, *args, **kwargs):
            orig_init(self, config, *args, **kwargs)
            self.conv_kernel_size = config.conv_kernel

        def update_conv_state(self, layer_idx, new_conv_state, cache_init=False):
            dev = self.conv_states[layer_idx].device
            if cache_init:
                self.conv_states[layer_idx] = new_conv_state.to(dev)
            else:
                self.conv_states[layer_idx] = self.conv_states[layer_idx].roll(shifts=-1, dims=-1)
                self.conv_states[layer_idx][:, :, -1] = new_conv_state[:, 0, :].to(dev)
            return self.conv_states[layer_idx]

        def update_ssm_state(self, layer_idx, new_ssm_state):
            self.ssm_states[layer_idx] = new_ssm_state.to(self.ssm_states[layer_idx].device)
            return self.ssm_states[layer_idx]

        cache_cls.__init__ = __init__
        cache_cls.update_conv_state = update_conv_state
        cache_cls.update_ssm_state = update_ssm_state
        cache_cls._streamrag_patched = True

        # NemotronHBlock.forward never hands the cache to attention layers, so cached decode
        # would attend to the current token only. Same forward, with past_key_value passed.
        block_cls = sys.modules[type(lm).__module__].NemotronHBlock

        def block_forward(self, hidden_states, cache_params=None, cache_position=None,
                          attention_mask=None):
            with torch.cuda.stream(torch.cuda.default_stream(hidden_states.device)):
                residual = hidden_states
                hidden_states = self.norm(hidden_states.to(dtype=self.norm.weight.dtype))
                if self.residual_in_fp32:
                    residual = residual.to(torch.float32)
                if self.block_type == "mamba":
                    hidden_states = self.mixer(hidden_states, cache_params=cache_params,
                                               cache_position=cache_position)
                elif self.block_type == "attention":
                    hidden_states = self.mixer(hidden_states, cache_position=cache_position,
                                               past_key_value=cache_params)[0]
                elif self.block_type == "mlp":
                    hidden_states = self.mixer(hidden_states)
                else:
                    raise ValueError(f"Invalid block_type: {self.block_type}")
                return residual + hidden_states

        block_cls.forward = block_forward

    orig = lm.prepare_inputs_for_generation

    @functools.wraps(orig)  # generate() inspects this signature (inputs_embeds, **kwargs)
    def prepare(input_ids, past_key_values=None, **kwargs):
        cache = kwargs.pop("cache_params", None)
        out = orig(input_ids, past_key_values=past_key_values if past_key_values is not None else cache, **kwargs)
        out["cache_params"] = out.pop("past_key_values")
        return out

    lm.prepare_inputs_for_generation = prepare


def _clip_frames(frames: list, lo: int, hi: int) -> list:
    """Subsample to at most `hi` frames; repeat to reach `lo`."""
    if len(frames) > hi:
        step = len(frames) / hi
        frames = [frames[int(i * step)] for i in range(hi)]
    while len(frames) < lo:
        frames = [f for f in frames for _ in (0, 1)][:lo]
    return frames
