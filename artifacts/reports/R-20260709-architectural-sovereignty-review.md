# Architectural Sovereignty Review

Date: 2026-07-09
Status: completed
Scope: current KnowledgeForge architecture/state/roadmap/backlog plus recent assimilation, consolidation, validation, readiness-audit, and production-campaign recommendation artifacts

## Review question

Does the current KnowledgeForge architecture appear to depend on, reference, mirror, integrate with, or expose project-specific interfaces to another EIP repository?

## Conclusion

Before correction: partially yes.

The prior assimilation/readiness work preserved KnowledgeForge's constitutional boundary in intent, but some current-state and next-task language drifted into project-specific coupling. The most important examples were:

- a named project-specific `EvidenceRef Adapter`;
- phrases implying a repository-to-repository bridge;
- package-readiness language tied to another repository's PostgreSQL schema and runtime state;
- current architecture headings framed as compatibility with a named project;
- backlog acceptance criteria requiring project-derived fixtures rather than KnowledgeForge-owned source evidence fixtures;
- roadmap prerequisites phrased as evidence-reference contracts with a named project.

After correction: no current authoritative architecture file requires another EIP repository's runtime interface, schema, database, package class, shared implementation package, or adapter.

Historical audit reports still contain project-specific evidence because they document what was actually audited. Those reports are now marked as historical evidence where necessary, and their project-specific adapter recommendations are superseded.

## Occurrence catalogue

A complete raw occurrence catalogue was produced at:

- `artifacts/reports/R-20260709-architectural-sovereignty-occurrence-catalogue.md`

The catalogue classified occurrences into:

- `sovereignty-blurring/actionable`: wording implying project-specific dependency, adapter, interface, or coupling;
- `boundary/reference-only`: acceptable boundary wording or scaffold/history references;
- `historical/evidence-context`: acceptable historical audit/evidence context when not used as current architecture.

The catalogue found 519 raw occurrences across 48 files. This count intentionally includes acceptable historical and boundary references so the review is auditable rather than cherry-picked.

## Actionable drift classes found

### 1. Project-specific adapter language

Examples before correction:

- `MacroForge WDI EvidenceRef Adapter and Real-Fixture Validation Slice`
- `read-only adapter/export slice`
- `adapter-mediated boundary`
- `MacroForge-derived fixture`

Architectural problem:

Adapter language implies a maintained interface between repositories. That violates KnowledgeForge sovereignty because it turns a useful evidence-source lesson into an architectural relationship with a named project.

Correction principle:

Replace with KnowledgeForge-owned source-evidence/package language:

- `Source Evidence Package v1 Real-Fixture Replay Validation Slice`
- `EvidenceReference`
- `SourceEvidencePackage`
- `ProvenanceEnvelope`
- source-snapshot/selection/method/package fingerprints

### 2. Project-specific evidence-reference ownership

Examples before correction:

- `MacroForge EvidenceRef`
- `evidence reference contract with MacroForge`
- `MacroForge package/run/query references`

Architectural problem:

These imply the evidence-reference contract belongs to, or must be negotiated with, another repository.

Correction principle:

KnowledgeForge owns evidence references. External systems may supply evidence, identifiers, snapshots, exports, or manifests, but KnowledgeForge converts them into its own `EvidenceReference` and package contracts.

### 3. Database/schema coupling language

Examples before correction:

- production readiness tied to another repository's PostgreSQL repository;
- next task requiring read-only PostgreSQL sample queries;
- readiness statements referring to another repository's schema state.

Architectural problem:

Even read-only database coupling would make production readiness depend on another repository's current implementation. KnowledgeForge may use source evidence snapshots or explicitly exported evidence fixtures, but the architecture must not require a foreign database schema.

Correction principle:

The next validation slice uses a tiny immutable external WDI evidence fixture or snapshot. If data originated from a database in historical audit work, that origin remains provenance, not a runtime contract.

### 4. Named downstream ownership language in current architecture

Examples before correction:

- current architecture diagrams naming downstream projects as architectural layers;
- statements that a named project owns interpretation or presentation.

Architectural problem:

Boundary labels are useful, but named downstream projects in authoritative architecture can make KnowledgeForge look like a component in a fixed inter-repository pipeline.

Correction principle:

Current architecture now uses role-based terms: observational systems, reasoning systems, navigation systems, forecasting systems, decision systems, and presentation systems. Historical reports may retain named context.

### 5. Origin-project residue in assimilated lessons

Examples before correction:

- wording that a KnowledgeForge pattern was adapted from a named project in current specs;
- source-family handling described as another project's discipline.

Architectural problem:

The source of inspiration should disappear after a KnowledgeForge design decision is made. Origin-project references belong in historical assimilation evidence, not current architecture.

Correction principle:

Current specs now present the design from first principles: source-family-specific handling precedes a common KnowledgeForge evidence boundary because evidence classes differ materially.

## Preserved architectural lessons

The correction does not discard useful improvements. It preserves these KnowledgeForge-owned concepts:

- explicit evidence references distinct from evidence evaluations;
- source-family-specific handling before common package boundaries;
- package-shaped reproducibility contracts;
- provenance envelopes;
- input/source-snapshot/query/method/template/package fingerprints;
- deterministic validators and classified blocker/warning outputs;
- knowledge-change/evolution reports;
- lifecycle state distinct from confidence and governance;
- local-first/no-model-by-default routing;
- real-fixture replay validation before production generation;
- explicit negative knowledge and contradiction handling;
- strict anti-interpretation boundaries.

## Constitutional boundary check

KnowledgeForge now owns:

- architecture: yes, current architecture is role-based and KnowledgeForge-owned;
- terminology: yes, current actionable terminology uses EvidenceReference, SourceEvidencePackage, ProvenanceEnvelope, package contracts, validators, lifecycle, and knowledge change;
- validation model: yes, Validation Framework v1 remains local and deterministic;
- package contracts: yes, contracts are KnowledgeForge package kinds, not foreign package classes;
- provenance model: yes, provenance envelope and fingerprint specs are KnowledgeForge-owned;
- lifecycle: yes, lifecycle states remain KnowledgeForge-owned and separate from confidence/governance.

KnowledgeForge now neither exposes nor consumes project-specific runtime interfaces in its current architecture.

## Remaining acceptable references

Some references remain acceptable because they are not current architectural dependencies:

- `ProjectForge` scaffold/operating-system references in generated-project instructions and summaries;
- historical assimilation reports that name reviewed projects;
- historical audit reports that describe evidence that was actually inspected;
- local advisory paths under `architecture/metaharvest/` inherited from scaffold/governance compatibility;
- foundational decisions that name sibling projects as historical boundary context.

These should not be used as production integration requirements.
