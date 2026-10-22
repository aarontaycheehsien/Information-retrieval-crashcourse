"""Deterministic Matplotlib figures and CSVs for the films and standalone reuse."""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import tempfile

from facts import B, K1, LENGTHS, DOCUMENT_FREQUENCIES, contributions, factor, totals, check_examples

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_plots(directory, manifest_hash):
    directory = Path(directory)
    assert sha(directory/"plots-manifest.json") == manifest_hash, "Plot manifest changed"
    manifest = json.loads((directory/"plots-manifest.json").read_text())
    for name, value in manifest["files"].items():
        assert sha(directory/name) == value, f"Plot asset changed: {name}"
    return manifest


def ensure_plots(directory):
    import importlib.metadata
    directory = Path(directory)
    directory.mkdir(exist_ok=True, parents=True)
    recipe = hashlib.sha256((HERE/"plots.py").read_bytes()+(HERE/"facts.py").read_bytes()+
                            importlib.metadata.version("matplotlib").encode()).hexdigest()
    manifest_path = directory/"plots-manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        if manifest["recipe_sha256"] == recipe and all((directory/n).is_file() and sha(directory/n) == v for n, v in manifest["files"].items()):
            return sha(manifest_path)
    check_examples()
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir())/"chapter3-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt
    import numpy as np

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 18, "axes.labelsize": 20,
             "axes.titlesize": 20, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter3-bm25-v1", "svg.fonttype": "none"}

    def axes(title, ymax=3.2):
        fig = plt.figure(figsize=(14, 5.6), dpi=100, facecolor=cream)
        ax = fig.add_axes([.095, .195, .875, .715], facecolor=paper)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color="#ccc4b6", alpha=.45)
        ax.set_axisbelow(True)
        ax.set_title(title, pad=15)
        ax.set_ylim(0, ymax)
        ax.set_ylabel("Term-frequency factor")
        return fig, ax

    def save(fig, name):
        fig.savefig(directory/(name+".png"), dpi=100, metadata={"Software": "Matplotlib; original BM25 teaching illustration"})
        fig.savefig(directory/(name+".svg"), metadata={"Date": None, "Creator": "Original BM25 teaching illustration"})
        plt.close(fig)

    with plt.rc_context(style):
        x = np.linspace(0, 20, 401)
        fig, ax = axes("Average document length · k₁ = 1.2")
        ax.plot(x, [factor(float(t)) for t in x], color=teal, lw=4)
        ax.axhline(2.2, color=blue, ls="--", lw=2)
        ax.text(11.2, 2.32, "Limit: 2.2", color=blue)
        for t, offset in [(1, (22, -34)), (2, (20, 18)), (20, (-105, -32))]:
            value = factor(t)
            ax.scatter([t], [value], color=teal, s=70, zorder=5)
            label = f"{t} → {value:.3f}" if t != 1 else "1 → 1.000"
            ax.annotate(label, (t, value), xytext=offset, textcoords="offset points", fontsize=17, color=teal)
        ax.set(xlim=(0, 20.4), xticks=[0, 1, 2, 5, 10, 15, 20], yticks=[0, 1, 2, 3], xlabel="Occurrences in this document · linear axes")
        save(fig, "saturation")

        fig, ax = axes("Different k₁ values · average document length · same linear scales")
        for k1, color in [(.5, blue), (1.2, teal), (2., red)]:
            ax.plot(x, [factor(float(t), k1=k1) for t in x], color=color, lw=3.5, label=f"k₁ = {k1:g}")
        ax.plot([1, 20], [1, 1], color=muted, lw=3, ls="--", label="k₁ = 0 (positive tf)")
        ax.scatter([0], [0], color=muted, s=40)
        ax.set(xlim=(0, 20.4), xticks=[0, 5, 10, 15, 20], yticks=[0, 1, 2, 3], xlabel="Occurrences in this document · tf = 0 always contributes 0")
        ax.legend(loc="lower right", frameon=False, fontsize=16, ncol=2)
        save(fig, "k1-curves")

        fig, ax = axes("One occurrence · average length = 100 · k₁ = 1.2", 1.65)
        locs = np.arange(2)
        first = ax.bar(locs-.17, [factor(1, n) for n in (40, 400)], width=.3, color=teal, label="b = 0.75")
        second = ax.bar(locs+.17, [factor(1, n, b=0) for n in (40, 400)], width=.3, color=blue, label="b = 0 (length disabled)")
        ax.bar_label(first, labels=[f"{factor(1,n):.3f}" for n in (40, 400)], padding=7, fontsize=20, color=teal)
        ax.bar_label(second, labels=["1.000", "1.000"], padding=7, fontsize=20, color=blue)
        ax.set(xticks=locs, xticklabels=["40 terms", "400 terms"], xlabel="Document length in analysed terms · linear axes")
        ax.legend(loc="upper right", frameon=False, fontsize=17)
        save(fig, "length-normalisation")

    with (directory/"frequency-factors.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tf", "factor_k1_0", "factor_k1_0.5", "factor_k1_1.2", "factor_k1_2", "length", "average_length"])
        for t in range(21):
            writer.writerow([t]+[format(factor(t,k1=k), ".17g") for k in (0,.5,1.2,2)]+[100,100])
    with (directory/"length-factors.csv").open("w", newline="") as f:
        writer = csv.writer(f);writer.writerow(["length", "tf", "average_length", "k1", "b", "factor"])
        for length in (40, 400):
            for b in (.75,0):writer.writerow([length,1,100,K1,b,format(factor(1,length,b=b), ".17g")])
    with (directory/"toy-scores.csv").open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["record", "length", "df_delulu", "df_job", "delulu_contribution", "job_contribution", "total", "strict_and_eligible"])
        for key, parts in contributions().items():
            writer.writerow([key,LENGTHS[key],DOCUMENT_FREQUENCIES["delulu"],DOCUMENT_FREQUENCIES["job"],
                             format(parts["delulu"], ".17g"),format(parts["job"], ".17g"),format(totals()[key], ".17g"),key in ("D1","D4")])
    files = {p.name: sha(p) for p in sorted(directory.iterdir()) if p.suffix in (".png", ".svg", ".csv")}
    manifest = {"recipe_sha256": recipe, "model": "single-field BM25 with positive IDF", "files": files,
                "k1": K1, "b": B, "axes": "linear", "passed": True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+"\n")
    return sha(manifest_path)
