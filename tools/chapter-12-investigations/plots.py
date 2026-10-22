"""Standalone Matplotlib figures and CSVs for Chapter 12 control arrangements and selected recovery examples."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile
import textwrap

from facts import ARRANGEMENTS, OUTPUT_PATTERNS, AUTISM_VARIANTS, AUTISM_BROADENING, AUTISM_DATABASES, CATALOGUE_EXAMPLES, EVIDENCE_DATES, check_examples


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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter12-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter12-agentic-control-v1", "svg.fonttype": "none"}

    def save(fig, name):
        for label in fig.texts:
            if label.get_position()[1] < .08:
                label.set_text(textwrap.fill(label.get_text(), width=125, break_long_words=False))
                label.set_fontsize(13)
                label.set_verticalalignment("bottom")
                label.set_y(.015)
        fig.canvas.draw()
        renderer=fig.canvas.get_renderer()
        for label in fig.texts:
            box=label.get_window_extent(renderer)
            assert box.x0>=0 and box.x1<=1400 and box.y0>=0 and box.y1<=560, (name,label.get_text(),box)
        for ax in fig.axes:
            for tab in ax.tables:
                for key,cell in tab.get_celld().items():
                    cb=cell.get_window_extent(renderer);tb=cell.get_text().get_window_extent(renderer)
                    assert tb.x0>=cb.x0+7 and tb.x1<=cb.x1-7 and tb.y0>=cb.y0 and tb.y1<=cb.y1, (name,key,cell.get_text().get_text(),cb,tb)
        boxes=[label.get_window_extent(renderer) for label in fig.texts]
        assert all(not a.overlaps(b) for i,a in enumerate(boxes) for b in boxes[i+1:]), (name,"Overlapping figure notes")
        fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; original search-control teaching illustration"})
        fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original search-control teaching illustration; not a model measurement"})
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
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Fixed workflow','Designer prescribes the sequence','Query contents may still adapt'],['Adaptive workflow','Rule, classifier or model selects a branch','Branches enumerated in advance'],['Agentic search','Model plans part of an action trajectory','Within permitted tools and limits']]
        t=table(ax,data,['Arrangement','Who chooses the next action?','Defining boundary'],[.23,.40,.37]);t.set_fontsize(16)
        ax.set_title('Three reference points along a continuum of control',pad=12)
        fig.text(.055,.045,'A model can choose an adaptive branch; an agent’s tools are predefined too. Inspect how the sequence is selected, not merely whether a model appears.',fontsize=14,color=muted)
        save(fig,'control-arrangements')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[[OUTPUT_PATTERNS[0],'Predetermined repeated retrieval','Records'],[OUTPUT_PATTERNS[1],'Model-planned retrieval trajectory','Records'],[OUTPUT_PATTERNS[2],'Predetermined retrieval then synthesis','Report / answer'],[OUTPUT_PATTERNS[3],'Model-planned retrieval and synthesis','Report / answer']]
        t=table(ax,data,['Pattern','Search trajectory','Main output'],[.29,.46,.25]);t.set_fontsize(16)
        ax.set_title('Output form and control are independent properties',pad=12)
        fig.text(.055,.045,'Repeated retrieval does not establish agency. A long report demonstrates generation; its search procedure may still be fixed.',fontsize=14,color=muted)
        save(fig,'output-patterns')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Hybrid','Which retrieval routes contribute?','Multiple candidate-generation routes'],['Multi-stage','How are earlier outputs processed?','Sequential operations'],['Agentic','Who selected the action sequence?','Model plans part of the trajectory']]
        t=table(ax,data,['Property','Question addressed','What it identifies'],[.20,.43,.37]);t.set_fontsize(16)
        ax.set_title('Control does not replace retrieval or change its scoring formula',pad=12)
        fig.text(.055,.045,'Model-planned BM25 searches need not be hybrid. Fixed lexical/dense retrieval with fusion need not be agentic. A system can have all three properties.',fontsize=14,color=muted)
        save(fig,'independent-properties')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['One-shot NDE rewrite','Autism and related synonyms','Still zero in the reported\nsame-index comparison'],['Model-driven loop','Broaden to subject coverage','PsycINFO; Education Research\nComplete; SocINDEX']]
        t=table(ax,data,['Reported arrangement','Input after autism request','Reported result'],[.26,.35,.39]);t.set_fontsize(16)
        ax.set_title('Selected catalogue example · Same underlying library index',pad=12)
        fig.text(.055,.045,'June 2026 account replaying selected 2023 queries. Not sampled, not a success rate, and not an experiment isolating the loop as sole cause.',fontsize=14,color=muted)
        save(fig,'catalogue-comparison')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Invisible menu','A trace hides unused or unavailable actions','Record tools and reachable sources'],['Compounding misses','Later rounds can inherit early blind spots','Record queries and intermediate sets'],['Stopping','Enough does not establish completeness','Record limits and decision criteria']]
        t=table(ax,data,['Issue','What can remain hidden','What to record'],[.21,.44,.35]);t.set_fontsize(16)
        ax.set_title('More rounds do not automatically establish coverage',pad=12)
        fig.text(.055,.045,'These are structural risks, not measured failure rates. An alternative action may recover candidates; neither success nor complete coverage is guaranteed.',fontsize=14,color=muted)
        save(fig,'loop-boundaries')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Before retrieval','User reviews a proposed strategy','Approval gate'],['During a run','Budget, round limit or interruption','Harness / user limit'],['During a run','Model judges evidence sufficient','A recorded decision criterion']]
        t=table(ax,data,['When','Control property','What it represents'],[.21,.45,.34]);t.set_fontsize(16)
        ax.set_title('Strategy approval and stopping are different control properties',pad=12)
        fig.text(.055,.045,'The chapter’s April 2026 Web of Science post documents prior strategy approval. A stopping decision or budget limit does not prove completeness.',fontsize=14,color=muted)
        save(fig,'approval-and-stopping')
    with (directory/'control-arrangements.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['source_control_category']);w.writerows([[x] for x in ARRANGEMENTS])
    with (directory/'catalogue-examples.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['selected_original_query','reported_reformulation_or_link','reported_result','logs_year','account_date','sampled','new_test'])
        for row in CATALOGUE_EXAMPLES:w.writerow([*row,'2023','June 2026',False,False])
    manifest={'recipe_sha256':recipe,'kind':'source control categories and dated selected recovery accounts','new_product_tests':False,'checks':check_examples(),'files':{p.name:sha(p) for p in sorted(directory.iterdir()) if p.suffix in ('.png','.svg','.csv')},'passed':True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return sha(manifest_path)
