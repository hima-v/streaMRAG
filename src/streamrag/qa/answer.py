"""QA reader shared by every memory method, and answer parsing.

The reader sees only the memory context for the question (<= budget tokens), the current
stream time and the question. It may abstain with "Not enough evidence."
(streaMRAG's time-anchored retrieval + citations — Phase 2 — will build its own context
and reuse answer_question / parse_answer.)
"""
from __future__ import annotations

import re

from streamrag.memory.tokens import fmt_t
from streamrag.types import QAItem

ABSTAIN = "Not enough evidence."

READER_PROMPT = """You answer questions about events observed earlier in a stream.
Use ONLY the notes below. Each note starts with the time it was observed [MM:SS] and its source.
If the notes do not contain enough information, answer "{abstain}"

Notes:
{context}

Current time: [{now}]
Question: {question}{options}
{instruction}
Answer:"""

INSTRUCTIONS = {
    "mc": "Answer with the letter of the correct option only.",
    "mc_multi": "Select all correct options. Answer with the letters only, separated by commas.",
    "yesno": "Answer Yes or No.",
    "open": "Answer in one short sentence.",
}


def format_options(options) -> str:
    if not options:
        return ""
    if isinstance(options, dict):
        lines = [f"{k}. {v}" for k, v in options.items()]
    else:
        lines = [str(o) for o in options]
    return "\nOptions:\n" + "\n".join(lines)


def build_prompt(q: QAItem, context: str) -> str:
    fmt = q.meta.get("format", "open")
    return READER_PROMPT.format(abstain=ABSTAIN, context=context or "(no notes)",
                                now=fmt_t(q.t_query), question=q.question,
                                options=format_options(q.options), instruction=INSTRUCTIONS[fmt])


def answer_question(q: QAItem, context: str, reader, max_new_tokens: int = 48) -> dict:
    raw = reader.generate(build_prompt(q, context), max_new_tokens=max_new_tokens)
    return {"raw": raw, **parse_answer(raw, q.meta.get("format", "open"))}


_LETTER = re.compile(r"\b([A-H])\b")


def parse_answer(raw: str, fmt: str) -> dict:
    text = raw.strip()
    low = text.lower()
    if "not enough evidence" in low:
        return {"pred": None, "abstained": True}
    if fmt == "mc":
        m = re.match(r"^\(?([A-H])(?:[\.\):\s]|$)", text) or \
            re.search(r"(?:answer|option)\s*(?:is)?\s*:?\s*\(?([A-H])\b", text, re.I) or \
            _LETTER.search(text.splitlines()[0] if text else "")
        return {"pred": m.group(1) if m else None, "abstained": False}
    if fmt == "mc_multi":
        first = text.splitlines()[0] if text else ""
        return {"pred": sorted(set(_LETTER.findall(first))), "abstained": False}
    if fmt == "yesno":
        m = re.match(r"^\W*(yes|no)\b", low)
        return {"pred": m.group(1).capitalize() if m else None, "abstained": False}
    return {"pred": text, "abstained": False}
