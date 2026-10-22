"""Source-exact lexical vectors and grouping; explicitly declared weighting toys."""
from collections import Counter
import math

VOCAB = ('attack','cancer','heart','interview','job','tips','treatment')
DOCUMENTS = {'D1':'heart attack treatment','D2':'job interview tips','D3':'cancer treatment'}
REPEATED = {**DOCUMENTS,'D1':'heart attack treatment treatment treatment'}
QUERY = ('heart','treatment')
SOURCE_BINARY = {'D1':(1,0,1,0,0,0,1),'D2':(0,0,0,1,1,1,0),'D3':(0,1,0,0,0,0,1)}
K1, B = 1.2, .75
# Schematic whole-word vocabulary; not a real model's subword outputs.
EXPANSION = {'heart':1.2,'attack':1.,'myocardial':.8,'infarction':.7}
BIBLIOGRAPHIC = {'year':2026,'pages':14,'references':32,'citations':87}
MATCHES = (('A',2),('A',7),('B',3),('A',9))
UNIT_COUNTS = {'abstract':1,'sections':10,'overlapping passages':50}


def vector(document, binary=False):
    c=Counter(document.split())
    return tuple(int(c[t]>0) if binary else c[t] for t in VOCAB)


def df(term):
    return sum(term in text.split() for text in DOCUMENTS.values())


def tfidf(term, name):
    return Counter(REPEATED[name].split())[term] * math.log(len(DOCUMENTS)/df(term))


def bm25(term,name,frequency=None):
    counts=Counter(REPEATED[name].split())
    f=counts[term] if frequency is None else frequency
    avg=sum(len(t.split()) for t in REPEATED.values())/len(REPEATED)
    idf=math.log(1+(len(REPEATED)-df(term)+.5)/(df(term)+.5))
    return idf*f*(K1+1)/(f+K1*(1-B+B*sum(counts.values())/avg)) if f else 0.


def groups():
    return {name:[n for p,n in MATCHES if p==name] for name in dict(MATCHES)}


def check_examples():
    assert tuple(sorted(set(' '.join(DOCUMENTS.values()).split()))) == VOCAB
    assert {n:vector(t,True) for n,t in DOCUMENTS.items()} == SOURCE_BINARY
    assert vector(' '.join(QUERY),True)==(0,0,1,0,0,0,1)
    overlaps={n:sum(t in text.split() for t in QUERY) for n,text in DOCUMENTS.items()}
    assert overlaps == {'D1':2,'D2':0,'D3':1}
    and_set=[n for n,text in DOCUMENTS.items() if all(t in text.split() for t in QUERY)]
    or_set=[n for n,text in DOCUMENTS.items() if any(t in text.split() for t in QUERY)]
    assert and_set == ['D1'] and or_set == ['D1','D3']
    assert vector(REPEATED['D1'])==(1,0,1,0,0,0,3)
    assert vector(REPEATED['D1'],True)==SOURCE_BINARY['D1']
    assert df('heart')==1 and df('treatment')==2
    assert math.log(3/df('heart'))>math.log(3/df('treatment'))>0
    assert bm25('treatment','D1',2)-bm25('treatment','D1',1)>bm25('treatment','D1',3)-bm25('treatment','D1',2)>0
    assert math.isclose(tfidf('heart','D1'),math.log(3))
    assert math.isclose(tfidf('treatment','D1'),3*math.log(1.5))
    assert math.isclose(EXPANSION['myocardial']+EXPANSION['infarction'],1.5)
    assert not set(('myocardial','infarction')) & set('heart attack'.split())
    assert all(BIBLIOGRAPHIC.values()) and len(BIBLIOGRAPHIC)==4
    assert len(MATCHES)==4 and groups()=={'A':[2,7,9],'B':[3]}
    assert UNIT_COUNTS=={'abstract':1,'sections':10,'overlapping passages':50}
    return {'source_binary_vectors':{n:list(v) for n,v in SOURCE_BINARY.items()},'overlap_scores':overlaps,
            'AND':and_set,'OR':or_set,'tfidf_variant':'raw TF * ln(N/df)',
            'bm25_parameters':{'k1':K1,'b':B,'average_length':10/3},
            'bm25_idf':'ln(1+(N-df+0.5)/(df+0.5))','invented_expansion_weights':EXPANSION,
            'measured_model_outputs':False,'passage_matches':4,'distinct_papers':2,'groups':groups(),
            'unit_counts_are_alternative_teaching_cases':True,'passed':True}
