"""Exact source examples and metric arithmetic; no retrieval system is run."""
from fractions import Fraction

MEASURES=('Precision','Recall')
METRICS=('Precision@k','MRR','MAP','nDCG')
RELEVANCE_PERSPECTIVES=('System or algorithmic relevance','Topical relevance','Cognitive relevance or pertinence','Situational relevance or usefulness')
RELEVANT=tuple('ABCDEFGHIJ')
BEFORE=tuple('AKLMBNOPQRCDEFGHIJST')
AFTER=tuple('ABKCDLEMFNGHIJOPQRST')
LOCAL_ROWS=(
 ('SLC6A4 promoter polymorphism',3,Fraction(3,10),Fraction(1,10)),
 ('barriers to adopting learning analytics in further education',5,Fraction(2,10),Fraction(5,10)),
 ('peer support reduces readmission / peer support increases readmission',4,Fraction(4,10),Fraction(4,10)))


def precision_at(ranking,k,relevant=RELEVANT):
    assert k>0 and len(ranking)>=k,'This complete-depth example uses k as denominator'
    return Fraction(sum(x in relevant for x in ranking[:k]),k)


def recall_at(ranking,k,relevant=RELEVANT):
    assert relevant and len(set(ranking))==len(ranking)
    return Fraction(len(set(ranking[:k])&set(relevant)),len(relevant))


def reciprocal_rank(ranking,relevant=RELEVANT):
    return next((Fraction(1,i) for i,x in enumerate(ranking,1) if x in relevant),Fraction(0))


def average_precision(ranking,relevant=RELEVANT):
    assert relevant
    return sum((precision_at(ranking,i,relevant) for i,x in enumerate(ranking,1) if x in relevant),Fraction(0))/len(relevant)


def row_mean(after=False):
    return sum((row[3 if after else 2] for row in LOCAL_ROWS),Fraction(0))/len(LOCAL_ROWS)


def check_examples():
    assert len(BEFORE)==len(AFTER)==20 and set(BEFORE)==set(AFTER)==set('ABCDEFGHIJKLMNOPQRST')
    assert len(set(BEFORE))==len(set(AFTER))==20
    assert precision_at(BEFORE,10)==recall_at(BEFORE,10)==Fraction(2,10)
    assert precision_at(AFTER,10)==recall_at(AFTER,10)==Fraction(6,10)
    assert recall_at(BEFORE,20)==recall_at(AFTER,20)==1
    assert reciprocal_rank(BEFORE)==reciprocal_rank(AFTER)==1
    assert average_precision(AFTER)>average_precision(BEFORE)
    assert row_mean()==Fraction(3,10) and row_mean(True)==Fraction(1,3)
    assert (LOCAL_ROWS[0][2]-LOCAL_ROWS[0][3])/LOCAL_ROWS[0][2]==Fraction(2,3)
    assert all(recall_at(BEFORE,k)<=recall_at(BEFORE,k+1) for k in range(1,20))
    assert precision_at(BEFORE,5)>precision_at(BEFORE,4) and precision_at(BEFORE,6)<precision_at(BEFORE,5)
    return {'source_measures':MEASURES,'source_ranked_metrics':METRICS,'source_relevance_perspectives':RELEVANCE_PERSPECTIVES,
            'controlled_source_reranking':{'relevant':RELEVANT,'before':BEFORE,'after':AFTER,'before_p10_r10':.2,'after_p10_r10':.6,'pool_recall_both':1,'complete_relevance_set_stipulated':True},
            'single_query_arithmetic':{'reciprocal_rank_both':1,'average_precision_before':float(average_precision(BEFORE)),'average_precision_after':float(average_precision(AFTER)),'not_a_multiquery_mrr_or_map_comparison':True},
            'illustrative_local_rows':{'before_equal_row_mean':float(row_mean()),'after_equal_row_mean':float(row_mean(True)),'third_row_averages_two_separately_judged_queries':True,'identifier_relative_precision_loss':float(Fraction(2,3))},
            'known_seeds_not_absolute_recall':True,'new_model_or_product_benchmarks':False,'passed':True}
