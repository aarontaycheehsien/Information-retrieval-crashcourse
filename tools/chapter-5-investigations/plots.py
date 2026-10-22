"""Standalone Matplotlib figures with explicit toy data and provenance hashes."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile

from facts import TOY_WORDS, PROJECTION_POINTS, analogy, project, check_examples

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_plots(directory, manifest_hash):
    directory = Path(directory)
    assert sha(directory / "plots-manifest.json") == manifest_hash
    manifest = json.loads((directory / "plots-manifest.json").read_text())
    for name, value in manifest["files"].items():
        assert sha(directory / name) == value, f"Plot asset changed: {name}"
    return manifest


def ensure_plots(directory):
    directory = Path(directory)
    directory.mkdir(exist_ok=True, parents=True)
    recipe = hashlib.sha256((HERE / "plots.py").read_bytes() + (HERE / "facts.py").read_bytes()
                            + importlib.metadata.version("matplotlib").encode()).hexdigest()
    manifest_path = directory / "plots-manifest.json"
    if manifest_path.exists():
        m = json.loads(manifest_path.read_text())
        if m["recipe_sha256"] == recipe and all((directory / n).is_file() and sha(directory / n) == v for n, v in m["files"].items()):
            return sha(manifest_path)
    check_examples()
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter5-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 17,
             "axes.titlesize": 20, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter5-declared-toy-v1", "svg.fonttype": "none"}

    def finish(fig, name):
        fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; declared toy geometry"})
        fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original declared toy geometry; not a model measurement"})
        plt.close(fig)

    with plt.rc_context(style):
        for revealed in (False, True):
            fig = plt.figure(figsize=(14, 5.6), dpi=100, facecolor=cream)
            ax = fig.add_axes([.075, .17, .53, .72], facecolor=paper)
            ax.set(xlim=(0, 7), ylim=(0, 6), xticks=range(8), yticks=range(7),
                   xlabel="Coordinate 1 · invented values", ylabel="Coordinate 2")
            ax.set_aspect("equal")
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(color="#ccc4b6", alpha=.4)
            for name, (x, y) in TOY_WORDS.items():
                color = teal if name in ("woman", "queen") else blue if name != "tree" else muted
                ax.scatter(x, y, s=100, color=color, zorder=3)
                offset = (-12, 10) if name in ("man", "king") else (8, 10)
                ax.annotate(name, (x, y), xytext=offset, textcoords="offset points", color=color,
                            ha="right" if name in ("man", "king") else "left")
            for a, b in [("man", "woman")] + ([("king", "queen")] if revealed else []):
                ax.annotate("", xy=TOY_WORDS[b], xytext=TOY_WORDS[a],
                            arrowprops={"arrowstyle": "->", "color": red, "lw": 3, "shrinkA": 10, "shrinkB": 10})
            fig.text(.65, .78, "A DECLARED TOY SPACE", fontsize=18, weight="bold", color=blue)
            fig.text(.65, .64, "man → woman: (3, 1)", fontsize=21)
            fig.text(.65, .52, "king → queen: (3, 1)" if revealed else "Can we reuse that move?", fontsize=21)
            if revealed:
                fig.text(.65, .37, "king − man + woman", fontsize=21)
                fig.text(.65, .27, f"= ({analogy()[0]:g}, {analogy()[1]:g}) = queen", fontsize=21, color=teal)
            fig.text(.075, .025, "Constructed coordinates, not trained vectors. Real analogy performance is model- and task-dependent.", fontsize=15, color=muted)
            finish(fig, "analogy-after" if revealed else "analogy-before")

        fig = plt.figure(figsize=(14, 5.6), dpi=100, facecolor=cream)
        ax = fig.add_axes([.06, .17, .39, .72], projection="3d", facecolor=paper)
        p, q = PROJECTION_POINTS.values()
        ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]], color=red, lw=3)
        for name, (x, y, z) in PROJECTION_POINTS.items():
            ax.scatter(x, y, z, s=90, color=blue if name == "P" else teal)
            ax.text(x+.15, y, z, f"{name} ({x:g}, {y:g}, {z:g})", fontsize=15)
        ax.set(xlim=(0, 4), ylim=(0, 4), zlim=(0, 10), xticks=[0, 2, 4], yticks=[0, 2, 4], zticks=[0, 5, 10])
        ax.set_title("Original 3D points · distance 10", pad=8)
        ax.set_xlabel("Coordinate 1", labelpad=5)
        ax.set_ylabel("Coordinate 2", labelpad=5)
        ax.set_zlabel("Coordinate 3", labelpad=5)
        ax.view_init(elev=18, azim=-55)
        bx = fig.add_axes([.62, .22, .3, .64], facecolor=paper)
        bx.set(xlim=(0, 4), ylim=(0, 4), xticks=range(5), yticks=range(5), xlabel="Coordinate 1", ylabel="Coordinate 2")
        bx.set_aspect("equal")
        bx.grid(color="#ccc4b6", alpha=.4)
        bx.spines[["top", "right"]].set_visible(False)
        bx.scatter(*project(p), s=160, color=red)
        bx.annotate("P and Q\n(2, 2)", project(p), xytext=(20, 16), textcoords="offset points")
        bx.set_title("Drop coordinate 3\nProjected distance 0", pad=13)
        fig.text(.47, .53, "→", fontsize=40, color=red)
        fig.text(.055, .025, "Constructed coordinate projection, not PCA. Coincidence in the picture does not imply coincidence in the full space.", fontsize=15, color=muted)
        finish(fig, "projection-loss")

    with (directory / "toy-geometry.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["example", "item", "coordinate_1", "coordinate_2", "coordinate_3", "measured_model_output"])
        for name, values in TOY_WORDS.items():
            w.writerow(["analogy", name, *values, "", False])
        for name, values in PROJECTION_POINTS.items():
            w.writerow(["projection", name, *values, False])
    manifest = {"recipe_sha256": recipe, "kind": "declared toy geometry",
                "trained_model_outputs": False, "checks": check_examples(),
                "files": {p.name: sha(p) for p in sorted(directory.iterdir()) if p.suffix in (".png", ".svg", ".csv")}, "passed": True}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return sha(manifest_path)
