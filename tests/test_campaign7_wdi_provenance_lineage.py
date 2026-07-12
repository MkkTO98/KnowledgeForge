from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign7_wdi_provenance_lineage.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign7_wdi_provenance_lineage", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign7WdiProvenanceLineageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_campaign_module()

    def test_campaign_produces_valid_provenance_lineage_objects_and_mature_family(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            summary = self.module.run_campaign(Path(tmp))
            self.assertEqual(summary["accepted"], 16)
            self.assertEqual(summary["rejected"], 4)
            self.assertTrue(summary["determinism_verified"])
            self.assertTrue(summary["fingerprint_stability"])
            self.assertFalse(summary["duplicate_knowledge_objects_detected"])
            self.assertEqual(summary["family_maturity_assessment"], "Mature")
            quality = json.loads((Path(tmp) / "production_quality_report.json").read_text())
            self.assertEqual(quality["average_evidence_references_per_knowledge_object"], 1.0)
            self.assertTrue(quality["provenance_completeness"])
            self.assertEqual(quality["lineage_completeness_observations"]["raw_artifact_hashes"], "exercised")
            self.assertEqual(quality["lineage_completeness_observations"]["release_keys"], "exercised")
            self.assertEqual(quality["campaign_family_maturity_assessment"]["classification"], "Mature")
            self.assertIn("provenance", quality["knowledge_categories_produced"])
            self.assertIn("methodological", quality["knowledge_categories_produced"])
            self.assertTrue((Path(tmp) / "reports" / "family_closeout_report.md").exists())

    def test_snapshot_is_deterministic_and_lineage_scoped(self) -> None:
        first = self.module.immutable_wdi_provenance_lineage_snapshot()
        second = self.module.immutable_wdi_provenance_lineage_snapshot()
        self.assertEqual(first, second)
        self.assertEqual(first["evidence_family"], "external_wdi_annual_scalar_demographic_structure_provenance_lineage")
        self.assertEqual(first["lineage_matrix"]["artifact_count"], 4)
        self.assertTrue(first["lineage_matrix"]["all_required_lineage_fields_present"])
        forbidden = " ".join(json.dumps(first).lower().split())
        for term in ["forecast", "causal", "recommendation", "investment", "policy meaning"]:
            self.assertNotIn(term, forbidden)

    def test_rejected_candidates_are_preserved_with_provenance_failure_reasons(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.module.run_campaign(Path(tmp))
            rejected = json.loads((Path(tmp) / "rejected_knowledge_object_catalogue.json").read_text())
            self.assertEqual(len(rejected), 4)
            categories = {category for item in rejected for category in item["reason_categories"]}
            self.assertIn("provenance", categories)
            self.assertIn("lineage_fingerprint", categories)
            self.assertIn("evidence_contract", categories)
            self.assertIn("unsupported_inference", categories)
            self.assertIn("constitutional_boundary", categories)


if __name__ == "__main__":
    unittest.main()
