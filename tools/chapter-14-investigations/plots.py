"""Standalone Matplotlib figures and CSVs for Chapter 14 evaluation arithmetic and source illustrations."""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import tempfile
import textwrap

from facts import BEFORE, AFTER, RELEVANT, LOCAL_ROWS, precision_at, recall_at, reciprocal_rank, average_precision, row_mean, check_examples


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
    os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "chapter14-matplotlib"))
    import matplotlib
    matplotlib.use("Agg")
    from matplotlib import pyplot as plt

    cream, paper, ink, muted = "#eee9e0", "#faf8f3", "#252728", "#6e6b63"
    blue, teal, red = "#2f577b", "#256c63", "#ad3d2d"
    style = {"font.family": "DejaVu Sans", "font.size": 17, "axes.labelsize": 18,
             "axes.titlesize": 19, "axes.edgecolor": muted, "axes.labelcolor": ink,
             "xtick.color": muted, "ytick.color": muted, "text.color": ink,
             "svg.hashsalt": "chapter14-retrieval-evaluation-v1", "svg.fonttype": "none"}

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
        fig.savefig(directory / (name + ".png"), dpi=100, metadata={"Software": "Matplotlib; original retrieval-evaluation teaching illustration"})
        fig.savefig(directory / (name + ".svg"), metadata={"Date": None, "Creator": "Original retrieval-evaluation teaching illustration; not a model measurement"})
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
        ax=fig.add_axes([.08,.23,.87,.60]);ax.set_facecolor(paper)
        xs=list(range(3));width=.32
        before=[float(precision_at(BEFORE,10)),float(recall_at(BEFORE,10)),float(recall_at(BEFORE,20))]
        after=[float(precision_at(AFTER,10)),float(recall_at(AFTER,10)),float(recall_at(AFTER,20))]
        for offset,values,color,label in [(-width/2,before,blue,'Before'),(width/2,after,teal,'After')]:
            bars=ax.bar([x+offset for x in xs],values,width,color=color,label=label)
            ax.bar_label(bars,labels=[f'{v:.1f}' for v in values],padding=5,fontsize=18)
        ax.set_xticks(xs,['Precision@10','Recall@10','Candidate-pool recall']);ax.set_ylim(0,1.22)
        ax.set_yticks([0,.2,.4,.6,.8,1]);ax.set_ylabel('Fraction under stated judgements')
        ax.spines[['top','right']].set_visible(False);ax.legend(loc='upper left',frameon=False,ncol=2)
        ax.set_title('Controlled source example · Same 20 candidates, exactly 10 relevant',pad=15)
        fig.text(.055,.045,'Figure 14.1 arithmetic. Reranking changes order, not membership. First-page precision and recall rise together; whole-pool recall stays fixed.',fontsize=14,color=muted)
        save(fig,'reranking-metrics')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Precision@k','Relevant records inside depth k','Order inside k and all records beyond k'],['MRR','An early first relevant hit','Every relevant hit after the first'],['MAP','Many binary relevant hits placed high','Differences between relevance grades'],['nDCG','Higher grades high, discounted by rank','Repeated evidence for only one aspect']]
        t=table(ax,data,['Metric','What it rewards','What it does not directly reward'],[.19,.39,.42]);t.set_fontsize(16)
        ax.set_title('Quoting a metric chooses a definition of better',pad=12)
        fig.text(.055,.045,'All require relevance judgements. MRR and MAP average query-level scores; none of these conventional measures directly rewards coverage across known aspects.',fontsize=14,color=muted)
        save(fig,'ranking-goals')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Reciprocal rank',f'{float(reciprocal_rank(BEFORE)):.3f}',f'{float(reciprocal_rank(AFTER)):.3f}','First relevant rank stays at 1'],['Average precision',f'{float(average_precision(BEFORE)):.3f}',f'{float(average_precision(AFTER)):.3f}','Many relevant papers move upward']]
        t=table(ax,data,['Single-query score','Before','After','What the arithmetic sees'],[.27,.13,.13,.47]);t.set_fontsize(17)
        ax.set_title('Two measures applied to the same controlled source rankings',pad=12)
        fig.text(.055,.045,'Computed over the full 20-record rankings with all 10 relevant identities stipulated. These are RR and AP for one query, not a multiquery MRR/MAP benchmark.',fontsize=14,color=muted)
        save(fig,'single-query-scores')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Precision@10','10 displayed records','Judge the returned page'],['Recall@10','All relevant records under the protocol','Complete total stipulated in the illustration'],['Known-seed recovery','The known relevant seed set','A useful check, not absolute collection recall'],['Relative recall','Relevant union found by compared strategies','Scope remains the discovered union']]
        t=table(ax,data,['Measure','Denominator','Qualification'],[.24,.38,.38]);t.set_fontsize(15)
        ax.set_title('Before comparing a recall number, ask where its denominator came from',pad=12)
        fig.text(.055,.045,'The first two denominators both equal ten in Figure 14.1 by coincidence. A live collection’s complete relevant total is usually unknown.',fontsize=14,color=muted)
        save(fig,'denominators')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.08,.25,.87,.57]);ax.set_facecolor(paper)
        xs=list(range(4));width=.32
        values_before=[float(r[2]) for r in LOCAL_ROWS]+[float(row_mean())]
        values_after=[float(r[3]) for r in LOCAL_ROWS]+[float(row_mean(True))]
        for offset,values,color,label in [(-width/2,values_before,blue,'Before'),(width/2,values_after,teal,'After')]:
            bars=ax.bar([x+offset for x in xs],values,width,color=color,label=label)
            ax.bar_label(bars,labels=[f'{v:.2f}' for v in values],padding=5,fontsize=17)
        ax.set_xticks(xs,['Identifier','Vocabulary mismatch','Composition row','Equal row mean']);ax.tick_params(axis='x',labelsize=15)
        ax.set_ylabel('Precision@10');ax.set_ylim(0,.69);ax.set_yticks([0,.1,.2,.3,.4,.5,.6])
        ax.spines[['top','right']].set_visible(False);ax.legend(loc='upper left',ncol=2,frameon=False)
        ax.set_title('Source’s hypothetical update · A mean gain hides the identifier loss',pad=15)
        fig.text(.055,.045,'Table 14.3: three equally weighted displayed rows. The composition row averages two separately judged queries. This is not a four-query mean or a product test.',fontsize=14,color=muted)
        save(fig,'local-regression')
        fig=plt.figure(figsize=(14,5.6),dpi=100,facecolor=cream)
        ax=fig.add_axes([.025,.14,.95,.74])
        data=[['Collection','Hold the documents fixed','State coverage and capture date'],['Queries / topics','Hold the requests fixed','State task and topic provenance'],['Judgements','Hold criteria and labels fixed','State assessors, depth and grades'],['Judgement pool','Union of top results from several runs','Unjudged need not mean irrelevant']]
        t=table(ax,data,['Evaluation input','Comparison control','What to disclose'],[.23,.38,.39]);t.set_fontsize(16)
        ax.set_title('A benchmark result is conditional on its evaluation apparatus',pad=12)
        fig.text(.055,.045,'Judgement pooling is not vector pooling. Under the described scoring protocol, unjudged useful records can receive no credit; novel approaches can be disadvantaged.',fontsize=14,color=muted)
        save(fig,'benchmark-controls')
    with (directory/'source-rankings.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['rank','before_record','before_judged_relevant','after_record','after_judged_relevant','displayed_at_10','controlled_source_illustration'])
        for i,(a,b) in enumerate(zip(BEFORE,AFTER),1):w.writerow([i,a,a in RELEVANT,b,b in RELEVANT,i<=10,True])
    with (directory/'local-regression.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['source_query_row','known_relevant_seed_count','before_p10','after_p10','row_averages_two_queries','hypothetical_update'])
        for i,(q,seed,a,b) in enumerate(LOCAL_ROWS):w.writerow([q,seed,float(a),float(b),i==2,True])
    manifest={'recipe_sha256':recipe,'kind':'source controlled rankings, metric arithmetic and hypothetical local regression','new_model_or_product_benchmarks':False,'checks':check_examples(),'files':{p.name:sha(p) for p in sorted(directory.iterdir()) if p.suffix in ('.png','.svg','.csv')},'passed':True}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n')
    return sha(manifest_path)
