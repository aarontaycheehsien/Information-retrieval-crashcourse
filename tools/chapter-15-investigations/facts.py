"""Pinned reporting/inspection categories, source mock trace and nineteen vendor questions."""
PIPELINE_AREAS=('Query interpretation','Candidate retrieval','Ranking and fusion','Retrieval control')
METHODS=('LLM or NLP query interpretation','Agentic orchestration','Strict Boolean','Ranked lexical retrieval, such as BM25','Single-vector dense retrieval','Learnt sparse retrieval','Late-interaction retrieval')
INSPECTION_STAGES=('Query parsing, rewriting, expansion and routing','Boolean eligibility and filters','BM25 and other lexical scoring','Dense retrieval','Learnt sparse and late interaction','Fusion, reranking and presentation','Agentic orchestration')
VENDOR_GROUPS=(
 ('Query interpretation, transformation and control',(
  'What does the system infer, change and decide?',
  'Who controls the retrieval trajectory?')),
 ('Retrieval coverage and architecture',(
  'Which retrieval and ranking components are used?',
  'What role does the neural model perform?',
  'What is the indexed unit?',
  'How are passage results assembled?',
  'How is the hybrid combined?')),
 ('Exactness and failure testing',(
  'Is exact lexical matching retained?',
  'How is text tokenised and analysed?',
  'How are exactness, negation and exclusions tested?',
  'What trained the relevance model?')),
 ('Auditability and repeatability',(
  'Can users inspect why a result appeared?',
  'Can the search be documented and rerun?',
  'Are model, index and ranking changes disclosed?')),
 ('Cost, limits and continuity',(
  'What does a search cost, and what limits apply?',
  'What happens when a mode is retired?')),
 ('Institutional evaluation',(
  'How is performance evaluated, and on whose queries?',
  'Are failure cases part of the evaluation?',
  'Can the library compare behaviour across an update?')))
ORIGINAL_INPUT='Does open access increase citations?'
TRANSFORMED_QUERY='“open access” AND citation*'
RATIONALE='“This paper closely addresses your question about open access and citations.”'
CANDIDATE_RANK,CANDIDATE_COUNT,FINAL_RANK,DISPLAY_K=18,100,3,10
TRACE_FIELDS={
 'Original input:':ORIGINAL_INPUT,
 'Transformed query:':TRANSFORMED_QUERY,
 'Retrieval route:':'lexical retrieval over indexed abstracts.',
 'Indexed evidence:':'P’s abstract contains “open access” and “citations”.',
 'Candidate rank:':'18 of 100 supplied candidates.',
 'Reranking:':'moved P to rank 3.',
 'Display cut-off:':'first 10 records.',
 'Reranker’s internal scoring details:':'not disclosed.'}
INSPECTION_LABELS=('Start at the record','Fusion and display','Scoring and reranking','Matched evidence','Keep going back','Candidate source','Transformed query','Original query')


def numbered_questions():
    items=[]
    for group,(title,questions) in enumerate(VENDOR_GROUPS,1):
        for question in questions:items.append((len(items)+1,group,title,question))
    return items


def check_examples():
    assert len(PIPELINE_AREAS)==4 and len(METHODS)==len(INSPECTION_STAGES)==7
    assert [len(x[1]) for x in VENDOR_GROUPS]==[2,5,4,3,2,3]
    items=numbered_questions()
    assert len(items)==len({x[3] for x in items})==19
    assert [x[0] for x in items]==list(range(1,20))
    assert [x[0] for x in items if x[1]==6]==[17,18,19]
    assert 1<=FINAL_RANK<=DISPLAY_K<CANDIDATE_RANK<=CANDIDATE_COUNT
    assert len(TRACE_FIELDS)==8 and TRACE_FIELDS['Reranker’s internal scoring details:']=='not disclosed.'
    assert INSPECTION_LABELS[-1]=='Original query'
    return {'source_pipeline_areas':PIPELINE_AREAS,'source_reporting_methods':METHODS,'source_inspection_stages':INSPECTION_STAGES,
            'source_vendor_group_sizes':[len(x[1]) for x in VENDOR_GROUPS],'source_vendor_question_count':len(items),
            'hypothetical_source_trace':{'original_input':ORIGINAL_INPUT,'transformed_query':TRANSFORMED_QUERY,'candidate_rank':CANDIDATE_RANK,'candidate_count':CANDIDATE_COUNT,'final_rank':FINAL_RANK,'display_k':DISPLAY_K,'internal_reranker_details':'not disclosed','actual_search_run':False},
            'backward_inspection_is_not_execution_order':True,'generated_rationale_not_causal_evidence':True,
            'vendor_answers_invented':False,'new_product_tests':False,'passed':True}
