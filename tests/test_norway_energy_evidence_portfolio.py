import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "artifacts/production/evidence-portfolio-energy-mining-norway-baseline-20260817/portfolio_manifest.json"
TOOL_PATH = ROOT / "tools/evidence_portfolio_production.py"

spec = importlib.util.spec_from_file_location("epp_norway_energy", TOOL_PATH)
assert spec is not None and spec.loader is not None
epp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(epp)


def manifest():
    return json.loads(MANIFEST_PATH.read_text())


def metric(outcome, name):
    return next(row["value"] for row in outcome["result_records"] if row["metric"] == name)


class NorwayEnergyPortfolioTests(unittest.TestCase):
    def test_frozen_two_candidate_manifest_validates_with_registered_family_and_unique_package_ids(self):
        frozen = manifest()
        self.assertEqual(frozen["candidate_order"], [
            "candidate-energy-mining-eg-elc-fosl-zs-nor-1990-2024-baseline-v1",
            "candidate-energy-mining-eg-elc-rnwx-zs-nor-1990-2024-baseline-v1",
        ])
        self.assertEqual(epp.validate_manifest(frozen), {"valid": True, "entry_count": 2})
        package_ids = [epp.stable_object_id(entry) for entry in frozen["entries"]]
        self.assertEqual(package_ids, [
            "pkg-object-eppilot-energy-mining-eg-elc-fosl-zs-nor-1990-2024-baseline-v1",
            "pkg-object-eppilot-energy-mining-eg-elc-rnwx-zs-nor-1990-2024-baseline-v1",
        ])
        self.assertEqual(len(package_ids), len(set(package_ids)))

    def test_retained_coverage_missingness_adjacency_and_percentage_point_units_are_exact(self):
        frozen = manifest()
        expected = {
            "EG.ELC.FOSL.ZS": {"observed": 34, "missing": 1, "coverage": "0.971428571429", "last": 2023, "adjacent": 33},
            "EG.ELC.RNWX.ZS": {"observed": 32, "missing": 3, "coverage": "0.914285714286", "last": 2021, "adjacent": 31},
        }
        for entry in frozen["entries"]:
            with self.subTest(indicator=entry["indicator"]["code"]):
                outcome = epp.execute_entry(entry, ROOT)
                self.assertEqual(outcome["disposition"], "valid")
                values = expected[entry["indicator"]["code"]]
                self.assertEqual(metric(outcome, "expected_observation_slot_count"), 35)
                self.assertEqual(metric(outcome, "observed_count"), values["observed"])
                self.assertEqual(metric(outcome, "missing_count"), values["missing"])
                self.assertEqual(metric(outcome, "coverage_share"), values["coverage"])
                self.assertEqual(metric(outcome, "last_valid_observation")["period"], values["last"])
                self.assertEqual(metric(outcome, "adjacent_first_difference_count"), values["adjacent"])
                for row in outcome["result_records"]:
                    if row["metric"] in epp._RATE_METRICS:
                        self.assertEqual(row["value"]["unit"], "percentage points per year")
                    elif row["metric"] in epp._ABSOLUTE_DELTA_METRICS:
                        self.assertEqual(row["value"]["unit"], "percentage points")

    def test_internal_missing_year_does_not_create_difference_across_calendar_gap(self):
        entry = manifest()["entries"][1]
        normalized = epp.read_json(ROOT / entry["input"]["path"])
        probe = copy.deepcopy(normalized)
        row = next(row for row in probe["observations"] if row["period"] == 2005)
        row.update(observed=False, value=None, value_canonical=None)
        outcome = epp.calculate_candidate(entry, probe)
        # Original retained count is 31. Removing an internal year removes the
        # 2004->2005 and 2005->2006 pairs and must not add 2004->2006.
        self.assertEqual(metric(outcome, "adjacent_first_difference_count"), 29)

    def test_manifest_coverage_contract_mismatch_fails_before_calculation(self):
        entry = copy.deepcopy(manifest()["entries"][0])
        entry["coverage_contract"]["observed_count"] = 35
        with mock.patch.object(epp, "calculate_candidate", side_effect=AssertionError("calculation reached")):
            outcome = epp.execute_entry(entry, ROOT)
        self.assertEqual(outcome["disposition"], "failed")
        self.assertEqual(outcome["stage"], "input_validation")
        self.assertIn("coverage contract", outcome["reason"])

    def test_altered_retained_input_bytes_fail_before_calculation(self):
        entry = copy.deepcopy(manifest()["entries"][0])
        source = ROOT / entry["input"]["path"]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            target = root / "fixture.json"
            target.write_bytes(source.read_bytes() + b"\n")
            entry["input"]["path"] = "fixture.json"
            with mock.patch.object(epp, "calculate_candidate", side_effect=AssertionError("calculation reached")):
                outcome = epp.execute_entry(entry, root)
        self.assertEqual(outcome["disposition"], "failed")
        self.assertEqual(outcome["stage"], "input_validation")
        self.assertEqual(outcome["reason"], "input hash mismatch")

    def test_duplicate_package_identity_is_rejected_at_manifest_boundary(self):
        frozen = manifest()
        duplicate = copy.deepcopy(frozen["entries"][0])
        duplicate["candidate_id"] = "candidate-energy-mining-duplicate-identity-probe"
        duplicate["canary"] = False
        frozen["entries"][1] = duplicate
        frozen["candidate_order"] = [entry["candidate_id"] for entry in frozen["entries"]]
        frozen["manifest_fingerprint"] = epp.fingerprint({key: value for key, value in frozen.items() if key != "manifest_fingerprint"})
        with self.assertRaisesRegex(ValueError, "duplicate.*package|package.*identity"):
            epp.validate_manifest(frozen)

    def test_output_budget_overflow_fails_closed(self):
        frozen = manifest()
        outcomes = [
            {"candidate_id": entry["candidate_id"], "disposition": "valid", "raw_result_count": 29, "valid_result_count": 29}
            for entry in frozen["entries"]
        ]
        with self.assertRaisesRegex(ValueError, "result.*limit|budget"):
            epp.enforce_aggregate_result_limit(frozen, outcomes)

    def test_elapsed_wall_telemetry_cannot_change_admission_or_persistence_eligibility(self):
        entry = manifest()["entries"][0]
        outcome = epp.execute_entry(entry, ROOT)
        self.assertEqual(outcome["disposition"], "valid")
        # Wall-clock telemetry is host-dependent evidence only. Even an observed
        # value above the manifest's telemetry threshold cannot change the
        # deterministic result-count acceptance boundary.
        elapsed = entry["computational_budget"]["maximum_wall_seconds"] + 1.0
        self.assertIsNone(epp.enforce_candidate_result_limits(entry, outcome, elapsed))

    def test_governing_question_and_claim_boundary_are_frozen(self):
        frozen = manifest()
        question = frozen["governing_question"]
        self.assertIn("without treating the two series as an exhaustive composition", question)
        self.assertIn("without", question)
        rendered = json.dumps(frozen, sort_keys=True).lower()
        self.assertNotIn('"coefficient":', rendered)
        self.assertNotIn('"calculated_value":', rendered)
        for entry in frozen["entries"]:
            limitations = " ".join(entry["family_configuration"]["package_limitations"]).lower()
            self.assertIn("not exhaustive", limitations)
            self.assertIn("no cross-series", limitations)
            self.assertIn("no interpolation", limitations)


if __name__ == "__main__":
    unittest.main()
