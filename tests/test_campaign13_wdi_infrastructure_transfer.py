from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign13_wdi_infrastructure_transfer.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign13_wdi_infrastructure_transfer", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign13WDIInfrastructureTransferTests(unittest.TestCase):
    def test_campaign13_snapshot_is_infrastructure_annual_scalar_scope(self) -> None:
        campaign = load_campaign_module()
        snapshot = campaign.immutable_wdi_infrastructure_snapshot()
        self.assertEqual(snapshot["source_short_name"], "WDI")
        self.assertEqual(snapshot["evidence_family"], "external_wdi_annual_scalar_infrastructure")
        self.assertEqual(snapshot["scope"]["domain_family"], "infrastructure evidence")
        self.assertEqual(snapshot["audited_inventory"]["indicators_total"], 142)
        self.assertEqual(snapshot["scope"]["frequency"], "annual")
        self.assertEqual(snapshot["scope"]["shape"], "scalar observations")

    def test_campaign13_builds_infrastructure_packages_without_boundary_terms(self) -> None:
        campaign = load_campaign_module()
        snapshot = campaign.immutable_wdi_infrastructure_snapshot()
        packages = campaign.build_source_packages(snapshot)
        self.assertGreaterEqual(len(packages), 12)
        categories = {pkg["evidence_payload"]["knowledge_category"] for pkg in packages}
        self.assertTrue({"factual", "coverage", "evidence_quality", "classified", "derived", "negative", "provenance", "methodological"}.issubset(categories))
        promoted_text = "\n".join(pkg["evidence_payload"]["factual_statement"].lower() for pkg in packages)
        for term in ["forecast", "recommendation", "policy", "investment", "causal"]:
            self.assertNotIn(term, promoted_text)

    def test_campaign13_run_is_deterministic_and_populates_repository(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign13"
            repo = Path(tmp) / "knowledge_repository"
            summary1 = campaign.run_campaign(output, repository_root=repo)
            quality1 = json.loads((output / "production_quality_report.json").read_text())
            packages1 = json.loads((output / "knowledge_object_packages.json").read_text())
            manifest1 = json.loads((repo / "manifest.json").read_text())
            summary2 = campaign.run_campaign(output, repository_root=repo)
            quality2 = json.loads((output / "production_quality_report.json").read_text())
            packages2 = json.loads((output / "knowledge_object_packages.json").read_text())
            manifest2 = json.loads((repo / "manifest.json").read_text())
        self.assertEqual(summary1["snapshot_fingerprint"], summary2["snapshot_fingerprint"])
        self.assertEqual(packages1, packages2)
        self.assertTrue(quality1["determinism_verification"])
        self.assertTrue(quality1["fingerprint_stability"])
        self.assertFalse(quality1["duplicate_knowledge_objects_detected"])
        self.assertEqual(quality1["knowledge_object_packages_accepted"], 19)
        self.assertEqual(quality1["rejected_candidates"], 4)
        self.assertEqual(quality1["cross_family_transfer_assessment"]["methodology_transfer"], "successful")
        self.assertEqual(quality1["knowledge_repository_population"]["persisted_count"], 19)
        self.assertEqual(manifest1["object_count"], 19)
        self.assertEqual(manifest1["repository_fingerprint"], manifest2["repository_fingerprint"])
        self.assertEqual(quality1["knowledge_repository_population"]["repository_fingerprint"], manifest1["repository_fingerprint"])
        self.assertEqual(quality2["knowledge_repository_population"]["repository_fingerprint"], manifest2["repository_fingerprint"])

    def test_campaign13_reports_operational_expansion_without_architecture_change(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign13"
            repo = Path(tmp) / "knowledge_repository"
            summary = campaign.run_campaign(output, repository_root=repo)
            final = (output / "reports" / "campaign_13_final_report.md").read_text()
            transfer = (output / "reports" / "cross_family_transfer_assessment.md").read_text()
        self.assertIn("Operational Expansion", final)
        self.assertIn("Knowledge Repository", final)
        self.assertIn("preserve the existing KnowledgeForge production methodology unchanged", summary["final_recommendation"])
        self.assertIn("Infrastructure-specific", transfer)
        self.assertIn("evidence-family-specific", transfer)
        self.assertIn("KnowledgeForge-wide", transfer)
        self.assertIn("architectural", transfer)


if __name__ == "__main__":
    unittest.main()
