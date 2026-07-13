# T-20260713 Post-Campaign-43 Test Discovery Correction

Status: completed
Date: 2026-07-13

## Objective

Restore repository-wide standard-library unittest discovery after Campaign 43 by removing the isolated undeclared pytest dependency from `tests/test_operational_state_checkpoint.py`.

## Scope

Changed only `tests/test_operational_state_checkpoint.py`.

No production code, canonical packages, PostgreSQL state, Relationship Export outputs, dependency declarations, schemas, doctrine, or architecture were changed.

## Conversion

Removed pytest constructs:

- `import pytest`
- `pytest.MonkeyPatch` annotation
- `monkeypatch.setattr(osc, "ROOT", ...)`
- two `pytest.raises(osc.CheckpointError)` contexts
- pytest function parameters/fixtures (`tmp_path`, `monkeypatch`)

Standard-library replacements:

- `unittest.TestCase`
- `tempfile.TemporaryDirectory()` with `Path(tmp)` for isolated temporary files
- `unittest.mock.patch.object(osc, "ROOT", ...)` for scoped restoration-safe monkeypatching
- `self.assertRaises(osc.CheckpointError)`
- `self.assertIs`, `self.assertTrue`, `self.assertGreater`, and `self.assertIn`

## Verification

- Focused module: `python3 -m unittest tests.test_operational_state_checkpoint -v` — 6 tests OK.
- Repository-wide discovery: `python3 -m unittest discover -s tests -v` — 336 tests OK.
- The repaired module was discovered and executed as `test_operational_state_checkpoint.OperationalStateCheckpointTests` with 6 tests.
- No `ModuleNotFoundError: pytest` remained.
- No failures, errors, skips, discovery/import warnings, or hidden module failures were reported.

Regression verification preserved canonical/PostgreSQL state; see `artifacts/reports/post-campaign43-test-discovery-correction-20260713/final_report.md`.
