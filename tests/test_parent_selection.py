import random
from collections import Counter

import pytest

from streamrag.meta.archive import Archive, Node


def make_node(node_id, score, parent_id=None):
    return Node(
        node_id=node_id,
        parent_id=parent_id,
        dataset="disastervqa",
        eval_stream="test_stream",
        budget=512,
        strategy_id="test_strategy",
        harness_id="test_harness",
        switches={},
        created_by={},
        scores=None if score is None else {"esqa_mean": score},
    )


@pytest.fixture
def archive(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "streamrag.meta.archive.OUTPUT_DIR", tmp_path
    )
    return Archive("disastervqa", "test_selection")


def test_best_selects_highest_score(archive):
    archive.nodes = {
        0: make_node(0, 0.20),
        1: make_node(1, 0.28),
        2: make_node(2, 0.24),
    }

    assert archive.select_parent("best").node_id == 1


def test_population_selection_explores_multiple_parents(archive):
    archive.nodes = {
        0: make_node(0, 0.20),
        1: make_node(1, 0.28),
        2: make_node(2, 0.24),
    }

    rng = random.Random(42)
    selected = {
        archive.select_parent("score_child_prop", rng).node_id
        for _ in range(1000)
    }

    assert selected == {0, 1, 2}


def test_population_selection_favors_higher_scores(archive):
    archive.nodes = {
        0: make_node(0, 0.10),
        1: make_node(1, 0.50),
    }

    rng = random.Random(42)
    counts = Counter(
        archive.select_parent("score_child_prop", rng).node_id
        for _ in range(1000)
    )

    assert counts[1] > counts[0]


def test_population_selection_penalizes_many_children(archive):
    archive.nodes = {
        0: make_node(0, 0.24),
        1: make_node(1, 0.24),
    }

    for i in range(2, 14):
        archive.nodes[i] = make_node(i, None, parent_id=0)

    rng = random.Random(42)
    counts = Counter(
        archive.select_parent("score_child_prop", rng).node_id
        for _ in range(1000)
    )

    assert counts[1] > counts[0]


def test_population_selection_is_reproducible(archive):
    archive.nodes = {
        0: make_node(0, 0.20),
        1: make_node(1, 0.28),
    }

    rng1 = random.Random(42)
    rng2 = random.Random(42)

    first = [
        archive.select_parent("score_child_prop", rng1).node_id
        for _ in range(100)
    ]

    second = [
        archive.select_parent("score_child_prop", rng2).node_id
        for _ in range(100)
    ]

    assert first == second


def test_unscored_nodes_are_not_selected(archive):
    archive.nodes = {
        0: make_node(0, 0.20),
        1: make_node(1, None),
    }

    assert archive.select_parent("best").node_id == 0
    assert archive.select_parent("score_child_prop").node_id == 0


def test_no_scored_nodes_raises_error(archive):
    archive.nodes = {
        0: make_node(0, None),
    }

    with pytest.raises(RuntimeError):
        archive.select_parent("score_child_prop")