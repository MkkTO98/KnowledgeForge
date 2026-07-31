# R-20260730 First Bounded Evidence Portfolio Production Pilot

Status: complete — successful bounded production pilot
Classification: production success with bounded implementation and verification-ripple correction; no architecture, doctrine, ontology, PostgreSQL-schema or cross-project change
Task: `T-20260730-first-bounded-evidence-portfolio-production-pilot`

## Executive outcome

KnowledgeForge executed its first machine-executable Evidence Portfolio through the accepted canonical package architecture. The canary passed, the pre-registered production wave continued in the same task, and two canonical `KnowledgeObjectPackage` objects were promoted append-only. The portfolio yielded 56 deterministic Evidence-Card-equivalent operational views from two source series; those views are not canonical objects and are not counted as independent knowledge packages.

Canonical repository state advanced from 560 to 562 packages with fingerprint `sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff`.

## 1. Family selection

Selected family: retained Campaign 40 WDI Health pair for Norway, 1990–2024:

- `SP.DYN.LE00.IN` — life expectancy at birth, years;
- `SH.DYN.MORT` — under-five mortality, per 1,000 live births.

Selection was frozen before new outcome calculation in `selection_rubric.json`. The source registry exposed eight eligible pre-existing Campaign 40 candidate pairs spanning seven topical families. Seven non-Health candidate pairs, spanning six families, were excluded before calculation because the pilot required one semantically coherent family. Health was selected because the retained pair was mature/admitted, locally durable, fully covered in admission metadata, territory/period consistent, denominator-explicit, low-cost, and useful for non-comparative baseline characterization. No source acquisition, live MacroForge query, or outcome-based selection occurred.

Known limitations were pre-registered: mutable upstream WDI vintage, modeled-estimation dependence, finite non-random annual sequences, non-inferential slopes/differences, and the difference between canonical decimal representation and measurement precision.

## 2. Pre-registered universe and exclusions

Manifest: `portfolio_manifest.json`

- Manifest candidates: 3.
- Executable candidates: 2.
- Expected pre-execution exclusion: 1.
- Campaign: `evidence-portfolio-pilot-health-baseline-20260730`.
- Bundle: `bundle-health-norway-annual-1990-2024-v1`.
- Maximum raw result records: 56.
- Maximum promoted objects: 2.

The excluded candidate was a life-expectancy compound annual growth calculation. It was rejected before execution because a CAGR could misleadingly imply an accumulation process for this health-state level series. It was not replaced after outcomes were observed.

Each executable entry froze input path and SHA-256, normalized fingerprint, indicator, territory, observational population, denominator/applicability basis, unit, annual 1990–2024 grain, transformations, method parameters, dependencies, bundle/campaign membership, budget, validation and promotion gates, stopping rules, and stable identity inputs.

## 3. Executed characterization classes

Each source series produced exactly 28 valid result records across six baseline classes:

- coverage and missingness: 5;
- sample and period descriptors: 5;
- level distribution: 8;
- adjacent first differences: 6;
- finite-window linear time-index descriptors: 2;
- variability/stability descriptors: 2.

No relationship calculation, correlation, significance test, causal claim, forecast, stationarity claim, all-pairs exploration, advanced statistical method or new canonical ontology was introduced.

## 4. Complete accounting

| Category | Canary | Production wave |
|---|---:|---:|
| Manifest candidates | 2 | 3 |
| Executed candidates | 1 | 2 |
| Valid candidates | 1 | 2 |
| Raw calculation results | 28 | 56 |
| Valid result records | 28 | 56 |
| Promoted canonical objects | 1 | 2 |
| Operational Evidence-Card-equivalent views | 28 | 56 |
| Distinct source series | 1 | 2 |
| Distinct transformations | 3 | 3 |
| Evidence Bundles | 1 | 1 |
| Dependency clusters | 1 | 2 |
| Rejected/pre-execution excluded candidates | 1 | 1 |
| Null candidates | 0 | 0 |
| Redundant candidates | 0 | 0 |
| Redundant result records | 0 | 0 |
| Execution failures | 0 | 0 |

The nominal 56 views therefore represent 56 distinct result-record semantics grouped into two canonical objects, not 56 independent canonical claims or packages.

## 5. Canary and rerun result

Canary: life expectancy baseline package plus the expected CAGR exclusion.

Result: PASS. The complete admitted-input → manifest → calculation → validation → canonical object → promotion → views → isolated projection → rerun path passed.

Canary calculation fingerprint matched exactly across reruns: `sha256:79fff1288b014e30e3fb560aea75b46824a2beabdd9a608f643799c93632c581`.

Production reruns also matched exactly:

- life expectancy: `sha256:79fff1288b014e30e3fb560aea75b46824a2beabdd9a608f643799c93632c581`;
- under-five mortality: `sha256:814aebef9011651051a314cbd65c72e30155d00934b36d1e30b52c835a701da8`.

Input hashes before and after calculation were identical. Promotion was append-only and rerun persistence was idempotent.

## 6. Promoted canonical knowledge

1. `pkg-object-eppilot-health-sp-dyn-le00-in-nor-1990-2024-baseline-v1`
   - 35/35 observations; coverage 1.0.
   - Retained-sequence level range: 76.537317073171 to 83.209756097561 years.
   - Mean: 80.276668989547 years; median: 80.39512195122 years.
   - 1990-to-2024 net level difference: +6.623658536585 years.
   - Finite-window OLS calendar-year slope descriptor: +0.207010589602 years/year.
   - Mean absolute adjacent annual difference: 0.241097560976 years/year.

2. `pkg-object-eppilot-health-sh-dyn-mort-nor-1990-2024-baseline-v1`
   - 35/35 observations; coverage 1.0.
   - Retained-sequence level range: 2.4 to 8.7 per 1,000 live births.
   - Mean: 4.125714285714; median: 3.7 per 1,000 live births.
   - 1990-to-2024 net level difference: −6.2 per 1,000 live births.
   - Finite-window OLS calendar-year slope descriptor: −0.155854341737 per 1,000 live births/year.
   - Mean absolute adjacent annual difference: 0.188235294118 per 1,000 live births/year.

These are bounded descriptive facts about retained annual sequences. They do not explain causes, establish persistence or stationarity, predict future values, compare the two series, or imply policy/investment conclusions.

## 7. Redundancy and identity controls

Stable semantic fingerprints include source, indicator, territory, period, applicability, method, transformation, class and metric. Exact duplicate semantics are rejected. Reusing one semantic identity with a different value fails closed as an identity collision. Views are derived from result records and are explicitly typed `EvidenceCardEquivalentView`; they are not `KnowledgeObjectPackage` objects. No duplicate promotion or canonical overwrite occurred.

## 8. Production cost and review burden

An isolated full production rerun of both candidates, including duplicate calculation comparison, package construction, 56 views and temporary repository persistence, took 0.07 seconds elapsed, 97% CPU and 21,184 KiB maximum RSS.

Compute cost is negligible at this scale. Human/governance review is the binding cost: two denominator/applicability analyses, one inapplicable-method exclusion, six characterization classes per series, 56 result-record views, package limitations, and projection/consumer adequacy. Scaling should therefore batch by coherent family while reviewing applicability at the series/method boundary, not treat the view count as a quota.

## 9. PostgreSQL projection compatibility

Result: PASS using disposable isolated PostgreSQL databases. No persistent/default PostgreSQL projection database was mutated. Disposable databases were created, rebuilt, verified and removed; the canonical filesystem knowledge repository was intentionally extended append-only from 560 to 562 packages.

The authoritative 562-package filesystem repository rebuilt into `knowledgeforge_projection`, verified with no missing/extra/payload/fingerprint failures, and returned both pilot packages by evidence family. Canonical JSONB lookup preserved indicator, territory, period, method, transformation, applicability basis, bundle/family and lifecycle state. Existing direct filters support evidence family, statement type, lifecycle state and package fingerprint.

Narrow limitation: indicator, territory, period, method, transformation and applicability are retrievable from canonical payload JSONB but are not all first-class generic filter arguments. This did not block the pilot and does not justify a second projection architecture.

## 10. Consumer and InsightForge compatibility

Direct canonical-package and read-only projection consumption are content-adequate without recalculation: both expose exact results, applicability, lineage, method, limitations, lifecycle and fingerprints.

The current `knowledgeforge_relationship_export_v1` contract is not semantically adequate for this portfolio because it is relationship-specific; its relationship metadata fields are inapplicable to baseline characterization even though it preserves the full canonical package. No accepted general InsightForge adapter contract was found. Therefore an InsightForge-specific compatibility claim remains unsupported. No InsightForge or other project was changed.

## 11. Verification

Focused pilot tests:

- 18 tests passed, including manifest determinism, stable identity, reproducibility, accounting, duplicate/collision handling, null/rejection/failure separation, applicability, input immutability, promotion gating, idempotence, isolated PostgreSQL projection and unrelated-path preservation.

Adversarial checks included manifest tampering, result-identity collision, duplicate semantics, incomplete promotion and changed unrelated paths. All failed closed as intended.

Repository-wide tests:

- initial run: 354 tests with 4 failures and 16 errors, all classified as canonical-baseline ripple or stale-live-projection test coupling after the legitimate 560→562 append;
- bounded correction: historical campaign gates retained legacy baselines and added the accepted 562-package state; relationship-export tests were isolated from live PostgreSQL;
- pre-closeout verification run: 354 tests passed in 34.312 seconds;
- final authoritative post-closeout run: 354 tests passed in 32.900 seconds.

Additional projection verification rebuilt and verified all 562 packages in a disposable database. Repository-wide coherence, context-health, architecture audit and final preservation evidence are recorded in closeout/handoff artifacts.

## 12. Architecture sustainability conclusion

Outcome classification: successful production pilot with no architectural contradiction.

The accepted architecture sustained deterministic portfolio production by composing existing candidate-registry evidence, canonical package validation/persistence, operational views and bounded projection. No parallel portfolio subsystem or ontology was required. The pilot demonstrates that baseline portfolios can be produced cheaply and reproducibly, with complete exclusions/accounting, while keeping canonical object count distinct from operational view count.

KnowledgeForge is ready for another bounded baseline-characterization portfolio and for gradual progress within the approximately 100-view planning envelope. It is not evidence for indiscriminate 1,000-output expansion, unrestricted statistics, or treating each view as independent knowledge.

## 13. Residual limitations and next task

Residual limitations:

- one family, one territory and two series are insufficient to establish broad family-level production maturity;
- no null or execution failure occurred naturally, though tests prove separate fail-closed handling;
- exact-duplicate and identity-collision behavior was adversarially tested rather than encountered in production;
- semantic review, not computation, will dominate larger portfolios;
- the generic projection filter API is narrower than payload content;
- no general non-relationship export/InsightForge adapter contract exists.

Smallest justified next task, not activated: pre-register and execute a second bounded baseline-characterization portfolio over the already admitted Campaign 40 Infrastructure pair for Sweden, with explicit technology-era applicability/structural-break limitations and the same canary, accounting and promotion gates. Do not create an adapter or generalized export contract unless actual consumer work is separately prioritized.

## 14. Governance disposition

No decision artifact was created because the pilot did not change settled architecture, doctrine, scope, ontology, package schema or projection schema. The canonical repository manifest/index/evolution files are the authoritative registry update. The task, roadmap, production evolution log, state, handoff and affected summaries are updated for continuity.

## 15. Exact working-tree and preservation result

Branch `main` remains at `3b8eacce73e0b460d940ef9b1fcfea9d719f6a72`, exactly aligned with `origin/main` (ahead 0, behind 0), with zero staged files. The final task-owned status delta contains 64 records: 35 modified tracked files and 29 task-owned untracked files. Full path identities and SHA-256 values are retained in `/tmp/knowledgeforge-evidence-portfolio-pilot-20260730/final_preservation.json`.

After excluding the recorded task allowlist/amendments, the pre-task and final trees each contain exactly 485 unrelated dirty status records. Their NUL-delimited status/path/staging populations are identical, with no removed, changed or added record. Baseline raw-status fingerprint: `26790546ddee454caea849ebaa45b6bc24fd64d195288a016bbaca285d11ef82`; final complete raw-status fingerprint: `83e38c6275d066bc89bb16e1448a991ec54811edbceb7dc20d4ea56a45c5de4c`.

Two preservation-proof limitations are explicit rather than hidden. First, preflight retained complete raw status/path identity but not byte hashes for every pre-existing dirty file, so exact unrelated status/path/staging preservation is proven while independent byte-for-byte content preservation of those pre-existing files cannot be proven from the retained baseline. Second, the final report was absent at task start and is task-owned, but its normal `R-...md` name differed from the prospectively listed report-directory placeholder; allowlist amendment v4 records this retrospective discrepancy.

Final structural verification: Architecture-to-Reality Audit 0 blocks/0 warnings; coherence and context health 0 blocks, with advisory warnings only for `state/architecture.md` approaching its size limit and stale task-specific `context/active_context.md`.
