from __future__ import annotations

import importlib.util
import json
import unittest
from decimal import Decimal, getcontext, ROUND_DOWN, ROUND_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign36CorrelationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.campaign = load("campaign36", "tools/run_campaign36_dnk_exports_imports_correlation.py")
        self.corr = load("corr", "tools/deterministic_pearson_correlation_v1.py")

    def test_contract_fingerprint_is_required_value(self) -> None:
        self.assertEqual(
            self.corr.calculation_contract_v1()["calculation_contract_fingerprint"],
            "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476",
        )

    def test_downgrade_and_non_https_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.campaign.acquire_url("http://api.worldbank.org/v2/indicator/NE.EXP.GNFS.ZS?format=json")

    def test_alignment_rejects_missing_threshold_and_duplicates(self) -> None:
        def s(code: str, vals: list[str | None]):
            return {
                "series_id": {"indicator_code": code, "indicator_name": code, "entity_id": "DNK", "entity_name": "Denmark", "frequency": "annual", "unit": "percent of GDP", "transformation": "raw"},
                "metadata": {"name": code},
                "provider_metadata": {},
                "raw_fingerprints": {},
                "normalized_series_fingerprint": code,
                "observations": [
                    {"period": 1990 + i, "observed": v is not None, "value_canonical": v, "unit": "percent of GDP"}
                    for i, v in enumerate(vals)
                ],
            }
        with self.assertRaises(ValueError):
            self.campaign.validate_and_align(s("A", ["1", "2"] + [None] * 33), s("B", ["1", "2"] + [None] * 33))
        dup = s("A", [str(i + 1) for i in range(35)])
        dup["observations"].append(dict(dup["observations"][-1]))
        with self.assertRaises(ValueError):
            self.campaign.validate_and_align(dup, s("B", [str(i + 2) for i in range(35)]))

    def test_package_prohibited_language_check_allows_only_limitation_context(self) -> None:
        bad = {"generated_statements": [{"text": "Exports cause imports and predicts investment gains."}]}
        self.assertTrue(self.campaign.prohibited_language_check(bad))

    def test_ambient_decimal_context_and_pair_order_stable(self) -> None:
        def series(code: str, vals: list[str]):
            return {"series_id": {"indicator_code": code, "entity_id": "DNK", "frequency": "annual", "unit": "percent of GDP", "transformation": "raw"}, "observations": [{"period": 1990 + i, "observed": True, "value_canonical": v} for i, v in enumerate(vals)]}
        a = series("NE.EXP.GNFS.ZS", [str(i) for i in range(1, 36)])
        b = series("NE.IMP.GNFS.ZS", [str(i * 2) for i in range(1, 36)])
        fingerprints = []
        for prec, rounding in [(10, ROUND_DOWN), (60, ROUND_UP)]:
            getcontext().prec = prec
            getcontext().rounding = rounding
            fingerprints.append(self.corr.compute_correlation(a, b)["output_fingerprint"])
        ab = self.corr.compute_correlation(a, b)
        ba = self.corr.compute_correlation(b, a)
        self.assertEqual(len(set(fingerprints)), 1)
        self.assertEqual(ab["canonical_pair_id"], ba["canonical_pair_id"])
        self.assertEqual(ab["coefficient"], ba["coefficient"])


if __name__ == "__main__":
    unittest.main()
