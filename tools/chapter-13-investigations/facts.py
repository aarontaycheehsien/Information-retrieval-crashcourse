"""Source diagnostic categories and declared exact-identity and relation contrasts."""
from collections import Counter
import re

DIAGNOSTIC_NOTICES=(
 'A known relevant record uses different terminology',
 'A coined term, identifier or specialised string disappears or behaves strangely',
 'A model works plausibly in general but poorly for this discipline, query style, corpus or retrieval purpose',
 'All the words occur, but their direction, negation or relationship is wrong')
VOCABULARY_QUESTIONS=(
 'Is there a corresponding term in the index vocabulary?',
 'Can the model tokeniser encode the string?',
 'Has the model learnt a useful representation?')
FIRST_STAGE_METHODS=('Strict Boolean','BM25','Single-vector dense retrieval')
SHIFT_SITES=('Query shift','Corpus or domain shift','Task or relevance shift')
BOUNDARIES=('Outside the collection','Excluded by a filter','Absent from the candidate pool','Retrieved but not displayed')
IDENTIFIER='DELULU-427'
ID_RECORDS=(('D1','DELULU-427'),('D2','DELULU-427'),('D3','DELULU-427'),('D4','DELULU-428'))
BERT_PIECES=('ri','##zz','##lord')
RELATION_PAIR=('A causes B','B causes A')
NEGATION_PAIR=('The intervention does not increase risk','The intervention does increase risk')


def exact_identifier_hits(query=IDENTIFIER):
    return [label for label,value in ID_RECORDS if value==query]


def bag_terms(value):
    return Counter(re.findall(r'\w+',value.casefold()))


def check_examples():
    assert len(DIAGNOSTIC_NOTICES)==4 and len(VOCABULARY_QUESTIONS)==3
    assert FIRST_STAGE_METHODS==('Strict Boolean','BM25','Single-vector dense retrieval')
    assert exact_identifier_hits()==['D1','D2','D3']
    assert exact_identifier_hits('DELULU-428')==['D4']
    assert len(ID_RECORDS)==4 and len({x[0] for x in ID_RECORDS})==4
    assert RELATION_PAIR[0]!=RELATION_PAIR[1] and bag_terms(RELATION_PAIR[0])==bag_terms(RELATION_PAIR[1])
    assert bag_terms(NEGATION_PAIR[0])-bag_terms(NEGATION_PAIR[1])==Counter({'not':1})
    assert BERT_PIECES==('ri','##zz','##lord')
    return {'source_diagnostic_notices':list(DIAGNOSTIC_NOTICES),'source_vocabulary_questions':list(VOCABULARY_QUESTIONS),
            'source_first_stage_methods':list(FIRST_STAGE_METHODS),'shift_sites':list(SHIFT_SITES),
            'declared_keyword_field_example':{'input':IDENTIFIER,'stored_values':ID_RECORDS,'exact_hits':exact_identifier_hits(),'actual_index_or_bm25_run':False},
            'relation_contrast_same_term_counts':True,'measured_relation_scores':False,
            'bert_pieces_reported_by_source':list(BERT_PIECES),'new_tokenizer_run':False,
            'diagnoses_are_nonexclusive_hypotheses':True,'new_model_or_product_tests':False,'passed':True}
