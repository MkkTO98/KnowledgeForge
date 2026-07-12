from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "campaign42_first_difference_companion_registry.py"


def load_module():
    spec = importlib.util.spec_from_file_location("campaign42_registry", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign42CompanionRegistryTests(unittest.TestCase):
    def test_enumerates_all_21_raw_pearson_packages_from_canonical_repository(self):
        m = load_module()
        inventory = m.enumerate_raw_pearson_packages(ROOT)
        self.assertEqual(len(inventory), 21)
        self.assertEqual(len({p["raw_package_id"] for p in inventory}), 21)
        self.assertTrue(all(p["raw_package_fingerprint"].startswith("sha256:") for p in inventory))

    def test_builds_coefficient_free_six_to_eight_candidate_registry(self):
        m = load_module()
        result = m.build_campaign42_registry(ROOT)
        registry = result["registry"]
        entries = registry["candidates"]
        self.assertLessEqual(len(entries), 8)
        if entries and not any((ROOT / "knowledge_repository/objects" / f"{e['expected_companion_package_id']}.json").exists() for e in entries):
            self.assertGreaterEqual(len(entries), 2)
        self.assertTrue(registry["coefficient_free"])
        serialized = json.dumps(registry, sort_keys=True).lower()
        forbidden = ["pearson_coefficient", "diagnostic_value", "p_value", "covariance", "significance", "forecast"]
        for term in forbidden:
            self.assertNotIn(term, serialized)
        self.assertLessEqual(sum(1 for e in entries if e["semantic_proximity"] == "remote"), 2)
        self.assertEqual(len({e["raw_companion_package_id"] for e in entries}), len(entries))
        self.assertEqual(len({e["expected_companion_package_id"] for e in entries}), len(entries))
        self.assertTrue(all("first-difference-pearson-companion-v1" in e["expected_companion_package_id"] for e in entries))

    def test_evidence_overlap_unit_and_existing_companion_validation(self):
        m = load_module()
        result = m.build_campaign42_registry(ROOT)
        for entry in result["registry"]["candidates"]:
            self.assertGreaterEqual(entry["expected_minimum_overlap"]["expected_aligned_transformed_observations"], 30)
            self.assertGreaterEqual(float(entry["expected_minimum_coverage"]["expected_transformed_coverage"]), 0.85)
            self.assertEqual(entry["transformation"]["id"], "wdi_annual_scalar_first_difference_v1")
            self.assertEqual(entry["method"]["id"], "wdi_annual_scalar_first_difference_pearson_v1")
            self.assertFalse(entry["existing_canonical_first_difference_companion_found"])
            for transformed_unit in entry["transformed_unit_semantics"].values():
                self.assertNotIn("growth", transformed_unit.lower())
                self.assertNotIn("percent change", transformed_unit.lower())

    def test_changing_stored_diagnostic_coefficients_does_not_change_selection(self):
        m = load_module()
        baseline = m.build_campaign42_registry(ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp) / "repo"
            shutil.copytree(ROOT / "knowledge_repository", tmp_root / "knowledge_repository")
            shutil.copytree(ROOT / "artifacts" / "evidence-fixtures", tmp_root / "artifacts" / "evidence-fixtures")
            for p in (tmp_root / "knowledge_repository" / "objects").glob("*.json"):
                data = json.loads(p.read_text())
                payload = data.get("generated_statements", [{}])[0].get("structured_payload", {})
                diag = payload.get("diagnostic_limitations")
                if isinstance(diag, dict) and "first_difference_pearson" in diag:
                    diag["first_difference_pearson"] = "0.999999999999"
                    p.write_text(json.dumps(data, indent=2, sort_keys=True))
            mutated = m.build_campaign42_registry(tmp_root)
        self.assertEqual(
            [e["raw_companion_package_id"] for e in baseline["registry"]["candidates"]],
            [e["raw_companion_package_id"] for e in mutated["registry"]["candidates"]],
        )
        self.assertEqual(baseline["registry_fingerprint"], mutated["registry_fingerprint"])

    def test_deterministic_regeneration_preserves_registry_and_spec_fingerprints(self):
        m = load_module()
        a = m.build_campaign42_registry(ROOT)
        b = m.build_campaign42_registry(ROOT)
        self.assertEqual(a["registry_fingerprint"], b["registry_fingerprint"])
        self.assertEqual(a["specification_fingerprint"], b["specification_fingerprint"])


if __name__ == "__main__":
    unittest.main()
