"""Standalone Matplotlib figures and CSVs for Chapter 15 reporting, inspection and vendor questions."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile
import textwrap

from facts import PIPELINE_AREAS, METHODS, INSPECTION_STAGES, VENDOR_GROUPS, TRACE_FIELDS, CANDIDATE_RANK, CANDIDATE_COUNT, FINAL_RANK, DISPLAY_K, numbered_questions, check_examples


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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter15-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter15-library-practice-v1", "svg.fonttype": "none"}

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
        fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; original library-practice teaching illustration"})
        fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original library-practice teaching illustration; not a model measurement"})
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
        data=[['Query interpretation','Original and transformed inputs, inferred filters, parser/model'],['Candidate retrieval','Database, version, fields, indexed unit, method and cutoffs'],['Ranking and fusion','Sort, component lists, fusion rule, reranking and final depth'],['Retrieval control','Arrangement, actual branch/actions, observations and stop']]
        t=table(ax,data,['Pipeline area','What to preserve'],[.29,.71]);t.set_fontsize(16)
        ax.set_title('A saved question does not document the whole search',pad=12)
        fig.text(.055,.045,'Table 15.1 reference summary. Save date, count, identifiers and raw exports where possible. Unknown internal details remain unknown; exact future recreation is conditional.',fontsize=14,color=muted)
        save(fig,'recording-layers')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Ranked lexical','Analysis, weights, configuration, rewriting, sort and k','Collection statistics can move rankings'],['Single-vector dense','Encoder, units, vectors, index, similarity and search','Fixed exact retrieval can be repeatable'],['Learnt sparse','Model, vocabulary terms/weights, index and scoring','Typed words alone omit generated terms'],['Late interaction','Model, units, compression, MaxSim, pruning and k','Alignments do not make vectors portable']]
        t=table(ax,data,['Component','Version and record the relevant settings','A qualification to retain'],[.20,.48,.32]);t.set_fontsize(14)
        ax.set_title('Repeatability depends on fixed components and recorded settings',pad=12)
        fig.text(.055,.045,'Table 15.2 summary. Boolean also needs database, platform, fields, limits, vocabulary version and date. Query generation and orchestration add their own records.',fontsize=14,color=muted)
        save(fig,'component-records')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Query transformation','Actual generated input and route','That intent was fully preserved'],['Eligibility / lexical score','Satisfied clauses and scoring evidence','Relevance, probability, or the final order'],['Dense / token evidence','Unit, similarity, settings, terms or alignments','A complete causal account of the model'],['Fusion / reranking / display','Candidate lists, ordering stages and cutoffs','That a snippet or rationale caused position']]
        t=table(ax,data,['Inspectable layer','What the evidence can show','What it cannot establish alone'],[.25,.38,.37]);t.set_fontsize(15)
        ax.set_title('Read an explanation alongside the limits of what it proves',pad=12)
        fig.text(.055,.045,'Table 15.3 summary. Agentic inspection adds executed actions and observations; a narrated account of reasoning does not establish why choices were made.',fontsize=14,color=muted)
        save(fig,'inspection-limits')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Lexical candidate stage',f'P at rank {CANDIDATE_RANK} of {CANDIDATE_COUNT}','Supplied to reranking'],['After reranking',f'P at rank {FINAL_RANK}','Within the display cutoff'],['Display',f'First {DISPLAY_K} records','P is displayed'],['Internal reranker details','Not disclosed','Do not fill the gap with a rationale']]
        t=table(ax,data,['Recorded mock stage','Source illustration','What is established here'],[.30,.25,.45]);t.set_fontsize(16)
        ax.set_title('Figure 15.1 · A recorded path still has an unexplained part',pad=12)
        fig.text(.055,.045,'Every rank and record detail is hypothetical. No actual product trace was obtained. In a real service, call these facts a trace only when they derive from executed search.',fontsize=14,color=muted)
        save(fig,'mock-record-trace')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[];start=1
        for title,questions in VENDOR_GROUPS:
            end=start+len(questions)-1
            data.append([f'{start}–{end}',title,str(len(questions))]);start=end+1
        t=table(ax,data,['Questions','Source procurement group','Count'],[.16,.72,.12]);t.set_fontsize(15)
        ax.set_title('Nineteen questions in six groups · Ask, record evidence, verify',pad=12)
        fig.text(.055,.045,'These are source questions, not vendor answers or a product scorecard. The accompanying CSV leaves answers, evidence, library verification and follow-up blank.',fontsize=14,color=muted)
        save(fig,'six-vendor-groups')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Observed evidence','What the executed run or export actually shows','Retain input, outputs and capture details'],['Vendor documentation','A stated product mechanism or limit','Record source, version, date and scope'],['Unknown','An internal detail unavailable to the library','Do not turn a plausible account into a fact']]
        t=table(ax,data,['Evidence status','What it means','How to retain the distinction'],[.25,.39,.36]);t.set_fontsize(15)
        ax.set_title('Preserve the difference between what is known and what is inferred',pad=12)
        fig.text(.055,.045,'A concise explanation can be useful without exposing model weights. Documentation, interpretability and an understandable mental model remain separate properties.',fontsize=14,color=muted)
        save(fig,'evidence-status')
    with (directory/'vendor-questions.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['question_number','group_number','source_group','source_question','vendor_answer','supporting_evidence','library_verification','follow_up'])
        for row in numbered_questions():w.writerow([*row,'','','',''])
    with (directory/'hypothetical-trace.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['source_mock_field','source_mock_value','hypothetical','actual_product_trace'])
        for label,value in TRACE_FIELDS.items():w.writerow([label,value,True,False])
    manifest={'recipe_sha256':recipe,'kind':'source reporting categories, hypothetical trace and unanswered vendor questions','new_product_tests':False,'checks':check_examples(),'files':{p.name:sha(p) for p in sorted(directory.iterdir()) if p.suffix in ('.png','.svg','.csv')},'passed':True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return sha(manifest_path)
