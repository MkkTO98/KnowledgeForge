from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "run_campaign35_wdi_nordic_exports_statistical_summary.py"
EXPECTED_CONTRACT = "sha256:80e6b07fd98faf37401103776b6ef82f4ab981c5ea890b381b036058c460e8a0"


def load_module():
    spec = importlib.util.spec_from_file_location("campaign35", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign35NordicExportsTest(unittest.TestCase):
    def test_campaign35_contract_and_scope_are_fixed(self):
        module = load_module()
        self.assertEqual(module.INDICATOR_CODE, "NE.EXP.GNFS.ZS")
        self.assertEqual(module.ENTITIES, ["DNK", "SWE", "NOR"])
        self.assertEqual(module.START_YEAR, 1990)
        self.assertEqual(module.END_YEAR, 2024)
        self.assertEqual(module.EXPECTED_CONTRACT_FINGERPRINT, EXPECTED_CONTRACT)
        contract = module.verify_loaded_v2_contract()
        self.assertEqual(contract["calculation_contract_fingerprint"], EXPECTED_CONTRACT)

    def test_validate_fixture_rejects_wrong_indicator_and_duplicate_keys(self):
        module = load_module()
        fixture = {
            "indicator_metadata": {"id": "WRONG", "name": "Exports of goods and services (% of GDP)", "unit": "", "definition": "Exports of goods and services represent the value of all goods and other market services provided to the rest of the world."},
            "selection_contract": {"indicator": {"code": "NE.EXP.GNFS.ZS"}, "entities": ["DNK", "NOR", "SWE"], "periods": {"start_year": 1990, "end_year": 2024}},
            "observations": [
                {"entity_id": "DNK", "indicator_code": "NE.EXP.GNFS.ZS", "period": 1990, "observed": True, "value_canonical": "1", "unit": "percent of GDP"},
                {"entity_id": "DNK", "indicator_code": "NE.EXP.GNFS.ZS", "period": 1990, "observed": True, "value_canonical": "1", "unit": "percent of GDP"},
            ],
            "expected_observation_slots": 105,
        }
        result = module.validate_campaign35_fixture(fixture)
        categories = {item["category"] for item in result["blockers"]}
        self.assertIn("indicator_identity", categories)
        self.assertIn("duplicate_keys", categories)

    def test_build_entity_package_rejects_prohibited_language(self):
        module = load_module()
        package = {"generated_statements": [{"text": "This trend forecasts investment implications.", "structured_payload": {}}], "provenance_envelope": {}, "fingerprints": {}}
        result = module.validate_campaign35_package(package, {})
        self.assertEqual(result["validation_result"], "reject")
        self.assertTrue(any(item["category"] == "boundary" for item in result["blockers"]))

    def test_per_entity_summary_from_fixture_shape(self):
        module = load_module()
        rows = []
        for entity in ["DNK", "NOR", "SWE"]:
            for year in range(1990, 2025):
                rows.append({"entity_id": entity, "entity_name": entity, "indicator_code": "NE.EXP.GNFS.ZS", "indicator_name": "Exports of goods and services (% of GDP)", "period": year, "frequency": "annual", "unit": "percent of GDP", "observed": True, "value_canonical": str(10 + (year - 1990) / 10), "missing_reason": None})
        normalized = {
            "indicator_metadata": {"id": "NE.EXP.GNFS.ZS", "name": "Exports of goods and services (% of GDP)", "unit": "", "definition": "Exports of goods and services represent the value of all goods and other market services provided to the rest of the world."},
            "selection_contract": {"selection_fingerprint": "sha256:" + "1" * 64, "indicator": {"code": "NE.EXP.GNFS.ZS"}, "entities": ["DNK", "NOR", "SWE"], "periods": {"start_year": 1990, "end_year": 2024}},
            "raw_artifacts": {"combined_raw_artifact_fingerprint": "sha256:" + "2" * 64},
            "provider_metadata": {"wdi_lastupdated": "2026-01-01", "sourceid": "2"},
            "source_raw_fixture_fingerprint": "sha256:" + "3" * 64,
            "normalized_fingerprint": "sha256:" + "4" * 64,
            "mutable_source_reproducibility_note": {"vintage_limitation": "mutable"},
            "observations": rows,
            "expected_observation_slots": 105,
        }
        summaries = module.compute_entity_summaries(normalized)
        self.assertEqual(sorted(summaries), ["DNK", "NOR", "SWE"])
        for entity, summary in summaries.items():
            self.assertEqual(summary["expected_observation_slot_count"], 35)
            self.assertEqual(summary["observed_count"], 35)
            self.assertEqual(summary["unit"], "percent of GDP")
            self.assertIn("population_standard_deviation", summary)


if __name__ == "__main__":
    unittest.main()
