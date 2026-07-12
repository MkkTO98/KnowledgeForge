# KnowledgeForge Architectural Assimilation Review

Date: 2026-07-09
Status: completed architecture review
Scope: ProjectForge, MacroForge, MetaHarvest current architectures
Boundary: documentation and governance only; no runtime implementation changes

## Executive conclusion

KnowledgeForge should assimilate architectural lessons from the rest of the EIP ecosystem, but it should not become a copy of ProjectForge, MacroForge, or MetaHarvest.

The most valuable cross-project discovery is not a folder layout or tool list. It is a reproducibility-oriented operating pattern:

```text
constitutional boundary
-> bounded task
-> explicit evidence/provenance contract
-> deterministic or locally reproducible transformation
-> validator/check artifacts
-> concise current-state pointers
-> closeout/handoff
-> maturity/confidence update
```

For KnowledgeForge, this pattern should become a knowledge-generation architecture:

```text
external or MacroForge evidence reference
-> evidence-source/evidence-evaluation record
-> deterministic normalization into a durable knowledge-object candidate
-> claim/facet/dependency/applicability validation
-> local-model or template-assisted drafting only where deterministic extraction is insufficient
-> reviewer/governance state
-> reusable knowledge object with reproducible provenance and audit trail
```

KnowledgeForge should therefore adopt or adapt the proven governance, evidence, validation, continuity, maturity, and deterministic-substrate mechanisms. It should reject runtime orchestration, generic framework extraction, dashboards, vector stores, always-fresh mirrors, graph-first architecture, and broad PostgreSQL commitments until implementation evidence demands them.

## Evidence basis

### ProjectForge current architecture

ProjectForge has matured into five constitutional systems: Project Identity, Context and Continuity, Governance and Decision, Work Execution Methodology, and Validation and Evidence. Its mature doctrine treats capabilities as primary and files as implementation expressions. It also emphasizes generated-project sovereignty, summary-first context, bounded current-state pointers, explicit context audits, architecture-reality audits, validator classification, terminology governance, and automation only when reliable, understandable, testable, observable, and reversible.

### MacroForge current architecture

MacroForge has matured around deterministic ingestion for public economic evidence. Its strongest transferable patterns are source-specific behavior before a stable observed boundary, post-boundary deterministic substrate, observed-package fingerprints, idempotent reruns, canonical lineage events, contract validation/drift detection, deterministic feedback, source-specific canonical loaders, capability maturity, evidence-backed campaign sizing, run-scoped validation, and PostgreSQL staging/curated/meta separation. Its negative lesson is equally important: do not extract generic frameworks until heterogeneous implementations prove convergence and measurable effort reduction.

### MetaHarvest current architecture

MetaHarvest has matured into a file-backed reusable architecture knowledge library. Its key lessons are knowledge/evidence separation, evidence-source taxonomy, snapshots over mirrors, optional materialization, source lifecycle based on architectural usefulness, prediction-before-analysis, knowledge evolution as scientific completion, contradiction preservation, problem-first retrieval, component cards as evidence-to-knowledge bridges, primitives/patterns/invariants only after repeated evidence, and advisory-only consumer boundaries.

## KnowledgeForge assimilation thesis

KnowledgeForge is closer to MetaHarvest in epistemic shape, closer to MacroForge in reproducibility demands, and closer to ProjectForge in governance/continuity mechanics.

It should therefore assimilate:

1. ProjectForge's operating-system discipline.
2. MacroForge's deterministic boundary and validation discipline.
3. MetaHarvest's evidence-to-knowledge and scientific-cycle discipline.

It should not assimilate:

1. ProjectForge's framework-generation responsibilities.
2. MacroForge's observational ingestion/database ownership.
3. MetaHarvest's advisory/recommendation role or external architecture-harvesting scope.

## High-value architectural opportunities

### 1. Reproducible knowledge-generation pipeline

KnowledgeForge currently has durable object fixtures and a validator. It needs an architectural pipeline model before production knowledge generation begins. This should adapt MacroForge's observed boundary and MetaHarvest's evidence-source doctrine into a KnowledgeForge-specific boundary:

```text
Evidence reference / evidence specimen
-> Evidence evaluation
-> Knowledge candidate package
-> Durable knowledge object validation
-> Governance/lifecycle transition
-> Published reusable knowledge object
```

The pipeline should be file-backed and deterministic first. Local-model assistance may draft summaries, extract candidate claims, or classify evidence only after deterministic pre-processing has produced a bounded input and after outputs are validated.

### 2. Evidence source and evaluation architecture

MetaHarvest's repository/evidence architecture should be adapted directly. KnowledgeForge needs an evidence-source taxonomy and a strict separation between evidence references and evidence evaluations. Unlike MetaHarvest, KnowledgeForge should focus on evidence that supports reusable domain knowledge: MacroForge reproducibility handles, source documentation, literature, institutional methodology pages, statistical result packages, and reviewed human curation.

### 3. Knowledge object package contract

MacroForge's `ObservedIngestionPackage` pattern should inspire a `KnowledgeObjectPackage` or equivalent architecture, but implementation must be deferred. The transferable idea is a portable, fingerprintable, validator-friendly boundary object. For KnowledgeForge this would package candidate object identity, content, claim facets, evidence references/evaluations, applicability, dependencies, lifecycle proposal, governance state, and revision metadata.

### 4. Deterministic validation expansion

KnowledgeForge should adopt ProjectForge/MacroForge validator discipline: validator outputs should be concise, classified, and runnable locally. Current Slice 0 validation should grow into checks for object-kernel invariants, evidence/evaluation distinction, dependency posture, claim-facet validity, applicability declarations, lifecycle transition gates, contradiction preservation, and reproducible fingerprinting.

### 5. Scientific-cycle completion before knowledge acceptance

MetaHarvest's prediction/evidence/evolution discipline should be adapted. For KnowledgeForge, a knowledge object should not be accepted merely because an LLM generated a plausible statement. Acceptance should require a completed evidence-evaluation cycle: candidate claim, evidence basis, contradiction search, applicability statement, confidence/uncertainty posture, dependency review, lifecycle decision, and revision trace.

### 6. Maturity and confidence tracking

MacroForge capability maturity and MetaHarvest pattern maturity should become KnowledgeForge object/capability maturity. The project needs maturity states for object types, evidence families, claim classes, and knowledge-generation pipelines. This should not become opaque scoring; labels must be evidence-backed and explainable.

### 7. Problem-first retrieval and provenance-first navigation

MetaHarvest's problem-first retrieval should be adapted into question-first or claim-first retrieval. KnowledgeForge should let agents ask: which concept/claim/mapping/evidence evaluation answers this reusable knowledge question, with what evidence, limitations, contradictions, and lifecycle state?

### 8. Local-first/frontier-LLM minimization architecture

ProjectForge's local-execution/cloud-governance and MacroForge's deterministic-computation posture should become a formal KnowledgeForge routing model. Candidate extraction, normalization, deduplication, validation, fingerprinting, and most classification should be deterministic or local-model first. Frontier LLMs should be reserved for ambiguous ontology decisions, contradiction synthesis, boundary disputes, and major architectural reviews.

### 9. Terminology governance

ProjectForge's terminology governance should be adapted because KnowledgeForge is semantics-heavy. KnowledgeForge needs governed terms for knowledge objects, claim facets, evidence states, lifecycle states, confidence labels, dependency facets, applicability dimensions, and mapping semantics. This must not become a universal ontology project.

### 10. Architecture-to-reality audits

ProjectForge's architecture-reality audit is immediately useful. KnowledgeForge should run it before major architecture changes and every 5-10 completed tasks, but tailor future checks toward knowledge-object reality: documented invariants vs fixtures, validators vs specifications, evidence records vs reports, and state/handoff correctness.

## Special-focus findings

### Reproducibility

The strongest reproducibility opportunities are package contracts, fingerprints, deterministic validators, evidence-source references, run/task-scoped reports, and idempotent generation checks. KnowledgeForge should treat every accepted knowledge artifact as reconstructible from its evidence references, evaluation metadata, transformation/drafting procedure, and revision history.

### Frontier LLM reduction

Many future KnowledgeForge steps do not require frontier LLMs:

- evidence-source metadata extraction from structured records;
- claim-facet validation;
- dependency graph consistency checks;
- lifecycle transition gate checks;
- contradiction presence checks;
- provenance and reference resolution;
- object fingerprinting;
- object-package diffing;
- stale/current state hygiene;
- template rendering;
- local summarization of bounded evidence packets;
- duplicate/near-duplicate candidate detection after deterministic normalization.

Frontier LLMs may remain useful for ambiguous claim granularity, ontology boundary disputes, contradiction synthesis, and high-level architecture review.

### Deterministic computation

Knowledge generation should be decomposed into deterministic stages before any LLM stage. LLM output should be treated as a candidate artifact, not as accepted knowledge. Deterministic validators should enforce admissibility.

### Local AI

Local models can likely handle bounded extraction/classification from small evidence packets once templates and validators exist. The architecture should preserve prompt templates, local-model outputs, and validation failures as auditable intermediate representations.

### Auditability and provenance

MetaHarvest's evidence-source architecture and MacroForge's lineage/fingerprint discipline both support KnowledgeForge's constitutional need for provenance. KnowledgeForge should adapt them into a provenance envelope for every durable object and every knowledge change.

### Maintainability

The main maintainability lesson is restraint. Do not add databases, graph systems, schedulers, vector stores, dashboards, or generic pipelines until file-backed packages and validators fail under real load.

## Compatibility finding

No source architecture should be imported wholesale. Every adoption must be translated into KnowledgeForge terms:

- ProjectForge patterns become operating discipline.
- MacroForge patterns become deterministic/evidence-boundary discipline.
- MetaHarvest patterns become evidence-to-knowledge/scientific-cycle discipline.

The assimilation campaign found one immediate constitutional inconsistency: `CONSTITUTION.md` still described ProjectForge rather than KnowledgeForge. This was corrected as documentation-level constitutional alignment with existing KnowledgeForge architecture, not as new implementation.
