from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "evidence_portfolio_production.py"
SPEC = importlib.util.spec_from_file_location("epp", TOOL)
epp = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(epp)
sys.path.insert(0, str(ROOT / "tools"))
import postgresql_operational_projection as projection


def synthetic_normalized(*, observed=35):
    rows = []
    for year in range(1990, 2025):
        is_observed = year < 1990 + observed
        rows.append({
            "entity_id": "NOR", "entity_name": "Norway", "indicator_code": "TEST.HEALTH",
            "period": year, "observed": is_observed,
            "value_canonical": str(50 + (year - 1990) * 0.5) if is_observed else None,
            "unit": "years",
        })
    value = {
        "selection_contract": {"indicator": {"code": "TEST.HEALTH", "name": "Test health"}, "entities": ["NOR"], "periods": {"start_year": 1990, "end_year": 2024}},
        "indicator_metadata": {"id": "TEST.HEALTH", "name": "Test health", "unit": "years", "definition": "fixture"},
        "provider_metadata": {"provider": "World Bank", "dataset": "World Development Indicators", "sourceid": "2", "wdi_lastupdated": "2026-07-01"},
        "raw_artifacts": {"combined_raw_artifact_fingerprint": "sha256:" + "1" * 64},
        "normalized_fingerprint": "sha256:" + "2" * 64,
        "expected_observation_slots": 35,
        "observations": rows,
    }
    return value


def manifest_entry():
    return {
        "candidate_id": "health-test-nor-1990-2024",
        "disposition": "execute",
        "canary": True,
        "input": {"path": "fixture.json", "sha256": "sha256:" + "3" * 64, "normalized_fingerprint": "sha256:" + "2" * 64},
        "indicator": {"code": "TEST.HEALTH", "name": "Test health", "definition": "Synthetic health-state duration fixture.", "family": "Health"},
        "territory": {"id": "NOR", "name": "Norway", "observational_population": "retained annual Norway observations"},
        "applicability": {"denominator_basis": "not_applicable_unit_years", "unit": "years", "period_start": 1990, "period_end": 2024, "frequency": "annual", "observation_grain": "territory_indicator_year"},
        "transformation": ["level", "first_difference", "time_index_linear_slope"],
        "method": {"id": "baseline_characterization_portfolio_v1", "version": "1.0", "parameters": {"minimum_observed_count": 30, "minimum_coverage_share": "0.85"}},
        "expected_output_class": "baseline_characterization",
        "dependencies": ["retained_campaign40_fixture", "wdi_annual_scalar_statistical_summary_v2@2.0"],
        "bundle_id": "bundle-health-norway-1990-2024",
        "campaign_id": "evidence-portfolio-pilot-health-baseline-20260730",
        "computational_budget": {"maximum_result_records": 28, "maximum_wall_seconds": 5},
        "validation_requirements": ["input_hash", "coverage", "identity", "applicability", "lineage", "schema", "nonredundancy"],
        "promotion_conditions": ["all_required_results_valid", "no_identity_collision", "package_validation_pass"],
        "exclusion_and_stopping_rules": ["stop_on_input_hash_mismatch", "exclude_growth_rates"],
        "identity_inputs": {"indicator_code": "TEST.HEALTH", "territory_id": "NOR", "period_start": 1990, "period_end": 2024, "method_id": "baseline_characterization_portfolio_v1", "method_version": "1.0"},
    }


class PortfolioUnitTests(unittest.TestCase):
    def test_stable_identity_is_order_independent(self):
        entry = manifest_entry()
        self.assertEqual(epp.stable_object_id(entry), epp.stable_object_id(json.loads(json.dumps(entry, sort_keys=True))))

    def test_calculation_is_reproducible(self):
        a = epp.calculate_candidate(manifest_entry(), synthetic_normalized())
        b = epp.calculate_candidate(manifest_entry(), synthetic_normalized())
        self.assertEqual(a, b)
        self.assertEqual(epp.fingerprint(a), epp.fingerprint(b))

    def test_expected_result_classes_and_count(self):
        result = epp.calculate_candidate(manifest_entry(), synthetic_normalized())
        records = result["result_records"]
        self.assertEqual(len(records), 28)
        self.assertEqual({r["class"] for r in records}, {"coverage_missingness", "sample_period", "level_distribution", "differences", "trend_descriptor", "variability_stability"})

    def test_applicability_is_repeated_on_every_result(self):
        records = epp.calculate_candidate(manifest_entry(), synthetic_normalized())["result_records"]
        self.assertTrue(all(r["applicability"]["denominator_basis"] == "not_applicable_unit_years" for r in records))

    def test_null_rejection_failure_are_separate(self):
        outcomes = [
            {"candidate_id": "a", "disposition": "valid"},
            {"candidate_id": "b", "disposition": "null"},
            {"candidate_id": "c", "disposition": "rejected"},
            {"candidate_id": "d", "disposition": "failed"},
        ]
        accounting = epp.account_outcomes(outcomes, [], [])
        self.assertEqual((accounting["valid_candidates"], accounting["null_candidates"], accounting["rejected_candidates"], accounting["execution_failures"]), (1, 1, 1, 1))

    def test_exact_duplicate_semantics_detected(self):
        records = epp.calculate_candidate(manifest_entry(), synthetic_normalized())["result_records"]
        duplicated = records + [copy.deepcopy(records[0])]
        unique, redundant = epp.detect_redundancy(duplicated)
        self.assertEqual(len(unique), 28)
        self.assertEqual(len(redundant), 1)

    def test_identity_collision_with_different_value_fails(self):
        records = epp.calculate_candidate(manifest_entry(), synthetic_normalized())["result_records"]
        collision = copy.deepcopy(records[0]); collision["value"] = "different"
        with self.assertRaisesRegex(ValueError, "identity collision"):
            epp.detect_redundancy(records + [collision])

    def test_promotion_rejects_incomplete_results(self):
        result = epp.calculate_candidate(manifest_entry(), synthetic_normalized())
        result["result_records"].pop()
        with self.assertRaisesRegex(ValueError, "required result"):
            epp.build_knowledge_object(manifest_entry(), result, "sha256:" + "4" * 64)

    def test_object_identity_and_fingerprint_stable(self):
        result = epp.calculate_candidate(manifest_entry(), synthetic_normalized())
        a = epp.build_knowledge_object(manifest_entry(), result, "sha256:" + "4" * 64)
        b = epp.build_knowledge_object(manifest_entry(), result, "sha256:" + "4" * 64)
        self.assertEqual(a, b)
        self.assertEqual(a["package_id"], epp.stable_object_id(manifest_entry()))

    def test_input_immutability(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "fixture.json"; p.write_text(json.dumps(synthetic_normalized()))
            before = hashlib.sha256(p.read_bytes()).hexdigest()
            data = json.loads(p.read_text())
            epp.calculate_candidate(manifest_entry(), data)
            self.assertEqual(before, hashlib.sha256(p.read_bytes()).hexdigest())

    def test_expected_exclusion_is_not_executed(self):
        excluded = manifest_entry(); excluded["candidate_id"] = "excluded-cagr"; excluded["disposition"] = "excluded_pre_execution"; excluded["exclusion_reason"] = "compound growth is inapplicable"
        outcome = epp.execute_entry(excluded, ROOT)
        self.assertEqual(outcome["disposition"], "rejected")
        self.assertEqual(outcome["stage"], "pre_execution")

    def test_manifest_validation_rejects_outcome_fields(self):
        manifest = {"manifest_id": "m", "entries": [manifest_entry()], "candidate_order": ["health-test-nor-1990-2024"], "computational_budget": copy.deepcopy(epp.REQUIRED_PORTFOLIO_LIMITS), "selection_rubric_fingerprint": "sha256:" + "4" * 64, "forbidden_outcome_fields": ["calculated_value", "interesting"]}
        manifest["entries"][0]["interesting"] = True
        with self.assertRaisesRegex(ValueError, "outcome field"):
            epp.validate_manifest(manifest)

    def test_rerun_repository_idempotence(self):
        result = epp.calculate_candidate(manifest_entry(), synthetic_normalized())
        package = epp.build_knowledge_object(manifest_entry(), result, "sha256:" + "4" * 64)
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td)
            first = epp.persist_packages([package], repo)
            second = epp.persist_packages([package], repo)
            self.assertEqual(first["repository_fingerprint"], second["repository_fingerprint"])
            self.assertEqual(first["object_count"], 1)

    def test_operational_views_are_not_canonical_objects(self):
        result = epp.calculate_candidate(manifest_entry(), synthetic_normalized())
        views = epp.render_operational_views(manifest_entry(), result)
        self.assertEqual(len(views), 28)
        self.assertTrue(all(v["view_kind"] == "EvidenceCardEquivalentView" for v in views))
        self.assertTrue(all("package_kind" not in v for v in views))

    def test_manifest_to_result_accounting(self):
        outcomes = [{"candidate_id": "a", "disposition": "valid", "raw_result_count": 28}, {"candidate_id": "b", "disposition": "rejected", "raw_result_count": 0}]
        accounting = epp.account_outcomes(outcomes, [{"package_id": "p", "scope": {"source_scope": {"indicator_code": "TEST.HEALTH"}}}], [{"view_id": str(i)} for i in range(28)])
        self.assertEqual(accounting["executed_candidates"], 1)
        self.assertEqual(accounting["raw_calculation_results"], 28)
        self.assertEqual(accounting["promoted_canonical_objects"], 1)
        self.assertEqual(accounting["operational_views"], 28)

    def test_unrelated_path_preservation_detects_only_outside_allowlist(self):
        baseline = {"unrelated.txt": {"status": "M", "sha256": "a"}, "task.json": {"status": "?", "sha256": "old"}}
        current = {"unrelated.txt": {"status": "M", "sha256": "a"}, "task.json": {"status": "?", "sha256": "new"}}
        self.assertTrue(epp.verify_unrelated_identity_preservation(baseline, current, {"task.json"})["valid"])
        current["unrelated.txt"]["sha256"] = "changed"
        result = epp.verify_unrelated_identity_preservation(baseline, current, {"task.json"})
        self.assertFalse(result["valid"])
        self.assertEqual(result["changed_unrelated_paths"], ["unrelated.txt"])

    def test_tampered_manifest_fingerprint_fails_closed(self):
        _, manifest = epp.build_preregistration()
        manifest["entries"][0]["applicability"]["unit"] = "tampered"
        with self.assertRaisesRegex(ValueError, "manifest fingerprint mismatch"):
            epp.validate_manifest(manifest)

    @unittest.skipUnless(all(shutil.which(name) for name in ("psql", "createdb", "dropdb")), "PostgreSQL CLI unavailable")
    def test_projection_compatibility_for_promoted_object(self):
        result = epp.calculate_candidate(manifest_entry(), synthetic_normalized())
        package = epp.build_knowledge_object(manifest_entry(), result, "sha256:" + "4" * 64)
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repository"
            epp.persist_packages([package], repo)
            db = f"knowledgeforge_eppilot_unit_{os.getpid()}"
            subprocess.run(["dropdb", "--if-exists", db], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            try:
                subprocess.run(["createdb", db], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                projection.rebuild_projection(repo, db)
                verified = projection.verify_projection(repo, db)
                filtered = projection.filter_packages(repo, db, evidence_family="external_wdi_annual_scalar_health_baseline_characterization")
                self.assertTrue(verified["valid"])
                self.assertEqual(filtered["package_ids"], [package["package_id"]])
            finally:
                subprocess.run(["dropdb", "--if-exists", db], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def boundary_manifest(entries=None):
    entries = copy.deepcopy(entries or [manifest_entry()])
    manifest = {"manifest_id": "manifest-boundary-test-v1", "manifest_version": "1.0", "campaign_id": epp.CAMPAIGN_ID, "entries": entries, "candidate_order": [entry["candidate_id"] for entry in entries], "computational_budget": {"maximum_executed_candidates": 2, "maximum_raw_result_records": 56, "maximum_promoted_objects": 2, "stop_on_canary_failure": True}, "selection_rubric_fingerprint": "sha256:" + "4" * 64, "forbidden_outcome_fields": epp.FORBIDDEN_OUTCOME_FIELDS}
    manifest["manifest_fingerprint"] = epp.fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
    return manifest


def valid_authorization(manifest):
    return epp.build_production_authorization(manifest, epp.manifest_bytes_fingerprint(manifest), accounting=epp.expected_canary_accounting(manifest), reruns=[{"candidate_id": entry["candidate_id"], "matched": True, "first_fingerprint": "sha256:" + "5" * 64, "second_fingerprint": "sha256:" + "5" * 64} for entry in manifest["entries"] if entry.get("canary") and entry["disposition"] == "execute"], publication={"disposition": "isolated_canary_admitted", "admitted_object_count": 1, "object_count": 1, "repository_fingerprint": "sha256:" + "6" * 64})


def authorized_repository_state(gate):
    return {"object_count": gate["publication"]["object_count"], "repository_fingerprint": gate["publication"]["repository_fingerprint"]}


class ProductionBoundaryAuthorizationTests(unittest.TestCase):
    def test_valid_exactly_bound_authorization_succeeds(self):
        manifest = boundary_manifest(); gate = valid_authorization(manifest)
        self.assertTrue(epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest), authorized_repository_state(gate))["valid"])

    def test_repository_target_state_must_match_canary_admitted_state(self):
        manifest = boundary_manifest(); gate = valid_authorization(manifest)
        wrong = {"object_count": gate["publication"]["object_count"] + 1, "repository_fingerprint": "sha256:" + "9" * 64}
        with self.assertRaisesRegex(ValueError, "repository state"):
            epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest), wrong)

    def test_rerun_rows_require_exact_sha256_fingerprints(self):
        manifest = boundary_manifest()
        for mutation in ("missing", "malformed", "extra"):
            gate = valid_authorization(manifest)
            if mutation == "missing":
                gate["reruns"][0].pop("first_fingerprint"); gate["reruns"][0].pop("second_fingerprint")
            elif mutation == "malformed":
                gate["reruns"][0]["first_fingerprint"] = gate["reruns"][0]["second_fingerprint"] = "same"
            else:
                gate["reruns"][0]["unbound"] = True
            gate["gate_fingerprint"] = epp.authorization_fingerprint(gate)
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, "rerun"):
                epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest), authorized_repository_state(gate))

    def test_bare_passed_true_fails(self):
        with self.assertRaisesRegex(ValueError, "authorization"):
            epp.validate_production_authorization({"passed": True}, boundary_manifest(), "sha256:" + "0" * 64)

    def test_wrong_top_level_types_fail_cleanly(self):
        for value in [True, [], "yes", 1, None]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                epp.validate_production_authorization(value, boundary_manifest(), "sha256:" + "0" * 64)

    def test_passed_false_and_truthy_non_booleans_fail(self):
        manifest = boundary_manifest()
        for value in [False, "true", 1, [], {}, [1]]:
            gate = valid_authorization(manifest); gate["passed"] = value; gate["gate_fingerprint"] = epp.authorization_fingerprint(gate)
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "Boolean true"):
                epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest))

    def test_missing_or_wrong_schema_version_fails(self):
        manifest = boundary_manifest()
        for key, value in [("schema_name", None), ("schema_name", "wrong"), ("schema_version", None), ("schema_version", "2.0")]:
            gate = valid_authorization(manifest)
            if value is None: gate.pop(key)
            else: gate[key] = value
            gate["gate_fingerprint"] = epp.authorization_fingerprint(gate)
            with self.subTest(key=key, value=value), self.assertRaises(ValueError):
                epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest))

    def test_wrong_campaign_manifest_or_byte_fingerprint_fails(self):
        manifest = boundary_manifest()
        for key, value in [("campaign_id", "other"), ("manifest_id", "other"), ("manifest_fingerprint", "sha256:" + "0" * 64), ("execution_manifest_byte_fingerprint", "sha256:" + "0" * 64)]:
            gate = valid_authorization(manifest); gate[key] = value; gate["gate_fingerprint"] = epp.authorization_fingerprint(gate)
            with self.subTest(key=key), self.assertRaises(ValueError):
                epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest))

    def test_changed_candidate_population_or_limits_fails(self):
        manifest = boundary_manifest()
        for key in ["candidate_population", "production_limits"]:
            gate = valid_authorization(manifest); gate[key] = copy.deepcopy(gate[key])
            if isinstance(gate[key], list): gate[key][0]["candidate_id"] = "other"
            else: gate[key]["portfolio"]["maximum_executed_candidates"] = 99
            gate["gate_fingerprint"] = epp.authorization_fingerprint(gate)
            with self.subTest(key=key), self.assertRaises(ValueError):
                epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest))

    def test_tampered_mode_or_gate_fingerprint_fails(self):
        manifest = boundary_manifest(); gate = valid_authorization(manifest); gate["execution_mode"] = "production"; gate["gate_fingerprint"] = epp.authorization_fingerprint(gate)
        with self.assertRaisesRegex(ValueError, "canary"): epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest))
        gate = valid_authorization(manifest); gate["gate_fingerprint"] = "sha256:" + "0" * 64
        with self.assertRaisesRegex(ValueError, "fingerprint"): epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest))

    def test_blockers_rerun_or_accounting_failure_fails(self):
        manifest = boundary_manifest()
        mutations = [lambda g: g.update(blockers=["bad"]), lambda g: g["reruns"][0].update(matched=False), lambda g: g["accounting"].update(valid_candidates=0)]
        for mutate in mutations:
            gate = valid_authorization(manifest); mutate(gate); gate["gate_fingerprint"] = epp.authorization_fingerprint(gate)
            with self.assertRaises(ValueError): epp.validate_production_authorization(gate, manifest, epp.manifest_bytes_fingerprint(manifest))

    def test_invalid_authorization_fails_before_calculation_or_persistence(self):
        manifest = boundary_manifest()
        with tempfile.TemporaryDirectory() as td, mock.patch.object(epp, "_rerun_match", side_effect=AssertionError("calculation reached")), mock.patch.object(epp, "persist_packages", side_effect=AssertionError("persistence reached")):
            with self.assertRaises(ValueError): epp.run_portfolio(manifest, "production", Path(td) / "out", Path(td) / "repo", Path(td) / "missing", manifest_file_fingerprint=epp.manifest_bytes_fingerprint(manifest), project_root=Path(td))

    def test_repository_state_mismatch_fails_before_calculation_or_persistence(self):
        manifest = boundary_manifest(); gate = valid_authorization(manifest)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); gate_path = root / "gate.json"; repo = root / "repo"; repo.mkdir()
            epp.write_json(gate_path, gate); epp.write_json(repo / "manifest.json", {"object_count": 2, "repository_fingerprint": "sha256:" + "9" * 64})
            with mock.patch.object(epp, "_rerun_match", side_effect=AssertionError("calculation reached")), mock.patch.object(epp, "persist_packages", side_effect=AssertionError("persistence reached")):
                with self.assertRaisesRegex(ValueError, "repository state"):
                    epp.run_portfolio(manifest, "production", root / "out", repo, gate_path, manifest_file_fingerprint=epp.manifest_bytes_fingerprint(manifest), project_root=root)

    def test_repository_state_change_during_calculation_blocks_persistence(self):
        first_entry = manifest_entry(); second_entry = copy.deepcopy(first_entry); second_entry["candidate_id"] = "second"; second_entry["canary"] = False
        manifest = boundary_manifest([first_entry, second_entry]); gate = valid_authorization(manifest)
        result1 = epp.calculate_candidate(first_entry, synthetic_normalized()); result2 = copy.deepcopy(result1); result2["candidate_id"] = "second"
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); gate_path = root / "gate.json"; repo = root / "repo"; repo.mkdir(); epp.write_json(gate_path, gate)
            epp.write_json(repo / "manifest.json", authorized_repository_state(gate))
            calls = iter([(result1, copy.deepcopy(result1), True), (result2, copy.deepcopy(result2), True)])
            def mutate_then_return(*_args):
                value = next(calls)
                epp.write_json(repo / "manifest.json", {"object_count": 99, "repository_fingerprint": "sha256:" + "9" * 64})
                return value
            with mock.patch.object(epp, "_rerun_match", side_effect=mutate_then_return), mock.patch.object(epp, "persist_packages", side_effect=AssertionError("persistence reached")):
                with self.assertRaisesRegex(RuntimeError, "repository state changed"):
                    epp.run_portfolio(manifest, "production", root / "out", repo, gate_path, manifest_file_fingerprint=epp.manifest_bytes_fingerprint(manifest), project_root=root)


class ProductionBoundaryLimitTests(unittest.TestCase):
    def test_candidate_count_below_and_at_limit_succeeds(self):
        manifest = boundary_manifest(); self.assertIsNone(epp.enforce_preexecution_limits(manifest, manifest["entries"]))
        two = [manifest_entry(), {**manifest_entry(), "candidate_id": "second"}]; self.assertIsNone(epp.enforce_preexecution_limits(boundary_manifest(two), two))

    def test_candidate_count_above_limit_fails_before_calculation(self):
        entries = [{**manifest_entry(), "candidate_id": f"c{i}"} for i in range(3)]
        with self.assertRaisesRegex(ValueError, "executed candidate"): epp.enforce_preexecution_limits(boundary_manifest(entries), entries)

    def test_promotion_limit_above_maximum_fails(self):
        with self.assertRaisesRegex(ValueError, "promoted object"): epp.enforce_promotion_limit(boundary_manifest(), [{}, {}, {}])

    def test_aggregate_raw_result_excess_fails(self):
        with self.assertRaisesRegex(ValueError, "raw result"): epp.enforce_aggregate_result_limit(boundary_manifest(), [{"raw_result_count": 57}])

    def test_per_entry_result_excess_fails(self):
        with self.assertRaisesRegex(ValueError, "candidate result"): epp.enforce_candidate_result_limits(manifest_entry(), {"raw_result_count": 29, "valid_result_count": 29}, 0.1)

    def test_wall_time_excess_blocks_admission_without_cancellation_claim(self):
        with self.assertRaisesRegex(ValueError, "wall time exceeded after calculation"): epp.enforce_candidate_result_limits(manifest_entry(), {"raw_result_count": 28, "valid_result_count": 28}, 5.01)

    def test_stop_on_canary_failure_must_be_literal_true(self):
        manifest = boundary_manifest(); manifest["computational_budget"]["stop_on_canary_failure"] = 1; manifest["manifest_fingerprint"] = epp.fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
        with self.assertRaisesRegex(ValueError, "stop_on_canary_failure"): epp.validate_manifest(manifest)

    def test_entry_canary_flag_must_be_literal_boolean(self):
        for value in ("false", 1, [], {}):
            manifest = boundary_manifest(); manifest["entries"][0]["canary"] = value; manifest["manifest_fingerprint"] = epp.fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "canary"):
                epp.validate_manifest(manifest)


class ManifestContainmentTests(unittest.TestCase):
    def test_valid_contained_relative_file_succeeds(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); p = root / "inside.json"; p.write_text("{}")
            self.assertEqual(epp.resolve_manifest_input(root, "inside.json"), p.resolve())

    def test_absolute_parent_normalized_and_symlink_escape_fail_before_hash(self):
        with tempfile.TemporaryDirectory() as td, tempfile.TemporaryDirectory() as outside_td:
            root = Path(td); outside = Path(outside_td) / "outside.json"; outside.write_text('{"secret": true}'); (root / "nested").mkdir(); (root / "escape.json").symlink_to(outside)
            with mock.patch.object(epp, "file_fingerprint", side_effect=AssertionError("external bytes hashed")):
                for probe in [str(outside), "../outside.json", "nested/../../outside.json", "escape.json"]:
                    with self.subTest(probe=probe), self.assertRaises(ValueError): epp.resolve_and_fingerprint_manifest_input(root, probe)

    def test_missing_and_directory_fail_controlled(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); (root / "directory").mkdir()
            for probe in ["missing.json", "directory"]:
                with self.subTest(probe=probe), self.assertRaises(ValueError): epp.resolve_manifest_input(root, probe)

    def test_existing_valid_repository_relative_manifest_paths_remain_supported(self):
        _, manifest = epp.build_preregistration()
        for entry in manifest["entries"]: self.assertTrue(epp.resolve_manifest_input(ROOT, entry["input"]["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
