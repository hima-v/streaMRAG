"""Visualize an experiment archive.

  python scripts/visualize_run.py --dataset disastervqa --archive run1

Writes to outputs/archive/<dataset>/<archive>/:
  best_score.png    best score so far (mean ESQA) at each iteration, plus every node's own score
  archive_tree.png  parent -> child tree of the generated hyperagents (node colour = score, best ringed)
and prints the tree as text. Works on archives written by older versions (archive.jsonl) too.
"""
from __future__ import annotations

import argparse
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.colors import LinearSegmentedColormap, Normalize  # noqa: E402

from streamrag.meta.archive import Archive  # noqa: E402

# reference palette (light mode): surfaces, text inks, series-1 blue, sequential blue ramp
SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#a3a29c", "#e4e3df"
SERIES1 = "#2a78d6"
RAMP = ["#b7d3f6", "#86b6ef", "#5598e7", "#2a78d6", "#1c5cab", "#104281"]   # steps 150 .. 650
SCORE_CMAP = LinearSegmentedColormap.from_list("score", RAMP)


def _style(ax):
    ax.set_facecolor(SURFACE)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
    ax.tick_params(colors=INK2, labelsize=9)
    ax.yaxis.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


def plot_best(arch: Archive, path) -> None:
    nodes = sorted((n for n in arch.nodes.values() if n.scores), key=lambda n: n.node_id)
    if not nodes:
        print("no scored nodes yet")
        return
    its = list(range(1, len(nodes) + 1))                 # one new node per iteration
    own = [n.scores["esqa_mean"] for n in nodes]
    best, best_node, cur, cur_node = [], [], -1.0, None
    for n, s in zip(nodes, own):
        if s >= cur:
            cur, cur_node = s, n.node_id
        best.append(cur)
        best_node.append(cur_node)

    fig, ax = plt.subplots(figsize=(max(6, 0.55 * len(its) + 3), 4), facecolor=SURFACE)
    _style(ax)
    ax.scatter(its, own, s=64, color=MUTED, edgecolor=SURFACE, linewidth=2, zorder=3, label="node score")
    ax.step(its, best, where="post", color=SERIES1, linewidth=2, zorder=4, label="best so far")
    ax.scatter(its, best, s=64, color=SERIES1, edgecolor=SURFACE, linewidth=2, zorder=5)
    ax.annotate(f"best: node {best_node[-1]}, {best[-1]:.3f}", (its[-1], best[-1]), xytext=(8, 8),
                textcoords="offset points", color=INK, fontsize=9)
    ax.set_xticks(its, [f"{i}\nn{n.node_id}" for i, n in zip(its, nodes)])
    ax.set_xlim(0.5, len(its) + 1.2)
    lo = min(own)
    ax.set_ylim(max(0.0, lo - 0.1), min(1.0, max(own) + 0.12))
    ax.set_xlabel("iteration (node created)", color=INK2, fontsize=10)
    ax.set_ylabel("mean ESQA (higher is better)", color=INK2, fontsize=10)
    ax.set_title(f"{arch.dir.name}: best hyperagent score per iteration", color=INK, fontsize=12, loc="left")
    leg = ax.legend(frameon=False, fontsize=9, loc="lower right")
    for t in leg.get_texts():
        t.set_color(INK2)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def tree_layout(arch: Archive) -> dict[int, tuple[float, float]]:
    kids = defaultdict(list)
    for n in arch.nodes.values():
        if n.parent_id is not None:
            kids[n.parent_id].append(n.node_id)
    pos, next_x = {}, [0]

    def place(nid: int, depth: int) -> float:
        ch = sorted(kids[nid])
        if not ch:
            x = next_x[0]
            next_x[0] += 1
        else:
            xs = [place(c, depth + 1) for c in ch]
            x = sum(xs) / len(xs)
        pos[nid] = (x, -depth)
        return x

    for root in sorted(n.node_id for n in arch.nodes.values() if n.parent_id is None):
        place(root, 0)
    return pos


def plot_tree(arch: Archive, path) -> None:
    pos = tree_layout(arch)
    scored = [n for n in arch.nodes.values() if n.scores]
    best = max(scored, key=lambda n: (n.scores["esqa_mean"], n.node_id)) if scored else None
    vals = [n.scores["esqa_mean"] for n in scored] or [0, 1]
    norm = Normalize(min(vals), max(vals) if max(vals) > min(vals) else min(vals) + 1e-6)
    width = max(pos.values(), key=lambda p: p[0])[0] + 1
    depth = -min(p[1] for p in pos.values()) + 1
    fig, ax = plt.subplots(figsize=(max(5, 1.3 * width + 2), max(3, 1.3 * depth + 1)), facecolor=SURFACE)
    ax.set_facecolor(SURFACE)
    ax.axis("off")
    for n in arch.nodes.values():
        if n.parent_id is not None:
            (x0, y0), (x1, y1) = pos[n.parent_id], pos[n.node_id]
            ax.plot([x0, x1], [y0, y1], color=MUTED, linewidth=1.5, zorder=1)
    for n in arch.nodes.values():
        x, y = pos[n.node_id]
        if n.scores:
            v = n.scores["esqa_mean"]
            fill = SCORE_CMAP(norm(v))
            txt_col = SURFACE if norm(v) > 0.45 else INK
            label = f"n{n.node_id}\n{v:.3f}"
            ax.scatter([x], [y], s=1500, color=fill, edgecolor=SURFACE, linewidth=2, zorder=2)
        else:
            txt_col, label = INK2, f"n{n.node_id}\nunscored"
            ax.scatter([x], [y], s=1500, color=SURFACE, edgecolor=MUTED, linewidth=1.5, linestyle="--", zorder=2)
        if best is not None and n.node_id == best.node_id:
            ax.scatter([x], [y], s=2100, facecolor="none", edgecolor=INK, linewidth=2.5, zorder=3)
            ax.annotate("best", (x, y), xytext=(28, 0), textcoords="offset points", ha="left", va="center",
                        color=INK, fontsize=9, fontweight="bold")
        ax.text(x, y, label, ha="center", va="center", fontsize=8, color=txt_col, zorder=4)
    ax.set_xlim(-0.8, width - 0.2)
    ax.set_ylim(-depth + 0.4, 0.7)
    ax.set_title(f"{arch.dir.name}: archive tree (root at top; colour = mean ESQA)",
                 color=INK, fontsize=12, loc="left")
    if scored:
        sm = plt.cm.ScalarMappable(cmap=SCORE_CMAP, norm=norm)
        cb = fig.colorbar(sm, ax=ax, fraction=0.04, pad=0.02)
        cb.set_label("mean ESQA", color=INK2, fontsize=9)
        cb.ax.tick_params(colors=INK2, labelsize=8)
        cb.outline.set_visible(False)
    fig.tight_layout()
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def text_tree(arch: Archive) -> str:
    kids = defaultdict(list)
    for n in arch.nodes.values():
        if n.parent_id is not None:
            kids[n.parent_id].append(n.node_id)
    scored = [n for n in arch.nodes.values() if n.scores]
    best = max(scored, key=lambda n: (n.scores["esqa_mean"], n.node_id)).node_id if scored else None
    out = []

    def walk(nid, prefix, last, root):
        n = arch.nodes[nid]
        sc = f"{n.scores['esqa_mean']:.3f}" if n.scores else "unscored"
        tag = "   <- best" if nid == best else ""
        out.append(("" if root else prefix + ("└── " if last else "├── ")) + f"node {nid}  {sc}{tag}")
        ch = sorted(kids[nid])
        for i, c in enumerate(ch):
            walk(c, "" if root else prefix + ("    " if last else "│   "), i == len(ch) - 1, False)

    for r in sorted(n.node_id for n in arch.nodes.values() if n.parent_id is None):
        walk(r, "", True, True)
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dataset", default="disastervqa")
    ap.add_argument("--archive", required=True)
    a = ap.parse_args()
    arch = Archive(a.dataset, a.archive)
    if not arch.nodes:
        raise SystemExit(f"archive {arch.dir} is empty")
    plot_best(arch, arch.dir / "best_score.png")
    plot_tree(arch, arch.dir / "archive_tree.png")
    print(text_tree(arch))
    print(f"\nwrote {arch.dir / 'best_score.png'}\n      {arch.dir / 'archive_tree.png'}")


if __name__ == "__main__":
    main()
