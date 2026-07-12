from __future__ import annotations

import importlib.util
import json
import unittest
from decimal import ROUND_DOWN, ROUND_HALF_EVEN, ROUND_UP, getcontext
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "run_campaign34_wdi_denmark_population_statistical_summary.py"
FIXTURE_PATH = PROJECT_ROOT / "artifacts" / "evidence-fixtures" / "wdi-demographic-population-total-denmark-1990-2024-https-corrected" / "normalized_observations.json"


def load_module():
    spec = importlib.util.spec_from_file_location("campaign34", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign34DecimalContextEvaluationTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.normalized = json.loads(FIXTURE_PATH.read_text())
        self.original_prec = getcontext().prec
        self.original_rounding = getcontext().rounding

    def tearDown(self):
        getcontext().prec = self.original_prec
        getcontext().rounding = self.original_rounding

    def _run_with_context(self, precision: int, rounding: str):
        getcontext().prec = precision
        getcontext().rounding = rounding
        measures = self.module.compute_statistical_summary(self.normalized)
        package = self.module.build_campaign34_package(self.normalized)
        return {
            "mean": measures["arithmetic_mean"],
            "stddev": measures["population_standard_deviation"],
            "package_fingerprint": package["fingerprints"]["package_manifest"],
        }

    def test_campaign34_v1_exposes_ambient_decimal_context_dependency(self):
        default = self._run_with_context(28, ROUND_HALF_EVEN)
        low_precision = self._run_with_context(10, ROUND_DOWN)
        high_precision = self._run_with_context(50, ROUND_UP)

        self.assertNotEqual(default, low_precision)
        self.assertNotEqual(default, high_precision)
        self.assertNotEqual(low_precision["package_fingerprint"], high_precision["package_fingerprint"])

        # This is a gate/evaluation test, not a production-regression test: it
        # intentionally documents that Campaign 34 v1 does not establish a
        # local Decimal context and therefore should not be replicated as-is.
        self.assertEqual("5506886.828571428571428571429", default["mean"])
        self.assertEqual("244565.4198270283104925028932", default["stddev"])


if __name__ == "__main__":
    unittest.main()
