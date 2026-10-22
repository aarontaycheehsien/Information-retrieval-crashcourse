"""Standalone Matplotlib figures and CSVs for Chapter 8 representations."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile

from facts import VOCAB, DOCUMENTS, REPEATED, SOURCE_BINARY, EXPANSION, vector, tfidf, bm25, check_examples


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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter8-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter8-representations-v1", "svg.fonttype": "none"}

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
        for binary in (True, False):
            fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
            ax=fig.add_axes([.035,.1,.93,.81])
            docs=DOCUMENTS if binary else REPEATED
            data=[[name]+list(vector(text,binary)) for name,text in docs.items()]
            if binary:data.append(['Query',0,0,1,0,0,0,1])
            t=table(ax,data,['Unit',*VOCAB],[.10]+[.90/7]*7)
            for i,row in enumerate(data,1):
                for j,value in enumerate(row[1:],1):
                    if value:
                        t[i,j].set_facecolor(teal if row[0]=='Query' else blue)
                        t[i,j].get_text().set_color(paper)
            ax.set_title('One fixed vocabulary · binary presence' if binary else 'Same vocabulary · raw counts after repeating treatment in D1',pad=12)
            fig.text(.055,.07,'D1: heart attack treatment    D2: job interview tips    D3: cancer treatment' if binary else 'D1: heart attack treatment treatment treatment · D2 and D3 stay the same',fontsize=16,color=muted)
            fig.text(.055,.025,'Query: heart treatment · Source-exact vocabulary and binary values' if binary else 'Binary presence in D1 is unchanged: [1, 0, 1, 0, 0, 0, 1]',fontsize=14,color=muted)
            save(fig,'binary-vectors' if binary else 'term-counts')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.04,.18,.92,.7])
        data=[[term,'1',str(vector(REPEATED['D1'])[VOCAB.index(term)]),f"{tfidf(term,'D1'):.3f}",f"{bm25(term,'D1'):.3f}"] for term in ('heart','treatment')]
        table(ax,data,['D1 coordinate','Presence','Raw TF','TF–IDF','BM25'],[.24,.19,.19,.19,.19])
        ax.set_title('Calculated weights in the repeated D1 · Declared formula variants',pad=12)
        fig.text(.055,.16,'TF–IDF = raw TF × ln(N/df) · BM25 IDF = ln(1 + (N − df + 0.5)/(df + 0.5))',fontsize=16,color=muted)
        fig.text(.055,.10,'BM25 = IDF × f(k₁+1) / [f + k₁(1−b+bL/avgL)] · k₁=1.2, b=0.75',fontsize=16,color=muted)
        fig.text(.055,.035,'N=3 · lengths=(5,3,2) · avgL=10/3 · df(heart)=1, df(treatment)=2 · Teaching values, not a benchmark',fontsize=14,color=muted)
        save(fig,'lexical-weights')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.035,.11,.93,.79])
        data=[['BM25','Sparse','Specified formula','Vocabulary terms'],['Bibliographic facts','Dense here','Recorded values','Year, pages, counts'],['SPLADE-style','Sparse','Learnt mapping','Subword vocabulary'],['Dense bi-encoder','Dense','Learnt mapping','Distributed latent features']]
        t=table(ax,data,['Case','Shape','Rule / provenance','Evidence coordinates'],[.24,.13,.25,.38])
        t.set_fontsize(16)
        ax.set_title('Independent questions about representations',pad=12)
        fig.text(.055,.045,'Density alone establishes no semantic capability. Learned sparse expansions and latent features depend on training.',fontsize=15,color=muted)
        save(fig,'representation-cases')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.09,.22,.85,.65],facecolor=paper)
        labels=list(EXPANSION);values=list(EXPANSION.values())
        bars=ax.bar(labels,values,color=[blue,blue,teal,teal],width=.55)
        for bar,value in zip(bars,values):ax.text(bar.get_x()+bar.get_width()/2,value+.04,f'{value:.1f}',ha='center',weight='bold')
        ax.set_ylim(0,1.5);ax.set_ylabel('Illustrative learnt weight')
        ax.spines[['top','right']].set_visible(False)
        ax.set_title('Input: heart attack · Predicted vocabulary weights can expand beyond input',pad=16)
        fig.text(.055,.10,'Blue: input terms · Teal: absent terms activated in this schematic representation',fontsize=16,color=muted)
        fig.text(.055,.035,'Invented weights, not measured SPLADE output. Whole-word labels simplify a real model’s subword vocabulary; most entries stay zero.',fontsize=14,color=muted)
        save(fig,'sparse-expansion')
    with (directory/'lexical-weights.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['document','term','binary','raw_tf','tfidf_raw_times_ln_N_df','bm25_k1_1.2_b_.75'])
        for name,text in REPEATED.items():
            for term in VOCAB:
                w.writerow([name,term,int(term in text.split()),vector(text)[VOCAB.index(term)],format(tfidf(term,name),'.17g'),format(bm25(term,name),'.17g')])
    with (directory/'sparse-expansion.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['schematic_term','invented_weight','in_input','measured_model_output'])
        for term,value in EXPANSION.items():w.writerow([term,value,term in ('heart','attack'),False])
    manifest={'recipe_sha256':recipe,'kind':'source-exact lexical vectors and declared illustrative weights','measured_model_outputs':False,'checks':check_examples(),'files':{p.name:sha(p) for p in sorted(directory.iterdir()) if p.suffix in ('.png','.svg','.csv')},'passed':True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return sha(manifest_path)
