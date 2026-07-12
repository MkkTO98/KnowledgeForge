# Knowledge Repository Architecture

Date: 2026-07-09
Status: operational architecture for persisted KnowledgeForge objects
Scope: file-backed persistence of validated KnowledgeObjectPackages

## 1. Purpose

The Knowledge Repository is the canonical operational destination for validated KnowledgeForge Knowledge Objects.

Reports remain governance, evidence, audit, and closeout artifacts. The repository is the operational materialization of accepted reusable knowledge.

## 2. Authoritative doctrine preserved

This architecture preserves unchanged:

- `CONSTITUTION.md`
- `docs/production_doctrine.md`
- `docs/architecture.md`
- accepted architectural decisions under `artifacts/decisions/`
- `docs/knowledge_package_contract.md`
- `docs/validation_framework_v1.md`
- `docs/validator_taxonomy.md`
- `docs/provenance_fingerprinting.md`
- WDI Demographic Family Closeout Report
- WDI Environment Family Closeout Report
- Production Methodology Closeout Report
- Phase 2 Production Expansion Strategy

Continuity classification: preserves agreed architecture.

## 3. Architectural boundary

The repository contains only KnowledgeForge-owned concepts.

It does not know, mirror, adapt, synchronize with, or couple to any other EIP project. It stores KnowledgeForge KnowledgeObjectPackages, not external objects.

It introduces no runtime service, API, adapter, shared schema, synchronization layer, database dependency, cache layer, local model generation, or frontier model generation.

## 4. Canonical representation

The canonical persisted object representation is the existing validated `KnowledgeObjectPackage` JSON.

The repository does not redesign the package model. It persists packages exactly as produced by the validated production methodology.

Repository metadata, indexes, and evolution records are stored separately from package files so the package contract remains unchanged.

## 5. Repository layout

```text
knowledge_repository/
  manifest.json
  objects/
    <package_id>.json
  indexes/
    by_package_id.json
    by_knowledge_identity.json
    by_evidence_family.json
    by_statement_type.json
    by_lifecycle_state.json
    by_package_manifest_fingerprint.json
  evolution/
    <package_id>.json
```

## 6. Persistence strategy

Persistence is deterministic, local, file-backed JSON.

- `objects/` stores exact KnowledgeObjectPackage JSON.
- `indexes/` stores deterministic retrieval maps derived from package content.
- `evolution/` stores extracted evolution/provenance/fingerprint/validation metadata for audit convenience.
- `manifest.json` records repository schema version, object count, package ids, index files, persistence policy, and repository fingerprint.

The repository is append/update-by-package-id at the file level. A repeated write of the same package content is idempotent.

## 7. Object identity

The primary persisted package identity is `package_id`.

Knowledge identity is derived from each `generated_statements[*].statement_id` and indexed to package ids. This preserves the existing package model while allowing retrieval by durable statement identity.

No new object identity scheme is introduced.

## 8. Indexing strategy

Initial deterministic indexes are:

- package id → object file path;
- knowledge statement id → package id list;
- evidence family → package id list;
- statement type → package id list;
- lifecycle state → package id list;
- package manifest fingerprint → package id list.

Indexes are derived operational conveniences, not canonical semantic authority.

## 9. Version and evolution tracking

Version and evolution are preserved from package fields:

- `package_version`;
- `status`;
- `lineage`;
- `evolution_metadata`;
- `validation_state`;
- `provenance_envelope`;
- `fingerprints`;
- lifecycle and reproducibility states.

The `evolution/` directory materializes these fields in one audit-oriented record per package without changing the package.

## 10. Provenance and fingerprint persistence

The repository preserves complete package-level provenance and fingerprints by storing the full package unchanged.

The manifest adds a repository fingerprint computed from package ids, canonical package fingerprints, and index content. This fingerprint is a repository-materialization fingerprint, not a replacement for package fingerprints.

## 11. Retrieval conventions

Consumers or future internal tools should retrieve knowledge by reading:

1. `manifest.json` to inspect repository version and fingerprint;
2. an index file under `indexes/` to find package ids;
3. exact packages under `objects/`;
4. optional audit convenience records under `evolution/`.

This is a file convention, not an API.

## 12. Knowledge category neutrality

The repository is for all validated Knowledge Objects.

It does not special-case correlations, classifications, coverage knowledge, deterministic derived relationships, provenance knowledge, methodological knowledge, or future deterministic categories. All use the same package persistence model.

## 13. Standard operational behaviour recommendation

Future production families should populate the Knowledge Repository as their primary operational output while continuing to generate reports as governance artifacts.

Classification: preserves agreed architecture.
