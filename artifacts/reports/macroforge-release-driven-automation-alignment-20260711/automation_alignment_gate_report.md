# MacroForge-Release-Driven Knowledge Automation Alignment Gate

## Status

Decision: **Proceed with a neutral, KnowledgeForge-owned release-automation boundary; do not couple to MacroForge private schema/runtime.**

Release-driven prototype implemented: **yes**. Synthetic release-v1/release-v2 prototype validates release discovery, seen-release registry, change detection, derivation/applicability registry, dependency-impact analysis, incremental recomputation planning, supersession, PostgreSQL publication planning, downstream delta export, compact AI retrieval cards, local-AI boundaries, and eventing recommendation.

No MacroForge files, InsightForge files, canonical Knowledge Objects, PostgreSQL schema, Production Doctrine, Campaign 41, commit, or push were modified.

## 1. Current automation capability audit

Audit scope: KnowledgeForge-local files and state only.

Existing local capabilities:

- correlation_batch_engine: True
- postgresql_projection_tool: True
- relationship_export_tool: True
- release_automation_tool: True

Gaps before this slice:
- no neutral evidence-release contract
- no seen-release registry
- no derivation/applicability registry
- no release-to-output impact analysis
- no incremental recomputation/supersession plan
- no downstream delta export for changed release evidence
- no eventing/scheduling recommendation tied to release detection


Boundary findings:

- Direct MacroForge dependency required: False
- MacroForge private tables required: False
- PostgreSQL schema expansion required: False
- Canonical Knowledge Object creation required: False

## 2. Independence-versus-automation decision

Adapt: automate around neutral contracts owned by KnowledgeForge, not around MacroForge private schemas or shared runtime.

Automation should consume neutral release contracts, not MacroForge internals. MacroForge compatibility means it could produce or hand off equivalent neutral release artifacts; it does not mean shared tables, shared ownership, or shared runtime code.

## 3. Neutral release-contract recommendation

Adopt a provider-neutral evidence-release contract as the boundary object for future MacroForge-compatible evidence transfer.

Contract identity: `knowledgeforge_neutral_evidence_release_contract_v1@1.0`.

The contract requires release identity, provider/dataset identity, release version, publication time, provenance, normalized evidence items, item fingerprints, and release content fingerprints. It distinguishes operational receipt time from deterministic release content.

## 4. Derivation/applicability registry

Registry identity: `knowledgeforge_derivation_applicability_registry_v1@1.0`.

Registered derivations:

- `synthetic_growth_SYN.A_DNK_annual`: family `growth_rate_candidate`, depends on series ['SYN.A'], entities ['DNK'], strategy `incremental_window_from_changed_period_minus_one`
- `synthetic_relationship_SYN.A_SYN.B_DNK_annual`: family `relationship_candidate`, depends on series ['SYN.A', 'SYN.B'], entities ['DNK'], strategy `recompute_aligned_pair_window_for_affected_series`
- `synthetic_unaffected_SYN.C_DNK_annual`: family `unaffected_control`, depends on series ['SYN.C'], entities ['DNK'], strategy `none_unless_SYN.C_changes`


## 5. Incremental recomputation and supersession model

Change detection from `synthetic-release-v1` to `synthetic-release-v2`:

- Added item IDs: ['obs:A:DNK:2022']
- Removed item IDs: []
- Changed item IDs: ['obs:A:DNK:2021']
- Unchanged item IDs: ['obs:A:DNK:2020', 'obs:B:DNK:2020']
- Change-set fingerprint: `sha256:0cf2c99e0a34e244647cd126954e838938a280f9d85f075f9d30e91ceb9bdae9`

Affected derivations:

- `synthetic_growth_SYN.A_DNK_annual` because {'changed_entities': ['DNK'], 'changed_periods': ['2021', '2022'], 'changed_series': ['SYN.A']}; recompute strategy `incremental_window_from_changed_period_minus_one`
- `synthetic_relationship_SYN.A_SYN.B_DNK_annual` because {'changed_entities': ['DNK'], 'changed_periods': ['2021', '2022'], 'changed_series': ['SYN.A']}; recompute strategy `recompute_aligned_pair_window_for_affected_series`


Unaffected derivations: ['synthetic_unaffected_SYN.C_DNK_annual'].

Affected-output fingerprint: `sha256:04d8b36e8d225213e3a5b2f75c6c66eff869aca5ac499ae85f33359f5b2cc3b1`.

Supersession: `synthetic-release-v1` is superseded by `synthetic-release-v2` by rule `newer release_version and explicit supersedes_release_id`. Canonical package mutation: False.

## 6. PostgreSQL maturation requirements

Current prototype publication plan:

- Schema expansion required: False
- Executed PostgreSQL write: False
- Publication mode: incremental_projection_refresh_plan_only

Requirements before PostgreSQL maturation:

- keep current schema for prototype
- later add incremental publication semantics only after canonical-output impact mapping exists
- measure query/update pressure before indexes/schema


## 7. Compact AI retrieval assessment

Retrieval unit: `release-impact-card`.

Frontier LLM required: False.

Local AI possible for summarization only: True.

Compact cards:

- `release_delta_SYN.A_DNK_v1_to_v2` estimate 160 tokens; keys: ['changed series SYN.A', 'changed period 2021', 'added period 2022', 'affected derivations: growth and relationship', 'unaffected: SYN.C control']


## 8. Local-AI benchmark gate

Current gate: `not required`.

Delegate to local AI when:

- summarize many release-impact-cards
- classify repetitive provider messages after deterministic extraction

Do not delegate:
- fingerprint authority
- change detection
- publication decisions
- canonical package mutation


## 9. Eventing recommendation

Recommendation: file/cron polling first; webhook/event bus only after repeated release cadence evidence.

Schedule model: bounded periodic release discovery against neutral release manifests.

Reasons:

- no network service requested
- provider-neutral prototype only
- avoid scheduler complexity before real release sources


## 10. Synthetic release-v1/release-v2 prototype

Release v1 fingerprint: `sha256:2c27969fa7e1a10f92b4aea43d2f9010f0f4ccab4c2eacac396272272332a335`.

Release v2 fingerprint: `sha256:4d9b67eebdd89915628df7697ea95738f5d172ec718b02b5354adf4c24f0b40d`.

Validation errors: {'v1': [], 'v2': []}.

Seen-release registry:

- `synthetic-release-v1`: `superseded_by_v2`, fingerprint `sha256:2c27969fa7e1a10f92b4aea43d2f9010f0f4ccab4c2eacac396272272332a335`
- `synthetic-release-v2`: `current`, fingerprint `sha256:4d9b67eebdd89915628df7697ea95738f5d172ec718b02b5354adf4c24f0b40d`


## 11. Exact change-detection and affected-output results

Added: ['obs:A:DNK:2022'].
Changed: ['obs:A:DNK:2021'].
Removed: [].
Unchanged: ['obs:A:DNK:2020', 'obs:B:DNK:2020'].
Affected derivations: ['synthetic_growth_SYN.A_DNK_annual', 'synthetic_relationship_SYN.A_SYN.B_DNK_annual'].
Unaffected derivations: ['synthetic_unaffected_SYN.C_DNK_annual'].

Downstream delta fingerprint: `sha256:2488ba01ff0b6cffeb2a027774b3a8809bf9093bf07a002caac90f81a2571ff3`.

## 12. Smallest next implementation slice

Implement file-backed seen-release registry plus release-diff CLI over one real provider-neutral fixture; still no MacroForge private access.

## Classification

- Repository inconsistency: none found.
- Governance inconsistency: active state previously pointed to Pearson production; this task updates state to the release-automation alignment decision.
- Tooling/environment issue: none blocking.
- Architecture contradiction: none. The prototype reinforces KnowledgeForge-owned contracts with provider-neutral evidence transfer.
