"""Pinned Chapter 11 taxonomies, visible Boolean example and scoped audit figures."""
QUERY_OBJECTS=(
 'Free-text string','Controlled term or structured expression','Citation edge','Seed document',
 'Relevance judgement','Browse or monitoring target','Programmatic predicate','Task brief')
RECEIVERS=('Lexical or Boolean retriever','Dense retriever','LLM query translator','Agentic controller','Undisclosed pipeline')
OBJECT_MECHANISMS=(
 'Lexical, dense or hybrid retrieval','Annotations, fields, filters, Boolean logic',
 'Direct links, coupling or co-citation','Text similarity, citation relations, or both',
 'Construct a later retrieval input','Collection browsing or continuing alerts',
 'API filters, identifiers, sorting, pagination','Controller scope, criteria and stopping')
STRUCTURED_PARTS=(
 ('Year range','PY=(2020-2024)'),('Organisation','OG_SMART=(university of california)'),
 ('Topic 1','TS=(apple)'),('Topic 2','TS=(oranges)'),('Topic 3','TS=(bananas)'))
STRUCTURED_QUERY=' AND '.join(clause for _,clause in STRUCTURED_PARTS)
GENERATED_TEXT=('A study of the open-access citation advantage compares citation counts for open and '
                'subscription articles, accounting for discipline and publication year.')
AUDIT_SOURCES=495
AUDIT_REPORTED_SHARES={'Protocol-defined database and hand searches':30,'Snowballing':51}
PRF_SEQUENCE=('initial query','initial ranking','assume top records relevant','construct later query','later retrieval')
SCREENING_SEQUENCE=('existing candidate pool','inclusion or exclusion judgements','reprioritise existing records')
GENERATED_PATHS={'Query2doc':'original query + generated language → lexical or dense retrieval',
                 'HyDE':'generated document → dense encoder → vector retrieval of real sources'}


def check_examples():
    assert len(QUERY_OBJECTS)==len(set(QUERY_OBJECTS))==len(OBJECT_MECHANISMS)==8
    assert len(RECEIVERS)==len(set(RECEIVERS))==5
    assert STRUCTURED_QUERY==('PY=(2020-2024) AND OG_SMART=(university of california) '
                              'AND TS=(apple) AND TS=(oranges) AND TS=(bananas)')
    assert len(STRUCTURED_PARTS)==5 and STRUCTURED_QUERY.count(' AND ')==4
    assert [clause for _,clause in STRUCTURED_PARTS if clause.startswith('TS=')]==['TS=(apple)','TS=(oranges)','TS=(bananas)']
    assert AUDIT_SOURCES==495 and list(AUDIT_REPORTED_SHARES.values())==[30,51]
    assert all(0<=value<=100 for value in AUDIT_REPORTED_SHARES.values())
    assert PRF_SEQUENCE.index('initial ranking')<PRF_SEQUENCE.index('construct later query')<PRF_SEQUENCE.index('later retrieval')
    assert 'later retrieval' not in SCREENING_SEQUENCE
    assert set(GENERATED_PATHS)=={'Query2doc','HyDE'}
    assert 'original query + generated language' in GENERATED_PATHS['Query2doc']
    assert 'dense encoder' in GENERATED_PATHS['HyDE']
    return {'source_query_objects':list(QUERY_OBJECTS),'receivers':list(RECEIVERS),
            'source_structured_expression':STRUCTURED_QUERY,'all_five_conditions_joined_with_AND':True,
            'scoped_review_audit':{'included_sources':AUDIT_SOURCES,'reported_percentages':AUDIT_REPORTED_SHARES,
                                 'universal_estimate':False,'converted_to_exact_source_counts':False},
            'prf_sequence':list(PRF_SEQUENCE),'screening_sequence':list(SCREENING_SEQUENCE),
            'generated_paths':GENERATED_PATHS,'generated_text_is_evidence':False,
            'new_product_or_model_tests':False,'passed':True}
