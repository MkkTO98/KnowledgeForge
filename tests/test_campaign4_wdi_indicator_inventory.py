from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign4_wdi_indicator_inventory.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign4_wdi_indicator_inventory", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign4WdiIndicatorInventoryTests(unittest.TestCase):
    def setUp(self):
        self.module = load_campaign_module()

    def test_snapshot_is_deterministic_and_inventory_scoped(self):
        first = self.module.immutable_wdi_indicator_inventory_snapshot()
        second = self.module.immutable_wdi_indicator_inventory_snapshot()
        self.assertEqual(first, second)
        self.assertTrue(first["snapshot_fingerprint"].startswith("sha256:"))
        self.assertEqual(first["audited_inventory"]["indicator_families_total"], 4)
        self.assertEqual(first["audited_inventory"]["indicators_total"], 182)
        self.assertEqual(first["dimension_inventory"]["supported_dimensions"], ["indicator", "territory", "period"])
        self.assertIn("age_band", first["dimension_inventory"]["unsupported_dimensions"])

    def test_campaign_produces_valid_inventory_objects(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "campaign4"
            summary = self.module.run_campaign(output)
            self.assertEqual(summary["accepted"], 14)
            self.assertEqual(summary["rejected"], 4)
            self.assertTrue(summary["determinism_verified"])
            self.assertTrue(summary["fingerprint_stability"])
            self.assertFalse(summary["duplicate_knowledge_objects_detected"])

            quality = json.loads((output / "production_quality_report.json").read_text())
            self.assertEqual(quality["knowledge_object_packages_accepted"], 14)
            self.assertEqual(quality["source_evidence_packages_processed"], 14)
            self.assertEqual(quality["rejected_candidates"], 4)
            self.assertIn("classified", quality["knowledge_categories_produced"])
            self.assertIn("factual", quality["knowledge_categories_produced"])
            self.assertIn("coverage", quality["knowledge_categories_produced"])
            self.assertIn("negative", quality["knowledge_categories_produced"])
            self.assertIn("campaign_4", quality["cross_campaign_metric_comparison"])
            self.assertTrue(quality["provenance_completeness"])
            self.assertEqual(quality["falsification_observations"]["classification_consistency"], "exercised")
            self.assertEqual(quality["falsification_observations"]["duplicate_pressure"], "not_observed")

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
            self.assertEqual(len(object_files), 14)
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
            output = Path(td) / "campaign4"
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
