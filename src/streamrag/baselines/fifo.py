import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from PIL import Image

from streamrag.memory.agent import Memory, MemLine
from streamrag.records import write_json


@dataclass
class FIFOMemory:
    """Fixed FIFO retention policy using the existing memory format."""

    budget: int
    memory: Memory = field(default_factory=Memory)

    def add(
        self,
        text: str,
        source_id: str,
        item_time: dict[str, str],
    ) -> list[str]:
        """Append an observation and evict oldest lines if over budget.

        Returns the IDs of evicted memory lines.
        """
        text = text.strip()
        if not text:
            return []

        line = MemLine(
            id=f"m{self.memory.next_id}",
            text=text,
            sources=[source_id],
        )
        self.memory.next_id += 1
        self.memory.lines.append(line)

        evicted = []
        while (
            self.memory.lines
            and self.memory.tokens(item_time) > self.budget
        ):
            oldest = self.memory.lines.pop(0)
            evicted.append(oldest.id)

        return evicted


def run_fifo_pass(
    vlm,
    stream: dict,
    budget: int,
    out_dir: Path,
    progress=print,
) -> list[dict]:
    """Generate independent observations and retain them using FIFO."""
    out_dir.mkdir(parents=True, exist_ok=True)

    fifo = FIFOMemory(budget)
    item_time = {
        item["item_id"]: item["time_str"]
        for item in stream["items"]
    }

    snapshots = []
    logs = []

    for k, item in enumerate(stream["items"], 1):
        start = time.time()

        images = []
        for frame in item.get("frames", []):
            with Image.open(frame["path"]) as image:
                images.append(image.convert("RGB"))

        prompt = (
            "Describe the observable facts in this evidence item concisely. "
            "Include visible objects, people, locations, actions, quantities, "
            "and changes of state when identifiable. "
            "Do not invent details. Output only the observation."
        )

        if images:
            caption = vlm.generate(
                prompt,
                images=images,
                max_new_tokens=96,
            ).strip()
        else:
            caption = ""

        text = (item.get("text") or "").strip()
        observation = "\n".join(
            part for part in (text, caption) if part
        )

        evicted = fifo.add(
            observation,
            item["item_id"],
            item_time,
        )

        memory = fifo.memory

        snapshot = {
            "step": item["step"],
            "tokens": memory.tokens(item_time),
            "lines": [asdict(line) for line in memory.lines],
        }
        snapshots.append(snapshot)

        log = {
            "step": item["step"],
            "item_id": item["item_id"],
            "n_lines": len(memory.lines),
            "tokens": snapshot["tokens"],
            "evicted": evicted,
            "fallback": None,
            "secs": round(time.time() - start, 2),
        }
        logs.append(log)

        write_json(out_dir / "snapshots.json", snapshots)
        write_json(out_dir / "memory_log.json", logs)

        progress(
            f"FIFO step {k}/{len(stream['items'])}: "
            f"{len(memory.lines)} lines, "
            f"{snapshot['tokens']}/{budget} tokens"
        )

    return snapshots