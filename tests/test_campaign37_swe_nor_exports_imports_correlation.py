from __future__ import annotations

import importlib.util
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


class Campaign37ReplicationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.campaign = load("campaign37", "tools/run_campaign37_swe_nor_exports_imports_correlation.py")
        self.corr = load("corr37", "tools/deterministic_pearson_correlation_v1.py")

    def test_contract_fingerprint_is_required_value(self) -> None:
        self.assertEqual(
            self.corr.calculation_contract_v1()["calculation_contract_fingerprint"],
            "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476",
        )

    def test_downgrade_and_non_https_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.campaign.acquire_url("http://api.worldbank.org/v2/indicator/NE.EXP.GNFS.ZS?format=json")

    def _series(self, entity: str, code: str, values: list[str | None]) -> dict:
        return {
            "series_id": {
                "indicator_code": code,
                "indicator_name": code,
                "entity_id": entity,
                "entity_name": entity,
                "frequency": "annual",
                "unit": "percent of GDP",
                "transformation": "raw",
            },
            "metadata": {"name": code},
            "provider_metadata": {},
            "raw_fingerprints": {},
            "normalized_series_fingerprint": code + entity,
            "observations": [
                {
                    "entity_id": entity,
                    "entity_name": entity,
                    "indicator_code": code,
                    "period": 1990 + i,
                    "frequency": "annual",
                    "transformation": "raw",
                    "unit": "percent of GDP",
                    "observed": value is not None,
                    "value_canonical": value,
                }
                for i, value in enumerate(values)
            ],
        }

    def test_per_entity_alignment_rejects_threshold_and_duplicate_keys(self) -> None:
        with self.assertRaises(ValueError):
            self.campaign.validate_and_align(
                "SWE",
                self._series("SWE", "NE.EXP.GNFS.ZS", ["1", "2"] + [None] * 33),
                self._series("SWE", "NE.IMP.GNFS.ZS", ["1", "2"] + [None] * 33),
            )
        dup = self._series("NOR", "NE.EXP.GNFS.ZS", [str(i + 1) for i in range(35)])
        dup["observations"].append(dict(dup["observations"][-1]))
        with self.assertRaises(ValueError):
            self.campaign.validate_and_align(
                "NOR",
                dup,
                self._series("NOR", "NE.IMP.GNFS.ZS", [str(i + 2) for i in range(35)]),
            )

    def test_ambient_decimal_context_and_pair_order_stable(self) -> None:
        def series(entity: str, code: str, vals: list[str]):
            return {
                "series_id": {
                    "indicator_code": code,
                    "entity_id": entity,
                    "frequency": "annual",
                    "unit": "percent of GDP",
                    "transformation": "raw",
                },
                "observations": [
                    {"period": 1990 + i, "observed": True, "value_canonical": value}
                    for i, value in enumerate(vals)
                ],
            }
        a = series("SWE", "NE.EXP.GNFS.ZS", [str(i) for i in range(1, 36)])
        b = series("SWE", "NE.IMP.GNFS.ZS", [str(i * 2) for i in range(1, 36)])
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

    def test_campaign37_does_not_retry_local_ai(self) -> None:
        self.assertFalse(hasattr(self.campaign, "local_ai_retry"))


if __name__ == "__main__":
    unittest.main()
