# Local-Model and Frontier-LLM Routing Policy

Date: 2026-07-09
Status: architecture specification; implementation not authorized

## 1. Purpose

KnowledgeForge should minimize frontier LLM usage by defaulting to deterministic computation, reusable templates, cached intermediates, and local models where appropriate. Model output is candidate material only.

## 2. Routing hierarchy

Use the lowest-cost, most reproducible method capable of the required quality:

1. No model: direct source reference, deterministic validation, schema checks, hashing, exact computation.
2. Deterministic computation: parsing, normalization, statistics, classification rules, templates, validators.
3. Local AI model: extraction, summarization, classification, candidate phrasing when deterministic methods are insufficient and output remains gated.
4. Frontier LLM: high-ambiguity architecture/evidence reasoning, difficult contradiction analysis, template design, or review tasks that local/deterministic methods cannot handle.

## 3. Default method by task type

| Task | Default route | Frontier allowed? |
| --- | --- | --- |
| Hashing/fingerprinting | Deterministic only | No. |
| Schema/package validation | Deterministic only | No. |
| Statistical characterization | Deterministic computation | No for computation; maybe for review explanation, not output authority. |
| Evidence-source classification | Deterministic rules/template first; local model if ambiguous. | Only if ambiguity affects architecture or acceptance. |
| Source text extraction | Deterministic parser/OCR first; local model if structure is irregular. | Only after local/model-free failure or high-stakes ambiguity. |
| Candidate statement phrasing | Template/local model. | Allowed with justification; output remains candidate. |
| Contradiction discovery | Deterministic search + templates first; local model for semantic matching. | Allowed for high-ambiguity review, with retained context/output. |
| Lifecycle/governance acceptance | Human/governance decision with deterministic evidence. | Frontier may advise but cannot decide. |
| Architecture redesign | Local context + deterministic evidence first; frontier allowed for high-leverage governance. | Yes with context audit/justification. |

## 4. Frontier LLM justification requirements

A frontier LLM call is allowed only when at least one applies:

- deterministic and local routes cannot resolve ambiguity materially affecting package validity;
- the task is architecture/governance review, not routine generation;
- contradiction or boundary evaluation requires broad semantic judgment and stakes justify cost;
- user explicitly requests frontier reasoning;
- repeated local attempts failed and failure is recorded.

The package or task artifact must record:

- why deterministic/local methods were insufficient;
- exact task given to the model;
- context/prompt/template fingerprint;
- model/provider/date;
- output artifact hash or retained output reference;
- how deterministic validators and human review constrained the output;
- whether any generated statement depends on model output.

## 5. Local model usage requirements

Local models may assist only under these constraints:

- output is candidate or intermediate evidence, never direct evidence;
- prompt/template and model identifiers are fingerprinted;
- output is retained or hashed;
- deterministic validators check schema, boundaries, provenance, and unsupported inference;
- human or governance review handles acceptance where required;
- nondeterminism is declared.

## 6. No-model requirement

No model should be used for:

- arithmetic or statistical computation;
- hashing/fingerprinting;
- schema validation;
- exact metadata extraction available from structured sources;
- replay comparison;
- file/state/coherence checks;
- acceptance state mutation.

## 7. Monitoring metrics for future implementation

When generation begins, KnowledgeForge should track:

- number of packages by route: deterministic, local, frontier;
- frontier calls per accepted package;
- token/cost estimate by package;
- percent of model-assisted outputs rejected or edited;
- validator blocker rates by route;
- reproducibility failures by route;
- contradiction discovery rate;
- package replay success rate;
- manual review burden.

These metrics should guide whether local models reduce frontier usage without lowering package quality.

## 8. Routing anti-patterns

Reject workflows that:

- ask a frontier LLM to "generate knowledge" from broad context without explicit evidence references;
- use local models to bypass evidence/source contracts;
- omit prompt/model fingerprints because the model is local;
- use models for deterministic computation;
- treat polished wording as higher confidence;
- use frontier LLMs because templates/validators have not yet been built.
