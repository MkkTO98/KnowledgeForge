from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign10_cross_campaign_recurrence_audit.py"
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
    spec = importlib.util.spec_from_file_location("campaign10", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign10CrossCampaignRecurrenceAuditTests(unittest.TestCase):
    def test_snapshot_uses_existing_campaign_artifacts_only(self) -> None:
        campaign = load_campaign_module()
        snapshot = campaign.build_cross_campaign_snapshot()
        self.assertEqual(snapshot["campaign_id"], campaign.CAMPAIGN_ID)
        self.assertEqual(snapshot["campaigns_audited"], 10)
        self.assertEqual(snapshot["campaign_range"], "0-9")
        self.assertTrue(all(row["quality_report_path"].startswith("artifacts/production/") for row in snapshot["campaign_summaries"]))
        self.assertTrue(all(row["quality_report_exists"] for row in snapshot["campaign_summaries"]))
        self.assertFalse(snapshot["external_data_accessed"])
        self.assertGreaterEqual(snapshot["aggregate_metrics"]["total_accepted_objects"], 1)
        self.assertGreaterEqual(snapshot["aggregate_metrics"]["total_rejected_candidates"], 1)

    def test_campaign10_generates_recurrence_objects_without_forbidden_terms(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            result = campaign.run_campaign(Path(tmp))
        objects = result["accepted_objects"]
        self.assertGreaterEqual(len(objects), 10)
        self.assertEqual(result["quality_report"]["knowledge_object_packages_accepted"], len(objects))
        self.assertTrue(all(len(obj["evidence_references"]) >= 2 for obj in objects if "cross_campaign" in obj["scope"].get("scope_type", "")))
        accepted_text = "\n".join(obj["generated_statements"][0]["text"].lower() for obj in objects)
        for term in FORBIDDEN_ACCEPTED_TERMS:
            self.assertNotIn(term, accepted_text)

    def test_campaign10_audits_duplicate_registry_and_helper_pressure(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            result = campaign.run_campaign(Path(tmp))
        qr = result["quality_report"]
        self.assertEqual(qr["duplicate_registry_implementation_justified"], False)
        self.assertEqual(qr["new_helper_extraction_justified"], False)
        self.assertEqual(qr["architecture_taxonomy_validator_or_workflow_pressure"], False)
        self.assertEqual(qr["roadmap_recommendation"], "continue_with_wdi_environment_maturation")
        self.assertEqual(qr["falsification_focus"]["prior_campaign_artifacts_as_source_evidence"], "validated")
        self.assertIn("PEL-007", qr["pel_implications"])

    def test_campaign10_is_deterministic_and_preserves_rejected_candidates(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = campaign.run_campaign(Path(first))
            two = campaign.run_campaign(Path(second))
        self.assertEqual(one["quality_report"]["final_snapshot_fingerprint"], two["quality_report"]["final_snapshot_fingerprint"])
        self.assertTrue(one["quality_report"]["determinism_verification"])
        self.assertTrue(one["quality_report"]["fingerprint_stability"])
        self.assertFalse(one["quality_report"]["duplicate_knowledge_objects_detected"])
        self.assertGreaterEqual(one["quality_report"]["rejected_candidates"], 4)
        categories = {cat for record in one["rejected_records"] for cat in record["reason_categories"]}
        self.assertIn("unsupported_inference", categories)
        self.assertIn("provenance", categories)


if __name__ == "__main__":
    unittest.main()
