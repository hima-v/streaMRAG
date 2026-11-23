
from streamrag.baselines.fifo import FIFOMemory


def test_fifo_adds_observations():
    fifo = FIFOMemory(budget=512)
    times = {"img1": "10:00", "img2": "10:01"}

    fifo.add("A flooded street", "img1", times)
    fifo.add("A damaged building", "img2", times)

    assert len(fifo.memory.lines) == 2
    assert fifo.memory.lines[0].text == "A flooded street"
    assert fifo.memory.lines[1].text == "A damaged building"


def test_fifo_preserves_sources():
    fifo = FIFOMemory(budget=512)
    times = {"img1": "10:00"}

    fifo.add("A flooded street", "img1", times)

    assert fifo.memory.lines[0].sources == ["img1"]
    assert fifo.memory.lines[0].id == "m1"


def test_fifo_evicts_oldest_first():
    times = {
        "img1": "10:00",
        "img2": "10:01",
        "img3": "10:02",
    }

    # Measure the actual token cost rather than guessing.
    probe = FIFOMemory(budget=512)
    probe.add("First observation", "img1", times)
    one_line_tokens = probe.memory.tokens(times)

    fifo = FIFOMemory(budget=one_line_tokens)
    fifo.add("First observation", "img1", times)
    fifo.add("Second observation", "img2", times)
    fifo.add("Third observation", "img3", times)

    assert len(fifo.memory.lines) == 1
    assert fifo.memory.lines[0].text == "Third observation"
    assert fifo.memory.tokens(times) <= fifo.budget


def test_fifo_respects_token_budget():
    fifo = FIFOMemory(budget=40)
    times = {f"img{i}": f"10:{i:02d}" for i in range(10)}

    for i in range(10):
        fifo.add(f"Observation number {i}", f"img{i}", times)
        assert fifo.memory.tokens(times) <= fifo.budget


def test_fifo_skips_empty_observations():
    fifo = FIFOMemory(budget=512)

    fifo.add("   ", "img1", {"img1": "10:00"})

    assert fifo.memory.lines == []
