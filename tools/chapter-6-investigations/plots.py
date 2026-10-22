"""Standalone Matplotlib figures of declared cosine examples, with CSV data."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile

from facts import ANGLES, QUERY_VECTOR, unit_vector, scores, token_ids, CONTEXT_VECTORS, mean_pool, check_examples

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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter6-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    import numpy as np

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    colors = {"positive": teal, "hard": red, "easy": muted}
    labels = {"positive": "Positive", "hard": "Hard negative", "easy": "Easy negative"}
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 17,
             "axes.titlesize": 20, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter6-declared-cosine-v1", "svg.fonttype": "none"}

    with plt.rc_context(style):
        for state in ANGLES:
            fig = plt.figure(figsize=(14, 5.6), dpi=100, facecolor=cream)
            ax = fig.add_axes([.065, .19, .43, .69], facecolor=paper)
            ax.set(xlim=(-1.3, 1.3), ylim=(-.35, 1.35), xticks=[-1, 0, 1], yticks=[0, 1],
                   xlabel="Coordinate 1", ylabel="Coordinate 2")
            ax.set_aspect("equal")
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(color="#ccc4b6", alpha=.35)
            theta = np.linspace(0, 2*np.pi, 361)
            ax.plot(np.cos(theta), np.sin(theta), color="#ccc4b6", lw=1.5, ls="--")
            ax.scatter(*QUERY_VECTOR, s=90, color=blue, zorder=4)
            ax.annotate("Query", QUERY_VECTOR, xytext=(0, -25), textcoords="offset points", ha="center", color=blue)
            ax.annotate("", xy=QUERY_VECTOR, xytext=(0, 0), arrowprops={"arrowstyle": "->", "color": blue, "lw": 3})
            for name, angle in ANGLES[state].items():
                v = unit_vector(angle)
                ax.annotate("", xy=v, xytext=(0, 0), arrowprops={"arrowstyle": "->", "color": colors[name], "lw": 2.5})
                ax.scatter(*v, s=80, color=colors[name], zorder=4)
                ax.annotate(labels[name], v, xytext=(0, 13), textcoords="offset points", ha="center", color=colors[name], fontsize=16)
            ax.set_title("Invented unit-length vectors", pad=15)
            bx = fig.add_axes([.665, .23, .30, .61], facecolor=paper)
            names = ("positive", "hard", "easy")
            values = scores(state)
            bx.barh(range(3), [values[n] for n in names], height=.48, color=[colors[n] for n in names])
            bx.set(yticks=range(3), yticklabels=[labels[n] for n in names], xlim=(-1.2, 1.2),
                   xticks=[-1, 0, 1], xlabel="Cosine similarity to query")
            bx.invert_yaxis()
            bx.spines[["top", "right", "left"]].set_visible(False)
            bx.axvline(0, color=muted, lw=1)
            for i, name in enumerate(names):
                value = values[name]
                inside = abs(value) > .6
                x = value-(.04 if value > 0 else -.04) if inside else value+(.04 if value > 0 else -.04)
                ha = ("right" if value > 0 else "left") if inside else ("left" if value > 0 else "right")
                bx.text(x, i, f"{value:.3f}", va="center", ha=ha, fontsize=16, color=paper if inside else ink)
            bx.set_title("Initial toy comparison" if state == "before" else "Desired toy comparison", pad=20)
            fig.text(.055, .025, "Constructed examples, not model measurements or a training trajectory. Cosine scores are not relevance probabilities.", fontsize=14, color=muted)
            name = f"comparison-{state}"
            fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; declared toy cosine example"})
            fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original declared toy comparison; not a model measurement"})
            plt.close(fig)

    with (directory / "toy-scores.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["state", "record_label", "angle_degrees", "coordinate_1", "coordinate_2", "cosine_to_query_1_0", "measured_model_output"])
        for state in ANGLES:
            for name, angle in ANGLES[state].items():
                writer.writerow([state, name, angle, *[format(x, ".17g") for x in unit_vector(angle)], format(scores(state)[name], ".17g"), False])
    with (directory / "toy-pooling.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["position", "character", "toy_token_id", "coordinate_1", "coordinate_2", "coordinate_3", "measured_model_output"])
        for i, (char, ident, vector) in enumerate(zip("delulu", token_ids(), CONTEXT_VECTORS), 1):
            writer.writerow([i, char, ident, *vector, False])
        writer.writerow(["mean", "", "", *mean_pool(), False])
    manifest = {"recipe_sha256": recipe, "kind": "declared cosine and pooling examples",
                "measured_model_outputs": False, "checks": check_examples(),
                "files": {p.name: sha(p) for p in sorted(directory.iterdir()) if p.suffix in (".png", ".svg", ".csv")}, "passed": True}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return sha(manifest_path)
