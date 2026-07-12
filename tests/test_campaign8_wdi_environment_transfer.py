from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign8_wdi_environment_transfer.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign8_wdi_environment_transfer", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign8WDIEnvironmentTransferTests(unittest.TestCase):
    def test_campaign8_snapshot_is_environment_annual_scalar_scope(self):
        campaign = load_campaign_module()
        snapshot = campaign.immutable_wdi_environment_snapshot()
        self.assertEqual(snapshot["source_short_name"], "WDI")
        self.assertEqual(snapshot["evidence_family"], "external_wdi_annual_scalar_environment")
        self.assertEqual(snapshot["scope"]["domain_family"], "environment evidence")
        self.assertEqual(snapshot["audited_inventory"]["indicators_total"], 188)
        self.assertEqual(snapshot["scope"]["frequency"], "annual")
        self.assertEqual(snapshot["scope"]["shape"], "scalar observations")

    def test_campaign8_builds_replicated_environment_packages_without_boundary_terms(self):
        campaign = load_campaign_module()
        snapshot = campaign.immutable_wdi_environment_snapshot()
        packages = campaign.build_source_packages(snapshot)
        self.assertGreaterEqual(len(packages), 12)
        categories = {pkg["evidence_payload"]["knowledge_category"] for pkg in packages}
        self.assertTrue({"factual", "coverage", "evidence_quality", "classified", "derived", "negative", "provenance", "methodological"}.issubset(categories))
        forbidden = ["forecast", "recommendation", "policy", "investment", "causal"]
        promoted_text = "\n".join(
            pkg["evidence_payload"]["factual_statement"].lower()
            for pkg in packages
        )
        for term in forbidden:
            self.assertNotIn(term, promoted_text)

    def test_campaign8_run_is_deterministic_and_preserves_rejected_candidates(self):
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign8"
            summary1 = campaign.run_campaign(output)
            first_quality = json.loads((output / "production_quality_report.json").read_text())
            first_catalogue = json.loads((output / "generated_knowledge_object_catalogue.json").read_text())
            summary2 = campaign.run_campaign(output)
            second_quality = json.loads((output / "production_quality_report.json").read_text())
            second_catalogue = json.loads((output / "generated_knowledge_object_catalogue.json").read_text())
        self.assertEqual(summary1["snapshot_fingerprint"], summary2["snapshot_fingerprint"])
        self.assertEqual(first_catalogue, second_catalogue)
        self.assertTrue(first_quality["determinism_verification"])
        self.assertTrue(first_quality["fingerprint_stability"])
        self.assertTrue(first_quality["provenance_completeness"])
        self.assertFalse(first_quality["duplicate_knowledge_objects_detected"])
        self.assertEqual(first_quality["rejected_candidates"], 4)
        self.assertEqual(first_quality["average_evidence_references_per_knowledge_object"], 1.0)
        self.assertEqual(first_quality["cross_family_transfer_assessment"]["methodology_transfer"], "successful")

    def test_campaign8_reports_replication_against_campaign1(self):
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign8"
            campaign.run_campaign(output)
            replication = (output / "reports" / "replication_assessment.md").read_text()
            transfer = (output / "reports" / "cross_family_transfer_assessment.md").read_text()
            final = (output / "reports" / "campaign_8_final_report.md").read_text()
        self.assertIn("Campaign 1", replication)
        self.assertIn("production workflow", replication)
        self.assertIn("successful", replication.lower())
        self.assertIn("Environment-specific", transfer)
        self.assertIn("evidence-family-specific", transfer)
        self.assertIn("KnowledgeForge-wide", transfer)
        self.assertIn("architectural", transfer)
        self.assertIn("Campaign 9 should proceed unchanged", final)


if __name__ == "__main__":
    unittest.main()
