from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module():
    spec = importlib.util.spec_from_file_location("first_difference_pearson", ROOT / "tools/first_difference_pearson_method_v1.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FirstDifferencePearsonMethodTest(unittest.TestCase):
    def setUp(self):
        self.m = load_module()

    def series(self, code="A", unit="percent of GDP", values=None, entity="DNK"):
        values = values or {2000: "1", 2001: "3", 2002: "6", 2003: "10"}
        return {
            "series_id": {
                "indicator_code": code,
                "indicator_name": f"Indicator {code}",
                "entity_id": entity,
                "frequency": "annual",
                "unit": unit,
                "transformation": "raw",
            },
            "evidence_identity": {"normalized_fingerprint": f"sha256:{code.lower()*64}"[:71]},
            "observations": [
                {"period": period, "observed": value is not None, "value_canonical": value}
                for period, value in values.items()
            ],
        }

    def test_first_difference_requires_consecutive_periods_and_does_not_bridge_gaps(self):
        s = self.series(values={2000: "1", 2001: None, 2002: "5", 2003: "9"})
        transformed = self.m.first_difference_series(s)
        self.assertEqual(transformed["series_id"]["transformation"], "first_difference")
        observed = {row["period"]: row["value_canonical"] for row in transformed["observations"] if row["observed"]}
        self.assertEqual(observed, {2003: "4"})
        missing_reasons = {row["period"]: row["missing_reason"] for row in transformed["observations"] if not row["observed"]}
        self.assertIn(2002, missing_reasons)
        self.assertIn("non_consecutive_or_missing_endpoint", missing_reasons[2002])

    def test_duplicate_nonfinite_and_unresolved_unit_fail_closed(self):
        dup = self.series(values={2000: "1", 2001: "2"})
        dup["observations"].append({"period": 2001, "observed": True, "value_canonical": "3"})
        with self.assertRaisesRegex(ValueError, "duplicate"):
            self.m.first_difference_series(dup)
        with self.assertRaisesRegex(ValueError, "non-finite|invalid decimal"):
            self.m.first_difference_series(self.series(values={2000: "1", 2001: "NaN"}))
        with self.assertRaisesRegex(ValueError, "unresolved unit"):
            self.m.first_difference_series(self.series(unit=""))

    def test_unit_semantics_are_absolute_first_differences_not_growth_rates(self):
        cases = {
            "percent of GDP": "year-to-year change in percentage points of GDP",
            "% of population": "year-to-year percentage-point change",
            "per 1,000 people": "absolute year-to-year change in per 1,000 people",
            "current US$": "year-to-year change in current US$",
            "count": "year-to-year change in count",
        }
        for raw, expected in cases.items():
            with self.subTest(raw=raw):
                self.assertEqual(self.m.transformed_unit(raw), expected)
                self.assertNotIn("growth", expected.lower())
                self.assertNotIn("percent change", expected.lower())

    def test_method_computes_first_difference_pearson_and_rejects_zero_variance_or_insufficient_overlap(self):
        a = self.series("A", values={y: str((y - 1999) ** 2) for y in range(2000, 2032)})
        b = self.series("B", values={y: str(((y - 1999) ** 2) * 2) for y in range(2000, 2032)})
        result = self.m.compute_first_difference_pearson(a, b)
        self.assertEqual(result["method_id"], "wdi_annual_scalar_first_difference_pearson_v1")
        self.assertEqual(result["coefficient"]["canonical"], "1")
        self.assertEqual(result["aligned_transformed_observation_count"], 31)
        with self.assertRaisesRegex(ValueError, "zero variance"):
            self.m.compute_first_difference_pearson(a, self.series("C", values={y: str(y * 3) for y in range(2000, 2032)}))
        with self.assertRaisesRegex(ValueError, "insufficient aligned transformed observations"):
            self.m.compute_first_difference_pearson(self.series("D", values={2000:"1",2001:"2"}), self.series("E", values={2000:"1",2001:"3"}))

    def test_reusable_and_reference_paths_agree_and_are_context_order_invariant(self):
        a = self.m.load_series_from_normalized("artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https/FS.AST.PRVT.GD.ZS__SWE__1990-2024/normalized_observations.json")
        b = self.m.load_series_from_normalized("artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https/IT.NET.USER.ZS__SWE__1990-2024/normalized_observations.json")
        baseline = self.m.compute_first_difference_pearson(a, b)
        reference = self.m.reference_first_difference_pearson(a, b)
        self.assertEqual(baseline["coefficient"]["canonical"], reference["coefficient"]["canonical"])
        original_prec, original_rounding = getcontext().prec, getcontext().rounding
        try:
            for prec, rounding in [(7, ROUND_FLOOR), (99, ROUND_CEILING)]:
                getcontext().prec = prec
                getcontext().rounding = rounding
                shuffled_a = dict(a); shuffled_a["observations"] = list(reversed(a["observations"]))
                shuffled_b = dict(b); shuffled_b["observations"] = list(reversed(b["observations"]))
                rerun = self.m.compute_first_difference_pearson(shuffled_a, shuffled_b)
                self.assertEqual(baseline["result_fingerprint"], rerun["result_fingerprint"])
        finally:
            getcontext().prec = original_prec
            getcontext().rounding = original_rounding

    def test_fingerprint_sensitivity_and_registry_is_coefficient_free(self):
        contract = self.m.method_contract_v1()
        changed = json.loads(json.dumps(contract))
        changed["transformation_contract"]["gap_behavior"] = "bridge gaps"
        self.assertNotEqual(contract["method_contract_fingerprint"], self.m.sha256_value({k:v for k,v in changed.items() if k != "method_contract_fingerprint"}))
        registry = self.m.build_validation_registry()
        self.assertTrue(registry["coefficient_free"])
        self.assertEqual(registry["validation_case_count"], len(registry["cases"]))
        text = json.dumps(registry).lower()
        for forbidden in ["coefficient\"", "pearson_coefficient", "p_value", "significance"]:
            self.assertNotIn(forbidden, text)
        self.assertTrue(registry["registry_fingerprint"].startswith("sha256:"))

    def test_diagnostic_reconciliation_and_representation_simulations(self):
        report = self.m.reconcile_existing_first_difference_diagnostics()
        self.assertGreaterEqual(report["compared_count"], 5)
        self.assertEqual(report["mismatch_count"], 0, report.get("mismatches"))
        package = self.m.simulate_companion_package_payload(report["comparisons"][0])
        proof = self.m.validate_representation_compatibility(package)
        self.assertTrue(proof["package_representation_valid"])
        self.assertTrue(proof["postgresql_projection_compatible"])
        self.assertTrue(proof["relationship_export_compatible"])
        self.assertIn("companion_raw_package_id", json.dumps(package))

    def test_separate_process_determinism(self):
        code = """
import importlib.util, json
from pathlib import Path
ROOT=Path('.').resolve()
spec=importlib.util.spec_from_file_location('m', ROOT/'tools/first_difference_pearson_method_v1.py')
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
a=m.load_series_from_normalized('artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https/SP.DYN.CBRT.IN__NOR__1990-2024/normalized_observations.json')
b=m.load_series_from_normalized('artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https/SH.DYN.MORT__NOR__1990-2024/normalized_observations.json')
print(json.dumps(m.compute_first_difference_pearson(a,b)['result_fingerprint']))
"""
        one = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True).strip()
        two = subprocess.check_output([sys.executable, "-c", code], cwd=ROOT, text=True).strip()
        self.assertEqual(one, two)


if __name__ == "__main__":
    unittest.main()
