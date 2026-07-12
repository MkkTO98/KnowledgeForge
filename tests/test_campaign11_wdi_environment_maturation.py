from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign11_wdi_environment_maturation.py"
FORBIDDEN_ACCEPTED_TERMS = [
    "causal claim",
    "forecast",
    "hypothesis",
    "investment",
    "policy meaning",
    "recommendation",
    "significant for",
]


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("campaign11", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign11WDIEnvironmentMaturationTests(unittest.TestCase):
    def test_environment_maturation_snapshot_has_inventory_territorial_and_temporal_matrices(self):
        campaign = load_campaign_module()
        snapshot = campaign.immutable_wdi_environment_maturation_snapshot()
        self.assertEqual(snapshot["evidence_family"], "external_wdi_annual_scalar_environment_maturation")
        self.assertEqual(snapshot["indicator_inventory"]["indicator_families_total"], 5)
        self.assertGreater(snapshot["territorial_matrix"]["matrix_cell_count"], 0)
        self.assertGreater(snapshot["temporal_matrix"]["matrix_cell_count"], 0)
        self.assertFalse(snapshot["architecture_change_authorized"])
        self.assertFalse(snapshot["external_data_accessed"])

    def test_campaign11_generates_valid_environment_maturation_objects(self):
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            result = campaign.run_campaign(Path(tmp))
        qr = result["quality_report"]
        self.assertGreaterEqual(qr["knowledge_object_packages_accepted"], 20)
        self.assertEqual(qr["environment_family_maturity_assessment"]["classification"], "Stable")
        self.assertFalse(qr["architecture_taxonomy_validator_or_workflow_pressure"])
        self.assertEqual(qr["comparison_against_campaign8"]["workflow_transfer"], "unchanged")
        self.assertEqual(qr["comparison_against_demographic_equivalent_stage"]["equivalent_stage"], "Campaigns 4-6")
        categories = qr["knowledge_categories_produced"]
        for category in ["factual", "classified", "coverage", "derived", "evidence_quality", "negative", "provenance", "methodological"]:
            self.assertIn(category, categories)
        accepted_text = "\n".join(obj["generated_statements"][0]["text"].lower() for obj in result["accepted_objects"])
        for term in FORBIDDEN_ACCEPTED_TERMS:
            self.assertNotIn(term, accepted_text)

    def test_campaign11_is_deterministic_and_preserves_rejected_candidates(self):
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = campaign.run_campaign(Path(first))
            two = campaign.run_campaign(Path(second))
        self.assertEqual(one["quality_report"]["final_snapshot_fingerprint"], two["quality_report"]["final_snapshot_fingerprint"])
        self.assertTrue(one["quality_report"]["determinism_verification"])
        self.assertTrue(one["quality_report"]["fingerprint_stability"])
        self.assertFalse(one["quality_report"]["duplicate_knowledge_objects_detected"])
        self.assertGreaterEqual(len(one["rejected_records"]), 4)
        reason_categories = {cat for record in one["rejected_records"] for cat in record["reason_categories"]}
        self.assertIn("unsupported_inference", reason_categories)
        self.assertIn("provenance", reason_categories)

    def test_environment_maturity_does_not_imply_knowledgeforge_methodology_mature(self):
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            result = campaign.run_campaign(Path(tmp))
        qr = result["quality_report"]
        self.assertEqual(qr["environment_family_maturity_assessment"]["classification"], "Stable")
        self.assertEqual(qr["knowledgeforge_methodology_maturity_assessment"], "wait_until_environment_family_reaches_mature")
        self.assertEqual(qr["next_recommended_campaign"], "Campaign 12 should execute WDI Environment provenance-lineage completeness as the family closeout campaign.")


if __name__ == "__main__":
    unittest.main()
