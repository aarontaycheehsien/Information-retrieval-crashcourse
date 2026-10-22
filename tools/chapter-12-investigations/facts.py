"""Pinned control/output categories and selected examples; declared identity-set illustration."""
ARRANGEMENTS=('Fixed workflow','Adaptive workflow','Agentic search')
OUTPUT_PATTERNS=('Scripted deep search','Agentic deep search','Scripted deep research','Agentic deep research')
TOY_RELATED=('A','B','C','D')
TOY_REFERENCES=('A','C')
AUTISM_VARIANTS=('autism','autistic disorder','ASD','autism spectrum','neurodevelopmental disorder','pervasive developmental disorder')
AUTISM_EXPRESSION=' OR '.join(f'({term})' for term in AUTISM_VARIANTS)
AUTISM_BROADENING=('psychology','medicine','education','disability')
AUTISM_DATABASES=('PsycINFO','Education Research Complete','SocINDEX')
CATALOGUE_EXAMPLES=(
 ('autism','psychology; medicine; education; disability','PsycINFO; Education Research Complete; SocINDEX'),
 ('cost of living','inflation; household expenditure; consumer prices','Economics databases; no names specified here'),
 ('Rolex watches','luxury goods','Statista; Passport'),
 ('statis','misspelling correction','Statista'),
 ('refinituv','name/rebrand association','LSEG; recovered rebrand postdates the original query'))
EVIDENCE_DATES={'task_probe':'December 2025','architecture_comparison':'April 2026',
                'catalogue_demonstration':'June 2026','zero_result_logs':'2023',
                'scite_mcp_documentation':'October 2026'}


def uncited_candidates(related=TOY_RELATED,references=TOY_REFERENCES):
    return sorted(set(related)-set(references))


def check_examples():
    assert len(ARRANGEMENTS)==len(set(ARRANGEMENTS))==3
    assert len(OUTPUT_PATTERNS)==len(set(OUTPUT_PATTERNS))==4
    assert uncited_candidates()==['B','D']
    assert set(uncited_candidates()).isdisjoint(TOY_REFERENCES)
    assert set(TOY_RELATED)==set(uncited_candidates())|set(TOY_REFERENCES)
    assert len(AUTISM_VARIANTS)==6 and AUTISM_EXPRESSION.count(' OR ')==5
    assert AUTISM_EXPRESSION==('(autism) OR (autistic disorder) OR (ASD) OR (autism spectrum) '
                               'OR (neurodevelopmental disorder) OR (pervasive developmental disorder)')
    assert len(AUTISM_BROADENING)==4 and len(AUTISM_DATABASES)==3
    assert 'autism' not in AUTISM_BROADENING
    assert CATALOGUE_EXAMPLES[0][2]=='; '.join(AUTISM_DATABASES)
    assert EVIDENCE_DATES['zero_result_logs']=='2023' and EVIDENCE_DATES['catalogue_demonstration']=='June 2026'
    return {'source_control_categories':list(ARRANGEMENTS),'source_output_patterns':list(OUTPUT_PATTERNS),
            'invented_set_example':{'related':list(TOY_RELATED),'references':list(TOY_REFERENCES),
                                    'remaining_candidates':uncited_candidates(),'verified_citation_omissions':False},
            'source_one_shot_expression':AUTISM_EXPRESSION,'source_broadening':list(AUTISM_BROADENING),
            'reported_selected_database_results':list(AUTISM_DATABASES),'source_evidence_dates':EVIDENCE_DATES,
            'catalogue_examples_selected_not_sampled':True,'measured_success_rate':False,
            'new_product_tests':False,'coverage_established_by_round_limit':False,'passed':True}
