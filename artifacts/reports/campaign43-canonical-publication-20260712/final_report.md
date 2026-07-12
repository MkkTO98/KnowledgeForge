# Campaign 43 Canonical Publication Final Report

Date: 2026-07-12
Status: completed locally; Git publication pending until commit/push step

## Outcome

Campaign 43 published exactly six first-difference Pearson companion KnowledgeObjectPackages append-only into the canonical Knowledge Repository.

Canonical result:

- package count: 560
- repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- package-set fingerprint: `sha256:9ed161b9dcf7472b7e13979cbd9cd1a24f1ce3009108e677c41dace20277d559`

No existing canonical package changed. Campaign 40-42 packages are unchanged. Campaign 41 raw source packages remain accepted and non-superseded.

## Packages

| Package | Manifest fingerprint | Coefficient | Count |
|---|---:|---:|---:|
| `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-first-difference-pearson-companion-v1` | `sha256:5dfcca7a3b90bf8ab058f20b32555145c684fa004140ad457d67fc3dd222db14` | `-0.018892915467` | 33 |
| `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-first-difference-pearson-companion-v1` | `sha256:46365f326c989e8aed78efc51e3d561a0ec77a2a6057949cbc854988240449a6` | `0.058190335423` | 33 |
| `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-first-difference-pearson-companion-v1` | `sha256:ca97d74262e76130c23c52267141fb2d00c0ad5b00706062fb054c731890aa2d` | `-0.101990610667` | 33 |
| `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-first-difference-pearson-companion-v1` | `sha256:c12ceeff3a8bf73f5c9e4cd84e8d051e5ffdaa3483213c1b5b2da502ba3a103b` | `0.037781664561` | 33 |
| `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-first-difference-pearson-companion-v1` | `sha256:75471a45ea8de19abf7dc0718a82d13598d754fbabac8c498665b94229696d0b` | `-0.083376899169` | 33 |
| `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-first-difference-pearson-companion-v1` | `sha256:f63c6055b35b3fb92dd8d485639f5b98acc14a26014a0eed8502b006b8edf4d2` | `0.3855860099` | 31 |

## PostgreSQL projection

Before mutation, target identity was confirmed:

- database: `knowledgeforge`
- schema: `knowledgeforge_projection`
- previous active projection: 554 packages, repository fingerprint `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`
- no projection tables in non-KnowledgeForge schemas

After rebuild:

- projected packages: 560
- missing package IDs: 0
- extra package IDs: 0
- payload-fidelity failures: 0
- package-fingerprint failures: 0
- repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- all six Campaign 43 packages retrievable

## Relationship Export

Exports and independent consumer simulation passed:

- all relationships: 35
- raw Pearson: 21
- first-difference Pearson by method: 14
- first-difference Pearson by transformation: 14
- raw/first-difference overlap: none
- all six Campaign 43 packages in first-difference retrieval
- none of the six in raw retrieval
- method, transformation, temporal scope, coefficient, source-package lineage, limitations, and non-supersession state exposed

## Interpretation

Five coefficients are near zero or weak after differencing. The approximately `0.3855860099` result remains descriptive and non-causal. Weakened transformed relationships are retained as robustness/limiting evidence. No package claims causality, prediction, structural interpretation, independence, absence of relationship, statistical significance, recommendation, or investment signal.

## Classification

Bounded append-only production publication and projection refresh. No doctrine, architecture, KnowledgeObjectPackage schema, PostgreSQL schema, method-family, or Relationship Export Contract change.
