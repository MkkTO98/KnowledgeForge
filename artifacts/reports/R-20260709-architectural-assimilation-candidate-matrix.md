# KnowledgeForge Architectural Assimilation Candidate Matrix

Date: 2026-07-09
Status: completed
Classification values: Adopt, Adapt, Reject, Defer

| ID | Candidate improvement | Source evidence | Classification | KnowledgeForge-local interpretation | Justification |
|---|---|---|---|---|---|
| C01 | Project-specific constitution matching actual project purpose | ProjectForge Project Identity; KnowledgeForge root inconsistency | Adopt | Replace generic ProjectForge constitution with KnowledgeForge constitution | A wrong constitution creates authority drift. This is foundational and immediately correctable as documentation. |
| C02 | Five-system operating model | ProjectForge v2 | Adapt | Use as review lens, not as KnowledgeForge architecture | Helps ensure identity/context/governance/work/validation coverage, but KnowledgeForge's domain model remains knowledge objects. |
| C03 | Summary-first context and concise current-state pointers | ProjectForge Context and Continuity | Adopt | Keep state/handoff concise; expand by summaries and task artifacts | Reduces token use and improves recovery without changing knowledge architecture. |
| C04 | Context audit before cloud/frontier escalation | ProjectForge context policy | Adopt | Require explicit evidence/context bundle before frontier LLM architecture reviews | Directly reduces frontier use and improves auditability. |
| C05 | Standard closeout discipline | ProjectForge continuity | Adopt | Task/status/state/handoff/summary/verification closeout | Proven durable recovery mechanism. |
| C06 | Architecture-to-reality audit cadence | ProjectForge Validation/Evidence | Adopt | Run before major KnowledgeForge architecture changes and every 5-10 tasks | Prevents docs/fixture/validator drift. |
| C07 | Validator finding classification | ProjectForge check_coherence classifications | Adapt | Classify as constitutional, knowledge-model, repository, governance, tooling/environment, compatibility | KnowledgeForge needs semantically meaningful failure classes. |
| C08 | Framework canonization workflow | ProjectForge canonization doctrine | Adapt | Use before adding reusable KnowledgeForge subsystems | Prevents premature abstraction and framework accumulation. |
| C09 | Terminology governance registry | ProjectForge terminology governance | Adapt | Govern KnowledgeForge terms, facets, lifecycle states, evidence states, confidence labels | High fit because KnowledgeForge is semantics-heavy; must not become universal ontology. |
| C10 | Automation doctrine | ProjectForge automation doctrine | Adopt | Automate only if reliable, understandable, testable, observable, reversible | Protects maintainability. |
| C11 | Source-specific-before-boundary pattern | MacroForge ingestion architecture | Adapt | Evidence-family-specific extraction before common knowledge-candidate package boundary | Avoids generic extraction framework too early. |
| C12 | Portable boundary package | MacroForge ObservedIngestionPackage | Adapt | Future `KnowledgeObjectPackage` / `KnowledgeChangePackage` concept | Enables fingerprints, deterministic validation, reproducibility; implementation deferred. |
| C13 | Package fingerprinting and comparison | MacroForge deterministic substrate | Adapt | Fingerprint knowledge packages/objects/revisions | Strong reproducibility/auditability value. |
| C14 | Idempotent rerun validation | MacroForge WDI campaigns | Adapt | Rebuilding same knowledge package from same evidence should produce same canonical object/fingerprint or explicit diff | Critical for reproducible knowledge generation. |
| C15 | Run-scoped validation | MacroForge TASK-176/178 lesson | Adapt | Validate only touched knowledge packages and affected dependencies, plus global invariants | Avoids broad expensive checks while maintaining safety. |
| C16 | Staging/curated/meta PostgreSQL separation | MacroForge PostgreSQL architecture | Defer | Use as storage design evidence only | Useful if/when relational store is selected; premature now. |
| C17 | PostgreSQL as default knowledge store | MacroForge canonical DB success | Reject | Do not choose storage from MacroForge by analogy | KnowledgeForge needs provenance/versioning/graph/document considerations; storage decision remains open. |
| C18 | Canonical lineage events | MacroForge lineage | Adapt | Create knowledge-change lineage/audit records for accepted object changes | Aligns with existing knowledge-change concept. |
| C19 | Contract validation and drift detection | MacroForge substrate | Adapt | Validate evidence-reference contracts, object schemas, vocabulary contracts, consumer interface contracts | High value for reproducibility and maintainability. |
| C20 | Deterministic feedback reports | MacroForge deterministic ingestion feedback | Adapt | Generate deterministic knowledge-generation feedback reports | Helps improve pipelines without relying on chat memory. |
| C21 | Capability maturity lifecycle | MacroForge maturity | Adapt | Track maturity of object types, evidence families, generation pipelines, and consumer contracts | Useful if evidence-backed and not opaque scoring. |
| C22 | DRDF / ACPF / CEF planning stack | MacroForge planning architecture | Adapt | Use analogous domain/capability/confidence-cell planning before knowledge-generation campaigns | Prevents blind knowledge generation. |
| C23 | Evidence-only slices | MacroForge evidence-only posture | Adopt | Allow evidence/evaluation/design slices that do not authorize architecture expansion | Prevents implementation drift. |
| C24 | Treat unavailable source indicators as exclusion evidence | MacroForge TASK-178 lesson | Adapt | Treat missing/invalid evidence as explicit negative evidence or deferred candidate, not as reason for new system | Supports scientific discipline. |
| C25 | Knowledge/evidence separation | MetaHarvest evidence-source architecture | Adopt | Knowledge objects are canonical; evidence sources support them | Direct fit with KnowledgeForge constitution. |
| C26 | Evidence-source taxonomy | MetaHarvest methodology | Adapt | Define KnowledgeForge-specific source types: MacroForge handle, source docs, literature, method spec, institutional publication, reviewed curation, etc. | Improves provenance and deterministic routing. |
| C27 | Snapshots over continuous mirrors | MetaHarvest repository doctrine | Adopt | Prefer immutable evidence references/snapshots over live freshness | Strong reproducibility; avoids infrastructure. |
| C28 | Optional materialization | MetaHarvest evidence architecture | Adopt | Do not require local caches for normal consultation if extracted knowledge and provenance exist | Reduces storage/maintenance burden. |
| C29 | Source lifecycle by architectural usefulness | MetaHarvest lifecycle | Adapt | Evidence/reference lifecycle by knowledge usefulness and reproducibility, not source activity | Fits KnowledgeForge but needs domain-specific states. |
| C30 | Prediction-before-analysis research cycle | MetaHarvest scientific cycle | Adapt | Candidate-before-evaluation cycle: expected claim/evidence posture before final object acceptance | Encourages falsification and reduces LLM confirmation bias. |
| C31 | Knowledge evolution report as completion point | MetaHarvest methodology | Adapt | Accepted knowledge changes require an evolution/change report | Aligns with KnowledgeForge knowledge-change concept. |
| C32 | Component cards as evidence-to-knowledge bridge | MetaHarvest cards | Adapt | Use compact object/evidence/evaluation cards for intermediate knowledge units | Useful for local retrieval and local-model inputs. |
| C33 | Primitives/patterns/invariants only after repeated evidence | MetaHarvest synthesis | Adopt | Do not promote reusable abstractions after one slice | Prevents premature ontology/framework growth. |
| C34 | Contradiction records | MetaHarvest contradictions | Adopt | Contradictions should be first-class knowledge/evidence-evaluation artifacts | Already aligned with invariants; needs artifact contract. |
| C35 | Problem-first retrieval | MetaHarvest retrieval | Adapt | Question/claim-first retrieval for reusable knowledge | Improves usability without runtime database initially. |
| C36 | Change discovery index | MetaHarvest change_discovery | Adapt | Lightweight index of KnowledgeForge-relevant knowledge/model changes | Helps future agents discover what changed without reading all reports. |
| C37 | Advisory-only consumer boundary | MetaHarvest doctrine | Adopt | Downstream systems consume/cite KnowledgeForge but do not mutate or validate it by use alone | Already in invariants; reinforce. |
| C38 | Runtime graph/vector/dashboard infrastructure | MetaHarvest rejected systems; ProjectForge/MacroForge restraint | Reject | No graph DB, vector store, dashboard, UI, service, or scheduler before file-backed approach fails | Would increase complexity and frontier usage pressure prematurely. |
| C39 | External architecture harvesting inside KnowledgeForge | MetaHarvest purpose | Reject | KnowledgeForge should not become MetaHarvest | Violates KnowledgeForge's domain reusable-knowledge boundary. |
| C40 | Automated knowledge generation daemon | MetaHarvest negative rules; ProjectForge automation doctrine | Reject | No autonomous generation without explicit task/gates | High risk to provenance, quality, and boundaries. |
| C41 | Local-model extraction with validated outputs | ProjectForge local-first; MetaHarvest evidence packets | Defer | Pilot only after deterministic package/evidence contracts exist | Promising but needs templates, validators, and acceptance gates first. |
| C42 | PostgreSQL interaction patterns for future empirical claims | MacroForge DB patterns | Defer | Revisit after evidence-reference contract and storage criteria are accepted | Useful but premature. |
| C43 | Reusable prompt/template library | ProjectForge/MetaHarvest repeatable workflows | Adapt | Templates for evidence evaluation, claim extraction, contradiction checks, lifecycle proposals | Can reduce frontier usage and improve reproducibility if outputs are validated. |
| C44 | Maturity/confidence numeric scoring | MetaHarvest pattern maturity; MacroForge confidence | Defer | Use explainable labels first; numbers only where evidence supports them | Avoid false precision. |
| C45 | Repository cleanup/removal of obsolete compatibility surfaces | MacroForge cleanup; ProjectForge sovereignty redesign | Adapt | Remove only obsolete KnowledgeForge placeholders after separate review | Current architecture/metaharvest surfaces are useful; no cleanup now. |
