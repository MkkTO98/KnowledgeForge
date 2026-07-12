from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "run_campaign34_wdi_denmark_population_statistical_summary.py"
FIXTURE_PATH = PROJECT_ROOT / "artifacts" / "evidence-fixtures" / "wdi-demographic-population-total-denmark-1990-2024-https-corrected" / "normalized_observations.json"


def load_module():
    spec = importlib.util.spec_from_file_location("campaign34", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign34StatisticalSummaryTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.normalized = json.loads(FIXTURE_PATH.read_text())

    def test_calculation_contract_uses_exact_decimal_population_methods(self):
        contract = self.module.calculation_contract(self.normalized)
        self.assertEqual(contract["decimal_parsing_method"], "Decimal from canonical base-10 strings")
        self.assertEqual(contract["standard_deviation"], "population standard deviation, denominator N")
        self.assertEqual(contract["rounding_mode"], "ROUND_HALF_EVEN")
        self.assertEqual(contract["minimum_observed_count"], 30)
        self.assertEqual(contract["minimum_coverage_share"], "0.85")
        self.assertNotIn("quantile", json.dumps(contract).lower())

    def test_statistical_measures_match_independent_decimal_recomputation(self):
        result = self.module.compute_statistical_summary(self.normalized)
        values = [Decimal(obs["value_canonical"]) for obs in self.normalized["observations"] if obs["observed"]]
        expected_mean = sum(values) / Decimal(len(values))
        expected_median = values[len(values) // 2]
        expected_variance = sum((v - expected_mean) * (v - expected_mean) for v in values) / Decimal(len(values))
        expected_std = expected_variance.sqrt()
        self.assertEqual(result["expected_observation_slot_count"], 35)
        self.assertEqual(result["observed_count"], 35)
        self.assertEqual(result["missing_count"], 0)
        self.assertEqual(result["missing_share"], "0")
        self.assertEqual(result["coverage_share"], "1")
        self.assertEqual(result["first_valid_observation"]["period"], 1990)
        self.assertEqual(result["last_valid_observation"]["period"], 2024)
        self.assertEqual(result["minimum"]["value"], min(values).to_eng_string())
        self.assertEqual(result["maximum"]["value"], max(values).to_eng_string())
        self.assertEqual(result["arithmetic_mean"], expected_mean.to_eng_string())
        self.assertEqual(result["median"], expected_median.to_eng_string())
        self.assertEqual(result["population_standard_deviation"], expected_std.to_eng_string())

    def test_package_contains_single_descriptive_statement_and_no_interpretation(self):
        package = self.module.build_campaign34_package(self.normalized)
        self.assertEqual(package["package_kind"], "KnowledgeObjectPackage")
        self.assertEqual(len(package["generated_statements"]), 1)
        statement_text = package["generated_statements"][0]["text"].lower()
        forbidden = ["because", "forecast", "recommend", "investment", "trend", "good", "bad", "expected future", "caused"]
        for term in forbidden:
            self.assertNotIn(term, statement_text)
        self.assertEqual(package["validation_state"]["validation_result"], "pass")
        self.assertIn("corrected_normalized_evidence_fingerprint", package["provenance_envelope"])

    def test_campaign_writes_one_candidate_one_object_and_validation_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "campaign34"
            repo = Path(tmp) / "repo"
            result = self.module.run_campaign(output_dir=out, repository_root=repo, fixture_path=FIXTURE_PATH)
            self.assertEqual(result["decision"], "accepted")
            self.assertEqual(result["packages_promoted"], 1)
            self.assertTrue((out / "candidate_statistical_summary.json").exists())
            self.assertTrue((out / "knowledge_object_package.json").exists())
            self.assertTrue((out / "validation_judgment.json").exists())
            self.assertEqual(json.loads((repo / "manifest.json").read_text())["object_count"], 1)

    def test_module_has_no_macroforge_runtime_or_database_dependency(self):
        source = MODULE_PATH.read_text()
        forbidden = ["MacroForge", "macroforge", "psql", "psycopg", "postgres", "sqlite", "duckdb"]
        for term in forbidden:
            self.assertNotIn(term, source)


if __name__ == "__main__":
    unittest.main()
