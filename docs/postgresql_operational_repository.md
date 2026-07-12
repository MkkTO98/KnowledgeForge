# PostgreSQL Operational Repository Projection

Status: first local implementation slice complete when verified against the local `knowledgeforge` database.

## Authority

Canonical authority remains exclusively with:

- `knowledge_repository/objects/*.json`

The PostgreSQL projection is KnowledgeForge-owned, operational, durable, derived, and rebuildable. It may not originate or mutate canonical knowledge. It is not co-authoritative and does not participate in canonical package or repository fingerprints.

## Database ownership and isolation

The local implementation uses a KnowledgeForge-owned PostgreSQL database:

- database: `knowledgeforge`
- owner on this host: `mkkto`
- schema: `knowledgeforge_projection`

The projection is not stored in MacroForge's database or schema. No shared EIP schema, shared database ownership, shared runtime code, InsightForge access, or consumer write path is introduced.

## Physical model

The first slice uses the smallest operational projection model needed for approved retrieval:

- `knowledgeforge_projection.projection_state`
  - projection identity, canonical repository fingerprint represented, canonical object count represented, tool version, status, validity, and logical projection fingerprint.
- `knowledgeforge_projection.projected_packages`
  - stable package identity, canonical package fingerprint, package manifest fingerprint, canonical filesystem pointer, evidence family, lifecycle state, payload hash, and lossless `jsonb` canonical payload.
- `knowledgeforge_projection.package_statement_types`
  - package-to-statement-type projection for approved statement-type filtering.
- `knowledgeforge_projection.provenance_lineage_edges`
  - only provenance and lineage relationships explicitly present in canonical packages.

No future statistical/correlation/covariance/lag/trend/mathematical schema is introduced in this slice.

## Rebuild and publication semantics

The first slice supports full rebuild only.

Rebuild behavior:

1. Enumerate canonical object files deterministically.
2. Validate manifest object count and package IDs against canonical package files.
3. Validate every package before publishing a new projection.
4. Build projection rows from canonical packages only.
5. Publish inside a PostgreSQL transaction.
6. Remove stale rows by replacing the previous projection state and dependent rows in one transaction.
7. Mark projection valid only after acceptance checks pass.
8. Verify projected count, package IDs, package fingerprints, payload fidelity, and logical projection fingerprint.

Failed, stale, or mismatched projections must not be used for PostgreSQL-backed retrieval.

## Freshness and failure behavior

PostgreSQL-backed retrieval first validates projection freshness against canonical repository state.

Freshness requires:

- active valid projection state;
- matching canonical repository fingerprint;
- matching canonical object count;
- matching projected row count;
- matching logical projection fingerprint.

If freshness cannot be proven, PostgreSQL-backed retrieval returns an explicit `stale_or_invalid_projection` result and does not silently fall back to filesystem reads. Canonical filesystem retrieval remains separately available through existing mechanisms.

## Supported operations

Implemented operations:

- deterministic full rebuild;
- projection verification;
- package-ID lookup;
- evidence-family filtering;
- statement-type filtering;
- lifecycle-state filtering;
- package-fingerprint filtering;
- provenance/lineage retrieval for explicit relationships present in canonical packages;
- database ownership/isolation evidence.

## Commands

Create/use the local KnowledgeForge-owned database:

```bash
python3 tools/postgresql_operational_projection.py --database knowledgeforge --create-database ensure-database
```

Rebuild projection:

```bash
python3 tools/postgresql_operational_projection.py --database knowledgeforge rebuild
```

Verify projection:

```bash
python3 tools/postgresql_operational_projection.py --database knowledgeforge verify
```

Lookup package:

```bash
python3 tools/postgresql_operational_projection.py --database knowledgeforge lookup pkg-object-srcpkg-campaign33-architectural-continuity-review
```

Filter by evidence family:

```bash
python3 tools/postgresql_operational_projection.py --database knowledgeforge filter --evidence-family external_wdi_annual_scalar_financial_sector_provenance_lineage
```

Filter by statement type:

```bash
python3 tools/postgresql_operational_projection.py --database knowledgeforge filter --statement-type methodological
```

Filter by lifecycle state:

```bash
python3 tools/postgresql_operational_projection.py --database knowledgeforge filter --lifecycle-state accepted
```

Retrieve explicit provenance/lineage edges:

```bash
python3 tools/postgresql_operational_projection.py --database knowledgeforge lineage pkg-object-srcpkg-campaign33-architectural-continuity-review
```

## Next gate

The next required gate is:

PostgreSQL Operational Projection Acceptance and Production-Sequencing Gate.

That later gate must decide whether this projection is sufficiently proven to permit deeper deterministic-knowledge production. It must not automatically authorize consumer access or ordinary breadth expansion.
