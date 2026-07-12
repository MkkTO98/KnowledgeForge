from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_helper():
    spec = importlib.util.spec_from_file_location(
        "coefficient_free_pearson_candidate_registry",
        ROOT / "tools/coefficient_free_pearson_candidate_registry.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CoefficientFreePearsonCandidateRegistryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = load_helper()
        self.outputs = self.helper.build_outputs()

    def test_builds_six_to_eight_valid_candidates_from_retained_evidence(self):
        validation = self.outputs["validation"]
        self.assertTrue(validation["valid"], validation.get("errors"))
        self.assertEqual(validation["candidate_count"], 8)
        self.assertEqual(len(validation["expected_package_ids"]), 8)
        self.assertEqual(len(set(validation["expected_package_ids"])), 8)

    def test_registry_and_selection_evidence_are_coefficient_free(self):
        registry = self.outputs["registry"]
        spec = self.outputs["spec"]
        self.assertFalse(self.helper.has_forbidden_key(registry))
        self.assertFalse(self.helper.has_forbidden_key(spec["selection_evidence"]))
        for record in registry["records"]:
            self.assertFalse(self.helper.has_forbidden_key(record))
            self.assertFalse(record["contains_pearson_coefficient"])
        self.assertTrue(registry["coefficient_free_proof"]["no_campaign41_coefficient_calculated"])

    def test_excludes_prior_relationships_and_self_pairs(self):
        candidates = self.outputs["spec"]["candidates"]
        keys = set()
        for c in candidates:
            a = c["series_a"]["identity"]["code"]
            b = c["series_b"]["identity"]["code"]
            self.assertNotEqual(a, b)
            key = self.helper.canonical_pair_key(c["entity"], a, b)
            self.assertNotIn(key, self.helper.EXCLUDED_PRIOR_PAIRS)
            self.assertNotIn(key, keys)
            keys.add(key)

    def test_deterministic_regeneration_identity(self):
        first = self.helper.build_outputs()
        second = self.helper.build_outputs()
        self.assertEqual(first["registry"]["registry_fingerprint"], second["registry"]["registry_fingerprint"])
        self.assertEqual(first["spec"]["batch_spec_fingerprint"], second["spec"]["batch_spec_fingerprint"])
        self.assertEqual(first["spec"], second["spec"])

    def test_writes_registry_and_spec_without_result_fields(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "report"
            spec_path = Path(td) / "campaign41.json"
            outputs = self.helper.build_outputs(report_root=report, spec_path=spec_path)
            written = self.helper.write_outputs(outputs, report, spec_path)
            self.assertTrue(Path(written["registry_path"]).exists() or (ROOT / written["registry_path"]).exists())
            self.assertTrue(Path(written["spec_path"]).exists() or (ROOT / written["spec_path"]).exists())
            self.assertTrue(written["valid"])

    def test_detects_engine_hardcoding_status(self):
        assessment = self.helper.detect_campaign40_engine_hardcoding()
        self.assertFalse(assessment["campaign40_hardcoded_package_internals_found"])
        self.assertEqual(assessment["calculation_gate_decision"], "existing engine sufficient for calculation")

    def test_successor_policy_historical_comparison_is_valid_and_coefficient_free(self):
        comparison = self.helper.build_successor_policy_historical_comparison()
        self.assertTrue(comparison["validation"]["valid"], comparison["validation"].get("errors"))
        self.assertEqual(comparison["mode"], "historical_comparison")
        self.assertTrue(comparison["dry_run_only"])
        self.assertTrue(comparison["not_campaign42_registry"])
        self.assertFalse(comparison["valid_future_production_evidence"])
        self.assertGreaterEqual(comparison["selected_candidate_count"], 6)
        self.assertFalse(self.helper.has_forbidden_key(comparison))
        self.assertEqual(comparison["semantic_proximity_distribution"].get("remote", 0), 2)
        self.assertGreaterEqual(comparison["semantic_proximity_distribution"].get("close", 0), 3)
        proof = comparison["coefficient_free_proof"]
        self.assertFalse(proof["candidate_pair_pearson_used"])
        self.assertFalse(proof["candidate_pair_first_difference_used"])
        self.assertFalse(proof["covariance_used"])
        self.assertFalse(proof["preliminary_result_cache_used"])

    def test_successor_policy_future_production_excludes_current_canonical_pearson_pairs(self):
        future = self.helper.build_successor_policy_future_production_dry_run()
        self.assertEqual(future["mode"], "future_production")
        self.assertTrue(future["valid_future_production_evidence"])
        canonical_keys = self.helper.load_current_canonical_pearson_relationship_keys()
        selected_keys = {
            self.helper.canonical_pair_key(
                c["entity"],
                c["series_a"]["identity"]["code"],
                c["series_b"]["identity"]["code"],
            )
            for c in future["selected_candidates"]
        }
        self.assertTrue(canonical_keys)
        self.assertTrue(selected_keys.isdisjoint(canonical_keys), selected_keys & canonical_keys)

    def test_successor_policy_future_production_excludes_reversed_canonical_pairs(self):
        canonical_keys = self.helper.load_current_canonical_pearson_relationship_keys()
        for entity, a, b in canonical_keys:
            self.assertIn(self.helper.canonical_pair_key(entity, b, a), canonical_keys)

    def test_comparison_mode_cannot_be_mistaken_for_future_production_mode(self):
        comparison = self.helper.build_successor_policy_historical_comparison()
        future = self.helper.build_successor_policy_future_production_dry_run()
        self.assertEqual(comparison["mode"], "historical_comparison")
        self.assertFalse(comparison["valid_future_production_evidence"])
        self.assertIn("historical/audit ranking only", comparison["mode_boundary"])
        self.assertEqual(future["mode"], "future_production")
        self.assertTrue(future["valid_future_production_evidence"])

    def test_successor_policy_preserves_campaign41_fingerprints(self):
        outputs = self.helper.build_outputs()
        self.assertEqual(
            outputs["registry"]["registry_fingerprint"],
            "sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc",
        )
        self.assertEqual(
            outputs["spec"]["batch_spec_fingerprint"],
            "sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2",
        )

    def test_successor_policy_candidate_metadata_contract(self):
        dry_run = self.helper.build_successor_policy_dry_run()
        valid_semantic = {"close", "moderate", "remote", "unresolved"}
        valid_risk = {"low", "moderate", "high", "unknown"}
        valid_purpose = {
            "positive_descriptive_knowledge",
            "baseline_relationship_knowledge",
            "cautionary_relationship_knowledge",
            "transformation_companion_candidate",
            "methodological_pressure_test_candidate",
        }
        for candidate in dry_run["selected_candidates"]:
            meta = candidate["successor_policy_metadata"]
            self.assertIn(meta["semantic_proximity"]["classification"], valid_semantic)
            self.assertIn(meta["time_risk"]["category"], valid_risk)
            self.assertIn(meta["candidate_utility_statement"]["purpose_classification"], valid_purpose)
            self.assertEqual(meta["candidate_utility_statement"]["coefficient_prediction"], "none; result-independent statement")
            self.assertTrue(meta["time_risk"]["permitted_inputs_only"])

    def test_successor_policy_rejects_hidden_outcome_fields(self):
        dry_run = self.helper.build_successor_policy_dry_run()
        polluted = json.loads(json.dumps(dry_run))
        polluted["selected_candidates"][0]["selection_evidence"]["pearson_coefficient"] = "0.99"
        self.assertTrue(self.helper.has_forbidden_key(polluted))

    def test_remote_cap_count_never_exceeds_declared_share(self):
        expectations = {
            1: 0,
            2: 0,
            3: 0,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            8: 2,
            9: 2,
            10: 2,
            11: 2,
            12: 3,
        }
        for batch_size, expected in expectations.items():
            with self.subTest(batch_size=batch_size):
                self.assertEqual(self.helper.remote_cap_count(batch_size, "0.25"), expected)
                self.assertLessEqual(expected, batch_size * 0.25)

    def test_future_production_remote_share_does_not_exceed_declared_cap(self):
        future = self.helper.build_successor_policy_future_production_dry_run()
        remote = future["semantic_proximity_distribution"].get("remote", 0)
        selected = future["selected_candidate_count"]
        self.assertLessEqual(remote, self.helper.remote_cap_count(selected, "0.25"))
        self.assertLessEqual(future["remote_share"], 0.25)


if __name__ == "__main__":
    unittest.main()
