from __future__ import annotations

import importlib.util
import unittest
from decimal import ROUND_CEILING, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_UP, getcontext
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "deterministic_pearson_correlation_v1.py"


def load_module():
    spec = importlib.util.spec_from_file_location("deterministic_pearson_correlation_v1", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def series(code, entity, values, *, unit="percent of GDP", transformation="raw", frequency="annual"):
    return {
        "series_id": {"indicator_code": code, "entity_id": entity, "frequency": frequency, "unit": unit, "transformation": transformation},
        "observations": [{"period": 2000 + i, "value_canonical": None if v is None else str(v), "observed": v is not None} for i, v in enumerate(values)],
    }


class PearsonCorrelationV1Test(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def test_contract_identity_and_fingerprint_are_stable(self):
        contract = self.module.calculation_contract_v1()
        self.assertEqual(contract["method_id"], "wdi_annual_scalar_pearson_correlation_v1")
        self.assertEqual(contract["method_version"], "1.0")
        self.assertTrue(contract["calculation_contract_fingerprint"].startswith("sha256:"))

    def test_perfect_positive_and_negative_and_zeroish(self):
        pos = self.module.compute_correlation(series("A", "DNK", [1, 2, 3, 4]), series("B", "DNK", [2, 4, 6, 8]), minimum_aligned_pairs=3)
        neg = self.module.compute_correlation(series("A", "DNK", [1, 2, 3, 4]), series("B", "DNK", [8, 6, 4, 2]), minimum_aligned_pairs=3)
        zeroish = self.module.compute_correlation(series("A", "DNK", [-1, 0, 1, 0]), series("B", "DNK", [0, 1, 0, -1]), minimum_aligned_pairs=3)
        self.assertEqual(pos["coefficient"]["canonical"], "1")
        self.assertEqual(neg["coefficient"]["canonical"], "-1")
        self.assertEqual(zeroish["coefficient"]["canonical"], "0")

    def test_fail_closed_invalid_alignment_and_variance_cases(self):
        with self.assertRaisesRegex(ValueError, "constant series"):
            self.module.compute_correlation(series("A", "DNK", [1, 1, 1]), series("B", "DNK", [1, 2, 3]), minimum_aligned_pairs=3)
        with self.assertRaisesRegex(ValueError, "insufficient aligned pairs"):
            self.module.compute_correlation(series("A", "DNK", [1]), series("B", "DNK", [1]), minimum_aligned_pairs=3)
        with self.assertRaisesRegex(ValueError, "no overlapping periods"):
            self.module.compute_correlation(series("A", "DNK", [1, 2]), {"series_id": {"indicator_code": "B", "entity_id": "DNK", "frequency": "annual", "unit": "percent", "transformation": "raw"}, "observations": [{"period": 2010, "value_canonical": "1", "observed": True}]}, minimum_aligned_pairs=1)
        bad = series("A", "DNK", [1, 2, 3]); bad["observations"].append({"period": 2000, "value_canonical": "9", "observed": True})
        with self.assertRaisesRegex(ValueError, "duplicate observation key"):
            self.module.compute_correlation(bad, series("B", "DNK", [1, 2, 3]), minimum_aligned_pairs=2)

    def test_mismatched_scope_and_transformations_fail_closed(self):
        with self.assertRaisesRegex(ValueError, "mismatched entities"):
            self.module.compute_correlation(series("A", "DNK", [1, 2, 3]), series("B", "SWE", [1, 2, 3]), same_entity_required=True, minimum_aligned_pairs=3)
        with self.assertRaisesRegex(ValueError, "mismatched frequencies"):
            self.module.compute_correlation(series("A", "DNK", [1, 2, 3]), series("B", "DNK", [1, 2, 3], frequency="monthly"), minimum_aligned_pairs=3)
        with self.assertRaisesRegex(ValueError, "mismatched transformations"):
            self.module.compute_correlation(series("A", "DNK", [1, 2, 3], transformation="raw"), series("B", "DNK", [1, 2, 3], transformation="first_difference"), minimum_aligned_pairs=3)

    def test_order_and_series_designation_do_not_change_canonical_pair_or_coefficient(self):
        a = series("Z", "DNK", [1, None, 3, 5, 7])
        b = series("A", "DNK", [2, 4, 6, None, 10])
        b["observations"] = list(reversed(b["observations"]))
        first = self.module.compute_correlation(a, b, minimum_aligned_pairs=2, coverage_threshold=__import__('decimal').Decimal('0'))
        second = self.module.compute_correlation(b, a, minimum_aligned_pairs=2, coverage_threshold=__import__('decimal').Decimal('0'))
        self.assertEqual(first["coefficient"], second["coefficient"])
        self.assertEqual(first["canonical_pair_id"], second["canonical_pair_id"])

    def test_decimal_context_cannot_alter_output(self):
        outputs = []
        original = (getcontext().prec, getcontext().rounding)
        for prec, rounding in [(10, ROUND_DOWN), (28, ROUND_HALF_EVEN), (50, ROUND_UP), (17, ROUND_CEILING)]:
            getcontext().prec = prec; getcontext().rounding = rounding
            outputs.append(self.module.compute_correlation(series("A", "DNK", ["0.0000001", "0.0000002", "0.0000003"]), series("B", "DNK", ["1000000000000", "2000000000000", "3000000000000"]), minimum_aligned_pairs=3)["output_fingerprint"])
        getcontext().prec, getcontext().rounding = original
        self.assertEqual(len(set(outputs)), 1)

    def test_spurious_and_structural_overlap_diagnostics_are_reported(self):
        result = self.module.compute_correlation(series("A", "DNK", [1, 2, 3, 4, 5]), series("B", "DNK", [2, 3, 4, 5, 6]), minimum_aligned_pairs=3)
        self.assertTrue(result["diagnostics"]["series_a_strong_time_ordering"])
        self.assertTrue(result["diagnostics"]["series_b_strong_time_ordering"])
        overlap = self.module.screen_candidate_pair({"series_a_code": "NE.EXP.GNFS.ZS", "series_b_code": "NE.TRD.GNFS.ZS", "relationship_risk": "component_vs_total"})
        self.assertEqual(overlap["decision"], "reject")


if __name__ == "__main__":
    unittest.main()
