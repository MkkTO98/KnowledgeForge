# Report: KnowledgeForge Architectural Review — Phase I

Date: 2026-06-29
Status: Review completed; recommendations not yet adopted
Scope: Core philosophy, project boundaries, knowledge classes, architectural invariants, long-term conceptual maintainability
Implementation status: No implementation introduced

## Executive judgment

The current KnowledgeForge specification is directionally strong and worth preserving, but it is not yet implementation-ready. Its strongest idea is the separation of observations, reusable knowledge, interpretation, navigation, presentation, prediction, and decision. Its weakest area is taxonomy: the current six knowledge classes mix content classes, applicability metadata, epistemic metadata, and lifecycle metadata as if they were peers.

The most important refinement is not a redesign. It is to make the architecture more explicit about axes:

1. What the object is about: semantic, structural, empirical, methodological, domain/entity/event.
2. Where and when it applies: contextual/applicability conditions.
3. Why it is believed: epistemic/evidence/provenance state.
4. How it evolves: lifecycle/revision state.

This preserves the current intent while reducing future conceptual confusion at scale.

## 1. Architectural strengths

### S1. Clear high-level identity

KnowledgeForge answers "What is known?" This is a good architectural identity because it is distinct from:

- MacroForge: "What happened?"
- InsightForge: "What does this mean?"
- AtlasForge: navigation
- BriefForge: presentation
- PredictionForge: "What is likely to happen?"
- DecisionForge: "What should be done?"

Rationale: the question-based boundary is simple enough for future agents to apply repeatedly.

### S2. Strong observation/knowledge separation

The specification repeatedly states that MacroForge owns observations and KnowledgeForge owns reusable knowledge. This is the most important boundary in the architecture.

Rationale: without this separation, KnowledgeForge would drift into a second data platform and duplicate MacroForge.

### S3. Provenance and uncertainty are treated as first-class concerns

The current design explicitly requires provenance, uncertainty, competing explanations, confidence, evidence, revision history, and lifecycle state.

Rationale: this prevents KnowledgeForge from becoming a brittle ontology or truth database.

### S4. Relationship objects are correctly elevated

Treating relationships as first-class versioned entities is architecturally correct.

Rationale: most long-term value will be in typed, evidence-backed, context-conditioned relationships, not only isolated concepts.

### S5. Specification-only phase is correct

Deferring runtime infrastructure, graph engines, databases, APIs, and statistical systems is the right decision.

Rationale: premature implementation would freeze an immature knowledge model and create cross-project coupling before ownership boundaries stabilize.

## 2. Architectural weaknesses

### W1. The phrase "canonical knowledge substrate" is useful but dangerous

Weakness: "canonical" can imply truth authority. The spec says KnowledgeForge does not determine truth, but the word canonical may lead future agents to treat accepted KnowledgeForge objects as settled facts.

Recommendation: retain "canonical substrate" only if paired with a stronger invariant: canonical means canonical identity and stewardship, not canonical truth.

Rationale: KnowledgeForge should own durable identifiers and knowledge records, not epistemic finality.

### W2. Knowledge classes are not orthogonal

Weakness: semantic, structural, and empirical knowledge are content classes. Contextual knowledge is applicability metadata. Epistemic knowledge is justification metadata. Evolutionary knowledge is lifecycle metadata. Treating all six as peer classes will create classification ambiguity.

Recommendation: recast them as separate architectural axes rather than a flat taxonomy.

Rationale: a single empirical relationship may also have semantic definitions, contextual applicability, epistemic evidence, and evolutionary lifecycle state. It should not be forced into only one class.

### W3. Structural knowledge risks overlapping with InsightForge

Weakness: "curated economic theory," "causal relationships," and "domain models" could become reasoning, interpretation, or hypothesis management.

Recommendation: narrow structural knowledge to reusable, cited, externally justified structure records. KnowledgeForge may preserve a theory or structural claim as an object, but InsightForge owns applying it to interpret current conditions.

Rationale: this keeps KnowledgeForge from becoming the reasoning layer.

### W4. Empirical knowledge risks overlapping with MacroForge, InsightForge, and PredictionForge

Weakness: statistical discovery touches observations, analysis, and prediction-adjacent lead-lag relationships.

Recommendation: define empirical knowledge as method-scoped reusable relationship records derived from referenced evidence. It must not own source data, analytical interpretation, predictive model objectives, forecasts, or action implications.

Rationale: this permits reusable statistical knowledge without letting KnowledgeForge become a data platform, analyst, or forecaster.

### W5. Cross-domain ambition is under-governed

Weakness: "eventually any reusable knowledge domain" is directionally useful but could turn KnowledgeForge into a universal ontology project.

Recommendation: add a domain-expansion invariant: new domains may be added only when they reuse the core knowledge-object model and do not require KnowledgeForge to own observations, reasoning, prediction, recommendation, presentation, or domain-specific operations.

Rationale: this preserves extensibility without scope creep.

## 3. Hidden assumptions

### H1. Knowledge can be separated from interpretation cleanly

This is only partly true. Some knowledge objects, especially causal structures and economic theory, embed interpretation.

Recommendation: distinguish "preserved interpretation from cited sources" from "active interpretation performed by EIP agents." KnowledgeForge may preserve the former; InsightForge owns the latter.

Rationale: academic literature and theory are not raw facts, but they are reusable knowledge records if provenance and contestability are preserved.

### H2. Evidence references from MacroForge will remain stable

The architecture assumes KnowledgeForge can reference MacroForge evidence without duplication.

Recommendation: treat evidence-reference stability as a required architectural contract before implementation.

Rationale: if MacroForge identifiers, releases, or lineage handles drift, KnowledgeForge provenance becomes non-reproducible.

### H3. Statistical relationships can be reusable without becoming conclusions

This is true only if method scope, evidence scope, parameterization, and limitations are explicit.

Recommendation: every empirical relationship should be method-qualified, parameter-qualified, evidence-qualified, and context-qualified.

Rationale: otherwise downstream users will overread statistical artifacts as general truths.

### H4. "Accepted" lifecycle state will not be mistaken for true

The lifecycle vocabulary includes Accepted. This can be misread as truth.

Recommendation: define Accepted as "accepted for reuse under stated evidence and validity conditions," not "proven true."

Rationale: this aligns lifecycle with the non-truth-oracle principle.

### H5. Downstream consumers will respect boundaries

The architecture assumes InsightForge, AtlasForge, PredictionForge, and DecisionForge will consume without duplicating.

Recommendation: make boundary-preserving consumer contracts a precondition for integration.

Rationale: project boundaries fail most often at integration points.

## 4. Boundary violations or near-violations

### B1. Curated economic theory / domain models

Potential violation: could belong to InsightForge if the project starts generating or choosing interpretations.

Refinement: KnowledgeForge may store theory records, structural claims, and domain model descriptions only as reusable, provenance-bearing knowledge objects. InsightForge owns using them to explain present conditions or generate hypotheses.

### B2. Supply chains

Potential violation: live supply-chain state could become observational data or company/industry operations data.

Refinement: KnowledgeForge may own durable supply-chain relationship knowledge. It must not own live shipments, production volumes, current disruptions, transactional data, or observational feeds.

### B3. Statistical discovery

Potential violation: statistical computation may duplicate MacroForge transformations or InsightForge analysis.

Refinement: KnowledgeForge owns only reusable relationship records, with evidence references and method metadata. MacroForge owns observational values and reproducibility. InsightForge owns interpretation. PredictionForge owns predictive use.

### B4. "Serves downstream projects"

Potential violation: could be read as API/runtime ownership now.

Refinement: during specification-only phase, "serves" means defines future interface contracts. Runtime serving is deferred.

### B5. BriefForge interface

Potential violation: direct KnowledgeForge citations in downstream presentation could tempt BriefForge to consume KnowledgeForge directly.

Refinement: BriefForge may cite KnowledgeForge identifiers only through presentation context generated by InsightForge or future approved consumers. KnowledgeForge does not produce presentation-ready content.

## 5. Missing architectural principles

### P1. Canonical identity is not canonical truth

Principle: KnowledgeForge canonicalizes identifiers, mappings, and stewardship records; it does not canonicalize truth.

Rationale: prevents future agents from collapsing uncertainty into authority.

### P2. Knowledge objects are multi-axis, not single-class

Principle: content type, applicability, evidence state, lifecycle state, and provenance are separate dimensions.

Rationale: avoids forced classification and improves conceptual scaling.

### P3. All knowledge is scoped

Principle: every knowledge object has explicit scope: domain, geography, time, regime, method, source, and validity conditions where applicable.

Rationale: unscoped knowledge becomes misleading at scale.

### P4. Preservation beats resolution

Principle: contradictions, competing explanations, and weakening evidence must be preserved rather than prematurely resolved.

Rationale: KnowledgeForge is not a truth arbiter.

### P5. Downstream use is not evidence

Principle: the fact that InsightForge, PredictionForge, DecisionForge, or a human used a knowledge object does not by itself strengthen that object's confidence.

Rationale: prevents popularity or repeated use from becoming circular evidence.

### P6. Domain expansion must reuse the core model

Principle: new domains may extend vocabulary, but not the fundamental ownership model.

Rationale: prevents KnowledgeForge from becoming a pile of domain-specific exceptions.

## 6. Missing invariants

The specification should explicitly define invariants. Recommended invariants:

1. Every knowledge object must have provenance.
   Rationale: without provenance, the object cannot be trusted, reviewed, or deprecated.

2. Every relationship must have evidence or be marked as unsupported/candidate.
   Rationale: prevents ungrounded edges from polluting the knowledge substrate.

3. Observational datasets are never owned or duplicated by KnowledgeForge.
   Rationale: preserves MacroForge's system-of-record role.

4. Empirical knowledge cannot overwrite semantic or structural knowledge.
   Rationale: statistical association cannot redefine concepts or theory by itself.

5. Structural knowledge cannot overwrite empirical contradictions.
   Rationale: theory should not erase contrary evidence.

6. Mappings must be typed and reversible.
   Rationale: users must be able to recover source identity and mapping assumptions.

7. Derived and proxy mappings must declare transformation/lossiness.
   Rationale: prevents weak equivalence from masquerading as exact equivalence.

8. Contradictions are preserved as first-class knowledge state.
   Rationale: KnowledgeForge preserves epistemic structure, not clean narratives.

9. Lifecycle transitions are append-only and auditable.
   Rationale: knowledge evolution must be reconstructable.

10. Accepted does not mean true.
    Rationale: accepted means reusable under stated evidence and validity conditions.

11. Empirical relationships are method- and parameter-scoped.
    Rationale: correlation windows, frequencies, lags, transformations, and samples change meaning.

12. Association is not causation unless a separate causal/structural claim is justified.
    Rationale: prevents PredictionForge/InsightForge leakage.

13. A downstream consumer cannot silently mutate KnowledgeForge state.
    Rationale: preserves project autonomy.

14. Knowledge objects must remain addressable after deprecation.
    Rationale: downstream citations and historical reports need stable references.

15. Absence of evidence is not encoded as evidence of absence unless explicitly justified.
    Rationale: prevents false negative knowledge.

16. Context validity is explicit, not implicit.
    Rationale: regime/geography/time applicability must be inspectable.

17. Confidence must be attached to a claim under scope, not to a concept globally.
    Rationale: a concept can be well-defined while a relationship involving it is uncertain.

18. Future domain expansion cannot bypass core invariants.
    Rationale: scale should not weaken architecture.

## 7. Missing concepts

### C1. Claim

Recommendation: introduce "claim" as a conceptual primitive distinct from concept and relationship.

Rationale: many knowledge objects are propositions: "X tends to lead Y under regime Z," "Definition A differs from definition B," or "Study S supports mechanism M." A claim can be about concepts or relationships without forcing every assertion to be a relationship edge.

### C2. Evidence object / evidence reference

Recommendation: explicitly distinguish evidence references from evidence evaluations.

Rationale: MacroForge may own the evidence source handle, while KnowledgeForge owns how that evidence supports, weakens, or contradicts a knowledge object.

### C3. Applicability condition

Recommendation: replace or supplement "contextual knowledge" with an explicit applicability-condition concept.

Rationale: context is usually a qualifier on other knowledge, not always a standalone knowledge object.

### C4. Methodological knowledge

Recommendation: add methodological knowledge as a bounded class or subtype.

Examples:

- statistical method definitions;
- transformation semantics;
- mapping derivation rules;
- comparability methodology;
- measurement-method compatibility.

Rationale: empirical relationships and source-indicator mappings require reusable method knowledge. MacroForge owns source metadata and computation reproducibility; KnowledgeForge owns reusable method meaning and comparability implications.

### C5. Validity scope

Recommendation: define validity scope as a required facet.

Rationale: scope should not be scattered across time validity, regime validity, geography, method, and source fields with no unifying concept.

### C6. Review state / stewardship state

Recommendation: separate lifecycle state from review/stewardship state.

Rationale: a knowledge object can be Candidate but reviewed, Accepted but needing revalidation, or Deprecated but still cited historically.

### C7. Negative knowledge

Recommendation: represent known incompatibilities, rejected mappings, failed relationships, and contradicted claims.

Rationale: avoiding rediscovery is central to long-term maintainability.

## 8. Recommended architectural refinements

### R1. Reframe the six knowledge classes as a multi-axis model

Recommendation:

- Content axis: semantic, structural, empirical, methodological, domain/entity/event as needed.
- Applicability axis: contextual validity conditions.
- Epistemic axis: evidence, provenance, confidence, uncertainty, contradictions.
- Evolution axis: lifecycle, revision history, review/stewardship.

Rationale: this is the highest-leverage refinement. It preserves the current categories while making them composable and scalable.

### R2. Add an explicit invariants document

Recommendation: create `docs/invariants.md` in a future documentation refinement task and make it authoritative before implementation planning.

Rationale: invariants are the simplest way to prevent boundary erosion once implementation starts.

### R3. Narrow structural knowledge language

Recommendation: replace broad phrases like "curated economic theory" and "domain models" with "provenance-bearing reusable theory records and structural claim records."

Rationale: this prevents KnowledgeForge from becoming InsightForge.

### R4. Strengthen empirical relationship boundaries

Recommendation: empirical records should include method, parameters, sample/evidence scope, transformations, frequency, lag/window, uncertainty, limitations, and explicit non-causality unless separately justified.

Rationale: protects against spurious reusable knowledge and PredictionForge leakage.

### R5. Clarify source-indicator mapping ownership

Recommendation: KnowledgeForge owns mapping semantics and comparability judgments; MacroForge owns source indicator metadata and observations.

Rationale: this is currently mostly clear but should become an invariant because it will be a recurring boundary pressure.

### R6. Add domain-expansion gate

Recommendation: future domains require a decision artifact proving that the domain can use the core model without causing KnowledgeForge to own observations, reasoning, prediction, recommendation, or presentation.

Rationale: controls scope creep while preserving long-term extensibility.

### R7. Treat contradiction as durable structure, not only metadata

Recommendation: contradictions should be represented as durable epistemic relationships or states, not merely text fields.

Rationale: at large scale, contradictions need to be discoverable, reviewable, and preserved across lifecycle changes.

### R8. Distinguish identity lifecycle from claim lifecycle

Recommendation: concept identities, mappings, relationships, and claims should not share lifecycle semantics blindly.

Rationale: a concept identity may remain stable while a relationship claim is deprecated; a mapping may be questioned while both source and target concepts remain accepted.

### R9. Replace "serves downstream projects" with "provides governed knowledge interfaces"

Recommendation: use interface language rather than service language during specification phase.

Rationale: avoids premature runtime assumptions.

### R10. Make non-governance explicit

Recommendation: state that KnowledgeForge does not approve downstream reasoning, forecasts, reports, or decisions merely because they cite KnowledgeForge.

Rationale: prevents KnowledgeForge's authority from leaking downstream.

## 9. Recommended priority order

1. Add architectural invariants.
2. Convert knowledge classes into a multi-axis model.
3. Tighten structural knowledge and empirical knowledge boundary language.
4. Add missing primitives: claim, evidence reference/evaluation, applicability condition, methodological knowledge, validity scope, negative knowledge.
5. Add domain-expansion gate.
6. Only then begin implementation-readiness decisions.

## 10. Final review conclusion

KnowledgeForge should proceed, but the current draft should not be treated as finished. The core identity is strong. The boundary model is mostly correct. The main architectural risk is conceptual overloading: using "knowledge" and the six knowledge classes too broadly.

The project does not need a redesign. It needs sharper invariants, a multi-axis conceptual model, and narrower boundary language before implementation begins.
