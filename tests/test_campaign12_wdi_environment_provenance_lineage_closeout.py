from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign12_wdi_environment_provenance_lineage_closeout.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign12_wdi_environment_provenance_lineage_closeout", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign12WDIEnvironmentProvenanceLineageCloseoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_campaign_module()

    def test_campaign12_produces_environment_provenance_lineage_closeout_and_mature_family(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.module.run_campaign(Path(tmp))
            quality = result["quality_report"]
            self.assertEqual(quality["knowledge_object_packages_accepted"], 17)
            self.assertEqual(quality["rejected_candidates"], 4)
            self.assertEqual(quality["environment_family_maturity_assessment"]["classification"], "Mature")
            self.assertEqual(quality["production_methodology_assessment"]["classification"], "validated_across_two_mature_families")
            self.assertTrue(quality["determinism_verification"])
            self.assertTrue(quality["fingerprint_stability"])
            self.assertFalse(quality["duplicate_knowledge_objects_detected"])
            self.assertFalse(quality["architecture_taxonomy_validator_or_workflow_pressure"])
            self.assertTrue((Path(tmp) / "reports" / "environment_family_closeout_report.md").exists())
            self.assertTrue((Path(tmp) / "reports" / "production_methodology_closeout_report.md").exists())

    def test_snapshot_is_environment_provenance_lineage_scoped_and_architecture_preserving(self) -> None:
        snapshot = self.module.immutable_wdi_environment_provenance_lineage_snapshot()
        self.assertEqual(snapshot["evidence_family"], "external_wdi_annual_scalar_environment_provenance_lineage")
        self.assertEqual(snapshot["lineage_matrix"]["artifact_count"], 5)
        self.assertTrue(snapshot["lineage_matrix"]["all_required_lineage_fields_present"])
        self.assertEqual(snapshot["architectural_continuity_review"]["default_posture"], "preserve_existing_architecture")
        self.assertTrue(snapshot["architectural_continuity_review"]["authoritative_design_reviewed"])
        for recommendation in snapshot["architectural_continuity_review"]["recommendations"]:
            self.assertEqual(recommendation["classification"], "preserves agreed architecture")

    def test_rejected_candidates_are_preserved_with_expected_failure_categories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.module.run_campaign(Path(tmp))
            categories = {category for item in result["rejected_records"] for category in item["reason_categories"]}
            self.assertIn("provenance", categories)
            self.assertIn("lineage_fingerprint", categories)
            self.assertIn("evidence_contract", categories)
            self.assertIn("unsupported_inference", categories)
            self.assertIn("constitutional_boundary", categories)
            rejected = json.loads((Path(tmp) / "rejected_candidates.json").read_text())
            self.assertEqual(len(rejected), 4)

    def test_methodology_closeout_recommends_third_family_without_architecture_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            quality = self.module.run_campaign(Path(tmp))["quality_report"]
            self.assertEqual(quality["final_recommendation"], "Broaden into a third evidence family using the established production methodology unchanged.")
            self.assertEqual(quality["recommendation_architectural_classification"], "preserves agreed architecture")
            self.assertEqual(quality["minimum_remaining_evidence_before_transition"], "none for WDI annual-scalar third-family broadening; non-WDI multi-source disagreement remains a later falsification gap")


if __name__ == "__main__":
    unittest.main()
