"""Standalone Matplotlib figures and CSVs for vector rules and neighbour search."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile

from facts import QUERY, VECTORS, ANN_QUERY, ANN_POINTS, APPROX_EXAMINED, normalise, scores, distances, nearest, check_examples

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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter7-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    colors = {"A": teal, "B": red, "C": muted}
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter7-vector-neighbours-v1", "svg.fonttype": "none"}

    def save(fig, name):
        fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; original vector teaching illustration"})
        fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original vector teaching illustration; not a model measurement"})
        plt.close(fig)

    def table(ax, data, headers, widths):
        ax.axis("off")
        t = ax.table(cellText=data, colLabels=headers, colWidths=widths, cellLoc="center", bbox=[0, .2, 1, .64])
        t.auto_set_font_size(False)
        t.set_fontsize(17)
        for (row, col), cell in t.get_celld().items():
            cell.set_edgecolor("#ccc4b6")
            cell.set_facecolor(paper)
            cell.get_text().set_color(ink)
            if row == 0:
                cell.get_text().set_weight("bold")
                cell.get_text().set_fontsize(16)
        return t

    with plt.rc_context(style):
        for unit in (False, True):
            fig = plt.figure(figsize=(14, 5.6), dpi=100, facecolor=cream)
            ax = fig.add_axes([.07, .18, .43, .71], facecolor=paper)
            ax.set(xlim=(-.8, 1.4), ylim=(-.25, 1.3), xticks=[-.5, 0, .5, 1], yticks=[0, .5, 1],
                   xlabel="Coordinate 1", ylabel="Coordinate 2")
            ax.set_aspect("equal")
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(color="#ccc4b6", alpha=.4)
            plotted = {n: normalise(v) if unit else v for n, v in VECTORS.items()}
            for name, vector in {"Q": QUERY, **plotted}.items():
                color = blue if name == "Q" else colors[name]
                ax.annotate("", xy=vector, xytext=(0, 0), arrowprops={"arrowstyle": "->", "color": color, "lw": 3})
                ax.scatter(*vector, s=70, color=color, zorder=4)
                ax.annotate(name, vector, xytext=(0, -25) if name == "Q" else (10, 8), textcoords="offset points", color=color, weight="bold")
            ax.set_title("Every vector normalised to unit length" if unit else "Declared toy vectors · Q = (1, 0)", pad=14)
            bx = fig.add_axes([.56, .16, .41, .72])
            rows = [[n, f"({v[0]:.3f}, {v[1]:.3f})" if unit else str(tuple(v)),
                     f"{scores('cosine', unit)[n]:.3f}", f"{scores('dot', unit)[n]:.3f}"] for n, v in plotted.items()]
            t = table(bx, rows, ["Vector", "Coordinates", "Cosine", "Dot"], [.14, .38, .24, .24])
            for row, col in [(1, 2), (1 if unit else 2, 3)]:
                t[row, col].set_facecolor(teal if row == 1 else red)
                t[row, col].get_text().set_color(paper)
                t[row, col].get_text().set_weight("bold")
            bx.set_title("Same values under both rules" if unit else "Same candidates, different leaders", pad=10)
            bx.text(.5, .07, "Both rules: A leads" if unit else "Cosine: A leads     Dot: B leads", ha="center", transform=bx.transAxes, fontsize=19, color=blue)
            fig.text(.055, .025, "Constructed vectors, not model measurements. Scores are not relevance probabilities; production rules should match training.", fontsize=14, color=muted)
            save(fig, "unit-rules" if unit else "comparison-rules")

        for approximate in (False, True):
            examined = APPROX_EXAMINED if approximate else tuple(ANN_POINTS)
            returned = nearest(examined)
            fig = plt.figure(figsize=(14, 5.6), dpi=100, facecolor=cream)
            ax = fig.add_axes([.08, .18, .39, .72], facecolor=paper)
            ax.set(xlim=(-.6, 5.5), ylim=(-.6, 5.7), xticks=range(6), yticks=range(6), xlabel="x", ylabel="y")
            ax.set_aspect("equal")
            ax.spines[["top", "right"]].set_visible(False)
            ax.grid(color="#ccc4b6", alpha=.4)
            ax.scatter(*ANN_QUERY, color=blue, marker="+", s=160, lw=3, zorder=5)
            ax.annotate("Q", ANN_QUERY, xytext=(-12, -18), textcoords="offset points", color=blue)
            for name, point in ANN_POINTS.items():
                ax.scatter(*point, s=90, facecolors=teal if name in examined else paper, edgecolors=teal, lw=2, zorder=4)
                if name in returned:
                    ax.scatter(*point, s=260, facecolors="none", edgecolors=red, lw=2, zorder=4)
                ax.annotate(name, point, xytext=(10, 9), textcoords="offset points", color=ink, weight="bold")
            ax.set_title("Q = (0, 0) · Euclidean distance", pad=14)
            bx = fig.add_axes([.54, .16, .43, .72])
            data = [[n, f"{distances()[n]:.3f}", "yes" if n in examined else "no", "yes" if n in returned else "no"] for n in ANN_POINTS]
            t = table(bx, data, ["Point", "Distance", "Examined", "Returned"], [.16, .25, .30, .29])
            t.set_fontsize(16)
            for row, name in enumerate(ANN_POINTS, 1):
                if name in returned:
                    t[row, 0].set_facecolor(red if name == "D" else teal)
                    t[row, 0].get_text().set_color(paper)
                if name not in examined:
                    for col in range(4):
                        t[row, col].get_text().set_color(muted)
            bx.set_title(f"{len(examined)} examined → {', '.join(returned)}", pad=10)
            bx.text(.5, .065, "C is closer than D but not examined." if approximate else "Exact under this rule; relevance remains open.", ha="center", transform=bx.transAxes, fontsize=17, color=red if approximate else blue)
            fig.text(.055, .025, "Source-exact six-point example. Table gives reference distances. Rings mark returned points; hollow points were not examined.", fontsize=14, color=muted)
            save(fig, "neighbours-approximate" if approximate else "neighbours-exact")

    with (directory / "similarity-scores.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["unit_normalised", "candidate", "x", "y", "cosine", "dot", "measured_model_output"])
        for unit in (False, True):
            for n, vector in VECTORS.items():
                v = normalise(vector) if unit else vector
                writer.writerow([unit, n, *[format(x, ".17g") for x in v], format(scores("cosine", unit)[n], ".17g"), format(scores("dot", unit)[n], ".17g"), False])
    with (directory / "neighbour-search.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["point", "x", "y", "euclidean_distance", "exact_examined", "exact_returned", "approximate_examined", "approximate_returned"])
        for n, v in ANN_POINTS.items():
            writer.writerow([n, *v, format(distances()[n], ".17g"), True, n in nearest(), n in APPROX_EXAMINED, n in nearest(APPROX_EXAMINED)])
    manifest = {"recipe_sha256": recipe, "kind": "toy similarity rules and source-exact neighbour example",
                "measured_model_outputs": False, "simulates_hnsw": False, "checks": check_examples(),
                "files": {p.name: sha(p) for p in sorted(directory.iterdir()) if p.suffix in (".png", ".svg", ".csv")}, "passed": True}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return sha(manifest_path)
