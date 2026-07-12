# Next Production Readiness Decision Before Campaign 43

Date: 2026-07-12
Status: completed
Decision: A — expand first-difference Pearson companions.

## Scope and boundary

This was a decision gate only. It did not begin Campaign 43, calculate coefficients, publish packages, mutate PostgreSQL production state, change package contracts, change schema, amend doctrine, redesign retrieval, or stage/resolve unrelated local residue.

## Preflight

Repository: `/home/mkkto/srv/EIP/projects/KnowledgeForge`
Branch: `main`
Expected starting HEAD and `origin/main`: `4ccf2710f4046135fd3908e80728671a1f5f1e69`

Verified in `preflight_summary.json`:

- current branch: `main`
- HEAD: `4ccf2710f4046135fd3908e80728671a1f5f1e69`
- `origin/main`: `4ccf2710f4046135fd3908e80728671a1f5f1e69`
- ahead/behind before work: `0 0`
- staged changes before work: none
- origin changed unexpectedly: no
- unrelated tracked deletions under `architecture/architectureharvest/`: present and deliberately untouched
- unrelated untracked/ignored local residue: preserved

## Evidence examined

Minimum evidence inspected:

- `CONSTITUTION.md`
- `state/active_goal.md`
- `state/project_state.md`
- `state/architecture.md`
- `context/latest_handoff.md`
- `docs/production_campaign_roadmap.md`
- Campaign 40 task/decision/report/spec/output evidence
- Campaign 41 task/decision/report/spec/registry/output evidence
- Campaign 42 task/decision/report/spec/registry/output evidence
- corrected Pearson policy v2 and consistency correction artifacts
- first-difference transformation and method contracts
- PostgreSQL operational projection tooling and tests
- Relationship Export Contract v1, export tooling, and independent consumer simulation evidence
- canonical repository manifest and canonical package corpus

## Adversarial findings

Recorded under `adversarial/adversarial_summary.json`.

1. Raw and first-difference relationships can be requested separately through supported Relationship Export Contract filters.
   - raw method query returned 21 relationships.
   - first-difference method query returned 8 relationships.
   - first-difference transformation query returned 8 relationships.
   - raw/first-difference overlap: `[]`.
   - first-difference method vs transformation symmetric difference: `[]`.

2. Returned records expose required interpretation metadata.
   - No exported raw, first-difference, or all-relationship row was missing method identifier, method version, method contract fingerprint, source package identity/fingerprint, provenance, limitations, temporal scope, frequency, entity, series metadata, coefficient, transformation state, or lifecycle state.

3. A clean independent consumer can retrieve relationship classes without campaign numbers, internal filenames, or package IDs.
   - Method-based raw query and method/transformation-based first-difference queries passed `relationship_export_consumer_simulator_v1.py`.
   - Discovery query by `statement_type=derived_relationship` returned all 29 relationships and exposed method/transformation classes.

4. Export behavior does not silently mix raw and transformed relationships when method/transformation filters are used.
   - Raw query returned only raw method records.
   - First-difference method/transformation queries returned only first-difference companion records.

5. Additional raw candidates exist under corrected policy.
   - Corrected future-production evidence contains 4 noncanonical raw candidates: three close NOR demographic/health pairs and one remote DNK forest/private-credit pair.
   - Prior correction classified all four as high time-risk and insufficient for a useful raw Campaign 42 registry before first-difference method validation.

6. Existing raw relationships have concrete first-difference justification.
   - Campaign 41 report records all eight Campaign 41 raw relationships as high shared-time-trend risk.
   - Campaign 42 already produced companions for two SWE Campaign 41 relationships.
   - Six Campaign 41 raw relationships remain as specific companion candidates with evidence-backed trend-risk justification:
     - DNK agricultural land / broad money
     - DNK agricultural land / private credit
     - DNK forest area / broad money
     - NOR crude birth rate / fossil electricity
     - NOR fossil electricity / under-5 mortality
     - NOR nonhydro renewable electricity / under-5 mortality

7. Retrieval/export improvement is not the next bounded correction.
   - Current Relationship Export Contract v1 supports class-level discovery and separation.
   - No independent-consumer failure was observed.
   - Building a broader query platform, catalog API, or schema redesign would exceed measured need.

## Option comparison

### A. Expand first-difference Pearson companions — selected

Expected incremental knowledge value: high enough for the next bounded slice. It converts already-canonical high-time-risk raw relationships into separate annual-change relationship knowledge without superseding raw packages.

Evidence basis:

- first-difference method contract is validated;
- Campaign 42 proved deterministic companion production, package immutability, non-supersession, PostgreSQL projection, and export separation;
- six specific Campaign 41 raw relationships have recorded high shared-time-trend risk and no corresponding Campaign 42 companion;
- consumers can retrieve raw and first-difference classes separately.

Reproducibility and risk:

- deterministic transformation/method contracts already exist;
- no schema/package/doctrine change required;
- expected implementation complexity is bounded to registry freeze and later production from existing method/tooling;
- no production package mutation is required; publication, if separately authorized later, should be append-only.

Prerequisites before implementation:

1. Create a coefficient-free Campaign 43 first-difference companion registry for the six specific remaining Campaign 41 high-time-risk raw relationships.
2. Freeze registry/spec fingerprints before coefficient calculation.
3. Prove each selected raw package has retained fixture coverage sufficient for first-difference threshold.
4. Stop after registry freeze unless separately authorized to calculate/publish.

### B. Resume raw Pearson candidate production — rejected for now

Reason:

- Corrected raw-production eligibility exists but is small: four candidates from the retained pool.
- All four were previously classified as high time-risk.
- Raw production would add baseline descriptors, but the next more valuable deterministic step is to complete robustness companions for already-published high-risk raw relationships.
- Selecting B now would resume raw expansion before exhausting the already-validated companion method on relationships whose risk is already documented.

B remains eligible after the next companion slice if the coefficient-free raw registry is refreshed and still passes corrected policy.

### C. Pause production for retrieval/export improvements — rejected

Reason:

- The adversarial export checks did not reproduce the failure condition for C.
- Independent consumer simulation can discover relationship classes and retrieve raw versus first-difference relationships without private repository files, campaign numbers, or package IDs.
- Exported records expose method, transformation, provenance, source package identity/fingerprint, temporal/population scope, lifecycle/non-supersession-relevant metadata, and limitations.
- No observed deficiency justifies pausing production for a broader query framework, generalized analytics API, schema change, or contract redesign.

## Decision

Choose A: expand first-difference Pearson companions.

This is not authorization to begin Campaign 43. It authorizes only the next decision/implementation task: a coefficient-free companion-registry freeze for specific existing raw relationships.

## Architecture/doctrine classification

- Doctrine amendment: not required.
- KnowledgeObjectPackage redesign: not required.
- PostgreSQL schema change: not required.
- Relationship Export Contract redesign: not required.
- Broad transformation framework: not authorized.
- Generalized query platform/API: not authorized.
- Production architecture classification: bounded production-readiness sequencing within existing Pearson v1, first-difference companion, package, PostgreSQL projection, and Relationship Export Contract architecture.

## Canonical immutability confirmation

No production packages were changed by this gate.

Required confirmation after verification:

- canonical count remains 554;
- repository fingerprint remains `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`;
- no Campaign 40-42 package was mutated;
- PostgreSQL production state was not modified; only read-only export/projection verification was used.

## Smallest exact next implementation task

Campaign 43 coefficient-free first-difference companion registry freeze for the six remaining Campaign 41 high-shared-time-trend raw Pearson relationships listed above, using the existing first-difference method contract, stopping before coefficient calculation or package publication.

## Closeout verification

Recorded under `artifacts/reports/next-production-readiness-decision-20260712/final_verification/closeout/`.

Results:

- Targeted relationship/export/PostgreSQL/first-difference tests: passed, 24 tests OK.
- Full `unittest discover`: 311 tests ran before one environment/dependency error; failure was `tests/test_operational_state_checkpoint.py` importing missing `pytest`, not a decision-gate package mutation failure.
- Python compileall over `tools` and `tests`: passed.
- PostgreSQL projection verify: passed with 554 canonical/projected packages, zero missing/extra IDs, zero payload-fidelity failures, zero package-fingerprint failures, repository fingerprint match.
- Repository-wide durability validator: command exited 0; sensitive scan passed with 0 actual secret blockers and 0 unsafe absolute-path dependencies; validator decision remains D due to pre-existing untracked recovery-critical implementation and operational checkpoint durability exposure.
- Coherence: 0 blocks; 1 non-blocking stale generated-bundle warning for `context/active_context.md`.
- Context health: 0 blocks; 1 non-blocking stale generated-bundle warning for `context/active_context.md`.
- Architecture-to-reality audit: 0 blocks, 0 warnings.
- `git diff --check`: passed.
- Canonical invariants: 554 packages, fingerprint `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`, no canonical package mutations, no new package files.

The full-suite pytest dependency gap is recorded as an environment/tooling issue. It does not alter the selected readiness path because targeted gate checks and canonical immutability checks passed.

## GitHub publication

Committed and pushed to `origin/main`.

- readiness-decision commit: `97179bce664e1f257776304cfc5bdcda66e03917`
- post-push verification recorded in `final_verification/closeout/post_push_verification.json`
- local `HEAD` and `origin/main` matched after fetch: `97179bce664e1f257776304cfc5bdcda66e03917`
- ahead/behind after push: `0 0`
- clean remote clone confirmed decision/report presence and canonical manifest count/fingerprint: 554 / `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`
- protected `architecture/architectureharvest/` deletions remained unstaged local residue.
