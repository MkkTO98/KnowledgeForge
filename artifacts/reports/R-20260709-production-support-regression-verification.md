# Regression Verification Report — Production Support Layer

Date: 2026-07-09
Status: completed
Scope: Campaigns 0-3 regression after minimal Production Support implementation

## RED evidence

Before implementation, `tests/test_production_support.py` failed because `tools/production_support.py` did not exist.

Command:

```bash
python3 -m unittest tests.test_production_support -v
```

Observed result:

- 2 errors;
- both errors were `FileNotFoundError: ... tools/production_support.py`.

## GREEN evidence

After implementation, targeted production-support and campaign regression tests passed.

Command:

```bash
python3 -m unittest tests.test_production_support tests.test_campaign1_wdi_demographic_evidence tests.test_campaign2_wdi_completeness_buckets tests.test_campaign3_wdi_freshness_metadata -v
```

Observed result:

- 11 tests OK.

Full test suite:

```bash
python3 -m unittest discover -s tests -v
```

Observed result:

- 34 tests OK.

## Behaviour-preservation comparison

A pre-refactor baseline was generated for Campaigns 1-3 under `/tmp/kf_psl_baseline/`.

After refactoring, Campaigns 1-3 were rerun and compared against the baseline after normalizing only absolute output paths.

Observed result:

```text
compared 163 changed 0 missing 0
```

This proves identical Campaigns 1-3 artifacts after the support-layer refactor, including Knowledge Objects, fingerprints, reports, validator behaviour records, and production metrics.

## Campaign rerun evidence

Campaigns 0-3 were rerun into their production artifact paths.

Campaign 0:

- accepted: 10
- rejected: 3
- determinism: true
- fingerprint stability: true
- snapshot fingerprint: repository-state-dependent; use `artifacts/production/campaign-0-repository-evidence-characterization/campaign_summary.json` for the latest rerun value.

Campaign 1:

- accepted: 12
- rejected: 4
- determinism: true
- fingerprint stability: true
- duplicate pressure: false
- snapshot fingerprint: `sha256:3feb2ccab6687c4ee729a8d126e73354794e0a5c00489cbe26166739a254ebc1`

Campaign 2:

- accepted: 14
- rejected: 4
- determinism: true
- fingerprint stability: true
- duplicate pressure: false
- snapshot fingerprint: `sha256:ad23e65284cf268e9e0bd4835ac471d73e255b8f6f92fb3a595b90e9a3e089c5`

Campaign 3:

- accepted: 12
- rejected: 4
- determinism: true
- fingerprint stability: true
- duplicate pressure: false
- snapshot fingerprint: `sha256:70cd67a482502a44c52e3de38417f52af751917c137378cb749e85e661f73e25`

## Campaign 0 note

Campaign 0 fingerprints changed relative to its prior committed/generated production output because Campaign 0 intentionally fingerprints selected repository files. Adding `tools/production_support.py`, `tests/test_production_support.py`, and refactoring campaign scripts changes the repository evidence snapshot. Campaign 0 still passes regression coverage for deterministic replay, validator behavior, accepted/rejected counts, and fingerprint stability against the new repository state.

## Verification conclusion

The implementation is behavior-preserving for the stable WDI campaign artifacts and regression-safe for Campaign 0 under its repository-snapshot semantics.
