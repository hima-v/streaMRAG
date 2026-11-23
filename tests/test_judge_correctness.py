
import pytest
from streamrag.eval.judge import correctness
from PIL import Image
import streamrag.eval.judge as judge_module

class FakeEvaluator:
    def answer_verdict(self, q, pred):
        # This test should never need to call the real LLM.
        return {"verdict": "incorrect"}


def test_exact_answer():
    q = {
        "format": "open",
        "accepted_answers": ["fire"],
    }
    a = {"pred": "fire"}

    score, reason = correctness(q, a, FakeEvaluator())
    assert score == 1.0


def test_negated_answer_should_not_be_correct():
    q = {
        "format": "open",
        "accepted_answers": ["fire"],
    }
    a = {"pred": "no fire"}

    score, reason = correctness(q, a, FakeEvaluator())
    assert score == 0.0


def test_multiple_choice():
    q = {
        "format": "mc",
        "gold": "B",
    }

    score, reason = correctness(
        q, {"pred": "B"}, FakeEvaluator()
    )
    assert score == 1.0



from streamrag.eval.judge import evaluate
from streamrag.qa.answering import parse_answer



class FakeCitationEvaluator:
    n_calls = 0

    def evidence_verdict(self, q, answer_text, items, facts):
        return {
            "verdict": "supported",
            "reason": "Test fixture"
        }


def test_unknown_citation_should_be_rejected(tmp_path):
    stream = {
        "items": [
            {"item_id": "E01", "step": 1}
        ],
        "questions": [
            {
                "qa_id": "q1",
                "format": "mc",
                "gold": "B",
                "options": {"A": "No", "B": "Yes"},
                "original": "Is there flooding?",
                "evidence_scope": ["E01"],
            }
        ],
        "reference_facts": {"E01": ["Flooding is visible"]},
    }

    snaps = [
        {
            "step": 1,
            "lines": [
                {
                    "id": "M01",
                    "sources": ["E01"],
                    "text": "Flooding is visible",
                }
            ],
        }
    ]

    parsed = parse_answer(
        '{"answer":"B","cited":["M01","FAKE_ID"]}',
        "mc",
        {"M01"},
    )

    answers = [
        {
            "step": 1,
            "qa_id": "q1",
            "label": "answerable",
            **parsed,
            "cited_items": ["E01"],
        }
    ]

    rows = evaluate(
        stream,
        snaps,
        answers,
        FakeCitationEvaluator(),
        tmp_path / "judgments.json",
        progress=lambda message: None,
    )

    assert parsed["cited_unknown"] == ["FAKE_ID"]
    assert rows[0]["citation_valid"] is False
    assert rows[0]["score"] == 0.0


def test_unparsed_evidence_verdict_should_not_get_credit(
    tmp_path,
):
    class UnparsedEvaluator:
        n_calls = 0

        def evidence_verdict(self, q, answer_text, items, facts):
            return {
                "verdict": "unparsed",
                "reason": "Invalid JSON returned by judge",
            }

    stream = {
        "items": [{"item_id": "E01", "step": 1}],
        "questions": [{
            "qa_id": "q1",
            "format": "mc",
            "gold": "B",
            "options": {"A": "No", "B": "Yes"},
            "original": "Is there flooding?",
            "evidence_scope": ["E01"],
        }],
        "reference_facts": {
            "E01": ["Flooding is visible"]
        },
    }

    snaps = [{
        "step": 1,
        "lines": [{
            "id": "M01",
            "sources": ["E01"],
            "text": "Flooding is visible",
        }],
    }]

    answers = [{
        "step": 1,
        "qa_id": "q1",
        "label": "answerable",
        "pred": "B",
        "abstained": False,
        "cited_items": ["E01"],
    }]

    rows = evaluate(
        stream,
        snaps,
        answers,
        UnparsedEvaluator(),
        tmp_path / "judgments.json",
        progress=lambda message: None,
    )

    assert rows[0]["evidence_verdict"] == "unparsed"
    assert rows[0]["score"] == 0.0


@pytest.mark.xfail(reason="cited-memory sufficiency check is future work", strict=False)
def test_cited_memory_must_support_answer(tmp_path):
    class FakeEvidenceEvaluator:
        n_calls = 0

        def evidence_verdict(self, q, answer_text, items, facts):
            # Original image supports the answer.
            return {
                "verdict": "supported",
                "reason": "Original image shows flooding",
            }

    stream = {
        "items": [{"item_id": "E01", "step": 1}],
        "questions": [{
            "qa_id": "q1",
            "format": "mc",
            "gold": "B",
            "options": {
                "A": "No",
                "B": "Yes",
            },
            "original": "Is the road flooded?",
            "evidence_scope": ["E01"],
        }],
        "reference_facts": {
            "E01": ["The road is flooded"]
        },
    }

    snaps = [{
        "step": 1,
        "lines": [{
            "id": "M01",
            "sources": ["E01"],
            "text": "A road is visible.",
        }],
    }]

    answers = [{
        "step": 1,
        "qa_id": "q1",
        "label": "answerable",
        "pred": "B",
        "abstained": False,
        "cited_lines": ["M01"],
        "cited_unknown": [],
        "cited_items": ["E01"],
    }]

    rows = evaluate(
        stream,
        snaps,
        answers,
        FakeEvidenceEvaluator(),
        tmp_path / "judgments.json",
        progress=lambda message: None,
    )

    # The citation points to the right image,
    # but the memory text does not establish flooding.
    assert rows[0]["score"] < 1.0


from streamrag.eval.judge import combine


def test_aggregation_weights_streams_equally():
    per_stream = {
        "A": {
            "esqa_mean": 1.0,
            "correct_count": "2/2",
            "retention_final": 1.0,
            "abstained": 0.0,
            "budget_fallbacks": 0,
            "categories": {"correct": 2},
            "n_questions": 2,
        },
        "B": {
            "esqa_mean": 0.0,
            "correct_count": "0/8",
            "retention_final": 0.0,
            "abstained": 0.0,
            "budget_fallbacks": 0,
            "categories": {"wrong_answer_evidence_missing": 8},
            "n_questions": 8,
        },
    }

    result = combine(per_stream)

    # Current intended implementation: equal weight per stream
    assert result["esqa_mean"] == 0.5

    # Retention is weighted by question count
    assert result["retention_final"] == 0.2

    assert result["correct_count"] == "2/10"



def test_unparsed_judge_response_should_not_be_cached(
    tmp_path, monkeypatch
):
    class FakeVLM:
        def __init__(self):
            self.calls = 0

        def generate(self, prompt, images=None, max_new_tokens=80):
            self.calls += 1

            # First response is malformed.
            if self.calls == 1:
                return "This is not valid JSON"

            # Second response is valid.
            return '{"verdict": "supported", "reason": "Valid evidence"}'

    # Use a temporary cache file to protect the real cache.
    monkeypatch.setattr(
        judge_module,
        "CACHE_PATH",
        tmp_path / "test_judge_cache.jsonl",
    )

    # Create a small test image.
    image_path = tmp_path / "test_image.png"
    Image.new("RGB", (10, 10), "white").save(image_path)

    fake_vlm = FakeVLM()

    evaluator = judge_module.Evaluator(
        vlm=fake_vlm,
        model_name="fake-test-model",
    )

    first = evaluator._ask(
        "Does this image show flooding?",
        [str(image_path)],
    )

    second = evaluator._ask(
        "Does this image show flooding?",
        [str(image_path)],
    )

    assert first["verdict"] == "unparsed"

    # A malformed response should not prevent a later retry.
    assert fake_vlm.calls == 2
    assert second["verdict"] == "supported"



def test_cache_invalidates_when_image_content_changes(
    tmp_path, monkeypatch
):
    class FakeVLM:
        def __init__(self):
            self.calls = 0

        def generate(self, prompt, images=None, max_new_tokens=80):
            self.calls += 1
            return '{"verdict": "supported", "reason": "Test"}'

    monkeypatch.setattr(
        judge_module,
        "CACHE_PATH",
        tmp_path / "image_cache.jsonl",
    )

    image_path = tmp_path / "evidence.png"

    # First version of the image.
    Image.new("RGB", (10, 10), "white").save(image_path)

    fake_vlm = FakeVLM()
    evaluator = judge_module.Evaluator(
        vlm=fake_vlm,
        model_name="fake-test-model",
    )

    evaluator._ask(
        "What does this image show?",
        [str(image_path)],
    )

    # Replace the image while keeping the same path.
    Image.new("RGB", (10, 10), "black").save(image_path)

    evaluator._ask(
        "What does this image show?",
        [str(image_path)],
    )

    # Changed image content should trigger a new judgment.
    assert fake_vlm.calls == 2
