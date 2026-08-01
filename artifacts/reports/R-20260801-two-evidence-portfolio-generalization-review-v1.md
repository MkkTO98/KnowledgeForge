# R-20260801 — Two-Evidence-Portfolio Generalization Review v1

Status: complete; fully validated uncommitted publication candidate
Task: `T-20260801-two-evidence-portfolio-generalization-review-v1`
Decision: `D-20260801-two-evidence-portfolio-generalization-review-v1`
Classification: `provisionally generalizable with bounded corrections`

## Executive conclusion

Norway Health and Sweden Infrastructure provide credible but bounded evidence that the accepted KnowledgeForge Evidence Portfolio model is reusable for deterministic annual-scalar baseline characterization. The model preserved outcome-blind selection, applicability, exact retained-input lineage, content-bound canary continuation, canonical package/view separation, complete accounting, replay, append-only repository evolution, and projection fidelity across two domains with materially different measure semantics.

The evidence is not two independent replications of the whole framework. Both portfolios use retained Campaign 40 WDI fixtures, one production engine, one statistical-summary method, one canonical repository, one projection, identical two-candidate/56-record budgets, complete annual data, and the same operational-view path. Natural null, redundancy, failure, contradiction, disagreement, missingness and supersession paths were not exercised.

The review found concrete cross-portfolio conformance weaknesses: machine accounting collapses pre-execution exclusions into `rejected_candidates`; narrative artifacts misdescribe the executed exclusion candidates; manifest and produced-record transformation identifiers are not always identical; neither portfolio binds candidates to a substantive analytical-use question; and declared dependency clusters do not express shared provider/acquisition/method dependence strongly enough to prevent corroboration overclaims.

The required next step is one bounded framework correction before any third portfolio. It must leave both portfolios and all canonical objects unchanged. A later third portfolio should be deliberately divergent, not merely another complete annual WDI pair.

## 1. Authentication, recovery and preservation

Authenticated starting state:

| Property | Result |
|---|---|
| Repository | `/home/mkkto/srv/EIP/projects/KnowledgeForge` |
| Branch | `main` |
| HEAD | `ba1e2ae5a001a31550a7fca7732f9ce262dc0530` |
| `origin/main` | same |
| Ahead/behind | `0/0` |
| Parent | `4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3` |
| Published tree | `0415ea24e20c65780f67bb14c52aaaef967aa2e5` |
| Index | empty |
| Interrupted Git operation / lock | none |
| Expanded Git-visible records | 493 |
| Ignored records | 313 |
| Raw status fingerprint | `sha256:0278e7d02d2d76a3ca7aba15f4a4cd2d45893c68b015cc7bda1a1c878847422d` |
| Protected mixed live paths | 8/8 exact |
| Protected recovery aggregate | `sha256:65b021ab0474f48d9d897bdfc2b1b4d904055c3a1ae71702bba953d1178a03ab` |
| Concurrent KnowledgeForge mutator found | none identified in the initial preflight; resumed closeout later found a separate live Hermes process with KnowledgeForge as cwd |

Canonical repository authentication independently recomputed:

- Knowledge Objects: 564;
- evolution records: 564;
- indexes: 6;
- manifest and recomputed fingerprint: `sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67`;
- result: pass.

The preflight baseline and complete per-path identities are retained outside the repository at `/tmp/knowledgeforge-two-portfolio-generalization-review-20260801-v1/preflight_baseline.json`. This is supporting preservation evidence, not repository authority.

`context/active_context.md` was not treated as authority. Recovery used Git identity, durable task/decision/report/manifests, canonical indexes and package/evolution files.

## 2. Authenticated portfolio inventories

A complete hash/size inventory of 23 Norway production artifacts, 21 Sweden production artifacts, and the eight canonical object/evolution files is retained at `/tmp/knowledgeforge-two-portfolio-generalization-review-20260801-v1/authenticated_portfolio_inventory.json`.

### 2.1 Norway Health

Authoritative durable surfaces:

- task: `artifacts/tasks/T-20260730-first-bounded-evidence-portfolio-production-pilot.md`;
- report: `artifacts/reports/R-20260730-first-bounded-evidence-portfolio-production-pilot.md`;
- production root: `artifacts/production/evidence-portfolio-pilot-health-baseline-20260730/`;
- manifest: `portfolio_manifest.json`, ID `manifest-evidence-portfolio-pilot-health-baseline-v1`, version 1.0, fingerprint `sha256:7c5f85ffe0660d012915db2cbec240e02e2ad4c0ca61efa2ef44298e55dedc15`;
- canonical objects:
  - `knowledge_repository/objects/pkg-object-eppilot-health-sp-dyn-le00-in-nor-1990-2024-baseline-v1.json`, SHA-256 `d032ecc5469695208e5133a042757fe4c2a68c5dd5f4081d5e17a4c977d5d6e0`;
  - `knowledge_repository/objects/pkg-object-eppilot-health-sh-dyn-mort-nor-1990-2024-baseline-v1.json`, SHA-256 `85dc171c55bc078a1177d1f9915ce995f4a51e28e6b52f8b56df8bbab0bb9add`;
- matching evolution records:
  - `knowledge_repository/evolution/pkg-object-eppilot-health-sp-dyn-le00-in-nor-1990-2024-baseline-v1.json`;
  - `knowledge_repository/evolution/pkg-object-eppilot-health-sh-dyn-mort-nor-1990-2024-baseline-v1.json`.

### 2.2 Sweden Infrastructure

Authoritative durable surfaces:

- task: `artifacts/tasks/T-20260731-second-evidence-portfolio-sweden-infrastructure-v1.md`;
- report: `artifacts/reports/R-20260731-second-evidence-portfolio-sweden-infrastructure-v1.md`;
- production root: `artifacts/production/evidence-portfolio-infrastructure-sweden-baseline-20260731/`;
- manifest: `portfolio_manifest.json`, ID `manifest-evidence-portfolio-infrastructure-sweden-baseline-v1`, version 1.1, fingerprint `sha256:d59dfd9944f47aa81adf6b4bd9b5b9ddcde8551956545e21e0ab2ed34744db1f`;
- canonical objects:
  - `knowledge_repository/objects/pkg-object-eppilot-infrastructure-it-net-user-zs-swe-1990-2024-baseline-v1.json`, SHA-256 `9de940fbd99aee23df8d71c24476fcfc7edefb1e6dca60294fba2d2e315cada3`;
  - `knowledge_repository/objects/pkg-object-eppilot-infrastructure-it-cel-sets-p2-swe-1990-2024-baseline-v1.json`, SHA-256 `e5626e56ded8e8498b335c54932db0ca6806bab78dec049f064da069c5962d5c`;
- matching evolution records:
  - `knowledge_repository/evolution/pkg-object-eppilot-infrastructure-it-net-user-zs-swe-1990-2024-baseline-v1.json`;
  - `knowledge_repository/evolution/pkg-object-eppilot-infrastructure-it-cel-sets-p2-swe-1990-2024-baseline-v1.json`.

## 3. Campaign 43 `constructed_not_published`

The statement is operation-scoped and temporal. It refers to the Campaign 43 **preflight**, not the final status of Campaign 43.

- `artifacts/decisions/D-20260712-campaign43-companion-package-publication-preflight-accepted.md` accepted six candidate packages for local publication readiness and explicitly withheld canonical publication, projection, export publication, staging, commit and push.
- `tools/campaign43_first_difference_companion_publication_preflight.py` persisted candidate packages only into a temporary repository copy and reported `constructed_not_published`.
- `artifacts/decisions/D-20260712-campaign43-canonical-publication-accepted.md` later authorized and recorded the separate append-only canonical publication of exactly six packages, reaching 560 packages.

Therefore, it must not be used to characterize the overall Campaign 43 work as unpublished. It accurately describes one prior package-construction/preflight operation.

## 4. Portfolio-by-portfolio reconstruction

### 4.1 Norway Health

**Governing question and use.** The durable task asks whether a bounded Evidence Portfolio can traverse admitted input, preregistration, canary, deterministic calculation, validation, canonical promotion, operational views, projection and rerun. The substantive output is baseline description of retained Norway annual health series. No durable field binds candidates to a concrete health decision question. Evidence: task objective and gates; `selection_rubric.json`; manifest `expected_output_class`.

**Scope.** Norway (`NOR`), annual 1990–2024, 35 slots each:

- `SP.DYN.LE00.IN`, life expectancy at birth, years;
- `SH.DYN.MORT`, under-five mortality, per 1,000 live births.

**Population and denominator.** Both summarize finite retained annual sequences, not random samples. Life expectancy has no scaled event denominator; under-five mortality is explicitly per 1,000 live births. Evidence: manifest applicability fields and the two normalized fixtures.

**Included/excluded evidence.** Two immutable retained Campaign 40 normalized WDI fixtures were included. Seven other candidate pairs from the pre-existing eight-pair eligible registry were excluded before new calculations because the pilot selected one coherent topical family. One life-expectancy CAGR candidate was preregistered as `excluded_pre_execution` because compound percentage growth could imply an unsuitable accumulation process. The portfolio did not execute the pre-existing Pearson relationship between the two indicators.

**Methods and outputs.** Each series generated 28 records across coverage/missingness, sample/period, level distribution, adjacent first differences, descriptive time-index slope, and variability/stability. Portfolio-wide unique transformations were `level`, `adjacent_first_difference`, and the linear-time-index descriptor. The two packages contain 56 records and render 56 operational views, but remain two canonical objects and two source-series clusters.

**Missingness/alignment.** Both were 35/35 with zero missing values; 34 adjacent differences. Cross-series annual alignment existed but was not analytically used. Missing-data and nonconsecutive-difference branches were therefore not empirically stressed.

**Negative accounting.** Machine accounting: 3 manifest candidates, 2 executed/valid, 56 raw/valid records, 2 canonical objects, 56 views, 1 `rejected_candidates`, 0 null, 0 redundancy and 0 failures. The manifest identifies that one machine “rejection” as a pre-execution exclusion.

**Provenance/reproducibility.** Input byte and normalized fingerprints are bound through manifest, result records, packages and evolution. Input-before/after hashes match. Exact calculation fingerprints matched reruns. A later v1 isolated replay reconstructed the 560-object pre-state, reproduced the same two objects and returned the 562-object fingerprint `sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff`.

**Validation/publication.** The original canary, wave, focused tests, full suite and disposable projection passed. The original weak canary gate was later correctly classified as historical and replaced for prospective authority by a v1 isolated replay. The portfolio artifacts and objects are now durable in Git HEAD; “unpublished” in the original closeout describes the task-time publication boundary, not their current Git durability.

**Cost/review burden.** The retained production cost reports 0.07 seconds, 97% CPU and 21,184 KiB maximum RSS. Human review of applicability, denominator, limitations and 56 record views—not compute—was the binding burden. Reviewer minutes were not measured.

**Limitations.** Single territory/family/provider platform; shared modeled-estimation dependence; complete annual data; one method; no natural null/redundancy/failure/disagreement; no structural-break, causal, predictive, inferential or supersession case.

### 4.2 Sweden Infrastructure

**Governing question and use.** The durable task asks whether the same production path generalizes from Norway Health to a materially different admitted infrastructure family. The outputs are baseline descriptions, not relationship, saturation, policy or causal claims. As with Norway, no manifest field binds candidates to a concrete downstream analytical decision question.

**Scope.** Sweden (`SWE`), annual 1990–2024, 35 slots each:

- `IT.NET.USER.ZS`, individuals using the Internet as percent of resident population;
- `IT.CEL.SETS.P2`, mobile cellular subscriptions per 100 resident people.

**Population and denominator.** Internet measures people; mobile measures subscriptions and may exceed 100 because it is not unique persons. Both summarize unweighted across-year retained sequences, not cross-sectional distributions or pooled-period estimates. These explicit differences are a real domain-generalization gain over Norway.

**Included/excluded evidence.** Two retained Campaign 40 WDI/ITU normalized fixtures were included. Seven other family pairs were excluded before outcome inspection. The authoritative manifest’s third candidate is Internet-user CAGR, `excluded_pre_execution` because compound growth is inapplicable to an adoption-share level series. The task/report’s “unrestricted all-pairs relationship” wording does not match the machine manifest.

**Methods and outputs.** The same 28-record profile and three transformation families were used. Independent semantic review initially blocked ambiguous derived units and missing across-year applicability language. Manifest v1.1 corrected percentage-point and mobile-subscription unit labels plus statistical-population limitations without changing candidates, calculations, methods or values. Fresh replay and rereview passed.

**Missingness/alignment.** Both were 35/35 with zero missing values and 34 adjacent differences. Again, missingness, irregular intervals and relationship alignment were configured but not empirically stressed.

**Negative accounting.** Machine accounting is numerically identical to Norway: 3 manifest candidates, 2 executed/valid, 56 raw/valid records, 2 objects, 56 views, 1 `rejected_candidates`, and zero null/redundancy/failure. Narrative artifacts separately claim one exclusion and zero rejected, exposing terminology drift.

**Provenance/reproducibility.** Exact fixture bytes, normalized fingerprints, method contract, manifest and lineage are retained in packages/evolution. Independent fresh 562-object source exports produced identical corrected packages, views, indexes, evolution and final 564-object fingerprint `sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67`.

**Validation/publication.** Canary/wave, 121 focused tests, 434 full-suite tests, independent replay, independent semantic rereview, architecture audit and isolated projection all passed at task closeout. The task itself stopped before Git publication, but the portfolio was later committed and is present at current HEAD. Production admission, accepted lifecycle, Git durability and separately authorized release/publication must remain distinct concepts.

**Cost/review burden.** Three calculation reruns totaled 0.019732132 seconds. Independent semantic review found three blockers and forced manifest v1.1 plus a complete fresh replay. This is direct evidence that deterministic schema conformance and low compute do not eliminate semantic review cost.

**Limitations.** Same provider/campaign/method infrastructure as Norway; complete annual data; one country; technology-definition and adoption-regime changes; mobile subscription/person ambiguity; no natural null/redundancy/failure/disagreement; no relationship, structural-break, causal, predictive, supersession or adapter case.

## 5. Exact combined accounting

Mechanically summed machine accounting across both production roots:

| Category | Combined |
|---|---:|
| Manifest candidates | 6 |
| Executed candidates | 4 |
| Valid candidates | 4 |
| Raw calculation records | 112 |
| Valid result records | 112 |
| Promoted canonical Knowledge Objects | 4 |
| Operational Evidence-Card-equivalent views | 112 |
| Distinct source series | 4 |
| Evidence Bundles | 2 |
| Declared dependency clusters | 4 |
| Machine `rejected_candidates` | 2 |
| Null candidates | 0 |
| Redundant candidates | 0 |
| Redundant result records | 0 |
| Execution failures | 0 |

There are only **three portfolio-wide unique transformation families**, not six: both portfolios reused the same three. The four declared dependency clusters are per-series execution/lineage clusters; they do not establish four independent evidence sources. All four series share WDI distribution, retained Campaign 40 fixture lineage and the same calculation method family.

## 6. Cross-portfolio comparison matrix

| Dimension | Norway Health evidence | Sweden Infrastructure evidence | Classification |
|---|---|---|---|
| Portfolio boundary | One Norway Health pair, one bundle, two execute + one excluded CAGR | One Sweden Infrastructure pair, one bundle, two execute + one excluded CAGR | Common mechanism worked |
| Question-to-evidence | Operational production question; only general “baseline utility” substantive use | Operational generalization question; only general “downstream baseline value” | Weak in both; substantive traceability unexercised |
| Denominator/population | Years versus per 1,000 live births; finite annual sequence | Percent of people versus subscriptions per 100 people; finite annual sequence | Common metadata mechanism; domain-specific semantics |
| Geographic/temporal comparability | One country, annual 1990–2024, complete | One country, annual 1990–2024, complete | Shared easy case; broader comparability untested |
| Transformation selection | Same three transformations; CAGR excluded | Same three transformations; CAGR excluded | Shared method path, not independent generality |
| Lag/subperiod handling | Adjacent differences only; no lag or subperiod analysis | Adjacent differences only; no lag or subperiod analysis | Not exercised beyond one-step differences |
| Missingness/alignment | 35/35; no gaps | 35/35; no gaps | Missing-data behavior untested empirically |
| Inclusion/rejection | Outcome-blind family selection and one manifest exclusion | Same; report misdescribes exclusion | Mechanism worked; reporting conformance weak |
| Null/contradiction | None natural | None natural | Untested; only adversarial tests |
| Source independence | Two WDI health series with shared provider/modeled processes | Two WDI/ITU infrastructure series with shared provider/campaign | No independent-source corroboration |
| Provenance | Exact path/hash/normalized/method/manifest/lineage | Same | Common mechanism worked |
| Reproducibility | Exact v1 isolated replay | Exact independent fresh replay | Common mechanism worked |
| Canonicalization/evolution | Two append-only packages and evolution records | Two append-only packages and evolution records; Norway unchanged | Common mechanism worked |
| Reviewer burden | Applicability and 56-view review identified; no measured minutes | Semantic review found unit/applicability defects and forced v1.1 replay | Review is binding; only Sweden exercised correction |
| Failure recovery | Historical weak-gate correction and replay | Semantic correction and complete replay | Different bounded recovery modes exercised |
| Downstream use | Package/projection adequate; no baseline adapter | Same | Content compatibility demonstrated; adapter compatibility untested |
| Overclaim controls | Descriptive-only limitations | Descriptive-only plus saturation/person-count cautions | Common mechanism worked; consumer certainty still needs discipline |

## 7. Exercised, one-sided and unexercised capabilities

### Exercised in both

- deterministic selection rubric and manifest;
- content-hash and normalized-fingerprint input binding;
- explicit units, territory, period, population, denominator and applicability;
- pre-execution method exclusion;
- canary and conditional wave;
- exact limits and complete accounting;
- stable result/package identities and collision controls;
- immutable-input checks;
- canonical package construction, validation, append-only promotion and idempotence;
- evolution records and supersession-ready dependencies;
- operational view rendering without canonical inflation;
- canonical repository authentication;
- isolated replay and projection verification;
- direct no-recalculation package/projection consumption.

Supporting evidence for both: the two `portfolio_manifest.json`, `canary_accounting.json`, `production_accounting.json`, `production_gate.json`, `production_packages.json`, `production_views.json`, `projection_compatibility.json`, canonical object/evolution pairs, and `tools/evidence_portfolio_production.py`.

### Exercised in only one

- Norway: exact legacy-portfolio compatibility path and retrospective v1 authorization replay after the historical weak gate.
- Sweden: explicit family configuration, quantity-aware derived-unit rendering, independent semantic-review failure, manifest v1.1 correction, fresh replay and rereview.

### Present in code/tests but not natural portfolio outcomes

- null candidate classification;
- execution failure and stop-on-canary-failure behavior;
- exact duplicate and semantic identity collision;
- redundant result handling;
- malformed/tampered authorization and path containment;
- concurrent repository-state mutation rejection.

### Not exercised in either

- partial/asymmetric missingness or nonconsecutive observations;
- irregular or nonannual frequency;
- multi-territory or cross-sectional population;
- genuine source disagreement or contradictory evidence;
- independent providers or methods;
- negative controls beyond an expected method exclusion;
- subperiod, lag, structural-break or regime sensitivity;
- object revision/supersession after portfolio production;
- general baseline export/InsightForge adapter;
- larger-wave review economics;
- causal, predictive or explanatory evidence classes.

## 8. Framework-wide findings versus specific behavior

### Framework-wide positive findings

1. **Canonical/view separation worked.** Four canonical packages contain 112 distinct result records/views; the repository never treats the 112 views as 112 packages. Evidence: both reports, manifests, `production_views.json`, repository object count evolution.
2. **Lineage and replay worked.** Every package binds retained evidence, normalized identity, calculation contract, manifest and result fingerprints. Independent replay returned exact package and repository identities.
3. **Applicability metadata carried different semantics.** Years, per-1,000-live-birth rates, people percentages and subscriptions per 100 people were represented without collapsing their denominators.
4. **Canary-bound continuation worked.** Both waves required an exact, content-bound successful canary and repository pre-state.
5. **Filesystem authority plus rebuildable projection worked.** Both object sets remained canonical files while PostgreSQL projection preserved payload fidelity.

### Domain/source/campaign-specific findings

- Norway’s life-expectancy and mortality limitations arise from health-state/rate semantics and modeled demographic estimation.
- Sweden’s percent-versus-subscription units, person uniqueness, technology definitions, adoption/saturation and regime cautions are infrastructure-specific.
- Both are WDI and retained Campaign 40 cases; source-independence claims are therefore unsupported.
- Norway’s legacy fallback and v1 replay are historical campaign compatibility behavior, not generic portfolio requirements.
- Sweden’s semantic correction demonstrates the risk of quantity rendering, not a universal defect in every domain.

### Apparent success caused by shared infrastructure

Identical budgets, exact 28-record counts, the same three transformations, the same production engine, complete annual windows, the same repository/projection and shared WDI acquisition path make several outcomes mechanically likely. The second portfolio proves configuration across a second family and preservation of prior objects. It does not prove that a different method, source topology, frequency or incomplete evidence population will work unchanged.

## 9. Adversarial blind-spot findings

1. **Survivorship bias — present.** Both reviewed portfolios completed successfully. Naturally failed or abandoned portfolio attempts are absent from this sample.
2. **Selection bias — material.** Both selected complete, low-cost, already admitted annual pairs. That is appropriate for first baselines but weak evidence for broad generality.
3. **Failed-candidate representation — insufficient empirically.** Each has one expected pre-execution exclusion; neither has a natural runtime rejection, null, redundancy or failure.
4. **Shared-source/method dependence — material.** Four source series are not four independent corroborations. All share WDI distribution, Campaign 40 retained-fixture lineage and one method engine.
5. **WDI/provider concentration — material.** No non-WDI portfolio exists.
6. **Denominator ambiguity — mitigated but not eliminated.** Metadata are explicit; Sweden review still found derived-unit ambiguity, and mobile subscriptions can be mistaken for people.
7. **Temporal-overlap artifacts — not stressed.** All four series have the same complete 1990–2024 annual window.
8. **Transformation cherry-picking — partly controlled.** Manifests were outcome-blind and CAGR was excluded before calculation, but the same fixed transformations were used twice and no alternative-method challenge occurred.
9. **Negative controls/disagreement — absent.** Expected method exclusion is not a substantive negative control or independent disagreement case.
10. **Structural breaks/regimes — limitations only.** Sweden documents technology-era risk, but neither portfolio tests subperiod sensitivity or definitional breaks.
11. **Schema meaning risk — observed.** Exact provenance did not prevent task/report exclusion-description drift or transformation-label drift.
12. **Provenance strength fallacy — material.** Complete lineage establishes origin/replay, not source independence, measurement validity, causal force or decision relevance.
13. **Reviewer burden — undermeasured.** Compute is negligible; only Sweden demonstrates a semantic-review correction. Neither records reviewer minutes or cost.
14. **Shared campaign machinery — major confound.** The positive cases show the machinery is reusable for a second configuration, not that the portfolio model is universal.
15. **Downstream certainty — bounded but still risky.** Canonical limitations are strong, yet no general consumer contract proves that caveats will remain salient.
16. **Version drift — controlled for retained bytes, untested for refresh.** Exact replay uses local immutable fixtures; WDI reacquisition is mutable and no source-update/supersession portfolio was tested.
17. **Non-hermetic full suite — confirmed portability issue.** A sibling MacroForge durable-export path is assumed by one KnowledgeForge test module.

## 10. Portability and fixture-topology assessment

The isolated-clone full-suite failure from the publication task is accurately classified as:

- **not** a semantic KnowledgeForge test failure;
- **not** evidence that the referenced MacroForge export is missing or nondurable;
- **yes**, a KnowledgeForge test-portability/fixture-topology dependency.

`tests/test_external_outbox_polling_supersession_v1.py` defaults to a sibling MacroForge export path and unconditionally copies it in setup. With the sibling export present, the six tests pass; with an absent configured path, all six fail during setup before testing portfolio semantics. MacroForge owns the producer export. The shared EIP sibling layout is environmental. KnowledgeForge owns a hermetic or explicitly provisioned fixture contract because the failing assumption is in its test suite.

This issue is valuable but non-blocking for the pre-third accounting/traceability correction. It should not be silently called a successful isolated full-suite run, and it should not be “fixed” by synthesizing producer data or coupling KnowledgeForge to MacroForge runtime state.

## 11. Generalization classification

Selected outcome: `provisionally generalizable with bounded corrections`.

### Demonstrated

- reusable deterministic production for two annual-scalar baseline families;
- explicit handling of four materially different units/denominators;
- stable canonical/view separation, lineage, replay, promotion, accounting and projection;
- bounded correction/replay when authorization or semantic-review defects are found.

### Suggested

- explicit family configuration can likely support further coherent annual-scalar baseline families;
- human review can catch domain-specific rendering/applicability defects before publication;
- current package and projection content can support read-only downstream use without recalculation.

### Untested

Everything listed under section 7’s unexercised capabilities, especially source/method diversity, missingness, disagreement, failures, supersession and general consumer contracts.

### Contradicted

- Narrative/machine conformance is not yet reliable: both portfolio narratives drift from the authoritative excluded CAGR candidate; machine `rejected_candidates` collapses an expected pre-execution exclusion; Sweden transformation labels differ between manifest and produced surfaces.
- “Dependency cluster” cannot be read as independent corroboration; the shared provider/campaign/method evidence contradicts that interpretation.

### Prohibited overclaims

Do not claim universal generality, four independent evidential supports, natural adverse-path coverage, broad production maturity, InsightForge adapter readiness, causal/explanatory validity, or readiness for quota-driven 100/1,000 output expansion.

### Confidence

Moderate. Confidence is high for the specific shared deterministic production path because two complete executions and replays exist. Confidence is low-to-moderate outside annual-scalar complete-data baseline characterization because both cases share most infrastructure and avoid the difficult conditions that should distinguish a general framework.

## 12. Change disposition

### Required before a third portfolio

1. Exact candidate-disposition taxonomy and phase-aware accounting.
2. Mechanical task/report-to-manifest candidate identity and exclusion-reason conformance.
3. Stable transformation identity from manifest through result/view/projection.
4. Explicit analytical question/intended use and candidate-to-question traceability.
5. Explicit separation of series dependency clusters from provider, acquisition and method dependence.

These corrections apply prospectively and must retain the two completed portfolios as immutable regression evidence.

### Valuable but non-blocking

- measure reviewer time and exception burden;
- improve projection filter convenience only for a real consumer need;
- correct isolated-clone fixture provisioning;
- retain explicit source-vintage drift assessments on future refresh.

### Deferred until diverse evidence exists

- generic baseline export or InsightForge adapter;
- structural-break/regime methods;
- multi-method/source disagreement synthesis;
- supersession policy refinements specific to portfolio refresh;
- larger-scale batching changes.

### Rejected as unnecessary complexity

- parallel portfolio architecture;
- new Evidence Card ontology;
- second database architecture;
- automated candidate padding;
- unrestricted relationships, graphs or advanced statistical roadmap.

## 13. Single successor task

Select option 1: **bounded framework correction before further portfolio production**.

Recommended task, not activated:

`Evidence Portfolio accounting, traceability and dependence conformance correction v1`

It should:

- preserve both portfolios and all canonical objects byte-for-byte;
- add prospective conformance rules/tests for exact disposition categories;
- bind task/report descriptions to manifest candidate IDs/reasons;
- enforce one transformation identifier end to end;
- require a bounded analytical question/use and traceability map;
- report provider/acquisition/method dependence separately from source-series clusters;
- use existing portfolio tests and manifests as regressions;
- stop after validated framework correction, without constructing portfolio three.

## 14. Most discriminating later third portfolio

After that correction, choose an already admitted, durable, outcome-blind family that differs on multiple axes:

- non-WDI or genuinely independent provider family;
- eligibility/exposure denominator rather than resident-population scaling;
- real partial missingness or irregular periods;
- different frequency where semantically justified;
- plausible source disagreement or contradictory estimate;
- known definitional/applicability break;
- at least one expected null, rejection or negative control;
- a concrete descriptive decision-use question;
- no need for causal, predictive or advanced relationship methods.

This is a selection rubric, not a selected portfolio and not production authorization.

## 15. Roadmap effect and explicit non-claims

Roadmap effect: pause additional portfolio production until the bounded conformance correction is separately authorized and validated. After correction, prefer one deliberately divergent third portfolio over convenient repetition or output-count expansion. The approximately 100-view horizon remains an envelope; the later 1,000-output horizon remains unsupported.

This review did not:

- create or select a third portfolio;
- acquire or recalculate evidence;
- modify canonical objects, indexes, evolution or manifests;
- alter either existing portfolio;
- mutate PostgreSQL or any sibling project;
- redesign doctrine, projection or publication authority;
- clean, stage, commit, push, tag, release or activate the successor.

## 16. Validation and closeout record

Validation preserved four classifications separately:

- **Repository/canonical correctness — pass.** Read-only recomputation authenticated 564 objects, 564 evolution records, six exact indexes, exact package IDs, zero evolution mismatches and repository fingerprint `sha256:777140d9d96c9b2e901604720b10be9645ba286f196d844f01503e4365bfac67`. A corrected canonical CLI smoke run persisted one existing package to an isolated temporary repository with six indexes and one evolution record. The canonical repository was not mutated.
- **Governance/artifact consistency — pass.** Focused tests passed 127/127; full tests passed 488/488; compilation and `git diff --check` passed; the candidate consistency scan passed; coherence and context health had zero blocks and only the two pre-existing warnings; the no-write Architecture-to-Reality Audit had zero blocks and zero warnings.
- **Security/hygiene — pass.** The four task-owned files had zero credential/secret-pattern hits, zero NUL, replacement-character, carriage-return, trailing-whitespace or conflict-marker issues, and remained within the bounded candidate size limit.
- **Tooling/environment portability — bounded pass.** External Python cache prefixes prevented verifier-induced ignored-bytecode drift. The existing isolated-clone sibling-fixture topology defect remains valuable but non-blocking and is not reclassified as a semantic production failure.
- **Command authorization/publication boundary — uncommitted candidate.** The review authorizes analysis and candidate creation, not staging, commit, push, tag or release. No publication action was attempted.

The resumed preservation gate passed exactly. All 806 frozen pre-review identities match, the ignored population is 313/313, and the pre-review raw Git status is exact after excluding the four authorized candidate paths. The eight protected mixed live paths are baseline-exact; HEAD and `origin/main` remain `ba1e2ae5a001a31550a7fca7732f9ce262dc0530`; ahead/behind is 0/0; and the index is empty. Repository process inspection found only the current Hermes process tree.

The exact task-owned delta is `docs/roadmap.md`, this report, the task and the decision. No unrelated cleanup, successor activation, third portfolio, evidence acquisition or calculation, canonical-object/index/evolution mutation, PostgreSQL mutation or sibling-project mutation occurred. The analytical classification remains `provisionally generalizable with bounded corrections`, and the single recommended successor remains inactive.
