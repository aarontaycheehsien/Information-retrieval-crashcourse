"""Source-exact invented MaxSim values, schematic selections and documented budgets."""
import math

QUERY_TOKENS=('citation','benefit')
DOCUMENT_TOKENS=('open','access','citation','advantage')
SIMILARITIES=((.10,.20,.90,.40),(.20,.30,.50,.80))
SHORTLIST=('A','B','C')
RERANKED=('B','A','C')
EXCLUDED='X'
ASPECTS={'A':'Overall citation advantage','B':'Overall citation advantage',
         'C':'Overall citation advantage','D':'Disciplinary differences',
         'E':'Selection-bias methods','F':'A weakly related topic'}
INDEPENDENT_SELECTION=('A','B','C')
DIVERSE_SELECTION=('A','D','E')
DOCUMENTED_BUDGETS={'Semantic Scholar (2025)':1000,'PubMed Best Match':500,
                    'Primo reranking':30,'Primo abstract context':5}


def row_maxima(matrix=SIMILARITIES):
    assert matrix and all(len(row)==len(matrix[0]) and row for row in matrix)
    return tuple(max(row) for row in matrix)


def maxsim(matrix=SIMILARITIES):
    return sum(row_maxima(matrix))


def alignments(matrix=SIMILARITIES):
    return tuple(max(range(len(row)),key=row.__getitem__) for row in matrix)


def aspect_count(selection):
    return len({ASPECTS[x] for x in selection})


def check_examples():
    assert len(QUERY_TOKENS)==len(SIMILARITIES)==2
    assert all(len(row)==len(DOCUMENT_TOKENS)==4 for row in SIMILARITIES)
    assert row_maxima()==(.9,.8) and alignments()==(2,3)
    assert math.isclose(maxsim(),1.7)
    # Each row is independent; the scorer permits reuse of the same winning column.
    repeated=(SIMILARITIES[0],SIMILARITIES[0])
    assert alignments(repeated)==(2,2) and math.isclose(maxsim(repeated),1.8)
    assert set(RERANKED)==set(SHORTLIST) and EXCLUDED not in RERANKED
    assert len(INDEPENDENT_SELECTION)==len(DIVERSE_SELECTION)==3
    assert aspect_count(INDEPENDENT_SELECTION)==1 and aspect_count(DIVERSE_SELECTION)==3
    assert 'F' not in (*INDEPENDENT_SELECTION,*DIVERSE_SELECTION)
    assert len(ASPECTS)==6 and len({'A','B','C'})==3  # distinct schematic studies
    assert DOCUMENTED_BUDGETS['Primo reranking']==30
    assert DOCUMENTED_BUDGETS['Primo abstract context']==5
    assert DOCUMENTED_BUDGETS['PubMed Best Match']==500
    assert DOCUMENTED_BUDGETS['Semantic Scholar (2025)']==1000
    return {'invented_source_similarities':[list(r) for r in SIMILARITIES],
            'row_maxima':list(row_maxima()),'maxsim':maxsim(),
            'winning_document_tokens':[DOCUMENT_TOKENS[x] for x in alignments()],
            'maxsim_allows_reused_document_tokens':True,'measured_model_output':False,
            'reranking_preserves_candidate_set':True,'excluded_record':EXCLUDED,
            'stipulated_selections':{'individual':list(INDEPENDENT_SELECTION),'diversified':list(DIVERSE_SELECTION)},
            'aspect_counts':{'individual':1,'diversified':3},'calculated_diversification_algorithm':False,
            'documented_budgets_not_relevance_counts':DOCUMENTED_BUDGETS,'passed':True}
