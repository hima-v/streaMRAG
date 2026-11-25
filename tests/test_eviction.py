import pytest

from streamrag.memory.agent import Memory, MemLine
from streamrag.memory.eviction import (
    enforce_budget,
    select_eviction_index,
)


ITEM_TIME = {
    "item_1": "00:01",
    "item_2": "00:02",
    "item_3": "00:03",
}


def make_memory():
    return Memory(
        lines=[
            MemLine("m1", "A damaged building.", ["item_1"]),
            MemLine("m2", "Flooded streets.", ["item_2"]),
            MemLine(
                "m3",
                "Flooding near residential buildings.",
                ["item_2", "item_3"],
            ),
        ],
        next_id=4,
    )


def test_oldest_policy_selects_first_line():
    memory = make_memory()

    assert select_eviction_index(
        memory, ITEM_TIME, "oldest"
    ) == 0


def test_source_aware_prefers_redundant_sources():
    memory = make_memory()

    assert select_eviction_index(
        memory, ITEM_TIME, "source_aware"
    ) == 1


def test_source_aware_preserves_source_coverage():
    memory = make_memory()
    original_sources = memory.sources()

    budget = memory.tokens(ITEM_TIME) - 1

    evicted = enforce_budget(
        memory, budget, ITEM_TIME, "source_aware"
    )

    assert len(evicted) == 1
    assert evicted[0]["id"] == "m2"
    assert memory.sources() == original_sources
    assert memory.tokens(ITEM_TIME) <= budget


def test_oldest_can_lose_unique_sources():
    memory = make_memory()
    budget = memory.tokens(ITEM_TIME) - 1

    evicted = enforce_budget(
        memory, budget, ITEM_TIME, "oldest"
    )

    assert evicted[0]["id"] == "m1"
    assert "item_1" not in memory.sources()


def test_source_aware_prefers_larger_token_savings():
    memory = Memory(
        lines=[
            MemLine("m1", "Flood.", ["item_1"]),
            MemLine(
                "m2",
                "Extensive flooding across residential streets.",
                ["item_1"],
            ),
        ]
    )

    assert select_eviction_index(
        memory, ITEM_TIME, "source_aware"
    ) == 1


@pytest.mark.parametrize("policy", ["oldest", "source_aware"])
def test_budget_is_strictly_enforced(policy):
    memory = make_memory()
    budget = memory.tokens(ITEM_TIME) // 2

    enforce_budget(memory, budget, ITEM_TIME, policy)

    assert memory.tokens(ITEM_TIME) <= budget


@pytest.mark.parametrize("policy", ["oldest", "source_aware"])
def test_no_eviction_when_within_budget(policy):
    memory = make_memory()
    original = memory.copy()

    evicted = enforce_budget(
        memory, memory.tokens(ITEM_TIME), ITEM_TIME, policy
    )

    assert evicted == []
    assert memory == original


def test_source_counts_are_recalculated():
    memory = Memory(
        lines=[
            MemLine("m1", "Flood.", ["item_1"]),
            MemLine("m2", "Flood.", ["item_1"]),
            MemLine("m3", "Flood.", ["item_2"]),
            MemLine("m4", "Flood.", ["item_2"]),
        ]
    )

    budget = memory.tokens(ITEM_TIME) // 2

    evicted = enforce_budget(
        memory, budget, ITEM_TIME, "source_aware"
    )

    assert len(evicted) == 2
    assert memory.sources() == {"item_1", "item_2"}


def test_zero_budget():
    memory = make_memory()

    enforce_budget(memory, 0, ITEM_TIME, "source_aware")

    assert memory.lines == []
    assert memory.tokens(ITEM_TIME) == 0


def test_eviction_is_deterministic():
    first = make_memory()
    second = make_memory()

    budget = first.tokens(ITEM_TIME) // 2

    evicted_first = enforce_budget(
        first, budget, ITEM_TIME, "source_aware"
    )
    evicted_second = enforce_budget(
        second, budget, ITEM_TIME, "source_aware"
    )

    assert evicted_first == evicted_second
    assert first == second


def test_invalid_policy_raises_error():
    with pytest.raises(ValueError):
        enforce_budget(
            make_memory(), 512, ITEM_TIME, "unknown"
        )


def test_negative_budget_raises_error():
    with pytest.raises(ValueError):
        enforce_budget(
            make_memory(), -1, ITEM_TIME, "source_aware"
        )