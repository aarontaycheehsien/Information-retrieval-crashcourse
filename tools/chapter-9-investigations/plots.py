"""Standalone Matplotlib figures and CSVs for Chapter 9 reranking examples."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile

from facts import QUERY_TOKENS, DOCUMENT_TOKENS, SIMILARITIES, row_maxima, maxsim, alignments, ASPECTS, INDEPENDENT_SELECTION, DIVERSE_SELECTION, check_examples


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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter9-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter9-reranking-v1", "svg.fonttype": "none"}

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
        for reveal in (False,True):
            fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
            ax=fig.add_axes([.035,.18,.68,.7])
            data=[[token]+[f'{v:.2f}' for v in row] for token,row in zip(QUERY_TOKENS,SIMILARITIES)]
            t=table(ax,data,['Query ↓ / Doc →',*DOCUMENT_TOKENS],[.29,.16,.16,.19,.20])
            t.set_fontsize(19)
            if reveal:
                for row,col in enumerate(alignments(),1):
                    t[row,col+1].set_facecolor(teal);t[row,col+1].get_text().set_color(paper)
                    t[row,col+1].get_text().set_weight('bold')
            ax.set_title('Source teaching case · Invented contextual token similarities',pad=13)
            bx=fig.add_axes([.76,.2,.21,.66]);bx.axis('off')
            bx.text(.5,.78,'MAXIMUM / ROW' if reveal else 'COMPARE',ha='center',fontsize=16,weight='bold',color=blue)
            bx.text(.5,.57,'0.90 + 0.80' if reveal else '2 query tokens',ha='center',fontsize=22,color=teal)
            bx.text(.5,.32,'= 1.70' if reveal else '4 document tokens',ha='center',fontsize=31 if reveal else 20,weight='bold',color=teal)
            fig.text(.055,.10,'Keep each query row’s strongest match, then sum.' if reveal else 'One query-token vector is compared with each document-token vector.',fontsize=18,color=ink)
            fig.text(.055,.035,'Invented values, not model measurements or word counts. Whole-word labels simplify a real tokeniser; matches need not be one-to-one.',fontsize=14,color=muted)
            save(fig,'maxsim' if reveal else 'maxsim-table')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.12,.95,.76])
        data=[['Pooled bi-encoder','Independent','One pooled vector / unit','Candidate retrieval'],['ColBERT-style','Independent','Token-vector sets','Retrieval or reranking'],['Cross-encoder','Joint query + candidate','Query-dependent pair score','Usually a shortlist']]
        t=table(ax,data,['Arrangement','Encoding','Representation / comparison','Typical position'],[.23,.22,.32,.23]);t.set_fontsize(16)
        ax.set_title('When do query and document interact?',pad=12)
        fig.text(.055,.05,'Qualitative arrangements, not a latency benchmark. Training and implementation determine actual behaviour and cost.',fontsize=15,color=muted)
        save(fig,'encoding-arrangements')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.12,.95,.76])
        data=[['Pointwise','One candidate','Independent judgement','Score calibration'],['Pairwise','Two candidates','Direct comparison','Many comparisons; inconsistency'],['Listwise','Several candidates','Comparative ordering','Context size; input order']]
        t=table(ax,data,['Prompt arrangement','Candidates shown','What it supplies','Possible limitation'],[.21,.20,.25,.34]);t.set_fontsize(16)
        ax.set_title('LLM reranking at inference time',pad=12)
        fig.text(.055,.05,'Prompting arrangements here, not the identically named classical training objectives. No equal-call or equal-latency assumption.',fontsize=14,color=muted)
        save(fig,'reranking-modes')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.13,.95,.76])
        data=[[paper,aspect,'selected' if paper in INDEPENDENT_SELECTION else '—','selected' if paper in DIVERSE_SELECTION else '—'] for paper,aspect in ASPECTS.items()]
        t=table(ax,data,['Paper','Stipulated aspect / usefulness','A, B, C','A, D, E'],[.10,.54,.18,.18]);t.set_fontsize(16)
        for row,paper in enumerate(ASPECTS,1):
            for col,selection,color in [(2,INDEPENDENT_SELECTION,blue),(3,DIVERSE_SELECTION,teal)]:
                if paper in selection:
                    t[row,col].set_facecolor(color);t[row,col].get_text().set_color('#faf8f3')
        ax.set_title('Same six-candidate pool · Repeated aspect versus three useful aspects',pad=12)
        fig.text(.055,.07,'A/B/C: 1 aspect · A/D/E: 3 aspects · F stays out: being different is insufficient.',fontsize=17,color=ink)
        fig.text(.055,.025,'Schematic papers and stipulated selections from the chapter. No actual study finding, numeric relevance score or diversification algorithm output.',fontsize=13,color=muted)
        save(fig,'aspect-coverage')
    with (directory/'token-similarities.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['query_token','document_token','invented_similarity','row_maximum','selected_alignment','measured_model_output'])
        for i,token in enumerate(QUERY_TOKENS):
            for j,doc_token in enumerate(DOCUMENT_TOKENS):w.writerow([token,doc_token,format(SIMILARITIES[i][j],'.17g'),format(row_maxima()[i],'.17g'),j==alignments()[i],False])
    with (directory/'aspect-selections.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['schematic_paper','aspect','individual_selection','diversified_selection','calculated_algorithm_output'])
        for paper,aspect in ASPECTS.items():w.writerow([paper,aspect,paper in INDEPENDENT_SELECTION,paper in DIVERSE_SELECTION,False])
    manifest={'recipe_sha256':recipe,'kind':'source-exact invented similarities and schematic diversification','measured_model_outputs':False,'checks':check_examples(),'files':{p.name:sha(p) for p in sorted(directory.iterdir()) if p.suffix in ('.png','.svg','.csv')},'passed':True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return sha(manifest_path)
