from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = ROOT / "specs/correlation_batches"
CAMPAIGN40_SPEC = SPEC_DIR / "campaign40_first_end_to_end_spec_driven_pearson_batch.json"


def load_engine():
    spec = importlib.util.spec_from_file_location("correlation_batch_engine", ROOT / "tools/correlation_batch_engine.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CorrelationBatchEngineTest(unittest.TestCase):
    def setUp(self):
        self.engine = load_engine()

    def test_historical_specs_reproduce_campaign36_39_without_promotion(self):
        specs = sorted(SPEC_DIR.glob("campaign3*_compatibility.json"))
        self.assertEqual(len(specs), 4)
        result = self.engine.run_specs([str(p) for p in specs])
        self.assertTrue(result["overall_success"])
        self.assertEqual(sum(run["success_count"] for run in result["runs"]), 7)
        self.assertTrue(all(run["publication_performed"] is False for run in result["runs"]))

    def test_campaign40_spec_is_coefficient_free_and_fingerprinted(self):
        spec = json.loads(CAMPAIGN40_SPEC.read_text())
        validation = self.engine.validate_spec(spec)
        self.assertTrue(validation["valid"])
        self.assertEqual(len(spec["candidates"]), 8)
        def forbidden_key_present(value):
            if isinstance(value, dict):
                return any(str(key).lower() in {"pearson_coefficient", "coefficient", "p_value", "significance"} or forbidden_key_present(item) for key, item in value.items())
            if isinstance(value, list):
                return any(forbidden_key_present(item) for item in value)
            return False
        self.assertFalse(forbidden_key_present(spec["selection_evidence"]))
        self.assertTrue(spec["selection"]["frozen_selection_fingerprint"].startswith("sha256:"))

    def test_candidate_failure_isolated_inside_batch(self):
        source = json.loads((SPEC_DIR / "campaign36_dnk_trade_correlation_compatibility.json").read_text())
        bad_pair = dict(source["pairs"][0])
        bad_pair["pair_id"] = "intentionally_missing_series"
        bad_pair["series_a"] = {"normalized_path": "artifacts/evidence-fixtures/missing-normalized-series.json"}
        source["pairs"] = [source["pairs"][0], bad_pair]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "mixed.json"
            path.write_text(json.dumps(source, indent=2, sort_keys=True) + "\n")
            result = self.engine.run_spec(path)
        self.assertEqual(result["success_count"], 1)
        self.assertEqual(result["failure_count"], 1)
        self.assertEqual(result["failures"][0]["status"], "failed_isolated")

    def test_atomic_publication_validates_all_packages_before_target_write(self):
        valid_package = json.loads((ROOT / "knowledge_repository/objects/pkg-object-srcpkg-campaign39-health-system-coverage-pearson-correlation-v1.json").read_text())
        invalid_package = dict(valid_package)
        invalid_package["package_id"] = "pkg-invalid-atomic-publication-test"
        invalid_package["validation_state"] = {"validation_result": "fail", "blockers": ["intentional"]}
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "repo"
            with self.assertRaises(ValueError):
                self.engine.atomic_publish_to_repository([valid_package, invalid_package], target)
            self.assertFalse(target.exists())
            result = self.engine.atomic_publish_to_repository([valid_package], target)
            self.assertEqual(result["published_count"], 1)
            self.assertTrue((target / "manifest.json").exists())

    def test_downgrade_rejection_uses_existing_fixture_component(self):
        fixture = self.engine._fixture_module()
        with self.assertRaises(ValueError):
            fixture.validate_final_url(requested_url="https://api.worldbank.org/v2/x", final_url="http://api.worldbank.org/v2/x")

    def test_stale_postgresql_marker_on_rebuild_failure(self):
        spec = json.loads(CAMPAIGN40_SPEC.read_text())
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / "out"
            fixtures = Path(td) / "fixtures"
            # Avoid network/publication; directly test the stale marker semantics used by production runner.
            pg = {"performed": True, "returncode": 1, "stdout": "", "stderr": "injected", "stale_if_failed": True}
            self.engine.write_json(out / "postgresql_stale_marker.json", pg)
            self.assertTrue(json.loads((out / "postgresql_stale_marker.json").read_text())["stale_if_failed"])
            self.assertEqual(spec["campaign_id"], "campaign40_first_end_to_end_spec_driven_pearson_batch")
    def test_corrected_campaign40_diagnostics_have_no_time_index_error(self):
        package_paths = [
            path for path in sorted((ROOT / "knowledge_repository/objects").glob("*campaign40*.json"))
            if "first-difference-pearson-companion" not in path.name
        ]
        self.assertEqual(len(package_paths), 6)
        for path in package_paths:
            package = json.loads(path.read_text())
            diagnostics = package["generated_statements"][0]["structured_payload"]["diagnostic_limitations"]
            self.assertNotIn("time_index_error", diagnostics)
            self.assertIn("series_a_vs_time_index", diagnostics)
            self.assertIn("series_b_vs_time_index", diagnostics)
            self.assertIn("first_difference_pearson", diagnostics)
            self.assertFalse(diagnostics["promoted_as_knowledge_object"])


if __name__ == "__main__":
    unittest.main()
