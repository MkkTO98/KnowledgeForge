
import json, subprocess, sys
from pathlib import Path
out=Path('artifacts/reports/campaign43-canonical-publication-20260712/relationship_export_verification')
out.mkdir(parents=True, exist_ok=True)
base={'query_contract':'knowledgeforge_relationship_query_v1@1.0','controls':{'sort':'package_id','limit':1000,'max_result_count':1000,'include_full_package_payload':True,'include_provenance':True,'only_current_valid_projection':True}}
queries={
 'all_relationships': {**base, 'filters': {'statement_type':'derived_relationship'}},
 'raw_pearson': {**base, 'filters': {'statement_type':'derived_relationship','method_identifier':'wdi_annual_scalar_pearson_correlation_v1','transformation_state':'raw'}},
 'first_difference_method': {**base, 'filters': {'statement_type':'derived_relationship','method_identifier':'wdi_annual_scalar_first_difference_pearson_v1'}},
 'first_difference_transformation': {**base, 'filters': {'statement_type':'derived_relationship','transformation_state':'first_difference'}},
}
for name,q in queries.items():
    (out/f'{name}_query.json').write_text(json.dumps(q, indent=2, sort_keys=True)+'\n')
    with (out/f'{name}_export.stdout.json').open('w') as stdout:
        subprocess.run(['python3','tools/relationship_export_v1.py','export','--database','knowledgeforge','--query',str(out/f'{name}_query.json'),'--output',str(out/f'{name}_export.json')], check=True, stdout=stdout)
    with (out/f'{name}_verify.json').open('w') as stdout:
        subprocess.run(['python3','tools/relationship_export_v1.py','verify','--export',str(out/f'{name}_export.json')], check=True, stdout=stdout)
    with (out/f'{name}_consumer.stdout.json').open('w') as stdout:
        subprocess.run(['python3','tools/relationship_export_consumer_simulator_v1.py','--export',str(out/f'{name}_export.json'),'--output',str(out/f'{name}_consumer.json')], check=True, stdout=stdout)
ids=set([
'pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-first-difference-pearson-companion-v1',
'pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-first-difference-pearson-companion-v1',
'pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-first-difference-pearson-companion-v1',
'pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-first-difference-pearson-companion-v1',
'pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-first-difference-pearson-companion-v1',
'pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-first-difference-pearson-companion-v1'])
def loadids(name):
    d=json.load(open(out/f'{name}_export.json'))['deterministic_content']
    return set(d['package_identities']), d
all_ids, all_d=loadids('all_relationships'); raw_ids, raw_d=loadids('raw_pearson'); fd_m_ids, fd_m_d=loadids('first_difference_method'); fd_t_ids, fd_t_d=loadids('first_difference_transformation')
exposure=[]
for r in fd_m_d['results']:
    if r['package_id'] in ids:
        meta=r['relationship_metadata']; payload=r['canonical_package']['generated_statements'][0]['structured_payload']
        exposure.append({'package_id':r['package_id'],'method':meta.get('method_identifier'),'transformation_state':meta.get('transformation_state'),'temporal_scope':meta.get('period_scope'),'coefficient':meta.get('coefficient'),'limitations_present':meta.get('limitations') is not None,'lineage_present':bool(r['canonical_package'].get('lineage')),'source_raw_package':payload.get('raw_package_reference',{}).get('package_id'),'non_supersession':payload.get('does_not_supersede_raw_package') is True})
summary={'counts':{'all_relationships':len(all_ids),'raw_pearson':len(raw_ids),'first_difference_method':len(fd_m_ids),'first_difference_transformation':len(fd_t_ids)},'raw_fd_overlap':sorted(raw_ids.intersection(fd_m_ids)),'six_in_fd_method':sorted(ids if ids.issubset(fd_m_ids) else []),'six_in_fd_transformation':sorted(ids if ids.issubset(fd_t_ids) else []),'six_in_raw':sorted(ids.intersection(raw_ids)),'consumer_valid':{name:json.load(open(out/f'{name}_consumer.json'))['valid'] for name in ['all_relationships','raw_pearson','first_difference_method','first_difference_transformation']},'six_exposure':exposure}
(out/'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True)+'\n')
print(json.dumps(summary, indent=2, sort_keys=True))
expected={'all_relationships':35,'raw_pearson':21,'first_difference_method':14,'first_difference_transformation':14}
if summary['counts']!=expected: sys.exit(6)
if summary['raw_fd_overlap'] or summary['six_in_raw'] or len(summary['six_in_fd_method'])!=6 or len(summary['six_in_fd_transformation'])!=6 or not all(summary['consumer_valid'].values()) or not all(x['limitations_present'] and x['lineage_present'] and x['non_supersession'] for x in exposure): sys.exit(7)
