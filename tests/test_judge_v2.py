"""Evaluator version 2: exact-match rule for open answers, unknown citations, unreadable verdicts
(retry, never cached, evaluator_error), image-content cache keys. Fake models only (no GPU)."""
from PIL import Image

import streamrag.eval.judge as J


class CountingEvaluator:
    """answer_verdict / evidence_verdict fake that records calls."""
    def __init__(self, answer="incorrect", evidence="supported"):
        self.answer, self.evidence, self.calls, self.n_calls = answer, evidence, [], 0

    def answer_verdict(self, q, pred):
        self.calls.append(("answer", pred))
        return {"verdict": self.answer, "reason": "fake"}

    def evidence_verdict(self, q, answer_text, items, facts):
        self.calls.append(("evidence", answer_text))
        return {"verdict": self.evidence, "reason": "fake"}


class ScriptedVLM:
    """Returns the scripted replies in order (the last one repeats)."""
    def __init__(self, *replies):
        self.replies, self.calls, self.prompts = list(replies), 0, []

    def generate(self, prompt, images=None, max_new_tokens=80):
        self.prompts.append(prompt)
        self.calls += 1
        return self.replies[min(self.calls, len(self.replies)) - 1]


OPEN = {"format": "open", "original": "What is shown?", "accepted_answers": ["fire"], "gold": "fire"}


def _stream():
    return {"items": [{"item_id": "E01", "step": 1, "time_str": "2017-01-01 00:00", "frames": []}],
            "questions": [{"qa_id": "q1", "format": "mc", "gold": "B", "options": {"A": "No", "B": "Yes"},
                           "original": "Is there flooding?", "evidence_scope": ["E01"]}],
            "reference_facts": {"E01": ["Flooding is visible"]}}


def _answer(**kw):
    return {"step": 1, "qa_id": "q1", "label": "answerable", "pred": "B", "abstained": False,
            "cited_lines": ["m1"], "cited_unknown": [], "cited_items": ["E01"], **kw}


SNAPS = [{"step": 1, "tokens": 5, "lines": [{"id": "m1", "sources": ["E01"], "text": "Flooding is visible"}]}]


# ---- 1. open answers: exact match only
def test_exact_open_answer_needs_no_model_call():
    ev = CountingEvaluator()
    assert J.correctness(OPEN, {"pred": " Fire. "}, ev) == (1.0, "accepted_match")
    assert ev.calls == []


def test_negations_and_longer_answers_go_to_the_model():
    for pred in ["no fire", "not fire", "without fire", "fire damage"]:
        ev = CountingEvaluator(answer="incorrect")
        assert J.correctness(OPEN, {"pred": pred}, ev) == (0.0, "llm:incorrect")
        assert ev.calls == [("answer", pred)]


def test_partial_and_unreadable_open_verdicts():
    assert J.correctness(OPEN, {"pred": "a fire"}, CountingEvaluator(answer="Partial."))[0] == 0.5
    assert J.correctness(OPEN, {"pred": "a fire"}, CountingEvaluator(answer="unparsed")) == (None, "llm:unparsed")


# ---- 2. citations
def test_only_unknown_citation_is_invalid(tmp_path):
    rows = J.evaluate(_stream(), SNAPS, [_answer(cited_lines=["m9"], cited_unknown=["m9"], cited_items=[])],
                      CountingEvaluator(), tmp_path / "j.json", progress=lambda m: None)
    assert rows[0]["category"] == "invalid_citation" and rows[0]["score"] == 0.0


def test_valid_citation_still_scores(tmp_path):
    rows = J.evaluate(_stream(), SNAPS, [_answer()], CountingEvaluator(evidence="supported"),
                      tmp_path / "j.json", progress=lambda m: None)
    assert rows[0]["category"] == "correct" and rows[0]["score"] == 1.0


# ---- 3. unreadable verdicts
def test_unreadable_evidence_verdict_is_evaluator_error(tmp_path):
    rows = J.evaluate(_stream(), SNAPS, [_answer()], CountingEvaluator(evidence="supported|unsupported|insufficient"),
                      tmp_path / "j.json", progress=lambda m: None)
    assert rows[0]["category"] == "evaluator_error" and rows[0]["score"] == 0.0


def test_insufficient_still_gets_half_credit(tmp_path):
    rows = J.evaluate(_stream(), SNAPS, [_answer()], CountingEvaluator(evidence="insufficient"),
                      tmp_path / "j.json", progress=lambda m: None)
    assert rows[0]["category"] == "evidence_insufficient" and rows[0]["score"] == 0.5


def test_retry_succeeds_after_unreadable_reply(tmp_path, monkeypatch):
    monkeypatch.setattr(J, "CACHE_PATH", tmp_path / "c.jsonl")
    vlm = ScriptedVLM("not json", '{"verdict": "correct", "reason": "ok"}')
    ev = J.Evaluator(vlm, "fake")
    assert ev.answer_verdict(OPEN, "blaze")["verdict"] == "correct"
    assert vlm.calls == 2 and J.RETRY_NOTE in vlm.prompts[1]


def test_template_verdict_counts_as_unreadable_and_is_not_cached(tmp_path, monkeypatch):
    cache = tmp_path / "c.jsonl"
    monkeypatch.setattr(J, "CACHE_PATH", cache)
    vlm = ScriptedVLM('{"verdict": "correct|partial|incorrect", "reason": "copied template"}')
    ev = J.Evaluator(vlm, "fake")
    assert ev.answer_verdict(OPEN, "blaze")["verdict"] == "unparsed"
    assert vlm.calls == 2 and not cache.exists()
    assert J.correctness(OPEN, {"pred": "blaze"}, ev) == (None, "llm:unparsed")


def test_evaluator_errors_counted_in_scores(tmp_path):
    rows = J.evaluate(_stream(), SNAPS, [_answer()], CountingEvaluator(evidence="?"), tmp_path / "j.json",
                      progress=lambda m: None)
    sc = J.summarize(_stream(), rows, [], SNAPS)
    assert sc["evaluator_errors"] == 1 and sc["evaluator_version"] == J.EVALUATOR_VERSION
    node = J.combine({"s": sc})
    assert node["evaluator_errors"] == 1 and node["evaluator_version"] == J.EVALUATOR_VERSION


# ---- 4. cache keyed by image contents
def test_same_image_at_new_path_hits_cache(tmp_path, monkeypatch):
    monkeypatch.setattr(J, "CACHE_PATH", tmp_path / "c.jsonl")
    a, b = tmp_path / "a.png", tmp_path / "b.png"
    Image.new("RGB", (10, 10), "white").save(a)
    Image.new("RGB", (10, 10), "white").save(b)
    vlm = ScriptedVLM('{"verdict": "supported", "reason": "x"}')
    ev = J.Evaluator(vlm, "fake")
    ev._ask("p", [str(a)]); ev._ask("p", [str(b)])
    assert vlm.calls == 1
    assert J.Evaluator(vlm, "fake")._ask("p", [str(a)])["verdict"] == "supported"   # persisted cache
    assert vlm.calls == 1
