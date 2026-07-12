from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "campaign43_first_difference_companion_calculation.py"


def load_module():
    spec = importlib.util.spec_from_file_location("campaign43_calculation", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign43FirstDifferenceCompanionCalculationTests(unittest.TestCase):
    def test_pre_execution_gate_verifies_frozen_identities_and_canonical_baseline(self):
        mod = load_module()
        gate = mod.pre_execution_gate(ROOT)
        self.assertTrue(gate["valid"])
        self.assertEqual(gate["registry_fingerprint"], mod.EXPECTED_REGISTRY_FP)
        self.assertEqual(gate["specification_fingerprint"], mod.EXPECTED_SPEC_FP)
        self.assertEqual(gate["repository_baseline"]["object_file_count"], mod.POST_PUBLICATION_REPOSITORY_COUNT)
        self.assertEqual(gate["repository_baseline"]["computed_repository_fingerprint"], mod.POST_PUBLICATION_REPOSITORY_FP)
        self.assertEqual(gate["repository_baseline"]["first_difference_pearson_companions"], 14)

    def test_recalculates_six_frozen_candidates_after_publication_without_mutation(self):
        mod = load_module()
        result = mod.calculate_campaign43(ROOT)
        self.assertEqual(result["execution_status"], "calculated_not_published")
        self.assertEqual(result["candidate_count"], 6)
        self.assertEqual(result["accepted_calculation_count"], 6)
        self.assertEqual(result["rejected_calculation_count"], 0)
        self.assertFalse(result["canonical_publication_performed"])
        self.assertFalse(result["postgresql_projection_performed"])
        self.assertFalse(result["knowledge_object_packages_constructed"])
        self.assertTrue(result["pre_existing_package_immutability"]["valid"])
        self.assertEqual(result["pre_existing_package_immutability"]["changed_object_files"], [])
        self.assertEqual(result["repository_after"]["object_file_count"], mod.POST_PUBLICATION_REPOSITORY_COUNT)
        self.assertEqual(result["repository_after"]["computed_repository_fingerprint"], mod.POST_PUBLICATION_REPOSITORY_FP)
        for candidate in result["candidate_results"]:
            self.assertEqual(candidate["status"], "calculated_not_published")
            self.assertGreaterEqual(candidate["aligned_transformed_observation_count"], 30)
            self.assertEqual(candidate["coefficient"], candidate["independent_recompute_coefficient"])
            rec = candidate["prior_embedded_diagnostic_reconciliation"]
            self.assertTrue(rec["coefficient_matches_prior_diagnostic_at_recorded_precision"])
            self.assertTrue(rec["aligned_count_matches_registry"])

    def test_deterministic_under_weird_decimal_context(self):
        mod = load_module()
        normal = mod.calculate_campaign43(ROOT)
        weird = mod.calculate_campaign43(ROOT, weird_decimal_context=True)
        self.assertEqual(normal["candidate_result_fingerprint"], weird["candidate_result_fingerprint"])
        self.assertEqual(
            [c["coefficient"] for c in normal["candidate_results"]],
            [c["coefficient"] for c in weird["candidate_results"]],
        )

    def test_expected_companion_ids_are_now_canonical_packages(self):
        mod = load_module()
        result = mod.calculate_campaign43(ROOT)
        for package_id in result["expected_companion_package_ids"]:
            path = ROOT / "knowledge_repository" / "objects" / f"{package_id}.json"
            self.assertTrue(path.exists(), package_id)
            package = json.loads(path.read_text())
            self.assertEqual(package["fingerprints"]["package_manifest"], mod.EXPECTED_COMPANION_MANIFEST_FINGERPRINTS[package_id])

    def test_artifact_results_match_helper_output(self):
        mod = load_module()
        artifact_path = ROOT / "artifacts" / "reports" / "campaign43-first-difference-companion-calculation-20260712" / "calculation_results.json"
        if not artifact_path.exists():
            self.skipTest("calculation artifact has not been written yet")
        artifact = json.loads(artifact_path.read_text())
        direct = mod.calculate_campaign43(ROOT)
        self.assertEqual(artifact["candidate_result_fingerprint"], direct["candidate_result_fingerprint"])
        self.assertIn(artifact["repository_after"]["computed_repository_fingerprint"], [mod.EXPECTED_REPOSITORY_FP, mod.POST_PUBLICATION_REPOSITORY_FP])


if __name__ == "__main__":
    unittest.main()
