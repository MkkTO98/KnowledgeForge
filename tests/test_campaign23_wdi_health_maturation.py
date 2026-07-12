from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign23_wdi_health_maturation.py"
CAMPAIGN19_PATH = PROJECT_ROOT / "tools" / "run_campaign22_wdi_health_transfer.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign23_wdi_health_maturation", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_campaign22_module():
    spec = importlib.util.spec_from_file_location("run_campaign22_wdi_health_transfer", CAMPAIGN19_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {CAMPAIGN19_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign23WDIHealthMaturationTests(unittest.TestCase):
    def test_health_maturation_snapshot_has_inventory_territorial_and_temporal_matrices(self) -> None:
        campaign = load_campaign_module()
        snapshot = campaign.immutable_wdi_health_maturation_snapshot()
        self.assertEqual(snapshot["source_short_name"], "WDI")
        self.assertEqual(snapshot["evidence_family"], "external_wdi_annual_scalar_health_maturation")
        self.assertEqual(snapshot["scope"]["domain_family"], "health evidence")
        self.assertEqual(snapshot["indicator_inventory"]["indicator_families_total"], 5)
        self.assertEqual(snapshot["territorial_matrix"]["territory_count"], 217)
        self.assertEqual(snapshot["temporal_matrix"]["period_count"], 35)

    def test_campaign23_generates_valid_health_maturation_objects_and_health_summary(self) -> None:
        campaign = load_campaign_module()
        snapshot = campaign.immutable_wdi_health_maturation_snapshot()
        packages = campaign.build_source_packages(snapshot)
        categories = {pkg["evidence_payload"]["knowledge_category"] for pkg in packages}
        self.assertTrue({"coverage", "derived", "classified", "negative", "methodological", "evidence_quality"}.issubset(categories))
        self.assertGreaterEqual(len(packages), 30)
        promoted_text = "\n".join(pkg["evidence_payload"]["factual_statement"].lower() for pkg in packages)
        self.assertIn("health", promoted_text)

    def test_campaign23_is_deterministic_preserves_rejections_and_populates_repository_after_campaign22(self) -> None:
        campaign = load_campaign_module()
        campaign22 = load_campaign22_module()
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            campaign22.run_campaign(Path(tmp) / "campaign22", repository_root=repo)
            output = Path(tmp) / "campaign23"
            summary1 = campaign.run_campaign(output, repository_root=repo)
            quality1 = json.loads((output / "production_quality_report.json").read_text())
            packages1 = json.loads((output / "knowledge_object_packages.json").read_text())
            summary2 = campaign.run_campaign(output, repository_root=repo)
            quality2 = json.loads((output / "production_quality_report.json").read_text())
            packages2 = json.loads((output / "knowledge_object_packages.json").read_text())
            health_exists = (output / "reports" / "repository_health_summary.md").exists()
            impact_exists = (output / "reports" / "knowledge_repository_impact_assessment.md").exists()
        self.assertEqual(summary1["quality_report"]["final_snapshot_fingerprint"], summary2["quality_report"]["final_snapshot_fingerprint"])
        self.assertEqual(packages1, packages2)
        self.assertEqual(quality1["knowledge_object_packages_accepted"], 36)
        self.assertEqual(quality1["rejected_candidates"], 4)
        self.assertTrue(quality1["determinism_verification"])
        self.assertTrue(quality1["fingerprint_stability"])
        self.assertFalse(quality1["duplicate_knowledge_objects_detected"])
        self.assertEqual(quality1["knowledge_repository_impact_assessment"]["repository_object_count_before"], 19)
        self.assertEqual(quality1["knowledge_repository_impact_assessment"]["repository_object_count_after"], 55)
        self.assertEqual(quality2["knowledge_repository_impact_assessment"]["repository_object_count_after"], 55)
        self.assertTrue(health_exists)
        self.assertTrue(impact_exists)

    def test_health_stable_not_mature_and_doctrine_preserved(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            summary = campaign.run_campaign(Path(tmp) / "campaign23", repository_root=Path(tmp) / "knowledge_repository")
            quality = summary["quality_report"]
            final = (Path(tmp) / "campaign23" / "reports" / "campaign_23_final_report.md").read_text()
        self.assertEqual(quality["health_family_maturity_assessment"]["classification"], "Stable")
        self.assertFalse(quality["architecture_taxonomy_validator_or_workflow_pressure"])
        self.assertIn("preserves agreed architecture", final)
        self.assertIn("provenance-lineage", quality["final_recommendation"])


if __name__ == "__main__":
    unittest.main()
