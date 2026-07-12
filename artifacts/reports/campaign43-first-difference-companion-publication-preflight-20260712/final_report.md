# Campaign 43 Companion Package Publication Preflight Final Report

Date: 2026-07-12
Status: preflight completed; superseded by authorized canonical publication on 2026-07-12

## Outcome

Exactly six Campaign 43 first-difference Pearson companion KnowledgeObjectPackage candidates were constructed outside the canonical repository and validated for publication readiness.

No canonical package publication, manifest/index/evolution mutation, PostgreSQL mutation, Relationship Export publication, staging, commit, or push occurred during this preflight. A later separately authorized Campaign 43 canonical publication performed those publication steps and is recorded under `artifacts/reports/campaign43-canonical-publication-20260712/`.

## Package set

Package-set fingerprint: `sha256:9ed161b9dcf7472b7e13979cbd9cd1a24f1ce3009108e677c41dace20277d559`

| Package | Fingerprint | Coefficient | Aligned transformed observations |
|---|---:|---:|---:|
| `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-first-difference-pearson-companion-v1` | `sha256:5dfcca7a3b90bf8ab058f20b32555145c684fa004140ad457d67fc3dd222db14` | `-0.018892915467` | 33 |
| `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-first-difference-pearson-companion-v1` | `sha256:46365f326c989e8aed78efc51e3d561a0ec77a2a6057949cbc854988240449a6` | `0.058190335423` | 33 |
| `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-first-difference-pearson-companion-v1` | `sha256:ca97d74262e76130c23c52267141fb2d00c0ad5b00706062fb054c731890aa2d` | `-0.101990610667` | 33 |
| `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-first-difference-pearson-companion-v1` | `sha256:c12ceeff3a8bf73f5c9e4cd84e8d051e5ffdaa3483213c1b5b2da502ba3a103b` | `0.037781664561` | 33 |
| `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-first-difference-pearson-companion-v1` | `sha256:75471a45ea8de19abf7dc0718a82d13598d754fbabac8c498665b94229696d0b` | `-0.083376899169` | 33 |
| `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-first-difference-pearson-companion-v1` | `sha256:f63c6055b35b3fb92dd8d485639f5b98acc14a26014a0eed8502b006b8edf4d2` | `0.3855860099` | 31 |

All six package validations passed.

## Publication preflight

A safe temporary-copy dry run computed expected publication effects without mutating `knowledge_repository/`:

- expected post-publication package count: 560
- expected post-publication repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- expected PostgreSQL projected package count: 560
- expected Relationship Export counts: raw Pearson 21; first-difference Pearson 14

Publication would add the six candidate package JSON files under `knowledge_repository/objects/`, add six evolution files, and modify only canonical manifest/index files recorded in `publication_preflight.json`.

## Interpretation treatment

Each package states that the raw Campaign 41 package is not superseded. Raw-level Pearson and first-difference Pearson are separate estimands. First differencing changes the estimand to annual-change co-movement and discards one observation before missing-value alignment.

Near-zero coefficients are retained as bounded robustness/limiting evidence. No package claims causality, prediction, structural interpretation, independence, statistical significance, investment relevance, or proof of absence of any relationship. The `0.3855860099` Norwegian result remains descriptive association evidence only.

## Verification

- 49 targeted unittest tests passed.
- Canonical repository validation passed: 554 packages, validation errors `[]`, fingerprint unchanged.
- `git diff --check` passed.
- Coherence and context health passed with only the stale generated `context/active_context.md` warning after concise handoff update.
- Architecture-to-reality audit passed: 0 blocks, 0 warnings.
- Repository-wide durability/sensitive validator exit 0, sensitive scan passed, actual secret blockers 0, unsafe absolute path dependencies 0. Validator decision remained D because untracked recovery-critical files and operational checkpoint state are not machine-loss durable until committed/backed up.

## Boundary and residue

Unrelated tracked deletions under `architecture/architectureharvest/` were preserved and unstaged. Pre-existing operational/checkpoint/report residue, `workspace_config.yaml`, caches, generated active context, dumps, restore copies, temporary verification artifacts, and the previously blocked temp path were not cleaned or resolved.
