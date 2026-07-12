# Knowledge Repository Persistence Specification

Date: 2026-07-09
Status: operational persistence specification
Implementation: `tools/knowledge_repository.py`
Repository root: `knowledge_repository/`

## 1. Purpose

This specification defines the minimum deterministic persistence capability for validated KnowledgeForge Knowledge Objects.

It persists the existing KnowledgeObjectPackage model. It does not redesign production, packages, validators, taxonomy, provenance, fingerprints, or governance.

## 2. Accepted input

Input must be one validated `KnowledgeObjectPackage` or a JSON list of validated `KnowledgeObjectPackage` objects.

A package is persistable only when:

1. `package_kind == "KnowledgeObjectPackage"`;
2. `validation_state.validation_result == "pass"`;
3. `validation_state.blockers` is empty;
4. `provenance_envelope` is present;
5. `fingerprints` is present;
6. `confidence_quality.lifecycle_state` is present;
7. `confidence_quality.reproducibility_state` is present;
8. every generated statement has `statement_id`.

Invalid packages are rejected before persistence.

## 3. Persistence command

```bash
python3 tools/knowledge_repository.py <knowledge_object_packages.json> --repository-root knowledge_repository
```

The command writes or rewrites deterministic files under the repository root and prints a JSON result containing:

- repository root;
- persisted count;
- rejected count;
- total object count;
- repository fingerprint;
- manifest path.

## 4. Stored package invariant

Each package is written exactly to:

```text
knowledge_repository/objects/<package_id>.json
```

The persisted object file must equal the input package JSON after canonical parse/write. No wrapper, projection, schema conversion, source-specific mapping, or consumer-specific representation is inserted into the object file.

## 5. Manifest

`knowledge_repository/manifest.json` records:

- repository kind: `KnowledgeForgeKnowledgeRepository`;
- schema version;
- repository root;
- object count;
- package ids;
- index files;
- object and evolution directories;
- repository fingerprint;
- persistence policy.

The repository fingerprint is deterministic over package ids, package content fingerprints, and index content.

## 6. Indexes

The implementation writes:

- `indexes/by_package_id.json`
- `indexes/by_knowledge_identity.json`
- `indexes/by_evidence_family.json`
- `indexes/by_statement_type.json`
- `indexes/by_lifecycle_state.json`
- `indexes/by_package_manifest_fingerprint.json`

Indexes are derived from package content and sorted deterministically.

## 7. Evolution records

For each package, the implementation writes:

```text
knowledge_repository/evolution/<package_id>.json
```

The evolution record contains only extracted package fields:

- package id;
- package version;
- status;
- lineage;
- evolution metadata;
- provenance envelope;
- fingerprints;
- validation state;
- lifecycle state;
- reproducibility state.

This is an audit convenience record, not a new canonical package type.

## 8. Reproducibility

Persistence is reproducible when the same package set produces the same repository fingerprint and equivalent files.

The implementation is deterministic and has no network access, external-service dependency, random seed, runtime service, API, adapter, database, cache, synchronization process, or model call.

## 9. Future-family rule

Future production families should populate this repository after KnowledgeObjectPackage validation passes. Reports remain required governance artifacts, but persisted Knowledge Objects become the primary operational output.

Classification: preserves agreed architecture.
