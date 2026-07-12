# T-20260712 Campaign 43 Canonical Publication, PostgreSQL Projection, and Export Closeout

Status: completed; committed/push pending until Git publication step
Date: 2026-07-12

## Objective

Publish exactly six verified Campaign 43 first-difference Pearson companion packages append-only into the canonical Knowledge Repository, rebuild the established KnowledgeForge PostgreSQL projection, verify Relationship Export behavior, and close Campaign 43 without changing architecture, doctrine, schema, method family, or existing package bytes.

## Published packages

Exactly six canonical object files were added under `knowledge_repository/objects/`:

1. `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-first-difference-pearson-companion-v1` — `sha256:5dfcca7a3b90bf8ab058f20b32555145c684fa004140ad457d67fc3dd222db14`
2. `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-first-difference-pearson-companion-v1` — `sha256:46365f326c989e8aed78efc51e3d561a0ec77a2a6057949cbc854988240449a6`
3. `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-first-difference-pearson-companion-v1` — `sha256:ca97d74262e76130c23c52267141fb2d00c0ad5b00706062fb054c731890aa2d`
4. `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-first-difference-pearson-companion-v1` — `sha256:c12ceeff3a8bf73f5c9e4cd84e8d051e5ffdaa3483213c1b5b2da502ba3a103b`
5. `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-first-difference-pearson-companion-v1` — `sha256:75471a45ea8de19abf7dc0718a82d13598d754fbabac8c498665b94229696d0b`
6. `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-first-difference-pearson-companion-v1` — `sha256:f63c6055b35b3fb92dd8d485639f5b98acc14a26014a0eed8502b006b8edf4d2`

Package-set fingerprint: `sha256:9ed161b9dcf7472b7e13979cbd9cd1a24f1ce3009108e677c41dace20277d559`

## Canonical result

- package count: 560
- repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- six evolution records added, one per package
- manifest and canonical indexes updated deterministically by `tools/knowledge_repository.py`
- deterministic/idempotent rerun of the publication mechanism produced no further diff
- no existing canonical object changed
- no Campaign 40-42 package changed

## PostgreSQL projection

Target database was confirmed as KnowledgeForge-owned before mutation:

- database: `knowledgeforge`
- schema: `knowledgeforge_projection`
- prior active projection count/fingerprint: 554, `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`
- non-KnowledgeForge projection-table schemas: `[]`

Projection rebuild result:

- projected package count: 560
- missing package IDs: none
- extra package IDs: none
- payload-fidelity failures: 0
- package-fingerprint failures: 0
- repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- all six Campaign 43 packages retrievable

## Relationship Export

Verified through `tools/relationship_export_v1.py` and independent `tools/relationship_export_consumer_simulator_v1.py`:

- all relationships: 35
- raw Pearson: 21
- first-difference Pearson by method: 14
- first-difference Pearson by transformation: 14
- raw/first-difference overlap: none
- all six Campaign 43 packages appear in first-difference method and transformation retrieval
- no Campaign 43 first-difference package appears in raw retrieval
- source lineage, method, transformation, temporal scope, coefficient, limitations, and non-supersession state remain exposed

## Interpretation

Five coefficients are near zero or weak after differencing. The approximately `0.3855860099` result remains descriptive, finite-window, non-causal association evidence only. Weakened transformed relationships are retained as robustness/limiting evidence. Raw Campaign 41 packages remain current and are not superseded.

## Classification

Bounded append-only canonical publication and operational projection refresh. No doctrine, architecture, schema, PostgreSQL schema, Relationship Export Contract, KnowledgeObjectPackage design, or method-family change.
