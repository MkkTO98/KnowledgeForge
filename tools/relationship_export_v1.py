#!/usr/bin/env python3
"""KnowledgeForge-owned read-only relationship export contract v1.

The external consumer receives deterministic export JSON. It does not need
KnowledgeForge PostgreSQL table names, canonical filesystem layout, or runtime code.
"""
from __future__ import annotations
import argparse, hashlib, json, subprocess, time, sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

PROJECT_ROOT=Path(__file__).resolve().parents[1]
REPOSITORY_ROOT=PROJECT_ROOT/'knowledge_repository'
CONTRACT_ID='knowledgeforge_relationship_export_v1@1.0'
QUERY_CONTRACT_ID='knowledgeforge_relationship_query_v1@1.0'
DATABASE_DEFAULT='knowledgeforge'
SCHEMA='knowledgeforge_projection'
METHOD_CONTRACT_V1='sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476'
METHOD_ID_V1='wdi_annual_scalar_pearson_correlation_v1'
METHOD_VERSION_V1='1.0'

class ExportError(RuntimeError): pass

def canonical_json(v:Any)->str:
    return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)

def sha256(v:Any)->str:
    return 'sha256:'+hashlib.sha256(canonical_json(v).encode()).hexdigest()

def sha_bytes(b:bytes)->str:
    return 'sha256:'+hashlib.sha256(b).hexdigest()

def sql_lit(s:str)->str:
    return "'"+str(s).replace("'","''")+"'"

def psql(db:str, sql:str)->str:
    p=subprocess.run(['psql','-X','-v','ON_ERROR_STOP=1','-d',db,'-At'],input=sql,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if p.returncode: raise ExportError(p.stderr.strip() or p.stdout.strip())
    return p.stdout.strip()

def psql_json(db:str, sql:str)->Any:
    out=psql(db,sql)
    return json.loads(out) if out else None

def load_manifest(repo:Path=REPOSITORY_ROOT)->dict[str,Any]: return json.loads((repo/'manifest.json').read_text())

def active_freshness(db:str, repo:Path=REPOSITORY_ROOT, *, expected_repo_fp:str|None=None, expected_projection_id:str|None=None)->dict[str,Any]:
    manifest=load_manifest(repo)
    if expected_repo_fp and expected_repo_fp!=manifest.get('repository_fingerprint'):
        raise ExportError('fail_closed_repository_fingerprint_expectation_mismatch')
    state=psql_json(db,f"""SELECT row_to_json(s)::text FROM (
      SELECT projection_id, repository_fingerprint, object_count, logical_projection_fingerprint, tool_version, status, active
      FROM {SCHEMA}.projection_state WHERE active AND status='valid' ORDER BY build_finished_at DESC NULLS LAST LIMIT 1) s;""")
    if not state: raise ExportError('fail_closed_no_active_valid_projection')
    reasons=[]
    if expected_projection_id and expected_projection_id!=state.get('projection_id'): reasons.append('projection_id_expectation_mismatch')
    if state.get('repository_fingerprint')!=manifest.get('repository_fingerprint'): reasons.append('repository_fingerprint_mismatch')
    if state.get('object_count')!=manifest.get('object_count'): reasons.append('object_count_mismatch')
    count=psql_json(db,f"SELECT count(*)::int FROM {SCHEMA}.projected_packages WHERE projection_id={sql_lit(state['projection_id'])};")
    if count!=manifest.get('object_count'): reasons.append('projected_count_mismatch')
    if reasons: raise ExportError('fail_closed_stale_projection:'+','.join(sorted(reasons)))
    return {'valid':True,'state':state,'repository_fingerprint':manifest['repository_fingerprint'],'repository_object_count':manifest['object_count'],'projected_count':count}

ALLOWED_FILTERS={'package_id','statement_type','evidence_family','lifecycle_state','package_fingerprint','method_identifier','method_version','method_contract_fingerprint','series_code_involvement','entity','frequency','period_overlap','transformation_state','coefficient_min','coefficient_max','absolute_coefficient_min'}
ALLOWED_CONTROLS={'sort','limit','offset','include_full_package_payload','include_provenance','only_current_valid_projection','max_result_count'}

def validate_query(q:dict[str,Any])->dict[str,Any]:
    if q.get('query_contract')!=QUERY_CONTRACT_ID: raise ExportError('unsupported_query_contract')
    filters=q.get('filters') or {}; controls=q.get('controls') or {}
    if not isinstance(filters,dict) or not isinstance(controls,dict): raise ExportError('invalid_query_shape')
    extra=set(filters)-ALLOWED_FILTERS
    if extra: raise ExportError('unsupported_filters:'+','.join(sorted(extra)))
    extra=set(controls)-ALLOWED_CONTROLS
    if extra: raise ExportError('unsupported_controls:'+','.join(sorted(extra)))
    limit=int(controls.get('limit',controls.get('max_result_count',100)))
    max_result_count=int(controls.get('max_result_count',100))
    if limit<0 or max_result_count<0 or limit>max_result_count or max_result_count>1000: raise ExportError('invalid_or_unbounded_result_limit')
    if controls.get('sort','package_id')!='package_id': raise ExportError('unsupported_sort')
    if controls.get('only_current_valid_projection',True) is not True: raise ExportError('only_current_valid_projection_required')
    if controls.get('include_full_package_payload',True) is not True: raise ExportError('full_payload_required_for_v1')
    for k in ['coefficient_min','coefficient_max','absolute_coefficient_min']:
        if k in filters:
            try: Decimal(str(filters[k]))
            except InvalidOperation: raise ExportError('invalid_decimal_filter:'+k)
    return {'query_contract':QUERY_CONTRACT_ID,'filters':filters,'controls':{'sort':'package_id','limit':limit,'offset':int(controls.get('offset',0)),'include_full_package_payload':True,'include_provenance':bool(controls.get('include_provenance',True)),'only_current_valid_projection':True,'max_result_count':max_result_count}}

def method_expr():
    return f"COALESCE(payload_json #>> '{{generated_statements,0,structured_payload,method_id}}', CASE WHEN payload_json #>> '{{generated_statements,0,structured_payload,method_contract_fingerprint}}' = {sql_lit(METHOD_CONTRACT_V1)} THEN {sql_lit(METHOD_ID_V1)} ELSE NULL END)"

def method_version_expr():
    return f"COALESCE(payload_json #>> '{{generated_statements,0,structured_payload,method_version}}', CASE WHEN payload_json #>> '{{generated_statements,0,structured_payload,method_contract_fingerprint}}' = {sql_lit(METHOD_CONTRACT_V1)} THEN {sql_lit(METHOD_VERSION_V1)} ELSE NULL END)"

def transformation_expr():
    # Handles Campaign 36-39 object-shaped transformation_state and Campaign 40 scalar raw.
    return "CASE WHEN jsonb_typeof(payload_json #> '{generated_statements,0,structured_payload,transformation_state}')='object' THEN COALESCE(payload_json #>> '{generated_statements,0,structured_payload,transformation_state,series_a}', payload_json #>> '{generated_statements,0,structured_payload,transformation_state,series_b}') ELSE payload_json #>> '{generated_statements,0,structured_payload,transformation_state}' END"

def build_sql(qv:dict[str,Any], projection_id:str)->tuple[str,dict[str,float]]:
    f=qv['filters']; c=qv['controls']; wh=[f"p.projection_id={sql_lit(projection_id)}"]
    joins=''
    if 'statement_type' in f:
        joins+=f" JOIN {SCHEMA}.package_statement_types st ON st.projection_id=p.projection_id AND st.package_id=p.package_id"
        wh.append('st.statement_type='+sql_lit(f['statement_type']))
    if 'package_id' in f:
        vals=f['package_id'] if isinstance(f['package_id'],list) else [f['package_id']]
        wh.append('p.package_id IN ('+','.join(sql_lit(x) for x in vals)+')')
    if 'evidence_family' in f: wh.append('p.evidence_family='+sql_lit(f['evidence_family']))
    if 'lifecycle_state' in f: wh.append('p.lifecycle_state='+sql_lit(f['lifecycle_state']))
    if 'package_fingerprint' in f: wh.append('p.package_fingerprint='+sql_lit(f['package_fingerprint']))
    if 'method_contract_fingerprint' in f: wh.append("p.payload_json #>> '{generated_statements,0,structured_payload,method_contract_fingerprint}'="+sql_lit(f['method_contract_fingerprint']))
    if 'method_identifier' in f: wh.append(method_expr()+'='+sql_lit(f['method_identifier']))
    if 'method_version' in f: wh.append(method_version_expr()+'='+sql_lit(f['method_version']))
    if 'series_code_involvement' in f:
        code=sql_lit(f['series_code_involvement']); wh.append(f"(p.payload_json #>> '{{generated_statements,0,structured_payload,series_a,code}}'={code} OR p.payload_json #>> '{{generated_statements,0,structured_payload,series_b,code}}'={code})")
    if 'entity' in f: wh.append("p.payload_json #>> '{generated_statements,0,structured_payload,entity_id}'="+sql_lit(f['entity']))
    if 'frequency' in f: wh.append("p.payload_json #>> '{generated_statements,0,structured_payload,frequency}'="+sql_lit(f['frequency']))
    if 'transformation_state' in f: wh.append(transformation_expr()+'='+sql_lit(f['transformation_state']))
    if 'period_overlap' in f:
        po=f['period_overlap']; wh.append(f"((p.payload_json #>> '{{generated_statements,0,structured_payload,period_scope,start}}')::int <= {int(po['end'])} AND (p.payload_json #>> '{{generated_statements,0,structured_payload,period_scope,end}}')::int >= {int(po['start'])})")
    coeff="(p.payload_json #>> '{generated_statements,0,structured_payload,pearson_coefficient,canonical}')::numeric"
    if 'coefficient_min' in f: wh.append(coeff+'>='+str(Decimal(str(f['coefficient_min']))))
    if 'coefficient_max' in f: wh.append(coeff+'<='+str(Decimal(str(f['coefficient_max']))))
    if 'absolute_coefficient_min' in f: wh.append('abs('+coeff+')>='+str(Decimal(str(f['absolute_coefficient_min']))))
    sql=f"""SELECT COALESCE(json_agg(row_to_json(t) ORDER BY package_id),'[]'::json)::text FROM (
      SELECT p.package_id, p.package_fingerprint, p.package_manifest_fingerprint, p.evidence_family, p.lifecycle_state, p.payload_sha256, p.payload_json AS package_payload
      FROM {SCHEMA}.projected_packages p {joins}
      WHERE {' AND '.join(wh)}
      ORDER BY p.package_id
      LIMIT {int(c['limit'])} OFFSET {int(c['offset'])}
    ) t;"""
    shapes={'indexed_generic_filters':sum(1 for k in ['package_id','evidence_family','lifecycle_state','package_fingerprint','statement_type'] if k in f),'jsonb_payload_scans':sum(1 for k in ['method_identifier','method_version','method_contract_fingerprint','series_code_involvement','entity','frequency','period_overlap','transformation_state','coefficient_min','coefficient_max','absolute_coefficient_min'] if k in f)}
    return sql,shapes

def relationship_metadata(pkg:dict[str,Any])->dict[str,Any]:
    st=(pkg.get('generated_statements') or [{}])[0]; pl=st.get('structured_payload') or {}
    method_id=pl.get('method_id') or (METHOD_ID_V1 if pl.get('method_contract_fingerprint')==METHOD_CONTRACT_V1 else None)
    method_version=pl.get('method_version') or (METHOD_VERSION_V1 if method_id==METHOD_ID_V1 else None)
    limitations = pl.get('limitations') or pl.get('construction_risk') or pl.get('diagnostic_limitations') or pkg.get('limitations')
    if limitations is None:
        limitations = {
            'validation_warnings': pkg.get('validation_state', {}).get('warnings', []),
            'uncertainty_dimensions': pkg.get('confidence_quality', {}).get('uncertainty_dimensions', []),
        }
    return {'statement_type':st.get('statement_type'),'method_identifier':method_id,'method_version':method_version,'method_contract_fingerprint':pl.get('method_contract_fingerprint'),'evidence_family':pkg.get('scope',{}).get('evidence_family'),'series':[pl.get('series_a'),pl.get('series_b')],'entity':pl.get('entity_id'),'period_scope':pl.get('period_scope'),'frequency':pl.get('frequency'),'transformation_state':pl.get('transformation_state'),'coefficient':pl.get('pearson_coefficient'),'provenance':pkg.get('provenance_envelope'),'limitations':limitations,'lifecycle_state':pkg.get('confidence_quality',{}).get('lifecycle_state')}

def validate_row(row:dict[str,Any])->dict[str,Any]:
    pkg=row['package_payload']
    if sha256(pkg)!=row['package_fingerprint']: raise ExportError('package_fingerprint_validation_failed:'+row['package_id'])
    if pkg.get('fingerprints',{}).get('package_manifest')!=row['package_manifest_fingerprint']: raise ExportError('package_manifest_fingerprint_validation_failed:'+row['package_id'])
    if pkg.get('package_id')!=row['package_id']: raise ExportError('package_identity_mismatch:'+row['package_id'])
    return {'package_id':row['package_id'],'package_fingerprint':row['package_fingerprint'],'package_manifest_fingerprint':row['package_manifest_fingerprint'],'lifecycle_state':row['lifecycle_state'],'relationship_metadata':relationship_metadata(pkg),'canonical_package':pkg}

def export(query:dict[str,Any], output:Path, *, db:str=DATABASE_DEFAULT, repo:Path=REPOSITORY_ROOT, expected_repo_fp:str|None=None, simulate_stale:bool=False)->dict[str,Any]:
    qv=validate_query(query)
    if simulate_stale: expected_repo_fp='sha256:simulated-stale'
    t0=time.perf_counter(); fresh=active_freshness(db,repo,expected_repo_fp=expected_repo_fp); freshness_s=time.perf_counter()-t0
    projection_id=fresh['state']['projection_id']
    sql,shapes=build_sql(qv,projection_id)
    t=time.perf_counter(); rows=psql_json(db,sql) or []; query_s=time.perf_counter()-t
    t=time.perf_counter(); results=[validate_row(r) for r in rows]; validate_s=time.perf_counter()-t
    ids=[r['package_id'] for r in results]
    if ids!=sorted(ids): raise ExportError('unstable_order')
    deterministic={'contract':{'name':'knowledgeforge_relationship_export_v1','version':'1.0','identity':CONTRACT_ID},'query':qv,'query_fingerprint':sha256(qv),'freshness':{'repository_fingerprint':fresh['repository_fingerprint'],'repository_object_count':fresh['repository_object_count'],'projection_id':projection_id,'logical_projection_fingerprint':fresh['state']['logical_projection_fingerprint'],'projection_tool_version':fresh['state']['tool_version']},'result_count':len(results),'stable_order':'package_id_ascending','package_identities':ids,'results':results}
    deterministic['result_set_fingerprint']=sha256([{'package_id':r['package_id'],'package_fingerprint':r['package_fingerprint'],'package_manifest_fingerprint':r['package_manifest_fingerprint']} for r in results])
    export_obj={'deterministic_content':deterministic,'deterministic_content_fingerprint':sha256(deterministic),'operational_metadata':{'created_at':datetime.now(timezone.utc).isoformat(),'tool':'relationship_export_v1','performance_seconds':{'freshness_validation':round(freshness_s,6),'query_execution':round(query_s,6),'payload_validation':round(validate_s,6),'serialization':0},'query_shape':shapes,'sql_shape_evidence':'internal; table and schema details intentionally excluded from contract'}}
    t=time.perf_counter(); output.parent.mkdir(parents=True,exist_ok=True); output.write_text(json.dumps(export_obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n'); export_obj['operational_metadata']['performance_seconds']['serialization']=round(time.perf_counter()-t,6); output.write_text(json.dumps(export_obj,indent=2,sort_keys=True,ensure_ascii=False)+'\n')
    return export_obj

def verify_export(path:Path)->dict[str,Any]:
    obj=json.loads(path.read_text()); det=obj.get('deterministic_content')
    if obj.get('deterministic_content_fingerprint')!=sha256(det): raise ExportError('deterministic_content_fingerprint_mismatch')
    qv=validate_query(det['query'])
    if det.get('query_fingerprint')!=sha256(qv): raise ExportError('query_fingerprint_mismatch')
    ids=det.get('package_identities') or []
    if ids!=sorted(ids) or len(ids)!=len(set(ids)): raise ExportError('ordering_or_duplicate_identity_failure')
    if det.get('result_count')!=len(det.get('results') or []): raise ExportError('result_count_mismatch')
    for r in det.get('results') or []:
        if sha256(r['canonical_package'])!=r['package_fingerprint']: raise ExportError('package_fingerprint_mismatch:'+r.get('package_id','?'))
        if not r['relationship_metadata'].get('provenance'): raise ExportError('missing_provenance:'+r['package_id'])
        if r['relationship_metadata'].get('limitations') is None: raise ExportError('missing_limitations:'+r['package_id'])
    expected=sha256([{'package_id':r['package_id'],'package_fingerprint':r['package_fingerprint'],'package_manifest_fingerprint':r['package_manifest_fingerprint']} for r in det['results']])
    if expected!=det.get('result_set_fingerprint'): raise ExportError('result_set_fingerprint_mismatch')
    return {'valid':True,'contract':det['contract']['identity'],'result_count':det['result_count'],'query_fingerprint':det['query_fingerprint'],'result_set_fingerprint':det['result_set_fingerprint']}

def main(argv=None):
    ap=argparse.ArgumentParser()
    sub=ap.add_subparsers(dest='cmd',required=True)
    e=sub.add_parser('export'); e.add_argument('--query',required=True); e.add_argument('--output',required=True); e.add_argument('--database',default=DATABASE_DEFAULT); e.add_argument('--simulate-stale',action='store_true')
    v=sub.add_parser('verify'); v.add_argument('--export',required=True)
    args=ap.parse_args(argv)
    try:
        if args.cmd=='export':
            q=json.loads(Path(args.query).read_text()); print(json.dumps(export(q,Path(args.output),db=args.database,simulate_stale=args.simulate_stale),indent=2,sort_keys=True))
        else: print(json.dumps(verify_export(Path(args.export)),indent=2,sort_keys=True))
    except ExportError as exc:
        print(json.dumps({'valid':False,'error':str(exc)},indent=2,sort_keys=True),file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
