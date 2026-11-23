
import json

from PIL import Image

from streamrag.baselines.fifo import run_fifo_pass


class MockVLM:
    def __init__(self):
        self.calls = []

    def generate(self, prompt, images=None, max_new_tokens=None):
        self.calls.append({
            "prompt": prompt,
            "images": images,
            "max_new_tokens": max_new_tokens,
        })
        return "A damaged building with debris on the road."


def test_fifo_visual_memory_pass(tmp_path):
    # Create a synthetic image.
    image_path = tmp_path / "frame.png"
    Image.new("RGB", (32, 32), "gray").save(image_path)

    stream = {
        "items": [
            {
                "item_id": "item_001",
                "step": 1,
                "source": "camera",
                "time_str": "00:01",
                "text": "Emergency footage",
                "frames": [{"path": str(image_path)}],
            }
        ]
    }

    vlm = MockVLM()
    out_dir = tmp_path / "fifo_run"

    snapshots = run_fifo_pass(
        vlm=vlm,
        stream=stream,
        budget=512,
        out_dir=out_dir,
        progress=lambda message: None,
    )

    assert len(vlm.calls) == 1
    assert len(vlm.calls[0]["images"]) == 1

    assert len(snapshots) == 1
    assert snapshots[0]["tokens"] <= 512

    memory_lines = snapshots[0]["lines"]
    assert len(memory_lines) == 1
    assert memory_lines[0]["sources"] == ["item_001"]
    assert "damaged building" in memory_lines[0]["text"]
    assert "Emergency footage" in memory_lines[0]["text"]

    assert (out_dir / "snapshots.json").exists()
    assert (out_dir / "memory_log.json").exists()

    saved_snapshots = json.loads(
        (out_dir / "snapshots.json").read_text()
    )
    assert saved_snapshots == snapshots
