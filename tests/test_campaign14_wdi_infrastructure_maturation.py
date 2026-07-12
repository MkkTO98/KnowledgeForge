from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign14_wdi_infrastructure_maturation.py"
CAMPAIGN13_PATH = PROJECT_ROOT / "tools" / "run_campaign13_wdi_infrastructure_transfer.py"

FORBIDDEN_ACCEPTED_TERMS = [
    "causal claim",
    "forecast",
    "hypothesis",
    "investment",
    "policy meaning",
    "recommendation",
    "significant for",
]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign14WDIInfrastructureMaturationTests(unittest.TestCase):
    def test_infrastructure_maturation_snapshot_has_inventory_territorial_and_temporal_matrices(self):
        campaign = load_module(SCRIPT_PATH, "campaign14")
        snapshot = campaign.immutable_wdi_infrastructure_maturation_snapshot()
        self.assertEqual(snapshot["evidence_family"], "external_wdi_annual_scalar_infrastructure_maturation")
        self.assertEqual(snapshot["indicator_inventory"]["indicator_families_total"], 5)
        self.assertEqual(snapshot["indicator_inventory"]["indicators_total"], 142)
        self.assertGreater(snapshot["territorial_matrix"]["matrix_cell_count"], 0)
        self.assertGreater(snapshot["temporal_matrix"]["matrix_cell_count"], 0)
        self.assertFalse(snapshot["architecture_change_authorized"])
        self.assertFalse(snapshot["external_data_accessed"])

    def test_campaign14_generates_valid_infrastructure_maturation_objects_and_health_summary(self):
        campaign = load_module(SCRIPT_PATH, "campaign14")
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            result = campaign.run_campaign(Path(tmp) / "campaign14", repository_root=repo)
        qr = result["quality_report"]
        self.assertEqual(qr["knowledge_object_packages_accepted"], 36)
        self.assertEqual(qr["infrastructure_family_maturity_assessment"]["classification"], "Stable")
        self.assertFalse(qr["architecture_taxonomy_validator_or_workflow_pressure"])
        self.assertEqual(qr["comparison_against_campaign13"]["workflow_transfer"], "unchanged")
        self.assertEqual(qr["comparison_against_demographic_equivalent_stage"]["equivalent_stage"], "Campaigns 4-6")
        categories = qr["knowledge_categories_produced"]
        for category in ["factual", "classified", "coverage", "derived", "evidence_quality", "negative", "provenance", "methodological"]:
            self.assertIn(category, categories)
        health = qr["repository_health_summary"]
        self.assertEqual(health["objects_added_this_campaign"], 36)
        self.assertEqual(health["repository_growth_since_previous_campaign"], 36)
        self.assertEqual(health["unresolved_repository_quality_concerns"], [])
        self.assertTrue(health["provenance_completeness"])
        self.assertTrue(health["fingerprint_stability"])
        impact = qr["knowledge_repository_impact_assessment"]
        self.assertEqual(impact["repository_object_count_before"], 0)
        self.assertEqual(impact["repository_object_count_after"], 36)
        self.assertEqual(impact["new_knowledge_objects_added"], 36)
        self.assertIn("infrastructure metadata family inventory", impact["new_reusable_knowledge_introduced"])
        self.assertIn("coverage", impact["knowledge_categories_expanded"])
        self.assertIn("external_wdi_annual_scalar_infrastructure_maturation", impact["evidence_family_coverage_expanded"])
        self.assertGreaterEqual(len(impact["future_recomputation_avoided_for_downstream_projects"]), 3)
        self.assertEqual(impact["repository_quality_concerns_discovered"], [])
        accepted_text = "\n".join(obj["generated_statements"][0]["text"].lower() for obj in result["accepted_objects"])
        for term in FORBIDDEN_ACCEPTED_TERMS:
            self.assertNotIn(term, accepted_text)

    def test_campaign14_is_deterministic_preserves_rejections_and_populates_repository_after_campaign13(self):
        campaign13 = load_module(CAMPAIGN13_PATH, "campaign13")
        campaign14 = load_module(SCRIPT_PATH, "campaign14")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            repo = root / "knowledge_repository"
            campaign13.run_campaign(root / "campaign13", repository_root=repo)
            before = json.loads((repo / "manifest.json").read_text())
            one = campaign14.run_campaign(root / "campaign14", repository_root=repo)
            after = json.loads((repo / "manifest.json").read_text())
            two = campaign14.run_campaign(root / "campaign14", repository_root=repo)
            after_second = json.loads((repo / "manifest.json").read_text())
        self.assertEqual(before["object_count"], 19)
        self.assertEqual(after["object_count"], 55)
        self.assertEqual(after_second["object_count"], 55)
        self.assertEqual(one["quality_report"]["repository_health_summary"]["total_knowledge_objects"], 55)
        self.assertEqual(one["quality_report"]["repository_health_summary"]["repository_growth_since_previous_campaign"], 36)
        self.assertEqual(two["quality_report"]["final_snapshot_fingerprint"], one["quality_report"]["final_snapshot_fingerprint"])
        self.assertTrue(one["quality_report"]["determinism_verification"])
        self.assertTrue(one["quality_report"]["fingerprint_stability"])
        self.assertFalse(one["quality_report"]["duplicate_knowledge_objects_detected"])
        self.assertGreaterEqual(len(one["rejected_records"]), 4)
        reason_categories = {cat for record in one["rejected_records"] for cat in record["reason_categories"]}
        self.assertIn("unsupported_inference", reason_categories)
        self.assertIn("provenance", reason_categories)

    def test_infrastructure_stable_not_mature_and_doctrine_preserved(self):
        campaign = load_module(SCRIPT_PATH, "campaign14")
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign14"
            result = campaign.run_campaign(output, repository_root=Path(tmp) / "repo")
            qr = result["quality_report"]
            final = (output / "reports" / "campaign_14_final_report.md").read_text()
            health = (output / "reports" / "repository_health_summary.md").read_text()
            impact = (output / "reports" / "knowledge_repository_impact_assessment.md").read_text()
        self.assertEqual(qr["infrastructure_family_maturity_assessment"]["classification"], "Stable")
        self.assertEqual(qr["architectural_continuity_classification"], "preserves agreed architecture")
        self.assertEqual(qr["next_recommended_campaign"], "Campaign 15 should execute WDI Infrastructure provenance-lineage completeness as the family closeout campaign.")
        self.assertIn("Repository Health", health)
        self.assertIn("Knowledge Repository Impact Assessment", impact)
        self.assertIn("Future recomputation avoided", impact)
        self.assertIn("Operational Expansion", final)
        self.assertIn("preserves agreed architecture", final)


if __name__ == "__main__":
    unittest.main()
