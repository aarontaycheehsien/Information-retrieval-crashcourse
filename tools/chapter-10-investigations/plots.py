"""Standalone Matplotlib figures and CSVs for Chapter 10 rank-fusion examples."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile
import textwrap

from facts import LEXICAL, DENSE, INPUT_LISTS, C, RAW_TIGHT, RAW_WIDE, contribution, rrf, fused_order, rank_in, input_cutoff, check_examples


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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter10-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter10-fusion-v1", "svg.fonttype": "none"}

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
        boxes=[label.get_window_extent(renderer) for label in fig.texts]
        assert all(not a.overlaps(b) for i,a in enumerate(boxes) for b in boxes[i+1:]), (name,"Overlapping figure notes")
        fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; original rank-fusion teaching illustration"})
        fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original rank-fusion teaching illustration; not a model measurement"})
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
        for name,focus in [('rrf-a',('A',)),('rrf-c',('C',)),('rrf-singletons',('B','D')),('rrf-contributions',tuple(rrf()))]:
            fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
            ax=fig.add_axes([.025,.16,.95,.72])
            data=[]
            for record in fused_order():
                ranks=[rank_in(record,xs) for xs in INPUT_LISTS]
                parts=[contribution(rank) if rank else 0 for rank in ranks]
                data.append([record,*[str(r) if r else '—' for r in ranks],*[str(v) for v in parts],f'{float(rrf()[record]):.5f}'])
            t=table(ax,data,['Record','Lexical rank','Dense rank','Lexical part','Dense part','Fused score'],[.12,.16,.16,.19,.19,.18])
            for row,record in enumerate(fused_order(),1):
                if record in focus:
                    for col in (0,5):t[row,col].set_facecolor(teal);t[row,col].get_text().set_color(paper)
                else:
                    for col in range(6):t[row,col].get_text().set_color(muted)
            ax.set_title('Source-exact lists · Lexical A/B/C, dense C/A/D · c = 60',pad=12)
            fig.text(.055,.10,'Each supplied occurrence contributes 1/(60 + rank). Missing list occurrence contributes zero.',fontsize=17,color=ink)
            fig.text(.055,.035,'Parts are exact fractions; fused scores are rounded to five decimals. Schematic records, not relevance judgements or measured retrieval results.',fontsize=14,color=muted)
            save(fig,name)
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.055,.16,.89,.72])
        data=[[r,f'{RAW_TIGHT[r]:.2f}',f'{RAW_WIDE[r]:.0f}',str(i),str(i)] for i,r in enumerate(LEXICAL,1)]
        table(ax,data,['Record','Tight-gap scores','Wide-gap scores','First ranking','Second ranking'],[.12,.24,.24,.20,.20])
        ax.set_title('Invented raw-score sets · Different gaps, identical A/B/C order',pad=12)
        fig.text(.055,.10,'With the same other input list, RRF is identical: A, C, B, D. It never receives these score gaps.',fontsize=17,color=ink)
        fig.text(.055,.035,'Arbitrary teaching scores, not BM25 or embedding measurements. The two score sets are alternative examples, not two new fusion routes.',fontsize=14,color=muted)
        save(fig,'score-gaps')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.075,.22,.49,.65],facecolor=paper)
        ranks=list(range(1,11))
        for constant,color in [(0,blue),(60,teal)]:
            values=[float(contribution(rank,constant)/contribution(1,constant)) for rank in ranks]
            ax.plot(ranks,values,'o-',color=color,lw=3,label=f'c = {constant}')
        ax.set(xlim=(.7,10.3),ylim=(0,1.06),xticks=[1,3,5,7,10],yticks=[0,.25,.5,.75,1],xlabel='Rank position',ylabel='Contribution / rank-1 contribution')
        ax.spines[['top','right']].set_visible(False);ax.grid(color='#ccc4b6',alpha=.35)
        ax.legend(frameon=False,loc='lower left');ax.set_title('Larger c softens the rank advantage',pad=12)
        bx=fig.add_axes([.62,.18,.35,.69])
        t=table(bx,[['0','1','1/3'],['60','1/61','1/63']],['c','Rank 1','Rank 3'],[.18,.41,.41]);t.set_fontsize(19)
        bx.set_title('Actual contributions',pad=12)
        fig.text(.055,.05,'Formula-derived curves, not model scores. The graph normalises each curve at rank 1; the table retains actual values.',fontsize=14,color=muted)
        save(fig,'constant-effect')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.04,.16,.92,.72])
        shallow=rrf(input_cutoff(2))
        data=[[r,f'{float(rrf()[r]):.5f}',f'{float(shallow[r]):.5f}' if r in shallow else 'Not supplied','L3 contribution lost' if r=='C' else 'Outside both inputs' if r=='D' else 'Unchanged'] for r in fused_order()]
        t=table(ax,data,['Record','Input depth 3','Input depth 2','What changed'],[.12,.23,.23,.42])
        for row in (2,4):t[row,0].set_facecolor(red);t[row,0].get_text().set_color(paper)
        ax.set_title('Input cutoff changes the evidence before fusion · c = 60',pad=12)
        fig.text(.055,.10,'Depth 2: lexical A/B and dense C/A. D is absent; C loses 1/63. Output depth is a later choice.',fontsize=17,color=ink)
        fig.text(.055,.035,'Derived variation of the source teaching case. No relevance judgement is implied by a missing input occurrence.',fontsize=14,color=muted)
        save(fig,'cutoff-effect')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.04,.16,.92,.72])
        changed=rrf(weights=(1,2));new_order=fused_order(weights=(1,2))
        data=[[r,f'{float(rrf()[r]):.6f}',f'{float(changed[r]):.6f}',str(fused_order().index(r)+1),str(new_order.index(r)+1)] for r in new_order]
        t=table(ax,data,['Record','Equal weights','Dense weight ×2','Old rank','New rank'],[.12,.25,.25,.19,.19])
        for row in (1,2):t[row,0].set_facecolor(teal);t[row,0].get_text().set_color(paper)
        ax.set_title('Declared weighted extension · Same input lists and c = 60',pad=12)
        fig.text(.055,.10,'New score = lexical contribution + 2 × dense contribution. New order: C, A, D, B.',fontsize=17,color=ink)
        fig.text(.055,.035,'A calculated illustration, not a quality recommendation or the chapter’s equal-weight baseline. Scores are not relevance probabilities.',fontsize=14,color=muted)
        save(fig,'weighted-fusion')
    with (directory/'rrf-values.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['record','lexical_rank','dense_rank','lexical_fraction','dense_fraction','fused_exact_fraction','fused_decimal','dense_double_weight_fraction'])
        for record in fused_order():
            ranks=[rank_in(record,xs) for xs in INPUT_LISTS]
            parts=[contribution(rank) if rank else 0 for rank in ranks]
            w.writerow([record,*[r or '' for r in ranks],*[str(v) for v in parts],str(rrf()[record]),format(float(rrf()[record]),'.17g'),str(rrf(weights=(1,2))[record])])
    with (directory/'constant-curves.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['constant','rank','exact_contribution','relative_to_rank_one'])
        for constant in (0,60):
            for rank in range(1,11):w.writerow([constant,rank,str(contribution(rank,constant)),str(contribution(rank,constant)/contribution(1,constant))])
    manifest={'recipe_sha256':recipe,'kind':'source-exact rank-fusion arithmetic and declared mathematical variations','measured_retrieval_results':False,'checks':check_examples(),'files':{p.name:sha(p) for p in sorted(directory.iterdir()) if p.suffix in ('.png','.svg','.csv')},'passed':True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return sha(manifest_path)
