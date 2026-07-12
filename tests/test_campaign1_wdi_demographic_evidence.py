from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign1_wdi_demographic_evidence.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign1_wdi_demographic_evidence", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign1WdiDemographicEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.module = load_campaign_module()

    def test_immutable_snapshot_is_deterministic(self):
        first = self.module.immutable_wdi_snapshot()
        second = self.module.immutable_wdi_snapshot()
        self.assertEqual(first, second)
        self.assertTrue(first["snapshot_fingerprint"].startswith("sha256:"))
        self.assertEqual(first["audited_inventory"]["period_count"], 35)
        self.assertEqual(first["demographic_structure_inventory"]["age_sex_cohort_indicators"], 68)

    def test_campaign_produces_valid_domain_specific_objects(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "campaign1"
            summary = self.module.run_campaign(output)
            self.assertEqual(summary["accepted"], 12)
            self.assertEqual(summary["rejected"], 4)
            self.assertTrue(summary["determinism_verified"])
            self.assertTrue(summary["fingerprint_stability"])

            quality = json.loads((output / "production_quality_report.json").read_text())
            self.assertEqual(quality["knowledge_object_packages_accepted"], 12)
            self.assertEqual(quality["source_evidence_packages_processed"], 12)
            self.assertEqual(quality["rejected_candidates"], 4)
            self.assertFalse(quality["duplicate_knowledge_objects_detected"])
            self.assertTrue(quality["provenance_completeness"])
            self.assertIn("coverage", quality["knowledge_categories_produced"])
            self.assertIn("evidence_quality", quality["knowledge_categories_produced"])
            self.assertIn("negative", quality["knowledge_categories_produced"])

            object_files = sorted((output / "knowledge_objects").glob("*.json"))
            self.assertEqual(len(object_files), 12)
            forbidden_terms = [
                "investors should",
                "policy implication",
                "investment implication",
                "forecast",
                "hypothesis",
                "causal claim",
                "presentation narrative",
            ]
            for path in object_files:
                obj = json.loads(path.read_text())
                validation = self.module.validator.validate_knowledge_object(obj)
                self.assertTrue(validation["ok"], path.name)
                text = json.dumps(obj).lower()
                for term in forbidden_terms:
                    self.assertNotIn(term, text)

    def test_rejected_candidates_are_preserved_with_reasons(self):
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "campaign1"
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


if __name__ == "__main__":
    unittest.main()
