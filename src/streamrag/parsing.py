"""Robust parsing of model outputs (JSON objects and <tag>...</tag> blocks)."""
from __future__ import annotations

import json
import re


def parse_json_object(text: str) -> dict | None:
    """First JSON object in `text` (tolerates ```json fences and trailing prose)."""
    text = re.sub(r"```(?:json)?", "", text)
    start = text.find("{")
    while start != -1:
        depth, in_str, esc = 0, False, False
        for i in range(start, len(text)):
            c = text[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
            elif c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    chunk = text[start:i + 1]
                    for cand in (chunk, re.sub(r",\s*([}\]])", r"\1", chunk)):
                        try:
                            obj = json.loads(cand, strict=False)
                            if isinstance(obj, dict):
                                return obj
                        except json.JSONDecodeError:
                            pass
                    break
        start = text.find("{", start + 1)
    return None


def parse_tag(text: str, tag: str) -> str | None:
    m = re.search(rf"<{tag}>\s*(.*?)\s*</{tag}>", text, re.S | re.I)
    if m:
        return m.group(1).strip()
    m = re.search(rf"<{tag}>\s*(.*?)(?=<\s*/?\s*[a-z_]+\s*>|$)", text, re.S | re.I)   # unterminated tag:
    return m.group(1).strip() if m else None                                     # stop at the next tag
