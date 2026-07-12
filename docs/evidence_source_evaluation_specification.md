# Evidence Source and Evidence Evaluation Specification

Date: 2026-07-09
Status: architecture specification; implementation not authorized

## 1. Purpose

This document defines what KnowledgeForge may treat as evidence and how it evaluates evidence without becoming a reasoning, interpretation, forecasting, recommendation, or presentation system.

Evidence references and evidence evaluations are distinct:

- Evidence references point to evidence, snapshots, data products, source claims, metadata, or reproducibility handles.
- Evidence evaluations are KnowledgeForge-owned assessments of how referenced evidence supports, weakens, contradicts, or bounds reusable knowledge.

## 2. Evidence-source architecture

### 2.1 Evidence classes

| Class | Description | May be evidence? | Ownership boundary |
| --- | --- | --- | --- |
| External observational data | Canonicalized or source-provided observational data, packages, extracts, immutable exports, or snapshots. | Yes, by reference or snapshot fingerprint. | The originating evidence system/source owns observations and canonicalization; KnowledgeForge references and evaluates. |
| External source metadata | Source, indicator, territory/entity, frequency, units, transformations, schema, release, and processing metadata. | Yes. Often stronger evidence for mapping/method claims than data values. | The originating source/evidence system owns metadata production; KnowledgeForge records references and evaluations. |
| External lineage/provenance | Reproducibility handles, source files, export manifests, validation reports, drift/contract checks, package fingerprints, or source snapshots. | Yes. Required for empirical/derived knowledge acceptance. | The evidence source owns observational lineage; KnowledgeForge records references and package-level provenance. |
| External source summaries | Source summaries, methodology summaries, and extracted source knowledge from reviewed external evidence packages. | Yes only for methodology, source-understanding, or source-scope claims; advisory otherwise. | The summarizing system or reviewer owns summary production; KnowledgeForge may preserve scoped knowledge with upstream references. |
| Manually supplied evidence | User-provided documents, excerpts, data extracts, citations, or notes. | Yes if source identity, capture method, access date, and scope are explicit. | Human/manual input is not automatically accepted. |
| Generated intermediate evidence | Deterministic computations, local-model extracts, template outputs, parsed tables, cached intermediate representations. | Yes only as intermediate evidence with upstream references and method. | Generated evidence cannot be stronger than its upstream evidence and method. |
| Official source documentation | Source methodology pages, manuals, codebooks, metadata docs, release notes. | Yes. | External source owns claims; KnowledgeForge preserves provenance. |
| Literature/source assertions | Papers, books, reports, expert documents, official publications. | Yes as source claims or literature-derived knowledge. | KnowledgeForge records claims and evaluations, not authority by prestige. |
| Consumer usage | Downstream usage by other systems or users. | No as truth evidence. | May indicate utility or priority, not validity. |
| Live web pages without snapshot | Current mutable pages. | Defer/weak evidence until snapshot/capture exists. | Freshness may be useful; reproducibility is weak. |
| LLM-generated text | Model output. | No as direct evidence. Candidate synthesis only, unless preserving the fact that a model produced text. | Requires upstream evidence and validation. |

### 2.2 Evidence-source families

KnowledgeForge should classify evidence by source family before common package generation:

- official statistical source data;
- official statistical metadata/methodology;
- external observation package or immutable source evidence snapshot;
- external validation/lineage report;
- literature/theory source;
- external architecture/source summary;
- manual/human-supplied source;
- generated deterministic intermediate;
- model-assisted intermediate candidate.

Source-family-specific handling precedes a common evidence boundary. A WDI-like statistical data snapshot, a methodology PDF, and a local-model extracted summary should not be forced through identical evidence checks before their differences are recorded.

## 3. Evidence evaluation dimensions

Every accepted evidence evaluation should address the following dimensions. Candidate packages may mark dimensions as unknown, but unknown required dimensions block acceptance.

| Dimension | Question | Blocking when missing? |
| --- | --- | --- |
| Validity | Is the evidence internally valid for the claim and source family? | Blocker for accepted/supporting use. |
| Freshness | What version/date/vintage/access time does the evidence represent? Is staleness material? | Blocker if freshness materially affects claim and no date/version exists. |
| Source family | What kind of evidence is this, and what checks apply? | Blocker. |
| Data lineage | What upstream source/package/run produced it? | Blocker for empirical/derived claims. |
| Reproducibility | Can the evidence reference or snapshot be reconstructed? | Blocker for accepted generated/derived packages; warning for preserved historical/manual notes. |
| Contradiction handling | Does evidence conflict with other evidence or claims? | Blocker if contradiction search is required and absent; warning if explicitly incomplete. |
| Uncertainty | What uncertainty is present: statistical, measurement, methodological, source, or model uncertainty? | Blocker when confidence/lifecycle depends on it; otherwise warning. |
| Missingness | What data/source/method gaps bound the claim? | Blocker for negative knowledge and statistical characterization; warning otherwise. |
| Auditability | Can a future reviewer inspect references, methods, and generated intermediates? | Blocker for accepted packages. |

## 4. Evidence evaluation outputs

An evidence evaluation may produce these reusable statements:

- supports claim under scope;
- weakens claim under scope;
- contradicts claim under scope;
- bounds applicability;
- identifies missing evidence;
- identifies methodological limitation;
- records non-observation under method;
- records source-family mismatch;
- records evidence insufficient for lifecycle transition.

It may not produce interpretive conclusions such as "this means growth is weakening" or "this is bullish/bearish". Those are downstream interpretation unless preserved as quoted external source claims.

## 5. Contradiction policy

Contradictions are preserved, not erased. A contradiction record must state:

- the claim or candidate being contradicted;
- the contradicting evidence reference;
- contradiction type: factual, methodological, scope, measurement, temporal, definitional, or interpretation-boundary;
- whether contradiction blocks acceptance, narrows applicability, lowers confidence, creates a competing claim, or merely requires review;
- whether the contradiction is unresolved, resolved by scope, resolved by method, or accepted as competing evidence.

## 6. Evidence that KnowledgeForge may not treat as direct evidence

KnowledgeForge may not treat these as direct evidence for accepted knowledge:

- unsupported LLM output;
- downstream consumer preference or usage;
- repository structure by analogy;
- stale/generated summaries without source links when source evidence is available;
- mutable live data without version/capture when reproducibility is required;
- downstream interpretation unless preserved as an external source claim and labeled accordingly.
