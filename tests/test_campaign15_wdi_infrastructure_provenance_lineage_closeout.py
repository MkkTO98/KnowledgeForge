from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign15_wdi_infrastructure_provenance_lineage_closeout.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign15_wdi_infrastructure_provenance_lineage_closeout", SCRIPT_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign15WDIInfrastructureProvenanceLineageCloseoutTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_campaign_module()

    def test_campaign15_produces_infrastructure_provenance_lineage_closeout_and_mature_family(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign15"
            repo = Path(tmp) / "repo"
            campaign13 = self.module.PROJECT_ROOT / "artifacts" / "production" / "campaign-13-wdi-infrastructure-annual-scalar-evidence-quality-coverage-transfer" / "knowledge_object_packages.json"
            campaign14 = self.module.PROJECT_ROOT / "artifacts" / "production" / "campaign-14-wdi-infrastructure-indicator-family-coverage-maturation" / "knowledge_object_packages.json"
            self.module.knowledge_repository.persist_knowledge_object_packages(json.loads(campaign13.read_text()), repo)
            self.module.knowledge_repository.persist_knowledge_object_packages(json.loads(campaign14.read_text()), repo)
            result = self.module.run_campaign(output, repository_root=repo)
            quality = result["quality_report"]
            health = quality["repository_health_summary"]
            impact = quality["knowledge_repository_impact_assessment"]
            self.assertEqual(quality["knowledge_object_packages_accepted"], 17)
            self.assertEqual(quality["rejected_candidates"], 4)
            self.assertEqual(quality["infrastructure_family_maturity_assessment"]["classification"], "Mature")
            self.assertTrue(quality["determinism_verification"])
            self.assertTrue(quality["fingerprint_stability"])
            self.assertFalse(quality["duplicate_knowledge_objects_detected"])
            self.assertEqual(quality["architectural_continuity_classification"], "preserves agreed architecture")
            self.assertEqual(health["previous_repository_object_count"], 55)
            self.assertEqual(health["total_knowledge_objects"], 72)
            self.assertEqual(health["objects_added_this_campaign"], 17)
            self.assertEqual(impact["repository_object_count_before"], 55)
            self.assertEqual(impact["repository_object_count_after"], 72)
            self.assertEqual(impact["new_knowledge_objects_added"], 17)
            self.assertTrue((output / "reports" / "infrastructure_family_closeout_report.md").exists())
            self.assertTrue((output / "reports" / "repository_health_summary.md").exists())
            self.assertTrue((output / "reports" / "knowledge_repository_impact_assessment.md").exists())

    def test_snapshot_is_infrastructure_provenance_lineage_scoped_and_architecture_preserving(self) -> None:
        snapshot = self.module.immutable_wdi_infrastructure_provenance_lineage_snapshot()
        self.assertEqual(snapshot["evidence_family"], "external_wdi_annual_scalar_infrastructure_provenance_lineage")
        self.assertEqual(snapshot["lineage_matrix"]["artifact_count"], 5)
        self.assertTrue(snapshot["lineage_matrix"]["all_required_lineage_fields_present"])
        self.assertEqual(snapshot["infrastructure_family_maturity"]["classification"], "Mature")
        for recommendation in snapshot["architectural_continuity_review"]["recommendations"]:
            self.assertEqual(recommendation["classification"], "preserves agreed architecture")

    def test_rejected_candidates_are_preserved_with_expected_failure_categories(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = self.module.run_campaign(Path(tmp) / "campaign15", repository_root=Path(tmp) / "repo")
            categories = {category for item in result["rejected_records"] for category in item["reason_categories"]}
            self.assertIn("provenance", categories)
            self.assertIn("lineage_fingerprint", categories)
            self.assertIn("evidence_contract", categories)
            self.assertIn("unsupported_inference", categories)
            self.assertIn("constitutional_boundary", categories)
            rejected = json.loads((Path(tmp) / "campaign15" / "rejected_candidates.json").read_text())
            self.assertEqual(len(rejected), 4)

    def test_campaign15_final_recommendation_moves_to_next_roadmap_family_without_architecture_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign15"
            result = self.module.run_campaign(output, repository_root=Path(tmp) / "repo")
            quality = result["quality_report"]
            self.assertEqual(quality["final_recommendation"], "Proceed to WDI Energy & Mining annual-scalar evidence as the next Phase 2 production family using the established Production Doctrine unchanged.")
            self.assertEqual(quality["architectural_continuity_classification"], "preserves agreed architecture")
            impact_text = (output / "reports" / "knowledge_repository_impact_assessment.md").read_text()
            self.assertIn("Future recomputation avoided", impact_text)
            self.assertIn("Infrastructure provenance-lineage", impact_text)


if __name__ == "__main__":
    unittest.main()
