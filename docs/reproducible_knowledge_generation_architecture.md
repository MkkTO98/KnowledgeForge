# Reproducible Knowledge-Generation Architecture Specification

Date: 2026-07-09
Status: architecture specification; implementation not authorized
Scope: KnowledgeForge assimilation consolidation after the 2026-07-09 Architectural Assimilation Campaign

## 1. Purpose

This specification converts the assimilation campaign into KnowledgeForge-local architecture contracts for reproducible knowledge generation.

KnowledgeForge must become a reproducible knowledge-generation engine, not an insight engine. It may transform explicit evidence references, deterministic computations, evidence evaluations, and governed templates into candidate or durable reusable knowledge objects. It must not own source observations, perform interpretation, generate investment or macro insight, forecast, recommend, or operate as an autonomous daemon.

## 2. Architectural posture

KnowledgeForge is downstream of evidence systems and upstream of interpretation systems:

```text
External evidence sources
  -> evidence references, metadata, lineage, reproducibility handles
KnowledgeForge
  -> reusable knowledge objects, evidence evaluations, candidate packages, validation state, provenance, contradiction records
Downstream consumers
  -> interpretation, meaning, synthesis, narrative, reports, decisions
```

KnowledgeForge's own generation boundary is governed by four rules:

1. Every generated statement must be traceable to explicit evidence, computation, template, or preserved source assertion.
2. Every generated package must be reproducible or explicitly marked non-reproducible and blocked from acceptance.
3. Model output is candidate material only until evidence, provenance, boundary, and validator gates pass.
4. Statistical or derived characterization may state method-scoped reusable facts; it may not state implications, causality, investment meaning, or narrative interpretation unless those are preserved as external source claims with provenance and scope.

## 3. Reproducible knowledge-generation boundary

### 3.1 Allowed outputs

KnowledgeForge may generate or preserve the following, subject to package and validation contracts:

| Output type | Allowed? | Boundary |
| --- | --- | --- |
| Factual knowledge | Yes | A source-backed, provenance-bearing statement about definitions, identities, metadata, methods, or observed facts already present in evidence. |
| Derived knowledge | Yes | Deterministically derived from referenced evidence and explicit computation recipes. Derivation must be replayable. |
| Statistical characterization | Yes | Method-scoped descriptive or associative result with data window, method, parameters, uncertainty/missingness, and limitations. No causal or investment meaning. |
| Classification | Yes | Governed vocabulary assignment supported by evidence or deterministic rules. Uncertain classifications remain candidate. |
| Candidate knowledge | Yes | Unaccepted proposed knowledge package awaiting validation/review. Must not be served as accepted knowledge. |
| Evidence evaluation | Yes | Assessment of how evidence supports, weakens, contradicts, or bounds reusable knowledge. Must stop before interpretation. |
| Negative knowledge | Yes | Missing, unsupported, contradicted, or not-observed finding only when evidence scope and method are explicit. |
| Methodological knowledge | Yes | Reusable method assumptions, limitations, comparability rules, and applicability constraints. Must not duplicate external observational execution metadata unnecessarily. |

### 3.2 Disallowed outputs

KnowledgeForge must not generate:

| Output type | Status | Reason |
| --- | --- | --- |
| Interpretation | Forbidden | Belongs to downstream reasoning systems. KnowledgeForge records evidence and scoped reusable statements, not meaning. |
| Hypothesis generation | Forbidden | Belongs to downstream reasoning/research workflows. KnowledgeForge may preserve externally sourced hypotheses as claims. |
| Insight | Forbidden | Insight is synthesis/implication, not reusable knowledge substrate. |
| Forecast | Forbidden | Belongs to PredictionForge. |
| Recommendation/action | Forbidden | Belongs to DecisionForge. |
| Presentation/report narrative | Forbidden | Belongs to presentation or consumer systems. |
| Observational data ownership | Forbidden | Belongs to external observational systems. KnowledgeForge references, evaluates, or characterizes evidence; it does not become an observational database. |

### 3.3 Boundary tests

A proposed statement is probably inside KnowledgeForge if it can answer all of these with concrete references:

- What evidence or computation produced it?
- What exact source scope, method scope, and applicability scope bound it?
- Can it be regenerated or audited without asking a frontier LLM to rediscover it?
- Does it avoid saying what the finding means for macro conditions, investment decisions, forecasts, or actions?

A proposed statement is probably downstream interpretation territory if it uses language such as "therefore investors should", "this implies", "the economy is likely", "the key takeaway", "regime signal", "risk-on/risk-off", "policy implication", or similar interpretation language not quoted as an external source claim.

## 4. Generation pipeline stages

The architecture recognizes these stages without implementing runtime orchestration:

1. Evidence selection: choose explicit evidence references or snapshots.
2. Evidence classification: assign evidence-source type and source family.
3. Evidence evaluation: evaluate validity, freshness, lineage, reproducibility, missingness, contradictions, and auditability.
4. Candidate generation: deterministic computation, template fill, local-model extraction, or justified frontier-LLM assistance may produce candidate statements.
5. Package assembly: candidate statements and metadata are wrapped in a Knowledge Package.
6. Deterministic validation: validators classify blockers and warnings.
7. Human/governance review: acceptance, deferral, questioning, or rejection is recorded separately from confidence.
8. Evolution reporting: any accepted or revised package records why knowledge changed.

## 5. Maturity states

Generation capability maturity is separate from knowledge-object lifecycle.

| Maturity | Meaning |
| --- | --- |
| M0 Specified | Architecture contract exists; no production generation. |
| M1 Fixture-backed | One or more manually curated fixture packages validate the contract. |
| M2 Deterministic replay | Package can be regenerated from frozen evidence and recipes. |
| M3 Local-assisted candidate generation | Local model may generate candidate text inside templates; deterministic validators remain authoritative. |
| M4 Frontier-assisted candidate generation | Frontier LLM may be used only with explicit justification, logged context, retained outputs, and review gates. |
| M5 Production governed | Repeated packages, validators, change reports, and audit evidence support controlled production use. |

KnowledgeForge is currently M0 for reproducible knowledge generation beyond Vertical Slice 0. The next work should move to M1/M2 through validators and fixture-backed package contracts, not production knowledge generation.

## 6. Storage and infrastructure posture

This specification does not require any specific database, vector search, graph databases, schedulers, daemons, dashboards, APIs, or UI infrastructure. File-backed packages and deterministic validators remain sufficient until package contracts and validation gates show concrete scaling pressure.

Database interaction is a future input-capability question: KnowledgeForge may eventually reference exported source evidence or query an approved evidence source, but it must first define source evidence handles, selection/query fingerprints, and package contracts. It must not create a KnowledgeForge database schema merely because an evidence source uses a database.

## 7. Authoritative companion specifications

- `docs/evidence_source_evaluation_specification.md`
- `docs/knowledge_package_contract.md`
- `docs/validator_taxonomy.md`
- `docs/provenance_fingerprinting.md`
- `docs/model_routing_policy.md`
- `docs/knowledge_evolution_change_report_contract.md`
