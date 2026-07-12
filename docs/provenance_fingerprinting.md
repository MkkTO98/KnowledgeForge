# Provenance Envelope and Fingerprinting Specification

Date: 2026-07-09
Status: architecture specification; implementation not authorized

## 1. Purpose

KnowledgeForge reproducibility depends on knowing exactly what inputs, evidence, computations, templates, models, and validators produced each package. Fingerprints prioritize auditability over convenience.

This document specifies the conceptual provenance envelope and fingerprint targets. It does not mandate a storage backend or implement hashing code.

## 2. Provenance envelope

Every KnowledgeForge package should include a provenance envelope containing:

- package identity and version;
- generation timestamp/date;
- creator: human, tool, model, or process;
- source system(s) and source owners;
- evidence references and source-family classification;
- input dataset/query/template/model identifiers;
- computation recipe and parameters;
- generated intermediate identifiers;
- validation tool/version and results;
- governance review actor/status;
- environment/toolchain notes where material;
- known nondeterminism and mitigation;
- reproducibility state.

## 3. Fingerprint targets

### 3.1 Input datasets

Fingerprint the exact dataset or extract used, not merely its name.

Required where applicable:

- source system and dataset identifier;
- source version/vintage/release date;
- source package/export/snapshot/run identifier where applicable;
- row/column schema or manifest;
- content hash or upstream package fingerprint;
- filter/window/frequency/unit selections;
- missingness profile when material.

### 3.2 Query definitions

Queries must be fingerprinted independently from query results.

Required where applicable:

- normalized query text or structured query spec;
- parameters;
- database/schema/source version assumptions;
- execution context;
- expected output schema;
- query hash.

A changed query is a changed method even if output currently matches.

### 3.3 Computation recipes

Fingerprint deterministic computation methods:

- algorithm name and version;
- source code file/commit or script hash when implemented;
- parameters;
- transformation sequence;
- random seed or nondeterminism declaration;
- dependency/tool versions when material;
- recipe hash.

### 3.4 Prompts/templates

If a prompt or template is used, fingerprint:

- template identifier;
- template version;
- full prompt text or rendered prompt artifact;
- included context manifest;
- system/instruction context relevant to output;
- prompt hash.

Prompt fingerprints are required even when using local models. A model-assisted candidate without retained prompt/template context cannot become accepted knowledge.

### 3.5 Local model identifiers

If a local model is used, record:

- model family/name;
- exact model file or registry identifier;
- quantization/variant;
- checksum if available;
- inference engine and version;
- decoding parameters;
- hardware/backend if material;
- seed/nondeterminism settings;
- output artifact hash.

Local model output is candidate material, not direct evidence.

### 3.6 Frontier LLM identifiers

If a frontier LLM is used, record:

- provider;
- model identifier;
- date/time;
- prompt/template/context hashes;
- relevant routing justification;
- output hash;
- human review requirement;
- cost/token estimate when available.

Frontier output must be retained as an intermediate artifact if it materially influenced a package.

### 3.7 Generated packages

Package fingerprint should cover:

- package manifest;
- generated statements;
- evidence reference list;
- computation recipe references;
- contradiction records;
- validation results;
- evolution metadata;
- schema/contract version.

### 3.8 Evidence snapshots

Evidence snapshots should capture:

- source URL/path/identifier;
- retrieval/capture date;
- content hash;
- license/access note if relevant;
- normalized text/table hash if normalization occurs;
- raw snapshot hash when available;
- transformation from raw to normalized snapshot.

## 4. Fingerprint rules

1. Prefer canonical serialization before hashing.
2. Hash manifests and components separately so changes are diagnosable.
3. Do not rely only on timestamps or file names.
4. Record unavailable fingerprints explicitly as missing, not silently omitted.
5. A changed input/query/recipe/template/model/validator may produce a new package revision even if generated statements are unchanged.
6. Fingerprint mismatches require an evolution/change report or block acceptance.

## 5. Reproducibility states

| State | Meaning |
| --- | --- |
| reproducible | Inputs, recipe, templates/models if any, and validation are available and replayable. |
| replayable-with-external-dependency | Replay depends on accessible external system but version/fingerprint is recorded. |
| audit-only | Evidence can be inspected but not fully replayed. |
| non-reproducible-candidate | Candidate retained but cannot be accepted. |
| broken-lineage | Required reference/fingerprint cannot be resolved or conflicts. |

Only reproducible or explicitly justified replayable-with-external-dependency packages may become accepted generated knowledge.
