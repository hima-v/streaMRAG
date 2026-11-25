"""Deterministic memory-budget enforcement policies."""

from collections import Counter
from dataclasses import asdict

from streamrag.memory.tokens import count_tokens


EVICTION_POLICIES = ("oldest", "source_aware")


def select_eviction_index(memory, item_time, policy):
    """Select a memory line for eviction."""

    if policy not in EVICTION_POLICIES:
        raise ValueError(f"Unknown eviction policy: {policy}")

    if not memory.lines:
        raise ValueError("Cannot evict from empty memory")

    if policy == "oldest":
        return 0

    source_counts = Counter(
        source
        for line in memory.lines
        for source in set(line.sources)
    )

    def eviction_priority(index):
        line = memory.lines[index]

        unique_sources = sum(
            source_counts[source] == 1
            for source in set(line.sources)
        )

        tokens_saved = count_tokens(
            line.render(item_time)
        ) + 1

        return (
            unique_sources,
            -tokens_saved,
            index,
        )

    return min(
        range(len(memory.lines)),
        key=eviction_priority,
    )


def enforce_budget(memory, budget, item_time, policy="oldest"):
    """Enforce the token budget and return evicted lines."""

    if policy not in EVICTION_POLICIES:
        raise ValueError(f"Unknown eviction policy: {policy}")

    if budget < 0:
        raise ValueError("Memory budget cannot be negative")

    evicted = []

    while memory.tokens(item_time) > budget and memory.lines:
        index = select_eviction_index(
            memory, item_time, policy
        )

        evicted.append(
            asdict(memory.lines.pop(index))
        )

    return evicted