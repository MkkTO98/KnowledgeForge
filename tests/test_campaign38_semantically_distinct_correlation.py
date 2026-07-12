from __future__ import annotations

import importlib.util
import json
import unittest
from decimal import ROUND_DOWN, ROUND_UP, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTION_PATH = ROOT / "artifacts/reports/campaign38-semantically-distinct-wdi-pearson-correlation-20260711/selection/campaign38_frozen_selection_decision.json"


def load_module(name: str, rel: str):
    path = ROOT / rel
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign38SemanticCorrelationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.selection = json.loads(SELECTION_PATH.read_text())
        self.campaign = load_module("campaign38", "tools/run_campaign38_semantically_distinct_correlation.py")
        self.corr = load_module("corr", "tools/deterministic_pearson_correlation_v1.py")

    def test_selection_was_frozen_without_coefficient_calculation(self) -> None:
        self.assertFalse(self.selection["coefficient_calculation_performed_during_selection"])
        self.assertEqual(self.selection["selected_candidate_id"], "demographic_life_expectancy_fertility_pair")
        self.assertEqual(self.selection["selected_entity"], "DNK")
        self.assertEqual(self.selection["selected_series"]["a"]["code"], "SP.DYN.LE00.IN")
        self.assertEqual(self.selection["selected_series"]["b"]["code"], "SP.DYN.TFRT.IN")
        serialized = json.dumps(self.selection, sort_keys=True).lower()
        self.assertNotIn("pearson_coefficient", serialized)
        self.assertNotIn("coefficient_value", serialized)

    def test_contract_fingerprint_is_pinned(self) -> None:
        self.assertEqual(
            self.corr.calculation_contract_v1()["calculation_contract_fingerprint"],
            "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476",
        )
        self.assertEqual(self.campaign.EXPECTED_CONTRACT_FINGERPRINT, self.corr.calculation_contract_v1()["calculation_contract_fingerprint"])

    def test_https_downgrade_rejected(self) -> None:
        with self.assertRaises(ValueError):
            self.campaign.acquire_url("http://api.worldbank.org/v2/indicator/SP.DYN.LE00.IN?format=json")

    def test_campaign_scope_matches_frozen_selection(self) -> None:
        scope = self.campaign.campaign_scope()
        self.assertEqual(scope["entity_id"], "DNK")
        self.assertEqual(scope["series_a"]["code"], "SP.DYN.LE00.IN")
        self.assertEqual(scope["series_b"]["code"], "SP.DYN.TFRT.IN")
        self.assertEqual(scope["series_a"]["unit"], "years")
        self.assertEqual(scope["series_b"]["unit"], "births per woman")
        self.assertEqual(scope["expected_aligned_pairs"], 35)
        self.assertEqual(scope["minimum_aligned_pairs"], 30)

    def test_decimal_context_and_pair_order_invariance_on_fixture_series(self) -> None:
        if not self.campaign.FIXTURE_DIR.exists():
            self.skipTest("Campaign 38 fixture not acquired yet")
        raw = self.campaign.read_json(self.campaign.FIXTURE_DIR / "raw_fixture_manifest.json")
        a = self.campaign.normalize_series("a", raw)
        b = self.campaign.normalize_series("b", raw)
        fingerprints = []
        for precision, rounding in [(10, ROUND_DOWN), (60, ROUND_UP)]:
            getcontext().prec = precision
            getcontext().rounding = rounding
            fingerprints.append(self.campaign.calculate(a, b, self.campaign.validate_and_align(a, b))["method_result"]["output_fingerprint"])
        ab = self.campaign.calculate(a, b, self.campaign.validate_and_align(a, b))["method_result"]
        ba = self.campaign.calculate(b, a, self.campaign.validate_and_align(b, a))["method_result"]
        self.assertEqual(len(set(fingerprints)), 1)
        self.assertEqual(ab["canonical_pair_id"], ba["canonical_pair_id"])
        self.assertEqual(ab["coefficient"], ba["coefficient"])

    def test_no_local_ai_retry_surface(self) -> None:
        self.assertFalse(hasattr(self.campaign, "local_ai_retry"))


if __name__ == "__main__":
    unittest.main()
