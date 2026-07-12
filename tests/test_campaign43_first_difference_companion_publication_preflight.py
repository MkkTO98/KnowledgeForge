from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "campaign43_first_difference_companion_publication_preflight.py"
CALC_MODULE_PATH = ROOT / "tools" / "campaign43_first_difference_companion_calculation.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign43CompanionPublicationPreflightTests(unittest.TestCase):
    def test_preflight_freezes_registry_calculation_and_canonical_baseline(self):
        mod = load_module(MODULE_PATH, "campaign43_publication_preflight")
        gate = mod.preflight(ROOT)
        self.assertTrue(gate["valid"])
        self.assertEqual(gate["registry_fingerprint"], mod.EXPECTED_REGISTRY_FP)
        self.assertEqual(gate["specification_fingerprint"], mod.EXPECTED_SPEC_FP)
        self.assertEqual(gate["calculation_result_fingerprint"], mod.EXPECTED_CALC_FP)
        self.assertEqual(gate["canonical_baseline"]["object_file_count"], mod.EXPECTED_POST_PUBLICATION_COUNT)
        self.assertEqual(gate["canonical_baseline"]["computed_repository_fingerprint"], mod.EXPECTED_POST_PUBLICATION_FP)
        self.assertEqual(gate["canonical_baseline"]["first_difference_pearson_relationship_count"], mod.EXPECTED_POST_PUBLICATION_FD_COUNT)

    def test_constructs_exactly_six_valid_one_to_one_packages_without_publication(self):
        mod = load_module(MODULE_PATH, "campaign43_publication_preflight")
        result = mod.run(ROOT)
        self.assertEqual(result["status"], "constructed_not_published")
        self.assertEqual(result["candidate_package_count"], 6)
        self.assertFalse(result["canonical_publication_performed"])
        self.assertFalse(result["canonical_manifest_or_index_mutation_performed"])
        self.assertFalse(result["postgresql_projection_performed"])
        self.assertFalse(result["relationship_export_publication_performed"])
        self.assertEqual(len(result["package_fingerprints_by_id"]), 6)
        self.assertEqual(len(set(result["package_fingerprints_by_id"])), 6)
        self.assertTrue(all(v["valid"] for v in result["package_validation"]))
        expected_ids = set(json.loads((ROOT / "artifacts/reports/campaign43-first-difference-companion-calculation-20260712/calculation_results.json").read_text())["expected_companion_package_ids"])
        self.assertEqual(set(result["package_fingerprints_by_id"]), expected_ids)

    def test_packages_preserve_coefficients_counts_and_interpretation_boundaries(self):
        mod = load_module(MODULE_PATH, "campaign43_publication_preflight")
        constructed = mod.construct_packages(ROOT)
        calc = json.loads((ROOT / mod.CALC_REL).read_text())
        calc_by_pid = {c["expected_companion_package_id"]: c for c in calc["candidate_results"]}
        for package in constructed["packages"]:
            payload = package["generated_statements"][0]["structured_payload"]
            evidence = calc_by_pid[package["package_id"]]
            self.assertEqual(payload["pearson_coefficient"], evidence["coefficient"])
            self.assertEqual(payload["first_difference_pearson_coefficient"], evidence["coefficient"])
            self.assertEqual(payload["aligned_transformed_count"], evidence["aligned_transformed_observation_count"])
            self.assertEqual(payload["independent_recompute_coefficient"], evidence["independent_recompute_coefficient"])
            self.assertEqual(payload["method_id"], mod.METHOD_ID)
            self.assertEqual(payload["transformation_id"], mod.TRANSFORMATION_ID)
            self.assertEqual(payload["transformation_state"], "first_difference")
            self.assertEqual(payload["raw_transformation_state"], "raw")
            self.assertTrue(payload["does_not_supersede_raw_package"])
            self.assertTrue(payload["raw_package_not_superseded"])
            self.assertTrue(payload["interpretation_boundary"]["near_zero_absence_claim_prohibited"])
            self.assertTrue(payload["interpretation_boundary"]["causal_interpretation_prohibited"])
            self.assertIn("First differencing discards one observation", " ".join(payload["limitations"]))
            text = json.dumps(package, sort_keys=True).lower()
            self.assertNotIn("proves absence", text)
            self.assertNotIn("proves no relationship", text)
            self.assertNotIn("investment signal is implied", text)

    def test_deterministic_ids_fingerprints_and_safe_dry_run(self):
        mod = load_module(MODULE_PATH, "campaign43_publication_preflight")
        first = mod.run(ROOT)
        second = mod.run(ROOT)
        self.assertEqual(first["package_fingerprints_by_id"], second["package_fingerprints_by_id"])
        self.assertEqual(first["package_set_fingerprint"], second["package_set_fingerprint"])
        dry = first["publication_preflight"]
        self.assertTrue(dry["safe_dry_run_performed_in_temporary_repository_copy"])
        self.assertFalse(dry["canonical_repository_mutated"])
        self.assertEqual(dry["collisions_with_existing_canonical_packages"], [])
        self.assertEqual(dry["expected_post_publication_package_count"], 560)
        self.assertEqual(dry["expected_post_publication_first_difference_relationship_count"], 14)
        self.assertEqual(dry["expected_post_publication_raw_pearson_relationship_count"], 21)
        self.assertEqual(dry["expected_postgresql_projected_package_count"], 560)
        self.assertTrue(dry["pre_existing_package_immutability_after_dry_run"]["valid"])

    def test_no_campaign42_duplication_and_raw_sources_remain_canonical(self):
        mod = load_module(MODULE_PATH, "campaign43_publication_preflight")
        constructed = mod.construct_packages(ROOT)
        raw_refs = set()
        for package in constructed["packages"]:
            self.assertNotIn("campaign42", package["package_id"])
            payload = package["generated_statements"][0]["structured_payload"]
            raw_id = payload["raw_package_reference"]["package_id"]
            raw_refs.add(raw_id)
            raw_path = ROOT / "knowledge_repository" / "objects" / f"{raw_id}.json"
            self.assertTrue(raw_path.exists())
            raw = json.loads(raw_path.read_text())
            self.assertEqual(raw["confidence_quality"]["lifecycle_state"], "accepted")
            self.assertIsNone(raw.get("lineage", {}).get("previous_package_id"))
        self.assertEqual(len(raw_refs), 6)

    def test_construction_does_not_mutate_canonical_repository(self):
        mod = load_module(MODULE_PATH, "campaign43_publication_preflight")
        before = mod.repository_baseline(ROOT)
        before_hashes = mod.object_hashes(ROOT)
        mod.run(ROOT)
        after = mod.repository_baseline(ROOT)
        after_hashes = mod.object_hashes(ROOT)
        self.assertEqual(before, after)
        self.assertEqual(before_hashes, after_hashes)

    def test_independent_recomputation_artifact_agrees_at_recorded_precision(self):
        # Package construction consumes the accepted calculation artifact; this test
        # verifies that the accepted artifact remains independently reproducible.
        calc_mod = load_module(CALC_MODULE_PATH, "campaign43_calculation")
        direct = calc_mod.calculate_campaign43(ROOT)
        artifact = json.loads((ROOT / "artifacts/reports/campaign43-first-difference-companion-calculation-20260712/calculation_results.json").read_text())
        self.assertEqual(direct["candidate_result_fingerprint"], artifact["candidate_result_fingerprint"])
        for direct_candidate, artifact_candidate in zip(direct["candidate_results"], artifact["candidate_results"]):
            self.assertEqual(direct_candidate["coefficient"], artifact_candidate["coefficient"])
            self.assertEqual(direct_candidate["independent_recompute_coefficient"], artifact_candidate["independent_recompute_coefficient"])


if __name__ == "__main__":
    unittest.main()
