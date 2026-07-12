#!/usr/bin/env python3
"""MacroForge-release-driven Knowledge Automation Alignment Gate prototype.

KnowledgeForge-owned, provider-neutral prototype. It does not import MacroForge,
query MacroForge private tables, write canonical Knowledge Objects, alter schema,
or publish to PostgreSQL. It models neutral release contracts and deterministic
incremental downstream effects over synthetic release-v1/release-v2 inputs.
"""
from __future__ import annotations

import argparse, copy, json, hashlib, time
from pathlib import Path
from typing import Any

CONTRACT_ID = "knowledgeforge_neutral_evidence_release_contract_v1@1.0"
SEEN_REGISTRY_ID = "knowledgeforge_seen_release_registry_v1@1.0"
DERIVATION_REGISTRY_ID = "knowledgeforge_derivation_applicability_registry_v1@1.0"
PROTOTYPE_ID = "macroforge_release_driven_knowledge_automation_alignment_gate@1.0"
ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "artifacts/reports/macroforge-release-driven-automation-alignment-20260711"
SPEC_DIR = ROOT / "specs/release_automation"


def canon(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def fp(obj: Any) -> str:
    return "sha256:" + hashlib.sha256(canon(obj).encode()).hexdigest()

def write_json(path: Path, obj: Any):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True, ensure_ascii=False) + "\n")

def load_json(path: Path) -> Any:
    return json.loads(path.read_text())

def release_contract_spec() -> dict[str, Any]:
    return {
        "contract_id": CONTRACT_ID,
        "purpose": "Provider-neutral evidence release contract for KnowledgeForge-owned release automation.",
        "authority_boundary": {
            "knowledgeforge_owns": ["release-contract semantics", "derivation applicability", "impact analysis", "recompute planning", "supersession decisions", "publication plans", "delta export semantics"],
            "external_provider_or_macroforge_may_supply": ["release metadata", "observations", "provider-native provenance", "source fingerprints"],
            "forbidden": ["MacroForge private table dependency", "shared runtime code", "consumer writes", "canonical package mutation", "PostgreSQL schema expansion"]
        },
        "required_release_fields": ["release_id", "provider_id", "dataset_id", "release_version", "published_at", "evidence_items", "provenance"],
        "required_item_fields": ["item_id", "series_code", "entity", "period", "frequency", "value", "unit", "as_of_date", "source_observation_fingerprint"],
        "fingerprints": {
            "release_content_fingerprint": "deterministic hash over release metadata excluding operational receipt time",
            "item_fingerprint": "deterministic hash over normalized evidence item",
            "change_set_fingerprint": "deterministic hash over added/removed/changed/unchanged item identities",
            "affected_output_fingerprint": "deterministic hash over affected derivations and recomputation plan"
        },
        "non_canonical_status": "Release contracts and registries are automation inputs/derived state, not canonical KnowledgeObjectPackages."
    }

def query_existing_capability_audit() -> dict[str, Any]:
    # File-backed audit only: no MacroForge access, no private DB introspection.
    files = {
        "postgresql_projection_tool": (ROOT / "tools/postgresql_operational_projection.py").exists(),
        "relationship_export_tool": (ROOT / "tools/relationship_export_v1.py").exists(),
        "correlation_batch_engine": (ROOT / "tools/correlation_batch_engine.py").exists(),
        "release_automation_tool": (ROOT / "tools/release_automation_alignment_v1.py").exists(),
    }
    return {
        "audit_scope": "KnowledgeForge-local files and state only",
        "existing_capabilities": files,
        "gaps_before_this_slice": [
            "no neutral evidence-release contract",
            "no seen-release registry",
            "no derivation/applicability registry",
            "no release-to-output impact analysis",
            "no incremental recomputation/supersession plan",
            "no downstream delta export for changed release evidence",
            "no eventing/scheduling recommendation tied to release detection"
        ],
        "boundary_findings": {
            "direct_macroforge_dependency_required": False,
            "private_macroforge_tables_required": False,
            "postgresql_schema_expansion_required_for_prototype": False,
            "canonical_knowledge_object_creation_required": False
        }
    }

def synthetic_releases() -> tuple[dict[str, Any], dict[str, Any]]:
    base = {
        "contract_id": CONTRACT_ID,
        "provider_id": "neutral_provider_synthetic",
        "dataset_id": "synthetic_macro_release_demo",
        "frequency": "annual",
        "provenance": {"source_url": "synthetic://neutral-provider/release-demo", "provider_native_release_key": "demo-release"},
    }
    items_v1 = [
        item("obs:A:DNK:2020", "SYN.A", "DNK", "2020", "10.0", "index", "2026-07-01"),
        item("obs:A:DNK:2021", "SYN.A", "DNK", "2021", "11.0", "index", "2026-07-01"),
        item("obs:B:DNK:2020", "SYN.B", "DNK", "2020", "20.0", "index", "2026-07-01"),
    ]
    items_v2 = [
        item("obs:A:DNK:2020", "SYN.A", "DNK", "2020", "10.0", "index", "2026-07-01"),
        item("obs:A:DNK:2021", "SYN.A", "DNK", "2021", "12.5", "index", "2026-07-08"),  # changed
        item("obs:A:DNK:2022", "SYN.A", "DNK", "2022", "13.0", "index", "2026-07-08"),  # added
        item("obs:B:DNK:2020", "SYN.B", "DNK", "2020", "20.0", "index", "2026-07-01"),
    ]
    v1 = {**base, "release_id": "synthetic-release-v1", "release_version": "v1", "published_at": "2026-07-01T00:00:00Z", "evidence_items": items_v1}
    v2 = {**base, "release_id": "synthetic-release-v2", "release_version": "v2", "published_at": "2026-07-08T00:00:00Z", "supersedes_release_id": "synthetic-release-v1", "evidence_items": items_v2}
    for rel in (v1, v2):
        rel["release_content_fingerprint"] = release_fingerprint(rel)
    return v1, v2

def item(item_id, series_code, entity, period, value, unit, as_of_date):
    obj = {"item_id": item_id, "series_code": series_code, "entity": entity, "period": period, "frequency": "annual", "value": value, "unit": unit, "as_of_date": as_of_date}
    obj["source_observation_fingerprint"] = fp(obj)
    return obj

def release_fingerprint(rel: dict[str, Any]) -> str:
    stable = {k:v for k,v in rel.items() if k not in {"received_at", "release_content_fingerprint"}}
    return fp(stable)

def validate_release(rel: dict[str, Any]) -> list[str]:
    errors=[]
    req=["contract_id","release_id","provider_id","dataset_id","release_version","published_at","evidence_items","provenance"]
    for k in req:
        if k not in rel: errors.append(f"missing_release_field:{k}")
    if rel.get("contract_id") != CONTRACT_ID: errors.append("unsupported_contract_id")
    seen=set()
    for it in rel.get("evidence_items",[]):
        for k in ["item_id","series_code","entity","period","frequency","value","unit","as_of_date","source_observation_fingerprint"]:
            if k not in it: errors.append(f"missing_item_field:{k}:{it.get('item_id','unknown')}")
        if it.get("item_id") in seen: errors.append(f"duplicate_item_id:{it.get('item_id')}")
        seen.add(it.get("item_id"))
    expected=release_fingerprint(rel)
    if rel.get("release_content_fingerprint") != expected: errors.append("release_fingerprint_mismatch")
    return errors

def derivation_registry() -> dict[str, Any]:
    return {
        "registry_id": DERIVATION_REGISTRY_ID,
        "derivations": [
            {
                "derivation_id": "synthetic_growth_SYN.A_DNK_annual",
                "output_family": "growth_rate_candidate",
                "depends_on": {"series_codes": ["SYN.A"], "entities": ["DNK"], "frequencies": ["annual"], "period_overlap": ["2020", "2022"]},
                "recompute_strategy": "incremental_window_from_changed_period_minus_one",
                "canonical_output_status": "not_created_in_this_task"
            },
            {
                "derivation_id": "synthetic_relationship_SYN.A_SYN.B_DNK_annual",
                "output_family": "relationship_candidate",
                "depends_on": {"series_codes": ["SYN.A", "SYN.B"], "entities": ["DNK"], "frequencies": ["annual"], "period_overlap": ["2020", "2022"]},
                "recompute_strategy": "recompute_aligned_pair_window_for_affected_series",
                "canonical_output_status": "not_created_in_this_task"
            },
            {
                "derivation_id": "synthetic_unaffected_SYN.C_DNK_annual",
                "output_family": "unaffected_control",
                "depends_on": {"series_codes": ["SYN.C"], "entities": ["DNK"], "frequencies": ["annual"], "period_overlap": ["2020", "2022"]},
                "recompute_strategy": "none_unless_SYN.C_changes",
                "canonical_output_status": "not_created_in_this_task"
            }
        ]
    }

def item_map(rel):
    return {it["item_id"]: it for it in rel["evidence_items"]}

def detect_changes(old, new) -> dict[str, Any]:
    a,b=item_map(old),item_map(new)
    added=sorted(set(b)-set(a)); removed=sorted(set(a)-set(b)); common=sorted(set(a)&set(b))
    changed=[i for i in common if a[i]["source_observation_fingerprint"] != b[i]["source_observation_fingerprint"]]
    unchanged=[i for i in common if i not in changed]
    result={"from_release_id":old["release_id"],"to_release_id":new["release_id"],"added_item_ids":added,"removed_item_ids":removed,"changed_item_ids":changed,"unchanged_item_ids":unchanged}
    result["change_set_fingerprint"] = fp(result)
    return result

def affected_derivations(change, new_rel, registry):
    changed_items = [it for it in new_rel["evidence_items"] if it["item_id"] in set(change["added_item_ids"]+change["changed_item_ids"])]
    changed_series={it["series_code"] for it in changed_items}; changed_entities={it["entity"] for it in changed_items}; changed_periods={it["period"] for it in changed_items}
    affected=[]
    for d in registry["derivations"]:
        dep=d["depends_on"]
        if changed_series.intersection(dep["series_codes"]) and changed_entities.intersection(dep["entities"]):
            affected.append({"derivation_id":d["derivation_id"],"reason":{"changed_series":sorted(changed_series.intersection(dep["series_codes"])),"changed_entities":sorted(changed_entities.intersection(dep["entities"])),"changed_periods":sorted(changed_periods)},"recompute_strategy":d["recompute_strategy"],"output_family":d["output_family"]})
    plan={"affected_derivations":affected,"unaffected_derivation_ids":[d["derivation_id"] for d in registry["derivations"] if d["derivation_id"] not in {a["derivation_id"] for a in affected}],"minimal_recompute": True}
    plan["affected_output_fingerprint"] = fp(plan)
    return plan

def build_run() -> dict[str, Any]:
    v1,v2=synthetic_releases(); reg=derivation_registry()
    errors={"v1":validate_release(v1),"v2":validate_release(v2)}
    change=detect_changes(v1,v2); impact=affected_derivations(change,v2,reg)
    seen={"registry_id":SEEN_REGISTRY_ID,"seen_releases":[{"release_id":v1["release_id"],"fingerprint":v1["release_content_fingerprint"],"status":"superseded_by_v2"},{"release_id":v2["release_id"],"fingerprint":v2["release_content_fingerprint"],"status":"current"}]}
    supersession={"superseded_release_id":v1["release_id"],"superseding_release_id":v2["release_id"],"rule":"newer release_version and explicit supersedes_release_id","canonical_package_mutation":False}
    pg_plan={"schema_expansion_required":False,"publication_mode":"incremental_projection_refresh_plan_only","affected_projection_rows":"derived from affected package/output identities when canonical outputs exist","executed_postgresql_write":False}
    delta={"delta_contract_id":"knowledgeforge_downstream_release_delta_v1@1.0","from_release_id":v1["release_id"],"to_release_id":v2["release_id"],"change_set":change,"affected_derivations":impact["affected_derivations"],"delta_fingerprint":fp({"change":change,"affected":impact["affected_derivations"]})}
    compact={"retrieval_unit":"release-impact-card","cards":[{"id":"release_delta_SYN.A_DNK_v1_to_v2","tokens_estimate":160,"content_keys":["changed series SYN.A","changed period 2021","added period 2022","affected derivations: growth and relationship","unaffected: SYN.C control"]}],"frontier_llm_required":False,"local_ai_possible_for_summarization_only":True}
    local_ai_gate={"current_gate":"not required","delegate_to_local_ai_when":["summarize many release-impact-cards", "classify repetitive provider messages after deterministic extraction"],"do_not_delegate":["fingerprint authority","change detection","publication decisions","canonical package mutation"]}
    eventing={"recommendation":"file/cron polling first; webhook/event bus only after repeated release cadence evidence","schedule":"bounded periodic release discovery against neutral release manifests","reasons":["no network service requested","provider-neutral prototype only","avoid scheduler complexity before real release sources"]}
    decisions={
        "independence_vs_automation":"Adapt: automate around neutral contracts owned by KnowledgeForge, not around MacroForge private schemas or shared runtime.",
        "neutral_release_contract_recommendation":"Adopt a provider-neutral evidence-release contract as the boundary object for future MacroForge-compatible evidence transfer.",
        "postgresql_maturation_requirements":["keep current schema for prototype","later add incremental publication semantics only after canonical-output impact mapping exists","measure query/update pressure before indexes/schema"],
        "smallest_next_slice":"Implement file-backed seen-release registry plus release-diff CLI over one real provider-neutral fixture; still no MacroForge private access."
    }
    return {"prototype_id":PROTOTYPE_ID,"release_contract":release_contract_spec(),"automation_capability_audit":query_existing_capability_audit(),"release_v1":v1,"release_v2":v2,"validation_errors":errors,"seen_release_registry":seen,"derivation_applicability_registry":reg,"change_detection":change,"dependency_impact_analysis":impact,"incremental_recomputation_model":{"minimal_recompute":impact["affected_derivations"],"full_recompute_required":False},"supersession_model":supersession,"incremental_postgresql_publication":pg_plan,"downstream_delta_export":delta,"compact_ai_retrieval_assessment":compact,"local_ai_benchmark_gate":local_ai_gate,"eventing_recommendation":eventing,"decisions":decisions}

def main(argv=None):
    ap=argparse.ArgumentParser()
    ap.add_argument("command", choices=["write-specs","run-prototype","verify"])
    ap.add_argument("--output", default=str(REPORT_DIR/"prototype_result.json"))
    args=ap.parse_args(argv)
    if args.command == "write-specs":
        write_json(SPEC_DIR/"neutral_evidence_release_contract_v1.json", release_contract_spec())
        write_json(SPEC_DIR/"derivation_applicability_registry_v1.schema.json", {"registry_id":DERIVATION_REGISTRY_ID,"required_derivation_fields":["derivation_id","output_family","depends_on","recompute_strategy"]})
        print(json.dumps({"wrote":[str(SPEC_DIR/"neutral_evidence_release_contract_v1.json"),str(SPEC_DIR/"derivation_applicability_registry_v1.schema.json")]}))
        return 0
    if args.command == "run-prototype":
        result=build_run(); write_json(Path(args.output), result); print(json.dumps({"output":args.output,"change_set_fingerprint":result["change_detection"]["change_set_fingerprint"],"affected":len(result["dependency_impact_analysis"]["affected_derivations"])})); return 0
    result=load_json(Path(args.output))
    errors=[]
    if result["validation_errors"] != {"v1":[],"v2":[]}: errors.append("release_validation_errors")
    ch=result["change_detection"]
    if ch["added_item_ids"] != ["obs:A:DNK:2022"]: errors.append("unexpected_added")
    if ch["changed_item_ids"] != ["obs:A:DNK:2021"]: errors.append("unexpected_changed")
    aff=[a["derivation_id"] for a in result["dependency_impact_analysis"]["affected_derivations"]]
    if aff != ["synthetic_growth_SYN.A_DNK_annual", "synthetic_relationship_SYN.A_SYN.B_DNK_annual"]: errors.append("unexpected_affected_derivations")
    if result["incremental_postgresql_publication"]["executed_postgresql_write"]: errors.append("postgresql_write_executed")
    ok=not errors
    print(json.dumps({"valid":ok,"errors":errors,"change_set_fingerprint":ch["change_set_fingerprint"],"affected_output_fingerprint":result["dependency_impact_analysis"]["affected_output_fingerprint"]}, indent=2, sort_keys=True))
    return 0 if ok else 2

if __name__ == "__main__":
    raise SystemExit(main())
