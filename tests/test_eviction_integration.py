import json

import pytest

from streamrag.memory.agent import Memory, MemLine, MemoryAgent


ITEM_TIME = {
    "item_1": "00:01",
    "item_2": "00:02",
    "item_3": "00:03",
}

ITEM = {
    "item_id": "item_3",
    "step": 3,
    "source": "test",
    "time_str": "00:03",
    "text": "Flooding near residential buildings.",
    "frames": [],
}

DELIVERED = set(ITEM_TIME)


class MockVLM:
    def __init__(self, responses):
        self.responses = iter(responses)
        self.calls = 0

    def generate(self, prompt, images=None, max_new_tokens=None):
        self.calls += 1
        return next(self.responses)


def make_memory():
    return Memory(
        lines=[
            MemLine("m1", "A damaged building.", ["item_1"]),
            MemLine("m2", "Flooded streets.", ["item_2"]),
        ],
        next_id=3,
    )


def make_edits():
    return {
        "add": [
            {
                "text": "Flooding near residential buildings.",
                "sources": ["item_2", "item_3"],
            }
        ]
    }


def make_candidate():
    memory = make_memory()
    memory.lines.append(
        MemLine(
            "m3",
            "Flooding near residential buildings.",
            ["item_2", "item_3"],
        )
    )
    memory.next_id = 4
    return memory


@pytest.mark.parametrize(
    "policy,expected_eviction,expected_sources",
    [
        ("oldest", "m1", {"item_2", "item_3"}),
        ("source_aware", "m2", DELIVERED),
    ],
)
def test_agent_budget_fallback(
    policy, expected_eviction, expected_sources
):
    memory = make_memory()
    original = memory.copy()
    budget = make_candidate().tokens(ITEM_TIME) - 1

    response = json.dumps(make_edits())
    vlm = MockVLM([response, response])

    agent = MemoryAgent(
        vlm,
        "Update memory.",
        budget,
        eviction_policy=policy,
    )

    result, log = agent.step(
        memory, ITEM, DELIVERED, ITEM_TIME
    )

    assert vlm.calls == 2
    assert result.tokens(ITEM_TIME) <= budget
    assert result.sources() == expected_sources
    assert log["eviction_policy"] == policy
    assert log["fallback"] == f"budget_evict_{policy}"
    assert log["evicted"][0]["id"] == expected_eviction
    assert len(log["evicted"]) == 1
    assert memory == original


def test_agent_accepts_valid_memory_without_eviction():
    memory = make_memory()
    vlm = MockVLM([json.dumps(make_edits())])

    agent = MemoryAgent(
        vlm,
        "Update memory.",
        512,
        eviction_policy="source_aware",
    )

    result, log = agent.step(
        memory, ITEM, DELIVERED, ITEM_TIME
    )

    assert vlm.calls == 1
    assert result.sources() == DELIVERED
    assert result.tokens(ITEM_TIME) <= 512
    assert not log.get("fallback")
    assert "evicted" not in log


def test_agent_retry_can_avoid_eviction():
    memory = make_memory()
    budget = make_candidate().tokens(ITEM_TIME) - 1

    vlm = MockVLM([
        json.dumps(make_edits()),
        json.dumps({"add": [], "update": [], "delete": []}),
    ])

    agent = MemoryAgent(
        vlm,
        "Update memory.",
        budget,
        eviction_policy="source_aware",
    )

    result, log = agent.step(
        memory, ITEM, DELIVERED, ITEM_TIME
    )

    assert vlm.calls == 2
    assert result.tokens(ITEM_TIME) <= budget
    assert not log.get("fallback")
    assert "evicted" not in log


def test_agent_default_policy_is_oldest():
    agent = MemoryAgent(
        MockVLM([]),
        "Update memory.",
        512,
    )

    assert agent.eviction_policy == "oldest"


def test_agent_rejects_invalid_policy():
    with pytest.raises(ValueError):
        MemoryAgent(
            MockVLM([]),
            "Update memory.",
            512,
            eviction_policy="unknown",
        )