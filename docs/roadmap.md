# KnowledgeForge Roadmap

Status: Provisional specification freeze candidate

## Phase 0 — Specification-only foundation (current)

Purpose: establish ownership, boundaries, principles, interfaces, governance, and future responsibilities before implementation.

Allowed work:

- architecture specification;
- principles;
- interface contracts;
- decision artifacts;
- task artifacts;
- open-question capture;
- state/handoff/summaries;
- coherence verification.

Forbidden work:

- runtime code;
- databases;
- APIs;
- graph computation;
- statistical pipelines;
- external services;
- deployment;
- cross-project mutation.

Exit criteria:

- foundational scope accepted;
- MacroForge boundary accepted;
- InsightForge/AtlasForge/BriefForge/future-project boundaries accepted;
- knowledge object component model stable enough for implementation planning;
- claim facets and governed vocabulary posture accepted;
- relationship-representation and dependency posture/facet responsibilities accepted;
- lifecycle, provenance, evidence, governance, stable identity, knowledge-change, and invariant requirements accepted;
- open questions triaged into pre-implementation blockers versus implementation-pressure deferrals.

## Phase 1 — Conceptual model hardening

Purpose: convert the foundational architecture into implementation-ready contracts without building runtime systems.

Likely artifacts:

- knowledge object component specification;
- claim facet vocabulary and claim object specification;
- stable identity/revision/split/merge semantics;
- relationship representation specification;
- knowledge dependency posture/facet specification;
- canonical concept and source-indicator mapping specification;
- evidence reference contract with MacroForge;
- evidence evaluation contract;
- lifecycle state machine specification;
- governance/review state specification;
- confidence/uncertainty representation decision;
- provenance model specification;
- methodological knowledge specification;
- negative knowledge specification;
- knowledge-change audit concept specification;
- storage selection criteria.

Exit criteria:

- a future implementer can build a minimal vertical slice without redefining ownership boundaries;
- no unresolved L3/L4 boundary questions remain for the first slice.

## Phase 2 — Minimal implementation planning

Purpose: choose one narrow vertical slice that proves the architecture without turning KnowledgeForge into a platform too early.

Candidate first slice:

```text
One MacroForge-backed economic source indicator
  ↓ reference only
One canonical concept
  ↓
One mapping object
  ↓
One claim object
  ↓
One relationship representation or negative finding
  ↓
One dependency declaration
  ↓
One evidence/provenance/lifecycle/governance record
  ↓
One read-only consumer contract for InsightForge or AtlasForge
```

The slice should be deterministic, fixture-backed where possible, and explicitly non-production.

Exit criteria:

- task artifact for implementation exists;
- storage decision exists;
- tests and verification plan exist;
- rollback/migration plan exists;
- no external credentials or production data required.

## Phase 3 — Minimal implementation

Purpose: implement the smallest end-to-end reusable knowledge path.

Allowed only after explicit approval.

Likely implementation concerns:

- schemas or equivalent contracts;
- persistent knowledge store or file-backed prototype;
- evidence reference validation;
- lifecycle state validation;
- claim object creation;
- relationship representation or negative-knowledge object creation;
- dependency declaration validation;
- deterministic tests;
- export/read interface.

Non-goals:

- broad ontology;
- generalized graph platform;
- large-scale statistical discovery;
- dashboards;
- reasoning;
- forecasting;
- decision automation.

## Phase 4 — Empirical relationship subsystem

Purpose: compute or preserve reusable empirical claims and relationship representations as governed knowledge objects, including negative empirical findings when method and evidence scope are explicit.

Preconditions:

- MacroForge evidence reference contract stable;
- method metadata model stable;
- uncertainty/confidence model stable;
- lifecycle gates defined;
- spurious discovery safeguards defined.

Initial method candidates:

- Pearson;
- Spearman;
- Kendall;
- cross-correlation;
- rolling correlations.

More complex methods such as mutual information, cointegration, and regime-dependent models should wait until simpler relationship governance has proven reliable.

## Phase 5 — Consumer integration

Purpose: let InsightForge and AtlasForge consume KnowledgeForge without duplicating its responsibilities.

Likely integrations:

- InsightForge consumes concepts, claims, relationship representations, dependencies, evidence, uncertainty, contradictions, negative knowledge, methodological knowledge, and lifecycle state.
- AtlasForge consumes concept neighborhoods, claim/relationship metadata, and dependency metadata for navigation.

KnowledgeForge still does not generate reports or visualization.

## Phase 6 — Domain expansion

Purpose: expand beyond economics only after the economics substrate proves stable.

Candidate domains:

- companies;
- industries;
- products;
- regulations;
- supply chains;
- events;
- academic knowledge;
- geographic entities.

Expansion rule: add a domain only when it has a clear reusable knowledge need, can reuse the component-based knowledge model and invariants, and does not require KnowledgeForge to own observations, reasoning, forecasting, recommendations, presentation, or domain operations.
