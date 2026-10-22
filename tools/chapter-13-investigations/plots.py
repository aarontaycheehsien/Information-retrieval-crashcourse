"""Standalone Matplotlib figures and CSVs for Chapter 13 diagnostic lenses and declared contrasts."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile
import textwrap

from facts import DIAGNOSTIC_NOTICES, VOCABULARY_QUESTIONS, FIRST_STAGE_METHODS, SHIFT_SITES, ID_RECORDS, IDENTIFIER, RELATION_PAIR, NEGATION_PAIR, check_examples


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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter13-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter13-agentic-control-v1", "svg.fonttype": "none"}

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
        fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; original retrieval-diagnosis teaching illustration"})
        fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original retrieval-diagnosis teaching illustration; not a model measurement"})
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
        data=[['Vocabulary mismatch','Query and relevant record use different words','Test a terminology bridge'],['OOV / weak representation','A named component loses usable evidence','Inspect fields and representations'],['Suspected OOD','Training conditions may not transfer','Compare locally for the actual task'],['Relation / composition','Direction, negation or binding is lost','Test controlled relation contrasts']]
        t=table(ax,data,['Lens','What the hypothesis concerns','A next investigation'],[.24,.44,.32]);t.set_fontsize(15)
        ax.set_title('Four diagnostic lenses · Evidence first, remedy second',pad=12)
        fig.text(.055,.045,'Establish eligibility and boundaries first. These are nonexclusive prompts for investigation, not exhaustive categories or proven causes.',fontsize=14,color=muted)
        save(fig,'diagnostic-lenses')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Lexical index','Analysed term and posting list exist','Does the field preserve the evidence?'],['Model tokeniser','String can be encoded as model tokens','Which vocabulary and fallback?'],['Learnt representation','Tokens provide useful retrieval evidence','Encoding alone does not establish this']]
        t=table(ax,data,['Layer','Different question','What to inspect'],[.24,.39,.37]);t.set_fontsize(16)
        ax.set_title('Out of whose vocabulary?',pad=12)
        fig.text(.055,.045,'Literal OOV concerns a named vocabulary. A representable string can still have a weak retrieval representation; the layers need separate evidence.',fontsize=14,color=muted)
        save(fig,'vocabulary-layers')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Query shift','Style, register, length, intent or query type'],['Corpus / domain shift','Discipline, genre, language, document type or period'],['Task / relevance shift','Answer-bearing passage vs evidence set, known item or citation']]
        t=table(ax,data,['Site of possible shift','What may differ from training'],[.30,.70]);t.set_fontsize(16)
        ax.set_title('Familiar words do not establish successful transfer',pad=12)
        fig.text(.055,.045,'These sites overlap and are not a fixed formal partition. A single poor result cannot prove OOD; compare performance locally and record training uncertainty.',fontsize=14,color=muted)
        save(fig,'distribution-shifts')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Strict Boolean','Explicit logic over analysed terms','A weak operator can change eligibility'],['BM25','Analysed lexical evidence','Weak vocabulary bridging;\nno inherent phrase meaning'],['Single-vector dense','Overall learnt similarity','Pooling may blur identity or local detail']]
        t=table(ax,data,['First-stage pattern','What it preserves best','Characteristic blind spot'],[.25,.32,.43]);t.set_fontsize(15)
        ax.set_title('Different methods preserve different retrieval evidence',pad=12)
        fig.text(.055,.045,'Three reference patterns, not an exhaustive list. Learnt sparse and late interaction can also retrieve candidates; real pipelines can combine methods.',fontsize=14,color=muted)
        save(fig,'first-stage-preservation')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Outside collection','Coverage or indexing lag','Was the record searchable?'],['Filtered out','Applied limit or metadata','Was the record eligible?'],['Absent from pool','Retrieval and candidate cutoff','Did the first stage supply it?'],['Below display boundary','Later ranking or presentation','Was it matched but hidden?']]
        t=table(ax,data,['Possible explanation','Boundary to investigate','Evidence question'],[.28,.35,.37]);t.set_fontsize(16)
        ax.set_title('The same missing record can suggest different stages',pad=12)
        fig.text(.055,.045,'Alternative hypothetical paths, not a traced search. A failed lookup or missing internal trace alone does not identify which boundary excluded the paper.',fontsize=14,color=muted)
        save(fig,'missing-record-boundaries')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Vocabulary mismatch','Explicit synonym or controlled term','Check known relevant records'],['Exact identity','Preserved lexical field / route','Check analysis and neighbouring strings'],['Suspected transfer failure','Local comparison, then adaptation','Match the actual relevance purpose'],['Relation failure','Logic, positions, interaction or training','Test direction and negation contrasts']]
        t=table(ax,data,['Suspected lost evidence','A remedy to test','What makes the test informative'],[.28,.38,.34]);t.set_fontsize(15)
        ax.set_title('Choose an intervention from the suspected cause',pad=12)
        fig.text(.055,.045,'A remedy is a hypothesis test, not a guarantee. Establish that the record could have been returned, preserve observations and mark unknowns.',fontsize=14,color=muted)
        save(fig,'remedy-tests')
    with (directory/'diagnostic-contrasts.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['contrast','left','right','interpretation','measured_model_result'])
        w.writerow(['direction',*RELATION_PAIR,'Equal term counts; different causal direction',False])
        w.writerow(['negation',*NEGATION_PAIR,'Decisive proposition differs',False])
        w.writerow(['exact identity',IDENTIFIER,'DELULU-428','Literal keyword-field identity in declared toy records',False])
    with (directory/'keyword-field-example.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['invented_record','stored_keyword','literal_exact_match','real_index_run'])
        for label,value in ID_RECORDS:w.writerow([label,value,value==IDENTIFIER,False])
    manifest={'recipe_sha256':recipe,'kind':'source diagnostic categories and declared text/identity contrasts','new_model_or_product_tests':False,'checks':check_examples(),'files':{p.name:sha(p) for p in sorted(directory.iterdir()) if p.suffix in ('.png','.svg','.csv')},'passed':True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return sha(manifest_path)
