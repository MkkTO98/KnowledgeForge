from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign33_wdi_financial_sector_provenance_lineage_closeout.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign33_wdi_financial_sector_provenance_lineage_closeout", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {SCRIPT_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign33WDIFinancialSectorProvenanceLineageCloseoutTests(unittest.TestCase):
    def test_snapshot_is_financial_sector_provenance_lineage_scoped_and_architecture_preserving(self) -> None:
        campaign = load_campaign_module()
        snapshot = campaign.immutable_wdi_financial_sector_provenance_lineage_snapshot()
        self.assertEqual(snapshot["source_short_name"], "WDI")
        self.assertEqual(snapshot["evidence_family"], "external_wdi_annual_scalar_financial_sector_provenance_lineage")
        self.assertEqual(snapshot["scope"]["domain_family"], "financial_sector evidence")
        self.assertTrue(snapshot["financial_sector_family_maturity"]["classification"] == "Mature")
        self.assertFalse(snapshot["architectural_continuity_review"]["refinements_supported"])
        self.assertEqual(snapshot["doctrine_review_acceptance"]["accepted_decision"], "Recommendation B")
        self.assertEqual(snapshot["next_required_task_after_campaign33"], "Bounded PostgreSQL Knowledge Repository Realization Decision")

    def test_campaign33_produces_financial_sector_provenance_lineage_closeout_and_mature_family(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign33"
            repo = Path(tmp) / "knowledge_repository"
            summary1 = campaign.run_campaign(output, repository_root=repo)
            quality1 = json.loads((output / "production_quality_report.json").read_text())
            packages1 = json.loads((output / "knowledge_object_packages.json").read_text())
            summary2 = campaign.run_campaign(output, repository_root=repo)
            quality2 = json.loads((output / "production_quality_report.json").read_text())
            packages2 = json.loads((output / "knowledge_object_packages.json").read_text())
            family_report = (output / "reports" / "financial_sector_family_closeout_report.md").read_text()
            method_report = (output / "reports" / "production_methodology_closeout_report.md").read_text()
        self.assertEqual(summary1["quality_report"]["final_snapshot_fingerprint"], summary2["quality_report"]["final_snapshot_fingerprint"])
        self.assertEqual(packages1, packages2)
        self.assertEqual(quality1["knowledge_object_packages_accepted"], 17)
        self.assertEqual(quality1["rejected_candidates"], 4)
        self.assertEqual(quality1["financial_sector_family_maturity_assessment"]["classification"], "Mature")
        self.assertTrue(quality1["determinism_verification"])
        self.assertTrue(quality1["fingerprint_stability"])
        self.assertFalse(quality1["duplicate_knowledge_objects_detected"])
        self.assertIn("WDI Financial Sector Production Family Closeout Report", family_report)
        self.assertIn("preserved across nine Mature WDI annual-scalar production families", method_report)
        self.assertEqual(quality2["knowledge_repository_impact_assessment"]["repository_object_count_after"], 17)

    def test_rejected_candidates_are_preserved_with_expected_failure_categories(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign33"
            summary = campaign.run_campaign(output, repository_root=Path(tmp) / "knowledge_repository")
            rejected = json.loads((output / "rejected_candidates.json").read_text())
        categories = {failure for candidate in rejected for failure in candidate["reason_categories"]}
        self.assertTrue({"unsupported_inference", "provenance", "lineage_fingerprint", "constitutional_boundary"}.issubset(categories))
        self.assertEqual(summary["quality_report"]["validator_failures_by_category"]["unsupported_inference"], 1)

    def test_final_recommendation_moves_to_next_roadmap_family_without_architecture_change(self) -> None:
        campaign = load_campaign_module()
        with tempfile.TemporaryDirectory() as tmp:
            summary = campaign.run_campaign(Path(tmp) / "campaign33", repository_root=Path(tmp) / "knowledge_repository")
            final = (Path(tmp) / "campaign33" / "reports" / "campaign_33_final_report.md").read_text()
        self.assertEqual(summary["quality_report"]["recommendation_architectural_classification"], "preserves agreed architecture")
        self.assertIn("Architecture/taxonomy/validator/workflow pressure: false", final)
        self.assertIn("bounded PostgreSQL Knowledge Repository Realization Decision", summary["quality_report"]["final_recommendation"])


if __name__ == "__main__":
    unittest.main()
