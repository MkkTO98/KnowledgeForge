# KnowledgeForge Interfaces and Boundary Contracts

Status: Foundational specification
Runtime interfaces: Deferred

## 1. Interface philosophy

KnowledgeForge participates in an autonomous EIP ecosystem. It exchanges governed reusable knowledge, evidence references, claims, relationship representations, dependency metadata, navigation structures, and context through explicit contracts. It does not govern other projects and other projects do not govern it.

Interfaces begin as architectural contracts. Runtime APIs, schemas, database protocols, and file formats are deferred.

## 2. MacroForge ↔ KnowledgeForge

### MacroForge owns

- ingestion;
- validation;
- canonicalization;
- observational lineage;
- reproducibility;
- canonical economic database;
- source observational identities;
- quantitative observations.

### KnowledgeForge owns

- reusable concepts;
- semantic identities;
- mappings from source indicators to canonical concepts;
- durable claims;
- relationship representations;
- knowledge dependencies;
- negative knowledge;
- methodological knowledge;
- evidence-backed empirical claims;
- provenance and epistemic state for knowledge objects;
- lifecycle and governance state of knowledge objects.

### Allowed flow

MacroForge may provide or expose:

- canonical observational identifiers;
- source indicator metadata;
- reproducibility handles;
- dataset/series references;
- release/version references;
- quality/lineage metadata;
- evidence references.

KnowledgeForge may store references to these MacroForge artifacts. It must not copy full observational datasets into its own persistent store.

### Boundary rule

If an artifact is primarily about measured values and their reproducibility, it belongs to MacroForge. If it is primarily about reusable meaning, claims, relationship representations, mappings, knowledge dependencies, evidence evaluations, methodological meaning, or epistemic status, it belongs to KnowledgeForge.

## 3. KnowledgeForge → InsightForge

InsightForge should eventually consume KnowledgeForge rather than implement durable knowledge structures itself.

KnowledgeForge provides:

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

InsightForge owns:

- reasoning;
- interpretation;
- analytical understanding;
- hypotheses;
- report generation;
- narrative synthesis.

Boundary rule: If the artifact preserves a governed, provenance-bearing reusable claim about what is known, under what applicability conditions, and why it is believed or contested, it belongs to KnowledgeForge. If it says what this implies for an analysis, current situation, hypothesis, narrative, or report, it belongs to InsightForge.

## 4. KnowledgeForge → AtlasForge

AtlasForge is the navigation layer. It may eventually navigate both MacroForge data and KnowledgeForge knowledge.

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

AtlasForge owns:

- visualization;
- navigation UX;
- exploration workflows;
- presentation of traversals;
- user-facing maps.

Boundary rule: KnowledgeForge stores navigable knowledge and dependency metadata. AtlasForge makes it navigable to humans. KnowledgeForge does not implement visualization or navigation UX.

## 5. InsightForge/KnowledgeForge → BriefForge

BriefForge is presentation only. It consumes outputs from InsightForge and potentially future projects.

KnowledgeForge does not generate reports or presentation artifacts. It may be cited by downstream reports through evidence references, claim identifiers, and knowledge object identifiers, normally through presentation context produced by InsightForge or another approved downstream consumer.

## 6. KnowledgeForge → PredictionForge

PredictionForge is future-facing and should answer: "What is likely to happen?"

PredictionForge may consume:

- empirical claims and relationship representations;
- regime-dependent knowledge;
- structural dependencies;
- methodological limitations;
- negative knowledge;
- uncertainty metadata;
- evidence and limitations.

KnowledgeForge must not produce forecasts, probability distributions for future outcomes, scenario predictions, or model recommendations. Empirical lead-lag knowledge is allowed only as reusable knowledge, not as a forecast.

## 7. KnowledgeForge → DecisionForge

DecisionForge, if created, should answer: "What should be done?"

DecisionForge may consume:

- contextual knowledge and applicability conditions;
- uncertainty;
- competing explanations;
- negative knowledge;
- methodological limitations;
- lifecycle status;
- evidence references;
- prediction outputs from PredictionForge.

KnowledgeForge must not recommend actions, portfolio changes, policies, trades, or interventions.

## 8. Cross-domain future interfaces

KnowledgeForge should later support domains beyond economics, including companies, industries, products, regulations, supply chains, events, academic knowledge, and geography.

Cross-domain expansion must preserve the same boundary rules:

- observations remain with domain observational systems;
- reusable knowledge belongs to KnowledgeForge;
- interpretation belongs to reasoning systems;
- presentation belongs to presentation systems;
- predictions belong to prediction systems;
- decisions belong to decision systems.

## 9. Interface artifacts required before runtime implementation

Before any runtime API or database integration, create accepted decision artifacts for:

1. MacroForge evidence reference contract.
2. Knowledge object identifier contract.
3. Concept/source-indicator mapping contract.
4. Claim object contract.
5. Relationship representation contract.
6. Knowledge dependency contract.
7. Evidence evaluation contract.
8. Lifecycle state transition contract.
9. Governance/review state contract.
10. Consumer interface contract for InsightForge and AtlasForge.
11. Versioning and backward-compatibility contract.
