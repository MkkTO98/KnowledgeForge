# D-20260713 Post-Campaign-43 Next Production Readiness Gate

Date: 2026-07-13
Status: accepted; selected correction implemented locally 2026-07-13

## Decision

Select path D: perform a bounded production-enabling correction before additional production.

The selected task is to convert the isolated undeclared `pytest` dependency in `tests/test_operational_state_checkpoint.py` to standard-library `unittest` semantics, without installing pytest, changing dependency declarations, or changing production behavior. The implementation must preserve operational-state-checkpoint coverage and prove `python3 -m unittest discover -s tests -v` runs cleanly afterward.

This decision does not authorize coefficient calculation, transformation execution, package construction, package publication, PostgreSQL mutation, Relationship Export output mutation, schema change, doctrine amendment, broad test-framework redesign, staging, commit, or push.

## Basis

- Campaign 43 is closed and pushed at `bda3f13808bf70c7b108bcf215f98f5789d937fe`.
- Canonical repository state is valid at 560 packages with fingerprint `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`.
- PostgreSQL projection is valid at 560 packages.
- Relationship Export v1 retrieves 35 total relationships, 21 raw Pearson relationships, and 14 first-difference Pearson relationships with no raw/first-difference overlap.
- Repository history and documentation establish `python3 -m unittest` and often `python3 -m unittest discover -s tests -v` as the repository-native test path; no `pyproject.toml`, lockfile, pytest config, or declared pytest environment is present.
- `python3 -m unittest discover -s tests -v` currently runs 331 tests but fails discovery because `tests/test_operational_state_checkpoint.py` imports undeclared `pytest`.
- The failure can hide unexecuted tests and creates a credible risk of false completion claims if agents rely only on hand-picked targeted suites.
- The defect is isolated and correctable by replacing `pytest.MonkeyPatch` and `pytest.raises` usage with `unittest.mock.patch` and `self.assertRaises`, preserving coverage and avoiding new dependencies.

## Candidate comparison

### A. Resume corrected-policy raw Pearson production for the four remaining candidates — rejected for next task

The four remaining candidates would create new raw baseline descriptors, but all are high time-risk. Three are close NOR demographic/health pairs and one is a remote DNK forest/private-credit pair. Raw-only publication is predictably incomplete because each already has foreseeable first-difference companion need. Option A is not selected until the verification surface is reliable and a raw-plus-companion sequencing rule is explicit.

### B. Define a paired raw-plus-first-difference production contract — rejected for next task

A paired contract is epistemically attractive for high-time-risk candidates and can fit existing architecture if raw and transformed packages remain separate, non-superseding, and method-distinct. However, defining that contract now would be a new production sequencing layer while the repository-wide test discovery path is known broken. The smaller prerequisite is to restore repeatable verification first.

### C. Select another documented knowledge-production candidate — rejected for next task

Backlog/roadmap alternatives such as WDI family expansion, statistical-summary replication, release automation, or MacroForge integration are documented, but none offers a stronger immediate incremental knowledge value than repairing the verification defect that will govern all subsequent production. Some alternatives are deferred or cross-project and would be a larger boundary than this gate requires.

### D. Bounded production-enabling correction — selected

Selected because the defect materially weakens repeatable repository-wide verification, contradicts the repository's documented standard-library unittest posture, and is isolated enough to correct without architecture, doctrine, dependency, package, or production-data changes.

## Treatment of four remaining Pearson candidates

Each candidate is retained as eligible future evidence only, not selected for immediate raw-only production:

1. NOR crude birth rate / under-5 mortality
   - Source: retained World Bank WDI fixtures.
   - Scope: 1990-2024, 35 aligned annual observations, coverage 1.0.
   - Classification: close semantic proximity, high time-risk.
   - Raw value: could add a finite-window baseline/cautionary descriptor.
   - Raw-only risk: misleading if consumed without first-difference companion because both series have high accepted time-index diagnostic risk.
   - Companion foreseeable: yes.

2. NOR crude birth rate / life expectancy
   - Source: retained World Bank WDI fixtures.
   - Scope: 1990-2024, 35 aligned annual observations, coverage 1.0.
   - Classification: close semantic proximity, high time-risk.
   - Raw value: could describe a demographic fertility/survival baseline.
   - Raw-only risk: misleading if presented without robustness/limiting evidence.
   - Companion foreseeable: yes.

3. NOR crude death rate / under-5 mortality
   - Source: retained World Bank WDI fixtures.
   - Scope: 1990-2024, 35 aligned annual observations, coverage 1.0.
   - Classification: close semantic proximity, high time-risk.
   - Raw value: could describe a mortality/vital-rates baseline.
   - Raw-only risk: misleading because the same high time-risk concern applies to both series.
   - Companion foreseeable: yes.

4. DNK forest area / private credit
   - Source: retained World Bank WDI fixtures.
   - Scope: 1990-2024, 34 aligned annual observations, coverage 0.9714285714285714.
   - Classification: remote semantic proximity, high time-risk.
   - Raw value: only bounded cautionary/pressure-test value, not ordinary positive relationship discovery.
   - Raw-only risk: especially high due remote semantics plus high time-risk.
   - Companion foreseeable: yes if raw production is ever accepted.

## Paired-contract finding

A future paired raw-plus-first-difference production contract can remain within existing architecture only if:

- raw and first-difference packages remain separate KnowledgeObjectPackages;
- neither supersedes the other;
- method and transformation identities remain distinct;
- weak transformed results remain publishable as limiting evidence;
- the workflow stays a bounded Pearson production rule, not a generalized transformation framework.

## Architecture classification

Bounded test-governance and production-enabling correction inside existing architecture.

No Production Doctrine amendment, KnowledgeObjectPackage redesign, PostgreSQL schema change, Relationship Export Contract redesign, method-family change, broad transformation framework, or package publication is required or authorized.

## Consequence

The selected implementation was completed locally in `T-20260713-post-campaign43-test-discovery-correction.md` and `artifacts/reports/post-campaign43-test-discovery-correction-20260713/final_report.md`.

Repository-wide discovery now passes:

`python3 -m unittest discover -s tests -v` — 336 tests OK.

No package production or production-state mutation was authorized or performed by this decision.
