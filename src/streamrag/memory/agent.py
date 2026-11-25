"""Strategy-driven memory agent harness (codebase_plan.md §11.2).

The memory agent (Nemotron, a VLM) sees each new evidence item (image + text) once, together
with its strategy text and current memory, and replies with JSON edit operations. The harness
enforces provenance (sources must be delivered items) and the token budget, retries once on
invalid or over-budget output, falls back deterministically, and logs every step.
"""
from __future__ import annotations

import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from PIL import Image

from streamrag.config import CONFIG_DIR, load_yaml
from streamrag.memory.tokens import count_tokens
from streamrag.memory.eviction import EVICTION_POLICIES, enforce_budget
from streamrag.parsing import parse_json_object
from streamrag.records import lines, write_json

FRAME = (CONFIG_DIR / "memory" / "frame.txt").read_text()


@dataclass
class MemLine:
    id: str
    text: str
    sources: list[str]

    def render(self, item_time: dict[str, str]) -> str:
        src = ", ".join(f"{s} @{item_time.get(s, '?')}" for s in self.sources)
        return f"{self.id} [src {src}] {self.text}"


@dataclass
class Memory:
    lines: list[MemLine] = field(default_factory=list)
    next_id: int = 1

    def render(self, item_time: dict[str, str]) -> str:
        return "\n".join(l.render(item_time) for l in self.lines) or "(empty)"

    def tokens(self, item_time: dict[str, str]) -> int:
        return sum(count_tokens(l.render(item_time)) + 1 for l in self.lines)

    def copy(self) -> "Memory":
        return Memory([MemLine(l.id, l.text, list(l.sources)) for l in self.lines], self.next_id)

    def sources(self) -> set[str]:
        return {s for l in self.lines for s in l.sources}


def apply_edits(mem: Memory, edits: dict, delivered: set[str]) -> tuple[Memory, list[str]]:
    """Apply add/update/delete ops; returns new memory and a list of rule problems."""
    new, problems = mem.copy(), []
    by_id = {l.id: l for l in new.lines}
    for mid in edits.get("delete") or []:
        if mid in by_id:
            new.lines.remove(by_id.pop(mid))
        else:
            problems.append(f"delete of unknown line {mid}")
    for u in edits.get("update") or []:
        l = by_id.get(str(u.get("id")))
        if l is None:
            problems.append(f"update of unknown line {u.get('id')}")
            continue
        srcs = [s for s in (u.get("sources") or l.sources) if s in delivered]
        if len(srcs) < len(u.get("sources") or []):
            problems.append(f"update {l.id}: undelivered sources dropped")
        l.text = str(u.get("text", l.text)).strip() or l.text
        l.sources = sorted(set(l.sources) | set(srcs))
    for a in edits.get("add") or []:
        text = str(a.get("text", "")).strip()
        srcs = [s for s in (a.get("sources") or []) if s in delivered]
        if not text:
            continue
        if not srcs:
            problems.append("add without valid sources")
            continue
        new.lines.append(MemLine(f"m{new.next_id}", text, sorted(set(srcs))))
        new.next_id += 1
    return new, problems


class MemoryAgent:
    def __init__(self, vlm, strategy: str, budget: int,
                 frame: str | None = None,
                 eviction_policy: str = "oldest"):
        if eviction_policy not in EVICTION_POLICIES:
            raise ValueError(
                f"Unknown eviction policy: {eviction_policy}"
            )
        if budget < 0:
            raise ValueError("Memory budget cannot be negative")

        self.vlm, self.strategy, self.budget = vlm, strategy, budget
        self.eviction_policy = eviction_policy
        self.frame = frame or FRAME
        self.max_new_tokens = load_yaml("eval")["memory_agent"]["max_new_tokens"]

    def _prompt(self, mem: Memory, item: dict, item_time: dict, note: str = "") -> str:
        text = f"\nText: {item['text']}" if item.get("text") else ""
        p = self.frame.format(budget=self.budget, strategy=self.strategy.strip(), used=mem.tokens(item_time),
                         memory=mem.render(item_time), item_id=item["item_id"], source=item["source"],
                         time_str=item["time_str"], text=text)
        return p + (f"\n\nNOTE: {note}" if note else "")

    def step(self, mem: Memory, item: dict, delivered: set[str], item_time: dict) -> tuple[Memory, dict]:
        images = [Image.open(f["path"]).convert("RGB") for f in item.get("frames", [])]
        log = {"item_id": item["item_id"], "step": item["step"], "attempts": []}
        note = ""
        t0 = time.time()
        result = None
        for attempt in range(2):
            raw = self.vlm.generate(self._prompt(mem, item, item_time, note), images=images or None,
                                    max_new_tokens=self.max_new_tokens)
            edits = parse_json_object(raw)
            entry = {"raw": lines(raw), "valid_json": edits is not None}
            if edits is None:
                note = "Your previous reply was not a valid JSON object. Reply with ONLY the JSON object."
                log["attempts"].append(entry)
                continue
            cand, problems = apply_edits(mem, edits, delivered)
            used = cand.tokens(item_time)
            entry.update({"edits": edits, "problems": problems, "tokens_after": used})
            log["attempts"].append(entry)
            result = cand
            if used <= self.budget:
                break
            note = (f"Your edits would make the memory {used} tokens, over the budget of {self.budget} "
                    f"by {used - self.budget}. Delete or shorten lines so it fits.")
        if result is None:                       # two invalid replies: keep memory unchanged
            result, log["fallback"] = mem.copy(), "invalid_output_noop"
        evicted = enforce_budget(
            result,
            self.budget,
            item_time,
            self.eviction_policy,
        )

        log["eviction_policy"] = self.eviction_policy

        if evicted:
            log["fallback"] = log.get(
                "fallback",
                f"budget_evict_{self.eviction_policy}",
            )
            log["evicted"] = evicted
        log.update({"tokens": result.tokens(item_time), "n_lines": len(result.lines),
                    "secs": round(time.time() - t0, 2)})
        return result, log


def run_memory_pass(vlm, strategy: str, stream: dict, budget: int, out_dir: Path,
                    frame: str | None = None, progress=print,
                    eviction_policy: str = "oldest") -> list[dict]:
    """Feed the stream from step 1; write snapshots.json and memory_log.json (indented, rewritten
    after every step so partial runs are readable). Returns the snapshots."""
    out_dir.mkdir(parents=True, exist_ok=True)
    agent = MemoryAgent(
        vlm, strategy, budget, frame,
        eviction_policy=eviction_policy,
    )
    item_time = {it["item_id"]: it["time_str"] for it in stream["items"]}
    mem, delivered, snaps, logs = Memory(), set(), [], []
    N = len(stream["items"])
    for k, item in enumerate(stream["items"], 1):
        delivered.add(item["item_id"])
        mem, log = agent.step(mem, item, delivered, item_time)
        snaps.append({"step": item["step"], "tokens": mem.tokens(item_time),
                      "lines": [asdict(l) for l in mem.lines]})
        logs.append(log)
        write_json(out_dir / "snapshots.json", snaps)
        write_json(out_dir / "memory_log.json", logs)
        progress(f"memory step {k:2d}/{N} ({item['item_id']}): {log['n_lines']} lines, "
                 f"{log['tokens']}/{budget} tokens, {log['secs']:.1f}s"
                 + (f"  [{log['fallback']}]" if log.get("fallback") else ""))
    return snaps
