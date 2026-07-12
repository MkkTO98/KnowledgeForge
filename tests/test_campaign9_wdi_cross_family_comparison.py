from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign9_wdi_cross_family_comparison.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("campaign9", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign9WDICrossFamilyComparisonTests(unittest.TestCase):
    def test_campaign9_snapshot_compares_demographic_and_environment_families(self):
        campaign = load_campaign_module()
        snapshot = campaign.immutable_cross_family_snapshot()
        self.assertEqual(snapshot["campaign_id"], campaign.CAMPAIGN_ID)
        self.assertEqual(snapshot["families"]["demographic"]["evidence_family"], "external_wdi_annual_scalar_demographic_structure")
        self.assertEqual(snapshot["families"]["environment"]["evidence_family"], "external_wdi_annual_scalar_environment")
        self.assertEqual(snapshot["overlap"]["territory_count"], 217)
        self.assertEqual(snapshot["overlap"]["period_start"], 1990)
        self.assertEqual(snapshot["overlap"]["period_end"], 2024)
        self.assertNotEqual(snapshot["families"]["demographic"]["snapshot_fingerprint"], snapshot["families"]["environment"]["snapshot_fingerprint"])

    def test_campaign9_builds_multi_reference_objects_without_forbidden_comparison_terms(self):
        campaign = load_campaign_module()
        result = campaign.run_campaign(Path(tempfile.mkdtemp()))
        self.assertGreaterEqual(len(result["accepted_objects"]), 12)
        multi_ref_objects = [obj for obj in result["accepted_objects"] if len(obj["evidence_references"]) >= 2]
        self.assertGreaterEqual(len(multi_ref_objects), 8)
        self.assertGreater(result["quality_report"]["average_evidence_references_per_knowledge_object"], 1.0)
        self.assertTrue(result["quality_report"]["multi_reference_accepted_objects"])
        categories = {obj["generated_statements"][0]["statement_type"] for obj in result["accepted_objects"]}
        self.assertTrue({"coverage", "derived", "methodological", "negative", "provenance", "evidence_quality"}.issubset(categories))
        promoted_text = "\n".join(obj["generated_statements"][0]["text"].lower() for obj in result["accepted_objects"])
        for forbidden in ["significant", "causes", "forecast", "recommend", "policy meaning", "investment meaning", "hypothesis"]:
            self.assertNotIn(forbidden, promoted_text)

    def test_campaign9_run_is_deterministic_and_exercises_duplicate_pressure(self):
        campaign = load_campaign_module()
        first = campaign.run_campaign(Path(tempfile.mkdtemp()))
        second = campaign.run_campaign(Path(tempfile.mkdtemp()))
        self.assertEqual(first["snapshot_fingerprint"], second["snapshot_fingerprint"])
        self.assertEqual(first["quality_report"]["final_snapshot_fingerprint"], second["quality_report"]["final_snapshot_fingerprint"])
        self.assertTrue(first["quality_report"]["determinism_verification"])
        self.assertTrue(first["quality_report"]["fingerprint_stability"])
        self.assertTrue(first["quality_report"]["duplicate_pressure_exercised"])
        self.assertFalse(first["quality_report"]["duplicate_knowledge_objects_detected"])
        self.assertGreaterEqual(first["quality_report"]["rejected_candidates"], 4)

    def test_campaign9_reports_cross_family_falsification_focus(self):
        campaign = load_campaign_module()
        result = campaign.run_campaign(Path(tempfile.mkdtemp()))
        assessment = result["quality_report"]["cross_family_comparison_assessment"]
        self.assertEqual(assessment["multi_reference_accepted_objects"], "validated")
        self.assertEqual(assessment["partial_provenance_disagreement"], "naturally_present")
        self.assertEqual(assessment["cross_family_comparison_without_interpretation"], "validated")
        self.assertEqual(assessment["methodology_transfer_after_campaign8"], "successful")
        self.assertEqual(result["quality_report"]["final_recommendation"], "Campaign 10 should proceed unchanged; preserve the existing KnowledgeForge production methodology unchanged.")


if __name__ == "__main__":
    unittest.main()
