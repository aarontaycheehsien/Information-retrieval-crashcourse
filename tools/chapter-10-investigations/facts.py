"""Exact RRF arithmetic for pinned source lists and declared mathematical variations."""
from fractions import Fraction

LEXICAL=('A','B','C')
DENSE=('C','A','D')
INPUT_LISTS=(LEXICAL,DENSE)
C=60
RAW_TIGHT={'A':.90,'B':.89,'C':.88}
RAW_WIDE={'A':90.,'B':8.,'C':1.}


def contribution(rank,c=C,weight=1):
    assert isinstance(rank,int) and rank>=1 and isinstance(c,int) and c>=0 and weight>=0
    return Fraction(weight,c+rank)


def rrf(lists=INPUT_LISTS,c=C,weights=None):
    weights=(1,)*len(lists) if weights is None else weights
    assert len(weights)==len(lists) and all(len(set(xs))==len(xs) for xs in lists)
    totals={name:Fraction(0) for xs in lists for name in xs}
    for xs,weight in zip(lists,weights):
        for rank,name in enumerate(xs,1):totals[name]+=contribution(rank,c,weight)
    return totals


def fused_order(lists=INPUT_LISTS,c=C,weights=None):
    totals=rrf(lists,c,weights)
    # Alphabetical tie handling is for reproducible examples, not a prescribed RRF rule.
    return sorted(totals,key=lambda name:(-totals[name],name))


def rank_in(name,listing):
    return listing.index(name)+1 if name in listing else None


def input_cutoff(depth):
    return tuple(xs[:depth] for xs in INPUT_LISTS)


def check_examples():
    exact={'A':Fraction(1,61)+Fraction(1,62),'C':Fraction(1,63)+Fraction(1,61),
           'B':Fraction(1,62),'D':Fraction(1,63)}
    assert rrf()==exact and fused_order()==['A','C','B','D']
    assert {n:f'{float(v):.5f}' for n,v in exact.items()}=={'A':'0.03252','C':'0.03227','B':'0.01613','D':'0.01587'}
    assert len(set(LEXICAL)&set(DENSE))==2 and set(LEXICAL)&set(DENSE)=={'A','C'}
    assert sum(map(len,INPUT_LISTS))==6 and len(rrf())==4
    shallow=rrf(input_cutoff(2))
    assert set(shallow)=={'A','B','C'} and 'D' not in shallow
    assert shallow['C']==exact['C']-Fraction(1,63) and shallow['A']==exact['A']
    assert fused_order(input_cutoff(2))==['A','C','B']
    assert fused_order()[:2]==['A','C'] and set(rrf())=={'A','B','C','D'}
    assert rrf(input_cutoff(1))=={'A':Fraction(1,61),'C':Fraction(1,61)}
    assert contribution(1,0)/contribution(3,0)==3
    assert contribution(1,60)/contribution(3,60)==Fraction(63,61)
    assert fused_order(weights=(1,2))==['C','A','D','B']
    assert rrf(weights=(1,2))['C']>rrf(weights=(1,2))['A']
    assert sorted(RAW_TIGHT,key=RAW_TIGHT.get,reverse=True)==list(LEXICAL)
    assert sorted(RAW_WIDE,key=RAW_WIDE.get,reverse=True)==list(LEXICAL)
    assert RAW_TIGHT['A']-RAW_TIGHT['B'] < RAW_WIDE['A']-RAW_WIDE['B']
    return {'source_lists':[list(xs) for xs in INPUT_LISTS],'constant':C,
            'exact_fraction_scores':{n:str(v) for n,v in exact.items()},
            'rounded_source_scores':{n:f'{float(v):.5f}' for n,v in exact.items()},
            'baseline_order':fused_order(),'input_occurrences':6,'distinct_candidates':4,
            'shallower_order':fused_order(input_cutoff(2)),'shallower_candidates':list(shallow),
            'dense_double_weight_order':fused_order(weights=(1,2)),
            'score_gap_examples_are_invented':True,'measured_retrieval_results':False,
            'fused_scores_are_relevance_probabilities':False,'passed':True}
