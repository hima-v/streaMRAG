"""Cross-encoder NLI: premise = stored claim, hypothesis = new claim."""
from __future__ import annotations

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

_CANON = {"entailment": "entailment", "neutral": "neutral", "contradiction": "contradiction",
          "not_entailment": "neutral"}


class NLIModel:
    def __init__(self, name: str, cfg: dict):
        self.name, self.cfg = name, cfg
        self.tokenizer = AutoTokenizer.from_pretrained(cfg["hf_id"])
        self.model = AutoModelForSequenceClassification.from_pretrained(
            cfg["hf_id"], torch_dtype=torch.float16).to(cfg.get("device", "cuda:0")).eval()
        self.labels = [_CANON[self.model.config.id2label[i].lower()]
                       for i in range(self.model.config.num_labels)]

    @torch.inference_mode()
    def predict(self, pairs: list[tuple[str, str]], batch_size: int = 32) -> list[dict[str, float]]:
        """Return {entailment, neutral, contradiction} probabilities per (premise, hypothesis)."""
        out: list[dict[str, float]] = []
        for i in range(0, len(pairs), batch_size):
            p, h = zip(*pairs[i:i + batch_size])
            enc = self.tokenizer(list(p), list(h), padding=True, truncation=True,
                                 max_length=256, return_tensors="pt").to(self.model.device)
            probs = self.model(**enc).logits.float().softmax(-1).cpu()
            out += [dict(zip(self.labels, row.tolist())) for row in probs]
        return out

    def label(self, premise: str, hypothesis: str) -> str:
        probs = self.predict([(premise, hypothesis)])[0]
        return max(probs, key=probs.get)
