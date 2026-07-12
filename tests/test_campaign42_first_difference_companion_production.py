from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "campaign42_first_difference_companion_production.py"


def load_module():
    spec = importlib.util.spec_from_file_location("campaign42_production", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign42FirstDifferenceCompanionProductionTests(unittest.TestCase):
    def test_pre_execution_gate_freezes_authorized_inputs(self):
        mod = load_module()
        gate = mod.pre_execution_gate(ROOT)
        self.assertTrue(gate["valid"])
        # The live repository is 546 before Campaign 42 publication and 554 after
        # successful append-only publication; the gate remains valid in the
        # published state only for idempotent collision-safe reruns.
        self.assertIn(gate["repository_baseline"]["object_count"], {546, 554})
        self.assertEqual(gate["repository_baseline"]["raw_pearson_objects"], 21)
        self.assertEqual(gate["repository_baseline"]["statistical_summary_objects"], 4)
        self.assertIn(gate["repository_baseline"]["first_difference_pearson_companions"], {0, 8})
        self.assertEqual(gate["registry_fingerprint"], "sha256:be7a085b5a74860c9a6c95fb2c9e6f45a066679d317fc743694959d502e3dc15")
        self.assertEqual(gate["specification_fingerprint"], "sha256:ec3eaf0f735a888bc01f9cf394f015dd87eab3096be2690e75de0c4ec6f86d00")

    def test_transform_and_compute_eight_candidates(self):
        mod = load_module()
        result = mod.produce_campaign42(ROOT, publish=False)
        self.assertEqual(result["accepted_count"], 8)
        self.assertEqual(result["rejected_count"], 0)
        for candidate in result["candidate_results"]:
            self.assertEqual(candidate["status"], "accepted")
            self.assertGreaterEqual(candidate["aligned_transformed_count"], 30)
            self.assertGreaterEqual(float(candidate["transformed_coverage"]), 0.85)
            self.assertEqual(candidate["coefficient"], candidate["independent_recompute_coefficient"])
            self.assertTrue(candidate["prior_diagnostic_reconciliation"]["coefficient_matches"])
            self.assertTrue(candidate["prior_diagnostic_reconciliation"]["aligned_count_matches"])
            self.assertIn("first-difference-pearson-companion", candidate["package_id"])

    def test_generated_packages_are_valid_companions_without_raw_supersession(self):
        mod = load_module()
        result = mod.produce_campaign42(ROOT, publish=False)
        raw_ids = {c["raw_package_id"] for c in result["candidate_results"]}
        companion_ids = {c["package_id"] for c in result["candidate_results"]}
        self.assertEqual(len(companion_ids), 8)
        for package in result["accepted_packages"]:
            payload = package["generated_statements"][0]["structured_payload"]
            self.assertEqual(payload["method_id"], "wdi_annual_scalar_first_difference_pearson_v1")
            self.assertEqual(payload["transformation_state"], "first_difference")
            self.assertIn(payload["raw_package_reference"]["package_id"], raw_ids)
            self.assertIn("does_not_supersede_raw_package", payload)
            self.assertTrue(payload["does_not_supersede_raw_package"])
            self.assertIsNone(package["lineage"]["previous_package_id"])
            self.assertEqual(package["lineage"]["source_campaign"], "Campaign 42")
            self.assertIn("Campaign 42", package["provenance_envelope"]["lineage_basis"])

    def test_order_and_decimal_context_determinism(self):
        mod = load_module()
        first = mod.produce_campaign42(ROOT, publish=False)
        second = mod.produce_campaign42(ROOT, publish=False, reverse_candidates=True, weird_decimal_context=True)
        self.assertEqual(first["accepted_package_fingerprints_by_id"], second["accepted_package_fingerprints_by_id"])
        self.assertEqual(first["candidate_result_fingerprint"], second["candidate_result_fingerprint"])

    def test_publication_is_idempotent_and_preserves_existing_bytes_in_temp_copy(self):
        mod = load_module()
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp) / "repo"
            shutil.copytree(ROOT / "knowledge_repository", tmp_root / "knowledge_repository")
            shutil.copytree(ROOT / "artifacts" / "evidence-fixtures", tmp_root / "artifacts" / "evidence-fixtures")
            shutil.copytree(ROOT / "specs" / "correlation_batches", tmp_root / "specs" / "correlation_batches")
            shutil.copytree(ROOT / "artifacts" / "reports" / "campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712", tmp_root / "artifacts" / "reports" / "campaign42-coefficient-free-first-difference-pearson-companion-registry-20260712")
            result = mod.produce_campaign42(tmp_root, publish=True)
            self.assertEqual(result["repository_after"]["object_count"], 554)
            self.assertTrue(result["pre_existing_package_immutability"]["valid"])
            second = mod.produce_campaign42(tmp_root, publish=True)
            self.assertTrue(second["idempotent_republish"]["collision_safe"])
            self.assertEqual(second["repository_after"]["object_count"], 554)


if __name__ == "__main__":
    unittest.main()
