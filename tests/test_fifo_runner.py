from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from scripts import run_experiment as runner


@pytest.mark.parametrize(
    "method, eviction_policy",
    [
        ("fifo", "oldest"),
        ("agent", "oldest"),
        ("agent", "source_aware"),
    ],
)
def test_memory_method_dispatch(
    tmp_path, monkeypatch, method, eviction_policy
):
    stream = {
        "stream_id": "test_stream",
        "n_steps": 1,
        "items": [{"item_id": "item_001"}],
    }

    node = SimpleNamespace(
        node_id=0,
        dataset="disastervqa",
        budget=512,
        models={"profile": "minimal"},
    )

    arch = Mock()
    arch.nodes = {0: node}
    arch.node_dir.return_value = tmp_path
    arch.strategy.return_value = "Test strategy"

    vlm = Mock()
    progress = Mock()

    snapshots = [
        {"step": 1, "tokens": 0, "lines": []}
    ]

    fifo_mock = Mock(return_value=snapshots)
    agent_mock = Mock(return_value=snapshots)

    monkeypatch.setattr(
        runner, "eval_streams", lambda node: [stream]
    )
    monkeypatch.setattr(
        runner, "profile_files",
        lambda *args: {"memory_frame": "test_frame"}
    )
    monkeypatch.setattr(
        runner, "read_cfg", lambda *args: "Test frame"
    )
    monkeypatch.setattr(
        runner, "run_fifo_pass", fifo_mock
    )
    monkeypatch.setattr(
        runner, "run_memory_pass", agent_mock
    )

    results = runner.memory_passes(
        arch,
        node,
        vlm,
        progress,
        memory_method=method,
        eviction_policy=eviction_policy,
    )

    run_dir = tmp_path / "runs" / stream["stream_id"]

    if method == "fifo":
        fifo_mock.assert_called_once_with(
            vlm,
            stream,
            node.budget,
            run_dir,
            progress=progress,
        )
        agent_mock.assert_not_called()
    else:
        agent_mock.assert_called_once_with(
            vlm,
            "Test strategy",
            stream,
            node.budget,
            run_dir,
            "Test frame",
            progress,
            eviction_policy=eviction_policy,
        )
        fifo_mock.assert_not_called()

    assert len(results) == 1
    assert results[0][0] == stream
    assert results[0][1] == run_dir
    assert results[0][2] == snapshots