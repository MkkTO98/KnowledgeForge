#!/usr/bin/env python3
"""Independent consumer simulator for KnowledgeForge relationship export v1.

This intentionally does not import KnowledgeForge runtime modules, connect to
PostgreSQL, or read knowledge_repository. It receives only an export JSON file.
"""
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any
CONTRACT_ID='knowledgeforge_relationship_export_v1@1.0'
QUERY_CONTRACT_ID='knowledgeforge_relationship_query_v1@1.0'

def canonical_json(v:Any)->str: return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha256(v:Any)->str: return 'sha256:'+hashlib.sha256(canonical_json(v).encode()).hexdigest()
class ConsumerError(RuntimeError): pass

def verify(path:Path)->dict[str,Any]:
    obj=json.loads(path.read_text()); det=obj.get('deterministic_content')
    if not isinstance(det,dict): raise ConsumerError('missing_deterministic_content')
    if det.get('contract',{}).get('identity')!=CONTRACT_ID: raise ConsumerError('unsupported_contract')
    if det.get('query',{}).get('query_contract')!=QUERY_CONTRACT_ID: raise ConsumerError('unsupported_query_contract')
    if obj.get('deterministic_content_fingerprint')!=sha256(det): raise ConsumerError('deterministic_content_fingerprint_mismatch')
    if det.get('query_fingerprint')!=sha256(det.get('query')): raise ConsumerError('query_fingerprint_mismatch')
    results=det.get('results') or []; ids=det.get('package_identities') or []
    if len(results)!=det.get('result_count') or len(ids)!=len(results): raise ConsumerError('result_count_mismatch')
    if ids!=sorted(ids) or len(ids)!=len(set(ids)): raise ConsumerError('stable_order_or_duplicate_failure')
    by_series={}; by_entity={}; by_method={}; methods=set(); high_abs=[]
    fp_basis=[]
    for r in results:
        if r.get('package_id') not in ids: raise ConsumerError('package_identity_not_declared')
        pkg=r.get('canonical_package')
        if sha256(pkg)!=r.get('package_fingerprint'): raise ConsumerError('package_fingerprint_mismatch:'+r.get('package_id','?'))
        meta=r.get('relationship_metadata') or {}
        if not meta.get('provenance'): raise ConsumerError('missing_provenance:'+r['package_id'])
        if meta.get('limitations') is None: raise ConsumerError('missing_limitations:'+r['package_id'])
        fp_basis.append({'package_id':r['package_id'],'package_fingerprint':r['package_fingerprint'],'package_manifest_fingerprint':r['package_manifest_fingerprint']})
        for s in meta.get('series') or []:
            if isinstance(s,dict) and s.get('code'): by_series.setdefault(s['code'],[]).append(r['package_id'])
        if meta.get('entity'): by_entity.setdefault(meta['entity'],[]).append(r['package_id'])
        m=(meta.get('method_identifier') or 'unknown')+'@'+(meta.get('method_version') or 'unknown')
        by_method.setdefault(m,[]).append(r['package_id']); methods.add(m)
        coeff=(meta.get('coefficient') or {}).get('canonical')
        try:
            if coeff is not None and abs(float(coeff))>=0.8: high_abs.append(r['package_id'])
        except Exception: pass
    if sha256(fp_basis)!=det.get('result_set_fingerprint'): raise ConsumerError('result_set_fingerprint_mismatch')
    usefulness={'series_index':{k:sorted(v) for k,v in sorted(by_series.items())},'entity_index':{k:sorted(v) for k,v in sorted(by_entity.items())},'method_index':{k:sorted(v) for k,v in sorted(by_method.items())},'mechanical_answers':{'methods':sorted(methods),'absolute_coefficient_at_least_0_8':sorted(high_abs)}}
    return {'valid':True,'contract':CONTRACT_ID,'repository_fingerprint':det.get('freshness',{}).get('repository_fingerprint'),'result_count':det.get('result_count'),'query_fingerprint':det.get('query_fingerprint'),'result_set_fingerprint':det.get('result_set_fingerprint'),'stable_order':ids,'consumer_local_index':usefulness,'independence':{'used_postgresql':False,'imported_knowledgeforge_runtime':False,'read_canonical_repository':False,'mutated_knowledgeforge':False}}

def main(argv=None):
    ap=argparse.ArgumentParser(); ap.add_argument('--export',required=True); ap.add_argument('--output')
    args=ap.parse_args(argv)
    try:
        res=verify(Path(args.export))
        s=json.dumps(res,indent=2,sort_keys=True)
        if args.output: Path(args.output).write_text(s+'\n')
        print(s)
    except ConsumerError as e:
        print(json.dumps({'valid':False,'error':str(e)},indent=2,sort_keys=True),file=sys.stderr); return 2
if __name__=='__main__': raise SystemExit(main())
