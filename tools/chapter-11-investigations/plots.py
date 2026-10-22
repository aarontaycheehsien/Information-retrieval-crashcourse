"""Standalone Matplotlib figures and CSVs for Chapter 11 query objects, transformations and retrieval aids."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile
import textwrap

from facts import QUERY_OBJECTS, RECEIVERS, OBJECT_MECHANISMS, STRUCTURED_PARTS, GENERATED_TEXT, AUDIT_SOURCES, AUDIT_REPORTED_SHARES, check_examples


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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter11-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter11-query-objects-v1", "svg.fonttype": "none"}

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
        fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; original query-mechanism teaching illustration"})
        fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original query-mechanism teaching illustration; not a model measurement"})
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
        t=table(ax,list(zip(QUERY_OBJECTS,OBJECT_MECHANISMS)),['What stands for the need','Mechanism addressed'],[.44,.56]);t.set_fontsize(15)
        ax.set_title('One information need · Eight overlapping ways into retrieval',pad=12)
        fig.text(.055,.045,'Source categories overlap: an API can carry text, and a seed can start citation traversal. These are mechanisms, not eight phrasing styles.',fontsize=14,color=muted)
        save(fig,'query-objects')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Lexical / Boolean','Concepts, variants, tested operators','Explanation may add query words'],['Dense retriever','Task-appropriate need description','Longer prose is not always better'],['LLM translator','Concepts, constraints, context','Validate the generated expression'],['Controller','Scope, criteria, sources, stopping','Each retriever may receive only a part'],['Undisclosed pipeline','Systematically varied input forms','Compare with known relevant records']]
        t=table(ax,data,['Receiver','Useful input','Do not assume'],[.23,.37,.40]);t.set_fontsize(16)
        ax.set_title('Choose wording for the receiving component',pad=12)
        fig.text(.055,.045,'Adapted from the pinned chapter. Useful form depends on training, domain and supported syntax; the input box does not reveal the receiver.',fontsize=14,color=muted)
        save(fig,'receiving-components')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.04,.14,.92,.74])
        t=table(ax,[list(row) for row in STRUCTURED_PARTS],['Interpreted part','Displayed structured clause'],[.28,.72]);t.set_fontsize(18)
        ax.set_title('Web of Science Smart Search · Source example · All five clauses joined with AND',pad=12)
        fig.text(.055,.045,'The chapter’s visible, editable interpretation of the fruit/year/affiliation request. Original illustration; no new product test or screenshot.',fontsize=14,color=muted)
        save(fig,'visible-boolean')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Retrieval feedback','Construct a later retrieval input','Search the collection again','May add candidates'],['Screening feedback','Reprioritise existing records','Existing candidate pool','No inherent additions']]
        t=table(ax,data,['Operation','What changes','Boundary','Candidate effect'],[.21,.31,.27,.21]);t.set_fontsize(16)
        ax.set_title('Relevance judgements can address different operations',pad=12)
        fig.text(.055,.045,'Explicit retrieval feedback uses searcher judgements; PRF assumes top results relevant. Active-learning screening need not construct a later query.',fontsize=14,color=muted)
        save(fig,'feedback-boundaries')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Query2doc','Pseudo-document text','Original query + generated language','Lexical or dense retriever'],['HyDE','Hypothetical document','Embed the generated document','Dense vector retrieval']]
        t=table(ax,data,['Method','LLM produces','Retrieval input','Receiver'],[.15,.25,.36,.24]);t.set_fontsize(16)
        ax.set_title('Generated text takes two routes to real indexed sources',pad=12)
        fig.text(.055,.045,'Both methods create retrieval aids. The generated text is not an identified source or evidence; retain it in the search record and assess real results.',fontsize=14,color=muted)
        save(fig,'generated-paths')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.28,.24,.65,.61],facecolor=paper)
        labels=['Protocol-defined database\n+ hand searches','Snowballing'];values=list(AUDIT_REPORTED_SHARES.values())
        bars=ax.barh(labels,values,color=[blue,teal],height=.48)
        for bar,value in zip(bars,values):ax.text(value+1.8,bar.get_y()+bar.get_height()/2,f'{value}%',va='center',fontsize=22,weight='bold')
        ax.set_xlim(0,100);ax.set_xticks([0,25,50,75,100]);ax.invert_yaxis()
        ax.set_xlabel('Reported share of included sources (%)');ax.spines[['top','right']].set_visible(False)
        ax.set_title('One review audit · 495 included sources',pad=18)
        fig.text(.055,.045,'Greenhalgh and Peacock audit reported in the chapter. Only two reported routes shown; percentages are not universal estimates or exact source counts.',fontsize=14,color=muted)
        save(fig,'review-audit')
    with (directory/'query-objects.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['source_query_object','mechanism_summary'])
        w.writerows(zip(QUERY_OBJECTS,OBJECT_MECHANISMS))
    with (directory/'review-audit.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['reported_route','reported_percentage','included_sources_in_one_audit','universal_estimate','exact_count_calculated'])
        for route,value in AUDIT_REPORTED_SHARES.items():w.writerow([route,value,AUDIT_SOURCES,False,False])
    manifest={'recipe_sha256':recipe,'kind':'source taxonomy, transformation paths and scoped reported audit shares','new_product_or_model_tests':False,'checks':check_examples(),'files':{p.name:sha(p) for p in sorted(directory.iterdir()) if p.suffix in ('.png','.svg','.csv')},'passed':True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return sha(manifest_path)
