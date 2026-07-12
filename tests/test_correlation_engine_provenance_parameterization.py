from __future__ import annotations

import copy
import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC_DIR = ROOT / "specs/correlation_batches"
CAMPAIGN40_SPEC = SPEC_DIR / "campaign40_first_end_to_end_spec_driven_pearson_batch.json"
CAMPAIGN41_READY_SPEC = SPEC_DIR / "campaign41_ready_pearson_batch_spec.json"
CAMPAIGN41_ORIGINAL_SPEC = SPEC_DIR / "campaign41_coefficient_free_pearson_batch_spec.json"


def load_engine():
    spec = importlib.util.spec_from_file_location("correlation_batch_engine_under_test", ROOT / "tools/correlation_batch_engine.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CorrelationEngineProvenanceParameterizationTest(unittest.TestCase):
    def setUp(self):
        self.engine = load_engine()
        self.c40 = json.loads(CAMPAIGN40_SPEC.read_text())
        self.c41 = json.loads(CAMPAIGN41_READY_SPEC.read_text())

    def test_campaign40_exact_backward_compatibility_payloads_and_fingerprints(self):
        with tempfile.TemporaryDirectory() as td:
            result = self.engine.run_production_spec(
                CAMPAIGN40_SPEC,
                output_dir=Path(td) / "out",
                fixture_dir=ROOT / "artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https",
                publish=False,
                offline_reuse=True,
                rebuild_postgres=False,
            )
            self.assertEqual(result["accepted_count"], 6)
            self.assertFalse(result["publication"]["performed"])
            self.assertFalse(result["postgresql"]["performed"])
            for path in sorted((Path(td) / "out" / "accepted_packages").glob("*.json")):
                generated = json.loads(path.read_text())
                canonical_path = ROOT / "knowledge_repository/objects" / path.name
                canonical = json.loads(canonical_path.read_text())
                self.assertEqual(generated, canonical, path.name)
                self.assertEqual(self.engine.sha256_value(generated), self.engine.sha256_value(canonical))

    def test_campaign41_spec_readiness_validates_without_calculating_coefficients(self):
        with mock.patch.object(self.engine, "_correlation_module", side_effect=AssertionError("calculation not allowed")):
            validation = self.engine.validate_spec(self.c41)
        self.assertTrue(validation["valid"])
        self.assertEqual(validation["candidate_count"], 8)
        self.assertTrue(validation["provenance_validation"]["checked"])

    def test_campaign41_original_frozen_candidate_set_preserved_in_ready_spec(self):
        original = json.loads(CAMPAIGN41_ORIGINAL_SPEC.read_text())
        keys = ["candidate_id", "entity", "expected_package_id", "family", "period", "series_a", "series_b", "thresholds", "construction_risk"]
        for original_candidate, ready_candidate in zip(original["candidates"], self.c41["candidates"]):
            for key in keys:
                self.assertEqual(ready_candidate.get(key), original_candidate.get(key), key)
        self.assertEqual([c["candidate_id"] for c in original["candidates"]], [c["candidate_id"] for c in self.c41["candidates"]])

    def test_deterministic_unique_ids_across_campaign41_candidates(self):
        first = [self.engine.candidate_provenance_ids(self.c41, c) for c in self.c41["candidates"]]
        second = [self.engine.candidate_provenance_ids(self.c41, c) for c in self.c41["candidates"]]
        self.assertEqual(first, second)
        generated = []
        for ids in first:
            generated.extend([ids["statement_id"], ids["calculation_id"], ids["evidence_ref_id"]])
        self.assertEqual(len(generated), len(set(generated)))

    def test_missing_provenance_metadata_fails(self):
        spec = copy.deepcopy(self.c41)
        spec.pop("package_provenance", None)
        with self.assertRaisesRegex(ValueError, "missing required package_provenance"):
            self.engine.validate_spec(spec)

    def test_malformed_provenance_metadata_fails(self):
        spec = copy.deepcopy(self.c41)
        spec["package_provenance"]["identity_namespace"] = "campaign41/../../bad"
        with self.assertRaisesRegex(ValueError, "unsafe|path-like"):
            self.engine.validate_spec(spec)

    def test_unknown_template_field_fails(self):
        spec = copy.deepcopy(self.c41)
        spec["package_provenance"]["statement_id_template"] = "stmt-{campaign_id}-{coefficient}"
        with self.assertRaisesRegex(ValueError, "unknown template"):
            self.engine.validate_spec(spec)

    def test_cross_candidate_identity_collision_fails(self):
        spec = copy.deepcopy(self.c41)
        spec["package_provenance"]["statement_id_template"] = "stmt-{identity_namespace}-constant"
        with self.assertRaisesRegex(ValueError, "duplicate generated provenance id"):
            self.engine.validate_spec(spec)

    def test_campaign_package_identity_inconsistency_fails(self):
        spec = copy.deepcopy(self.c41)
        spec["candidates"][0]["expected_package_id"] = spec["candidates"][0]["expected_package_id"].replace("campaign41", "campaign99")
        with self.assertRaisesRegex(ValueError, "campaign/package identity inconsistency"):
            self.engine.validate_spec(spec)

    def test_candidate_entity_is_used_for_time_index_diagnostics(self):
        series = self.engine._time_series([1990, 1991], "NOR")
        self.assertEqual(series["series_id"]["entity_id"], "NOR")
        self.assertTrue(all(row["entity_id"] == "NOR" for row in series["observations"]))

    def test_no_campaign_literals_remain_in_generic_runtime_logic(self):
        source = (ROOT / "tools/correlation_batch_engine.py").read_text().lower()
        self.assertNotIn("campaign40", source)
        self.assertNotIn("campaign41", source)


if __name__ == "__main__":
    unittest.main()
