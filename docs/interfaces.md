# KnowledgeForge Interfaces and Boundary Contracts

Status: Foundational specification
Runtime interfaces: Deferred

## 1. Interface philosophy

KnowledgeForge participates in an autonomous EIP ecosystem, but it remains a sovereign repository. It exchanges governed reusable knowledge, evidence references, claims, relationship representations, dependency metadata, and context through explicit KnowledgeForge-owned contracts.

KnowledgeForge does not govern other projects, and other projects do not govern KnowledgeForge.

Interfaces begin as architectural contracts. Runtime APIs, shared schemas, database protocols, shared implementation packages, and cross-repository adapters are deferred and are not authorized by this specification.

## 2. External evidence systems -> KnowledgeForge

### External evidence systems own

- source acquisition;
- observational ingestion;
- observational validation;
- observational canonicalization;
- observational lineage;
- observational reproducibility;
- source observational identities;
- quantitative observations;
- source-specific metadata production;
- observational databases or data stores.

### KnowledgeForge owns

- reusable concepts;
- semantic identities;
- mappings from source evidence indicators to canonical concepts;
- durable claims;
- relationship representations;
- knowledge dependencies;
- negative knowledge;
- methodological knowledge;
- evidence-backed empirical claims;
- evidence evaluations;
- KnowledgeForge package identity;
- provenance envelopes and fingerprints;
- lifecycle and governance state of knowledge objects.

### Allowed flow

External evidence systems or sources may provide:

- observational identifiers;
- source indicator metadata;
- reproducibility handles;
- dataset/series references;
- release/version/vintage references;
- quality/lineage metadata;
- immutable exports or snapshots;
- source documentation references.

KnowledgeForge may store references to these artifacts, or small immutable snapshots where justified by reproducibility. It must not copy full observational datasets into its own persistent store as owned KnowledgeForge data.

### Boundary rule

If an artifact is primarily about measured values and their observational reproducibility, it belongs to an external evidence system or source. If it is primarily about reusable meaning, claims, relationship representations, mappings, knowledge dependencies, evidence evaluations, methodological meaning, package provenance, or epistemic status, it belongs to KnowledgeForge.

## 3. KnowledgeForge -> downstream reasoning systems

Downstream reasoning systems should consume KnowledgeForge knowledge rather than implement durable knowledge structures themselves.

KnowledgeForge may provide:

- concepts;
- definitions;
- claims;
- relationship representations;
- knowledge dependencies;
- mapping semantics;
- empirical claim records;
- negative knowledge;
- methodological knowledge;
- evidence references and evidence evaluations;
- confidence and uncertainty;
- contradictions;
- lifecycle state;
- applicability regimes;
- literature/provenance pointers.

Downstream reasoning systems own:

- reasoning;
- interpretation;
- analytical understanding;
- hypotheses;
- narrative synthesis;
- explanation of current situations.

Boundary rule: if the artifact preserves a governed, provenance-bearing reusable claim about what is known, under what applicability conditions, and why it is believed or contested, it belongs to KnowledgeForge. If it says what this implies for an analysis, current situation, hypothesis, narrative, or report, it belongs to a downstream reasoning system.

## 4. KnowledgeForge -> navigation systems

KnowledgeForge may provide:

- concept neighborhoods;
- relationship metadata;
- claim metadata;
- upstream/downstream dependencies;
- alternative paths;
- regime applicability;
- evidence pointers;
- contradiction pointers;
- confidence and lifecycle metadata.

Navigation systems own:

- visualization;
- navigation UX;
- exploration workflows;
- presentation of traversals;
- user-facing maps.

Boundary rule: KnowledgeForge stores navigable knowledge and dependency metadata. Navigation systems make it navigable to humans. KnowledgeForge does not implement visualization or navigation UX.

## 5. KnowledgeForge -> presentation systems

KnowledgeForge does not generate reports or presentation artifacts. It may be cited by downstream reports through evidence references, claim identifiers, and knowledge object identifiers, normally through presentation context produced by an approved downstream consumer.

Presentation systems own:

- report layout;
- decks/documents;
- audience-specific rendering;
- narrative packaging;
- visual style and communication format.

## 6. KnowledgeForge -> forecasting systems

Forecasting systems may consume:

- empirical claims and relationship representations;
- regime-dependent knowledge;
- structural dependencies;
- methodological limitations;
- negative knowledge;
- uncertainty metadata;
- evidence and limitations.

KnowledgeForge must not produce forecasts, probability distributions for future outcomes, scenario predictions, or model recommendations. Empirical lead-lag knowledge is allowed only as reusable knowledge, not as a forecast.

## 7. KnowledgeForge -> decision systems

Decision systems may consume:

- contextual knowledge and applicability conditions;
- uncertainty;
- competing explanations;
- negative knowledge;
- methodological limitations;
- lifecycle status;
- evidence references;
- approved forecasting outputs from forecasting systems.

KnowledgeForge must not recommend actions, portfolio changes, policies, trades, or interventions.

## 8. Cross-domain future interfaces

KnowledgeForge should later support domains beyond economics, including companies, industries, products, regulations, supply chains, events, academic knowledge, and geography.

Cross-domain expansion must preserve the same boundary rules:

- observations remain with domain observational systems;
- reusable knowledge belongs to KnowledgeForge;
- interpretation belongs to reasoning systems;
- presentation belongs to presentation systems;
- predictions belong to forecasting systems;
- decisions belong to decision systems.

## 9. Contracts required before runtime implementation

Before any runtime API, database integration, shared schema, or cross-repository integration, create accepted decision artifacts for:

1. Source evidence reference contract.
2. Knowledge object identifier contract.
3. Concept/source-indicator mapping contract.
4. Claim object contract.
5. Relationship representation contract.
6. Knowledge dependency contract.
7. Evidence evaluation contract.
8. Provenance envelope and fingerprint contract.
9. Lifecycle state transition contract.
10. Governance/review state contract.
11. Downstream consumer export/reference contract.
12. Versioning and backward-compatibility contract.

No runtime integration may be inferred from these conceptual contracts.
