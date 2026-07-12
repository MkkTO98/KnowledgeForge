# KnowledgeForge Architectural Invariants

Status: Authoritative specification invariant set
Date: 2026-06-29
Implementation status: Specification-only; no runtime mechanism implied

These invariants constrain future KnowledgeForge architecture and implementation planning. They are architectural rules, not database schemas, APIs, graph requirements, or executable validations.

## I1. Observations remain outside KnowledgeForge

KnowledgeForge must never own or duplicate observational datasets.

External observational systems remain the systems of record for observational data, ingestion, validation, canonicalization, observational lineage, reproducibility, source observational identities, and observational databases.

KnowledgeForge may store references to evidence and may evaluate how referenced evidence supports or weakens reusable knowledge claims.

## I2. Every durable knowledge object requires provenance

A durable knowledge object without provenance is not admissible as KnowledgeForge knowledge.

Provenance may point to external observational evidence, literature, source documentation, reviewed human curation, prior KnowledgeForge objects, or other approved evidence references.

## I3. Evidence references and evidence evaluations remain distinct

Evidence references identify source material or reproducibility handles.

Evidence evaluations describe how those references support, weaken, contradict, limit, or fail to support a knowledge object.

KnowledgeForge owns evaluations of reusable knowledge. It does not thereby own the underlying observational evidence when that evidence belongs to an external observational system or source.

## I4. Claims are first-class

Durable assertions, definitions, mappings, methodological statements, empirical findings, negative findings, contradictions, and relationship statements must be representable as claims.

A relationship may represent a claim, but claims must not be forced into graph-edge form.

## I5. Claim classification uses governed facets, not inheritance

Claims must be classified through governed vocabularies and orthogonal facets rather than rigid object subclasses.

The initial architectural facets are assertion function, epistemic nature, polarity, domain role, and representation form. Vocabulary extension is a governance concern, not an implementation shortcut.

## I6. Relationships require claim linkage and evidence state

Every durable relationship representation must identify its associated claim or claims and must have evidence references or an explicit unsupported/candidate state.

A relationship is not admissible merely because two concepts can be connected.

## I7. Knowledge objects use orthogonal components

Identity, content, applicability, evidence, evolution, and governance are separate architectural components.

Semantic, structural, empirical, contextual, epistemic, and evolutionary concerns must not be treated as mutually exclusive peer classes.

## I8. Every durable object has a common kernel

Every durable knowledge object must have a common architectural kernel: stable identity, object kind, content summary, provenance, applicability/scope posture, evidence state, lifecycle state, governance/review state, revision history, and dependency posture.

Type-specific extensions may enrich objects, but no durable object is exempt from the kernel.

## I9. Durable identity is stable across revisions

Every durable knowledge object has stable identity independent of revision history. Revisions belong to the object unless the object meaning splits, multiple objects were incorrectly merged, or the identity was materially misidentified.

Identity correction, split, and merge events must be governed and historically traceable.

## I10. Applicability is explicit

Non-universal knowledge must declare its applicability conditions where known.

Applicability may include time, geography, regime, institutional setting, source scope, method scope, units, transformations, frequency, sample, lag, window, or other validity constraints.

## I11. Dependencies use explicit posture and facets

Every durable knowledge object must explicitly declare its dependency posture: dependencies listed, none known, not applicable, or unresolved.

Dependencies may include concepts, claims, mappings, methods, evidence evaluations, assumptions, applicability contexts, or relationship representations. Where dependencies are listed, they should distinguish type, necessity, strength, direction, scope, and review-propagation meaning.

Dependency declarations preserve reasoning structure and future review propagation. They do not require current graph computation.

## I12. Contradictions are preserved

Contradictions, competing explanations, weakening evidence, and incompatible mappings must be preserved rather than silently resolved.

KnowledgeForge may record review outcomes and lifecycle states, but it must not erase contested epistemic structure merely to produce a cleaner model.

## I13. Negative knowledge is admissible

Expected relationships not observed, failed empirical relationships, rejected mappings, disproven or unsupported external hypotheses, contradictory literature, and known limitations may become durable knowledge when evidence scope and method are explicit.

Absence of evidence is not evidence of absence unless the claim explicitly justifies that interpretation.

## I14. Empirical knowledge cannot overwrite semantic or structural knowledge

Statistical association cannot redefine concepts, units, source identities, or structural theory by itself.

Empirical knowledge may support, weaken, contradict, or motivate review of semantic or structural claims, but those changes require explicit governed revision.

## I15. Structural knowledge cannot erase empirical contradictions

Theory, literature, or curated structural models cannot silently suppress contrary empirical evidence.

Contrary evidence must remain discoverable, scoped, and reviewable.

## I16. Association is not causation

Empirical association must not be treated as causal unless supported by a separate causal or structural claim with its own evidence, applicability, dependencies, and lifecycle state.

## I17. Mappings are typed, reversible, and non-destructive

Source-indicator mappings must preserve source identity and mapping assumptions.

Derived, proxy, incompatible, and unknown mappings must declare uncertainty, transformation, lossiness, or incompatibility as appropriate.

## I18. Lifecycle state is not truth state

Accepted means accepted for reuse under stated evidence and applicability conditions. It does not mean proven true.

Lifecycle transitions must be auditable and preserve prior states.

## I19. Governance state is distinct from confidence

Review status, stewardship status, and lifecycle state do not equal epistemic confidence.

A reviewed object may remain uncertain; an accepted object may be narrow; a deprecated object may remain historically addressable.

## I20. Deprecated objects remain addressable

Knowledge objects must remain addressable after deprecation or archival so downstream citations, historical reports, and review trails remain interpretable.

## I21. Knowledge changes preserve conceptual coherence

Durable changes that affect multiple knowledge objects should be understood as coherent knowledge changes with shared rationale, scope, and review context.

A knowledge change is an architectural audit concept, not a database transaction, API operation, graph operation, workflow engine, or implementation mechanism.

## I22. Downstream use is not evidence

Use by downstream reasoning, navigation, presentation, forecasting, decision systems, or a human does not by itself increase confidence in a KnowledgeForge object.

Downstream systems may cite KnowledgeForge; they do not mutate KnowledgeForge state without governed KnowledgeForge review.

## I23. KnowledgeForge does not approve downstream conclusions

A downstream report, interpretation, forecast, or decision is not endorsed merely because it cites KnowledgeForge objects.

KnowledgeForge provides governed reusable knowledge, not reasoning approval, forecast approval, report approval, or decision approval.

## I24. Domain expansion cannot bypass invariants

New domains may extend vocabulary and content types only when they preserve KnowledgeForge's core ownership model and invariants.

Domain expansion must not cause KnowledgeForge to own observations, reasoning, prediction, recommendation, presentation, or domain-specific operations.

## I25. Representation choices are subordinate

Graphs, ontologies, relational schemas, document stores, APIs, and file-backed models are implementation or representation choices.

The architectural model remains governed, versioned, provenance-bearing reusable knowledge.
