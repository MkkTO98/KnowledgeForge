from __future__ import annotations

import importlib.util
import json
import unittest
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_UP, getcontext
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "deterministic_statistical_summary_v2.py"
FIXTURE_PATH = PROJECT_ROOT / "artifacts" / "evidence-fixtures" / "wdi-demographic-population-total-denmark-1990-2024-https-corrected" / "normalized_observations.json"


def load_module():
    spec = importlib.util.spec_from_file_location("summary_v2", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def normalized_from_values(values, *, indicator="TEST.RATE", entity="AAA", start=2000, unit="percent"):
    observations = []
    for idx, value in enumerate(values):
        period = start + idx
        observed = value is not None
        observations.append(
            {
                "entity_id": entity,
                "indicator_code": indicator,
                "period": period,
                "observed": observed,
                "value_canonical": None if value is None else str(value),
                "unit": unit,
            }
        )
    return {
        "normalized_fingerprint": "sha256:test-fixture",
        "expected_observation_slots": len(values),
        "selection_contract": {
            "indicator": {"code": indicator, "name": "Test indicator"},
            "entities": [entity],
            "periods": {"start_year": start, "end_year": start + len(values) - 1},
        },
        "provider_metadata": {"wdi_lastupdated": "test"},
        "raw_artifacts": {"combined_raw_artifact_fingerprint": "sha256:raw"},
        "observations": observations,
    }


class StatisticalSummaryV2ContractTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.original_prec = getcontext().prec
        self.original_rounding = getcontext().rounding

    def tearDown(self):
        getcontext().prec = self.original_prec
        getcontext().rounding = self.original_rounding

    def test_contract_serializes_pinned_precision_rounding_and_format_policy(self):
        contract = self.module.calculation_contract_v2()
        self.assertEqual(contract["method_id"], "wdi_annual_scalar_statistical_summary_v2")
        self.assertEqual(contract["method_version"], "2.0")
        self.assertEqual(contract["internal_decimal_precision"], 50)
        self.assertEqual(contract["internal_rounding_mode"], "ROUND_HALF_EVEN")
        self.assertEqual(contract["canonical_stored_decimal_places"], 12)
        self.assertEqual(contract["canonical_rounding_policy"], "ROUND_HALF_EVEN")
        self.assertEqual(contract["human_display_decimal_places"], 4)
        self.assertEqual(contract["trailing_zero_normalization"], "strip_fractional_trailing_zeros")
        self.assertEqual(contract["negative_zero_handling"], "canonicalize_to_zero")
        self.assertEqual(contract["scientific_notation_policy"], "forbidden_in_canonical_values")
        self.assertEqual(contract["minimum_observed_count"], 30)
        self.assertEqual(contract["minimum_coverage_share"], "0.85")
        self.assertTrue(contract["calculation_contract_fingerprint"].startswith("sha256:"))

    def test_results_and_fingerprints_are_identical_under_adversarial_decimal_contexts(self):
        normalized = normalized_from_values(["1", "2", "4", "8", "16"], unit="percent")
        contexts = [
            (10, ROUND_DOWN),
            (28, ROUND_HALF_EVEN),
            (50, ROUND_UP),
            (17, ROUND_CEILING),
        ]
        results = []
        for precision, rounding in contexts:
            getcontext().prec = precision
            getcontext().rounding = rounding
            result = self.module.build_candidate_payload_v2(normalized, package_id="pkg-test", minimum_observed_count=3)
            results.append(
                {
                    "measures": result["structured_payload"],
                    "contract_fingerprint": result["calculation_contract"]["calculation_contract_fingerprint"],
                    "candidate_fingerprint": result["candidate_payload_fingerprint"],
                    "package_fingerprint": result["package_manifest_fingerprint"],
                }
            )
        self.assertEqual(1, len({json.dumps(r, sort_keys=True) for r in results}))
        self.assertEqual("6.2", results[0]["measures"]["arithmetic_mean"]["canonical"])
        self.assertEqual("5.455272678794", results[0]["measures"]["population_standard_deviation"]["canonical"])

    def test_reversed_input_order_does_not_change_results_or_fingerprints(self):
        normal = normalized_from_values(["1.1", "2.2", "3.3", "4.4"])
        reversed_rows = json.loads(json.dumps(normal))
        reversed_rows["observations"] = list(reversed(reversed_rows["observations"]))
        first = self.module.build_candidate_payload_v2(normal, package_id="pkg-test", minimum_observed_count=3)
        second = self.module.build_candidate_payload_v2(reversed_rows, package_id="pkg-test", minimum_observed_count=3)
        self.assertEqual(first["structured_payload"], second["structured_payload"])
        self.assertEqual(first["candidate_payload_fingerprint"], second["candidate_payload_fingerprint"])

    def test_rejects_duplicate_observations_and_ambiguous_numeric_strings(self):
        duplicate = normalized_from_values(["1", "2", "3"])
        duplicate["observations"].append(dict(duplicate["observations"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate observation key"):
            self.module.compute_statistical_summary_v2(duplicate)

        ambiguous = normalized_from_values(["1", "1e3", "3"])
        with self.assertRaisesRegex(ValueError, "non-canonical numeric string"):
            self.module.compute_statistical_summary_v2(ambiguous, minimum_observed_count=3)

    def test_missing_zero_negative_large_fractional_even_odd_and_negative_zero_cases(self):
        with_missing = normalized_from_values(["0", "-0.00", "-2.5", "1000000000000000000000.25", None, "3.125", "4.375"])
        result = self.module.compute_statistical_summary_v2(with_missing, minimum_observed_count=3, minimum_coverage_share="0.85")
        self.assertEqual(result["expected_observation_slot_count"], 7)
        self.assertEqual(result["observed_count"], 6)
        self.assertEqual(result["missing_count"], 1)
        self.assertEqual(result["missing_share"]["canonical"], "0.142857142857")
        self.assertEqual(result["minimum"]["canonical"], "-2.5")
        self.assertEqual(result["maximum"]["canonical"], "1000000000000000000000.25")
        self.assertEqual(result["first_valid_observation"]["value"], "0")
        self.assertEqual(result["median"]["canonical"], "1.5625")

        odd = self.module.compute_statistical_summary_v2(normalized_from_values(["1", "2", "4"]), minimum_observed_count=3)
        even = self.module.compute_statistical_summary_v2(normalized_from_values(["1", "2", "4", "8"]), minimum_observed_count=3)
        self.assertEqual(odd["median"]["canonical"], "2")
        self.assertEqual(even["median"]["canonical"], "3")

    def test_rejects_invalid_missing_and_low_coverage(self):
        invalid_missing = normalized_from_values(["1", None, "3"])
        invalid_missing["observations"][1]["value_canonical"] = "2"
        with self.assertRaisesRegex(ValueError, "missing row must not carry value"):
            self.module.compute_statistical_summary_v2(invalid_missing, minimum_observed_count=2, minimum_coverage_share="0.5")

        low_coverage = normalized_from_values(["1", None, None, None])
        with self.assertRaisesRegex(ValueError, "observed count below minimum"):
            self.module.compute_statistical_summary_v2(low_coverage)

    def test_campaign34_v2_comparison_is_non_promoted_and_stable(self):
        normalized = json.loads(FIXTURE_PATH.read_text())
        comparison = self.module.build_campaign34_v2_comparison(normalized)
        self.assertEqual(comparison["promotion_status"], "non_promoted_comparison_only")
        self.assertEqual(comparison["method_id"], "wdi_annual_scalar_statistical_summary_v2")
        self.assertNotEqual(comparison["method_id"], "wdi_denmark_population_statistical_summary_v1")
        self.assertEqual(comparison["measures"]["observed_count"], 35)
        self.assertEqual(comparison["measures"]["coverage_share"]["canonical"], "1")
        self.assertEqual(comparison["measures"]["arithmetic_mean"]["canonical"], "5506886.828571428571")


if __name__ == "__main__":
    unittest.main()
