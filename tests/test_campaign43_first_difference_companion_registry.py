from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "campaign43_first_difference_companion_registry.py"
REGISTRY_PATH = ROOT / "specs" / "correlation_batches" / "campaign43_coefficient_free_first_difference_companion_registry.json"
EXPECTED_COUNT = 562
EXPECTED_REPOSITORY_FINGERPRINT = "sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff"
AUTHORIZED_RAW_IDS = [
    "pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1",
    "pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1",
    "pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1",
    "pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1",
    "pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1",
    "pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1",
]


def load_module():
    spec = importlib.util.spec_from_file_location("campaign43_registry", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign43CompanionRegistryTests(unittest.TestCase):
    def test_candidate_boundary_is_exactly_the_six_authorized_relationships(self):
        m = load_module()
        result = m.build_campaign43_registry(ROOT)
        entries = result["registry"]["entries"]
        self.assertEqual(len(entries), 6)
        self.assertEqual([e["source_raw_package"]["package_id"] for e in entries], AUTHORIZED_RAW_IDS)
        self.assertEqual([e["campaign43_candidate_id"] for e in entries], sorted(e["campaign43_candidate_id"] for e in entries))
        self.assertEqual(len({e["campaign43_candidate_id"] for e in entries}), 6)

    def test_every_entry_resolves_to_existing_campaign41_raw_package_with_matching_fingerprint(self):
        m = load_module()
        result = m.build_campaign43_registry(ROOT)
        for entry in result["registry"]["entries"]:
            package_id = entry["source_raw_package"]["package_id"]
            path = ROOT / "knowledge_repository" / "objects" / f"{package_id}.json"
            self.assertTrue(path.exists(), package_id)
            package = json.loads(path.read_text())
            self.assertEqual(package["lineage"]["source_campaign"], "Campaign 41")
            self.assertEqual(package["fingerprints"]["package_manifest"], entry["source_raw_package"]["package_manifest_fingerprint"])
            statement = package["generated_statements"][0]
            self.assertEqual(statement["applicability"]["method_id"], "wdi_annual_scalar_pearson_correlation_v1")
            self.assertEqual(statement["applicability"]["method_version"], "1.0")
            self.assertEqual(statement["applicability"]["frequency"], "annual")

    def test_no_source_relationship_is_superseded_and_no_equivalent_companion_exists(self):
        m = load_module()
        result = m.build_campaign43_registry(ROOT)
        for entry in result["registry"]["entries"]:
            self.assertEqual(entry["source_raw_package"]["lifecycle_state"], "accepted")
            self.assertIsNone(entry["source_raw_package"]["superseded_by"])
            expected_id = entry["future_first_difference_compatibility"]["expected_companion_package_id"]
            companion_path = ROOT / "knowledge_repository" / "objects" / f"{expected_id}.json"
            self.assertTrue(companion_path.exists(), expected_id)

    def test_included_entries_reference_accepted_method_and_transformation_contracts(self):
        m = load_module()
        registry = json.loads(REGISTRY_PATH.read_text())
        for entry in registry["entries"]:
            self.assertEqual(entry["eligibility_status"], "included")
            compat = entry["future_first_difference_compatibility"]
            self.assertEqual(compat["transformation"]["id"], "wdi_annual_scalar_first_difference_v1")
            self.assertEqual(compat["transformation"]["contract_fingerprint"], "sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f")
            self.assertEqual(compat["method"]["id"], "wdi_annual_scalar_first_difference_pearson_v1")
            self.assertEqual(compat["method"]["contract_fingerprint"], "sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade")
            self.assertGreaterEqual(compat["resolvable_aligned_period_count_for_future_differencing"], 30)
            self.assertTrue(entry["inclusion_or_exclusion_rationale"])
            self.assertIn("high_shared_time_trend_risk", entry["trend_risk"]["classification"])
            self.assertTrue(entry["trend_risk"]["evidence"])

    def test_registry_is_coefficient_free(self):
        m = load_module()
        result = m.build_campaign43_registry(ROOT)
        serialized = json.dumps(result["registry"], sort_keys=True).lower()
        forbidden = [
            "pearson_coefficient",
            "first_difference_pearson\"",
            "series_a_vs_time_index",
            "series_b_vs_time_index",
            "diagnostic_value",
            "p_value",
            "p-value",
            "covariance",
            "sample_mean",
            "sample_variance",
        ]
        for term in forbidden:
            self.assertNotIn(term, serialized)
        self.assertTrue(result["registry"]["coefficient_free"])
        self.assertFalse(result["registry"]["calculation_authorized"])
        self.assertFalse(result["registry"]["canonical_publication_authorized"])

    def test_generation_validation_and_fingerprints_are_deterministic_and_idempotent(self):
        m = load_module()
        first = m.build_campaign43_registry(ROOT)
        second = m.build_campaign43_registry(ROOT)
        self.assertEqual(first["registry"], second["registry"])
        self.assertEqual(first["registry_fingerprint"], second["registry_fingerprint"])
        self.assertEqual(first["specification_fingerprint"], second["specification_fingerprint"])
        self.assertEqual(m.validate_registry(ROOT, first["registry"])["valid"], True)
        stored = json.loads(REGISTRY_PATH.read_text())
        self.assertEqual(m.fingerprint(stored), "sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1")

    def test_changing_raw_coefficient_values_does_not_change_selection_or_registry_fingerprint(self):
        m = load_module()
        baseline = m.build_campaign43_registry(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp) / "repo"
            shutil.copytree(ROOT / "knowledge_repository", tmp_root / "knowledge_repository")
            shutil.copytree(ROOT / "artifacts" / "evidence-fixtures", tmp_root / "artifacts" / "evidence-fixtures")
            for package_id in AUTHORIZED_RAW_IDS:
                path = tmp_root / "knowledge_repository" / "objects" / f"{package_id}.json"
                data = json.loads(path.read_text())
                payload = data["generated_statements"][0]["structured_payload"]
                payload["pearson_coefficient"]["canonical"] = "0.000000000000"
                payload.get("diagnostic_limitations", {})["first_difference_pearson"] = "0.000000000000"
                payload.get("diagnostic_limitations", {})["series_a_vs_time_index"] = "0.000000000000"
                payload.get("diagnostic_limitations", {})["series_b_vs_time_index"] = "0.000000000000"
                path.write_text(json.dumps(data, indent=2, sort_keys=True))
            mutated = m.build_campaign43_registry(tmp_root)
        self.assertEqual([e["source_raw_package"]["package_id"] for e in baseline["registry"]["entries"]], [e["source_raw_package"]["package_id"] for e in mutated["registry"]["entries"]])
        self.assertEqual(baseline["registry_fingerprint"], mutated["registry_fingerprint"])

    def test_canonical_package_count_and_repository_fingerprint_remain_unchanged(self):
        objects = sorted((ROOT / "knowledge_repository" / "objects").glob("*.json"))
        manifest = json.loads((ROOT / "knowledge_repository" / "manifest.json").read_text())
        self.assertEqual(len(objects), EXPECTED_COUNT)
        self.assertEqual(manifest["object_count"], EXPECTED_COUNT)
        self.assertEqual(manifest["repository_fingerprint"], EXPECTED_REPOSITORY_FINGERPRINT)


if __name__ == "__main__":
    unittest.main()
