from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign5_wdi_territorial_coverage.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign5_wdi_territorial_coverage", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign5WdiTerritorialCoverageTests(unittest.TestCase):
    def setUp(self):
        self.module = load_campaign_module()

    def test_snapshot_is_deterministic_and_territorial_matrix_scoped(self):
        first = self.module.immutable_wdi_territorial_coverage_snapshot()
        second = self.module.immutable_wdi_territorial_coverage_snapshot()
        self.assertEqual(first, second)
        self.assertTrue(first["snapshot_fingerprint"].startswith("sha256:"))
        self.assertEqual(first["territorial_matrix"]["territory_count"], 217)
        self.assertEqual(first["territorial_matrix"]["indicator_family_count"], 4)
        self.assertEqual(first["territorial_matrix"]["coverage_bucket_count"], 4)
        self.assertIn("complete_or_near_complete", first["territorial_matrix"]["bucket_keys"])
        self.assertIn("insufficient_for_campaign_scope", first["territorial_matrix"]["bucket_keys"])

    def test_campaign_produces_valid_territorial_coverage_objects(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "campaign5"
            summary = self.module.run_campaign(output)
            self.assertEqual(summary["accepted"], 20)
            self.assertEqual(summary["rejected"], 4)
            self.assertTrue(summary["determinism_verified"])
            self.assertTrue(summary["fingerprint_stability"])
            self.assertFalse(summary["duplicate_knowledge_objects_detected"])
            self.assertEqual(summary["family_maturity_assessment"], "Stable")

            quality = json.loads((output / "production_quality_report.json").read_text())
            self.assertEqual(quality["knowledge_object_packages_accepted"], 20)
            self.assertEqual(quality["source_evidence_packages_processed"], 20)
            self.assertEqual(quality["rejected_candidates"], 4)
            self.assertIn("coverage", quality["knowledge_categories_produced"])
            self.assertIn("derived", quality["knowledge_categories_produced"])
            self.assertIn("negative", quality["knowledge_categories_produced"])
            self.assertIn("provenance", quality["knowledge_categories_produced"])
            self.assertIn("campaign_5", quality["cross_campaign_metric_comparison"])
            self.assertTrue(quality["provenance_completeness"])
            self.assertEqual(quality["territorial_coverage_observations"]["larger_object_set"], "exercised")
            self.assertEqual(quality["territorial_coverage_observations"]["duplicate_pressure"], "not_observed")

            forbidden_terms = [
                "investors should",
                "policy implication",
                "investment implication",
                "forecast",
                "hypothesis",
                "causal claim",
                "presentation narrative",
            ]
            object_files = sorted((output / "knowledge_objects").glob("*.json"))
            self.assertEqual(len(object_files), 20)
            statements = []
            for path in object_files:
                obj = json.loads(path.read_text())
                validation = self.module.validator.validate_knowledge_object(obj)
                self.assertTrue(validation["ok"], path.name)
                statements.append(obj["generated_statements"][0]["text"])
                text = json.dumps(obj).lower()
                for term in forbidden_terms:
                    self.assertNotIn(term, text)
            self.assertEqual(len(statements), len(set(statements)))

    def test_rejected_candidates_are_preserved_with_reasons(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "campaign5"
            self.module.run_campaign(output)
            rejected_files = sorted((output / "rejected").glob("*.json"))
            self.assertEqual(len(rejected_files), 4)
            categories = set()
            for path in rejected_files:
                record = json.loads(path.read_text())
                self.assertFalse(record["validation"]["ok"])
                categories.update(record["reason_categories"])
            self.assertIn("constitutional_boundary", categories)
            self.assertIn("evidence_contract", categories)
            self.assertIn("lineage_fingerprint", categories)
            self.assertIn("unsupported_inference", categories)


if __name__ == "__main__":
    unittest.main()
