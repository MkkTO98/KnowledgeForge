from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_helper():
    spec = importlib.util.spec_from_file_location(
        "coefficient_free_pearson_candidate_registry",
        ROOT / "tools/coefficient_free_pearson_candidate_registry.py",
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class CoefficientFreePearsonCandidateRegistryTest(unittest.TestCase):
    def setUp(self) -> None:
        self.helper = load_helper()
        self.outputs = self.helper.build_outputs()

    def test_builds_six_to_eight_valid_candidates_from_retained_evidence(self):
        validation = self.outputs["validation"]
        self.assertTrue(validation["valid"], validation.get("errors"))
        self.assertEqual(validation["candidate_count"], 8)
        self.assertEqual(len(validation["expected_package_ids"]), 8)
        self.assertEqual(len(set(validation["expected_package_ids"])), 8)

    def test_registry_and_selection_evidence_are_coefficient_free(self):
        registry = self.outputs["registry"]
        spec = self.outputs["spec"]
        self.assertFalse(self.helper.has_forbidden_key(registry))
        self.assertFalse(self.helper.has_forbidden_key(spec["selection_evidence"]))
        for record in registry["records"]:
            self.assertFalse(self.helper.has_forbidden_key(record))
            self.assertFalse(record["contains_pearson_coefficient"])
        self.assertTrue(registry["coefficient_free_proof"]["no_campaign41_coefficient_calculated"])

    def test_excludes_prior_relationships_and_self_pairs(self):
        candidates = self.outputs["spec"]["candidates"]
        keys = set()
        for c in candidates:
            a = c["series_a"]["identity"]["code"]
            b = c["series_b"]["identity"]["code"]
            self.assertNotEqual(a, b)
            key = self.helper.canonical_pair_key(c["entity"], a, b)
            self.assertNotIn(key, self.helper.EXCLUDED_PRIOR_PAIRS)
            self.assertNotIn(key, keys)
            keys.add(key)

    def test_deterministic_regeneration_identity(self):
        first = self.helper.build_outputs()
        second = self.helper.build_outputs()
        self.assertEqual(first["registry"]["registry_fingerprint"], second["registry"]["registry_fingerprint"])
        self.assertEqual(first["spec"]["batch_spec_fingerprint"], second["spec"]["batch_spec_fingerprint"])
        self.assertEqual(first["spec"], second["spec"])

    def test_writes_registry_and_spec_without_result_fields(self):
        with tempfile.TemporaryDirectory() as td:
            report = Path(td) / "report"
            spec_path = Path(td) / "campaign41.json"
            outputs = self.helper.build_outputs(report_root=report, spec_path=spec_path)
            written = self.helper.write_outputs(outputs, report, spec_path)
            self.assertTrue(Path(written["registry_path"]).exists() or (ROOT / written["registry_path"]).exists())
            self.assertTrue(Path(written["spec_path"]).exists() or (ROOT / written["spec_path"]).exists())
            self.assertTrue(written["valid"])

    def test_detects_engine_hardcoding_status(self):
        assessment = self.helper.detect_campaign40_engine_hardcoding()
        self.assertFalse(assessment["campaign40_hardcoded_package_internals_found"])
        self.assertEqual(assessment["calculation_gate_decision"], "existing engine sufficient for calculation")

    def test_successor_policy_historical_comparison_is_valid_and_coefficient_free(self):
        comparison = self.helper.build_successor_policy_historical_comparison()
        self.assertTrue(comparison["validation"]["valid"], comparison["validation"].get("errors"))
        self.assertEqual(comparison["mode"], "historical_comparison")
        self.assertTrue(comparison["dry_run_only"])
        self.assertTrue(comparison["not_campaign42_registry"])
        self.assertFalse(comparison["valid_future_production_evidence"])
        self.assertGreaterEqual(comparison["selected_candidate_count"], 6)
        self.assertFalse(self.helper.has_forbidden_key(comparison))
        self.assertEqual(comparison["semantic_proximity_distribution"].get("remote", 0), 2)
        self.assertGreaterEqual(comparison["semantic_proximity_distribution"].get("close", 0), 3)
        proof = comparison["coefficient_free_proof"]
        self.assertFalse(proof["candidate_pair_pearson_used"])
        self.assertFalse(proof["candidate_pair_first_difference_used"])
        self.assertFalse(proof["covariance_used"])
        self.assertFalse(proof["preliminary_result_cache_used"])

    def test_successor_policy_future_production_excludes_current_canonical_pearson_pairs(self):
        future = self.helper.build_successor_policy_future_production_dry_run()
        self.assertEqual(future["mode"], "future_production")
        self.assertTrue(future["valid_future_production_evidence"])
        canonical_keys = self.helper.load_current_canonical_pearson_relationship_keys()
        selected_keys = {
            self.helper.canonical_pair_key(
                c["entity"],
                c["series_a"]["identity"]["code"],
                c["series_b"]["identity"]["code"],
            )
            for c in future["selected_candidates"]
        }
        self.assertTrue(canonical_keys)
        self.assertTrue(selected_keys.isdisjoint(canonical_keys), selected_keys & canonical_keys)

    def test_successor_policy_future_production_excludes_reversed_canonical_pairs(self):
        canonical_keys = self.helper.load_current_canonical_pearson_relationship_keys()
        for entity, a, b in canonical_keys:
            self.assertIn(self.helper.canonical_pair_key(entity, b, a), canonical_keys)

    def test_comparison_mode_cannot_be_mistaken_for_future_production_mode(self):
        comparison = self.helper.build_successor_policy_historical_comparison()
        future = self.helper.build_successor_policy_future_production_dry_run()
        self.assertEqual(comparison["mode"], "historical_comparison")
        self.assertFalse(comparison["valid_future_production_evidence"])
        self.assertIn("historical/audit ranking only", comparison["mode_boundary"])
        self.assertEqual(future["mode"], "future_production")
        self.assertTrue(future["valid_future_production_evidence"])

    def test_successor_policy_preserves_campaign41_fingerprints(self):
        outputs = self.helper.build_outputs()
        self.assertEqual(
            outputs["registry"]["registry_fingerprint"],
            "sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc",
        )
        self.assertEqual(
            outputs["spec"]["batch_spec_fingerprint"],
            "sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2",
        )

    def test_successor_policy_candidate_metadata_contract(self):
        dry_run = self.helper.build_successor_policy_dry_run()
        valid_semantic = {"close", "moderate", "remote", "unresolved"}
        valid_risk = {"low", "moderate", "high", "unknown"}
        valid_purpose = {
            "positive_descriptive_knowledge",
            "baseline_relationship_knowledge",
            "cautionary_relationship_knowledge",
            "transformation_companion_candidate",
            "methodological_pressure_test_candidate",
        }
        for candidate in dry_run["selected_candidates"]:
            meta = candidate["successor_policy_metadata"]
            self.assertIn(meta["semantic_proximity"]["classification"], valid_semantic)
            self.assertIn(meta["time_risk"]["category"], valid_risk)
            self.assertIn(meta["candidate_utility_statement"]["purpose_classification"], valid_purpose)
            self.assertEqual(meta["candidate_utility_statement"]["coefficient_prediction"], "none; result-independent statement")
            self.assertTrue(meta["time_risk"]["permitted_inputs_only"])

    def test_successor_policy_rejects_hidden_outcome_fields(self):
        dry_run = self.helper.build_successor_policy_dry_run()
        polluted = json.loads(json.dumps(dry_run))
        polluted["selected_candidates"][0]["selection_evidence"]["pearson_coefficient"] = "0.99"
        self.assertTrue(self.helper.has_forbidden_key(polluted))

    def test_remote_cap_count_never_exceeds_declared_share(self):
        expectations = {
            1: 0,
            2: 0,
            3: 0,
            4: 1,
            5: 1,
            6: 1,
            7: 1,
            8: 2,
            9: 2,
            10: 2,
            11: 2,
            12: 3,
        }
        for batch_size, expected in expectations.items():
            with self.subTest(batch_size=batch_size):
                self.assertEqual(self.helper.remote_cap_count(batch_size, "0.25"), expected)
                self.assertLessEqual(expected, batch_size * 0.25)

    def test_future_production_remote_share_does_not_exceed_declared_cap(self):
        future = self.helper.build_successor_policy_future_production_dry_run()
        remote = future["semantic_proximity_distribution"].get("remote", 0)
        selected = future["selected_candidate_count"]
        self.assertLessEqual(remote, self.helper.remote_cap_count(selected, "0.25"))
        self.assertLessEqual(future["remote_share"], 0.25)

    def test_candidate_funnel_reduces_representative_population_before_escalation(self):
        outputs = self.helper.build_candidate_funnel_pilot()
        report = outputs["funnel_report"]
        self.assertTrue(report["validation"]["valid"], report["validation"]["errors"])
        self.assertEqual(report["source_candidate_count"], 40)
        self.assertEqual(report["disposition_counts"], {
            "deprioritized": 6,
            "excluded": 30,
            "selected": 4,
            "unresolved": 0,
        })
        self.assertEqual(len(report["candidate_classifications"]), 40)
        self.assertEqual(report["funnel_stage_counts"]["total_inventory"], 40)
        self.assertEqual(report["funnel_stage_counts"]["mechanically_excluded_count"], 30)
        self.assertEqual(report["funnel_stage_counts"]["mechanically_eligible_count"], 10)
        self.assertEqual(
            report["funnel_stage_counts"]["deterministic_semantic_classifications_by_class"],
            {"close": 4, "remote": 6},
        )
        self.assertEqual(report["funnel_stage_counts"]["unresolved_manual_review_count"], 0)
        self.assertEqual(report["funnel_stage_counts"]["escalation_inclusion_count"], 0)
        self.assertEqual(
            report["funnel_stage_counts"]["mechanical_exclusions_by_reason"],
            {
                "current_canonical_relationship": 14,
                "mechanical_exclusion": 3,
                "minimum_aligned_coverage": 16,
                "minimum_aligned_pairs": 16,
                "prior_relationship": 2,
            },
        )
        self.assertEqual(outputs["unresolved_escalation_package"]["packages"], [])
        self.assertEqual(outputs["run_evidence"]["human_review_candidate_count"], 0)
        self.assertEqual(outputs["run_evidence"]["deterministically_resolved_candidate_count"], 40)

    def test_candidate_funnel_is_deterministic_and_preserves_frozen_outputs(self):
        first = self.helper.build_candidate_funnel_pilot()
        second = self.helper.build_candidate_funnel_pilot()
        self.assertEqual(first, second)
        self.assertEqual(
            first["funnel_report"]["report_fingerprint"],
            second["funnel_report"]["report_fingerprint"],
        )
        outputs = self.helper.build_outputs()
        self.assertEqual(outputs["registry"]["registry_fingerprint"], "sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc")
        self.assertEqual(outputs["spec"]["batch_spec_fingerprint"], "sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2")

    def test_governed_outputs_ignore_differing_elapsed_observations(self):
        first = self.helper.build_candidate_funnel_pilot(
            self.helper.DEFAULT_FIXTURE_ROOT,
            "0.001",
        )
        second = self.helper.build_candidate_funnel_pilot(
            self.helper.DEFAULT_FIXTURE_ROOT,
            "9.999",
        )
        self.assertEqual(first, second)
        self.assertEqual(
            first["run_evidence"]["run_fingerprint"],
            second["run_evidence"]["run_fingerprint"],
        )
        self.assertNotIn("elapsed_time", first["run_evidence"])

    def test_run_evidence_uses_portable_root_relative_output_identities(self):
        outputs = self.helper.build_candidate_funnel_pilot(
            self.helper.DEFAULT_FIXTURE_ROOT,
            "0.001",
        )
        with tempfile.TemporaryDirectory() as first_td, tempfile.TemporaryDirectory() as second_td:
            first_root = Path(first_td) / "authorized-a"
            second_root = Path(second_td) / "authorized-b"
            first_root.mkdir()
            second_root.mkdir()
            self.helper.write_candidate_funnel_outputs(outputs, first_root, authorized_root=first_root)
            self.helper.write_candidate_funnel_outputs(outputs, second_root, authorized_root=second_root)
            self.assertEqual(
                (first_root / "run_evidence.json").read_bytes(),
                (second_root / "run_evidence.json").read_bytes(),
            )
        identities = outputs["run_evidence"]["output_artifact_identities"]
        self.assertEqual(
            {name: identity["path"] for name, identity in identities.items()},
            {
                "funnel_report": "funnel_report.json",
                "unresolved_escalation_package": "unresolved_escalation_package.json",
            },
        )
        for identity in identities.values():
            self.assertFalse(Path(identity["path"]).is_absolute())
            self.assertNotIn(str(self.helper.CANDIDATE_FUNNEL_REPORT_ROOT), identity["path"])

    def test_direct_report_validator_returns_stable_invalid_result_for_malformed_containers(self):
        valid = self.helper.build_candidate_funnel_pilot()["funnel_report"]
        malformed_reports = []
        changed = json.loads(json.dumps(valid)); changed["source_candidate_ids"] = None; malformed_reports.append(changed)
        changed = json.loads(json.dumps(valid)); changed["candidate_classifications"] = None; malformed_reports.append(changed)
        changed = json.loads(json.dumps(valid)); changed["disposition_counts"] = []; malformed_reports.append(changed)
        changed = json.loads(json.dumps(valid)); changed["funnel_stage_counts"] = []; malformed_reports.append(changed)
        changed = json.loads(json.dumps(valid)); changed["candidate_classifications"][0]["candidate_key"] = [{}]; malformed_reports.append(changed)
        expected = {"valid": False, "errors": ["malformed candidate funnel report"]}
        for report in malformed_reports:
            with self.subTest(mutated_fields=sorted(report)):
                self.assertEqual(self.helper.validate_candidate_funnel_report(report), expected)

    def test_unresolved_candidate_emits_compact_minimum_sufficient_escalation(self):
        proposals, _ = self.helper.enumerate_proposals(self.helper.load_series_pool())
        original = next(c for c in proposals if c["candidate_id"] == "dnk_forest_area_private_credit")
        index = self.helper._authenticated_series_index()
        a = index[original["series_a"]["evidence_identity"]["normalized_path"]]
        b = index[original["series_b"]["evidence_identity"]["normalized_path"]]
        a = self.helper.replace(a, definition="")
        candidate = self.helper.build_candidate(a, b)
        classification = self.helper._classify_verified_candidate_for_funnel(
            candidate, a, b, canonical_relationship_index={}
        )
        self.assertEqual(classification["disposition"], "unresolved")
        package = self.helper.build_unresolved_escalation_package(classification)
        self.assertIsNotNone(package)
        self.assertEqual(package["profile"], "knowledgeforge.candidate_funnel_unresolved.v1@1.0")
        self.assertEqual(set(package), {
            "candidate_id", "candidate_key", "contradiction_context", "escalation_id",
            "input_fingerprint", "profile", "provenance", "qualification",
            "recovery", "statistical_context", "unresolved",
        })
        self.assertTrue(package["provenance"]["method_contract_fingerprint"].startswith("sha256:"))
        self.assertEqual(package["candidate_id"], candidate["candidate_id"])
        self.assertEqual(package["candidate_key"], [candidate["entity"], candidate["series_a"]["identity"]["code"], candidate["series_b"]["identity"]["code"]])
        self.assertEqual(package["provenance"]["expected_package_id"], candidate["expected_package_id"])
        self.assertEqual(self.helper._evidence_reference_errors(candidate), [])
        for series in package["provenance"]["series"]:
            for name in ("normalized", "raw_fixture", "validation", "selection_contract", "acquisition_manifest"):
                self.assertTrue(series[f"{name}_path"])
                self.assertTrue(series[f"{name}_fingerprint"].startswith("sha256:"))
        self.assertTrue(package["qualification"]["passed"])
        self.assertIn("construction_limitations", package["contradiction_context"])
        self.assertIn("pair_time_risk", package["statistical_context"])
        self.assertEqual(package["recovery"]["resume_stage"], "semantic_classification")
        self.assertFalse(self.helper.has_forbidden_key(package))
        self.assertLess(len(self.helper.canonical_json(package).encode()), len(self.helper.canonical_json(candidate).encode()))
        self.assertLess(self.helper.scalar_leaf_count(package), self.helper.scalar_leaf_count(candidate))

    def test_escalation_is_unresolved_only_and_recovery_resolves_after_metadata_restore(self):
        proposals, _ = self.helper.enumerate_proposals(self.helper.load_series_pool())
        original = next(c for c in proposals if c["candidate_id"] == "dnk_forest_area_private_credit")
        index = self.helper._authenticated_series_index()
        a = index[original["series_a"]["evidence_identity"]["normalized_path"]]
        b = index[original["series_b"]["evidence_identity"]["normalized_path"]]
        unresolved_a = self.helper.replace(a, definition="")
        unresolved_candidate = self.helper.build_candidate(unresolved_a, b)
        first = self.helper._classify_verified_candidate_for_funnel(
            unresolved_candidate, unresolved_a, b, canonical_relationship_index={}
        )
        restored = self.helper.classify_candidate_for_funnel(
            original, canonical_relationship_index={}, authenticated_series_index=index
        )
        self.assertEqual(first["disposition"], "unresolved")
        self.assertIsNotNone(self.helper.build_unresolved_escalation_package(first))
        self.assertEqual(restored["disposition"], "eligible")
        self.assertEqual(restored["semantic_classification"]["classification"], "remote")
        self.assertIsNone(self.helper.build_unresolved_escalation_package(restored))

    def test_result_contamination_and_stale_or_missing_references_fail_closed(self):
        proposals, _ = self.helper.enumerate_proposals(self.helper.load_series_pool())
        for derived_key in (
            "pearson_coefficient", "correlation_coefficient", "lag_result", "effect_size",
            "preliminary_result_cache", "generated_statements", "p_values", "regressions", "lags",
            "effect_sizes", "candidate_pair_coefficient", "result_derived_statement", "p-value", "pvalue",
            "pearson-r", "pearson_r_value", "correlation_result", "lag_estimate", "regression_result",
            "generated_relationships",
        ):
            candidate = json.loads(json.dumps(proposals[0]))
            candidate["selection_evidence"][derived_key] = "must not enter"
            polluted = self.helper.classify_candidate_for_funnel(candidate, canonical_relationship_index={})
            self.assertEqual(polluted["disposition"], "invalid")
            self.assertIn("result_derived_input", polluted["reason_codes"])
            self.assertIsNone(self.helper.build_unresolved_escalation_package(polluted))

        candidate = json.loads(json.dumps(proposals[0]))
        candidate["series_a"]["evidence_identity"]["raw_fixture_fingerprint"] = "sha256:" + "0" * 64
        stale = self.helper.classify_candidate_for_funnel(candidate, canonical_relationship_index={})
        self.assertEqual(stale["disposition"], "invalid")
        self.assertIn("stale_evidence_reference", stale["reason_codes"])

        candidate = json.loads(json.dumps(proposals[0]))
        candidate["series_a"]["evidence_identity"]["raw_fixture_path"] = "artifacts/evidence-fixtures/absent.json"
        missing = self.helper.classify_candidate_for_funnel(candidate, canonical_relationship_index={})
        self.assertEqual(missing["disposition"], "invalid")
        self.assertIn("missing_evidence_reference", missing["reason_codes"])

    def test_normalized_payload_tampering_and_malformed_canonical_identity_fail_closed(self):
        fixture_root = self.helper.PROJECT_ROOT / self.helper.DEFAULT_FIXTURE_ROOT
        normalized = next(iter(sorted(fixture_root.rglob("normalized_observations.json"))))
        with tempfile.TemporaryDirectory() as td:
            copied_root = Path(td) / "fixture"
            shutil.copytree(normalized.parent, copied_root / normalized.parent.name)
            copied_normalized = copied_root / normalized.parent.name / "normalized_observations.json"
            payload = json.loads(copied_normalized.read_text())
            payload["observations"][0]["value"] = "tampered"
            copied_normalized.write_text(json.dumps(payload, sort_keys=True))
            with self.assertRaisesRegex(ValueError, "normalized evidence fingerprint mismatch"):
                self.helper.load_authenticated_series_pool(copied_root)

        with tempfile.TemporaryDirectory() as td:
            package = {
                "status": "accepted",
                "generated_statements": [{
                    "statement_type": "derived_relationship",
                    "structured_payload": {"method_contract_fingerprint": self.helper.METHOD_CONTRACT_FINGERPRINT},
                }],
            }
            (Path(td) / "malformed.json").write_text(json.dumps(package))
            with self.assertRaisesRegex(ValueError, "malformed accepted Pearson relationship identity"):
                self.helper.load_current_canonical_pearson_relationship_index(Path(td))

        with tempfile.TemporaryDirectory() as td:
            valid_statement = {
                "statement_type": "derived_relationship",
                "applicability": {"frequency": "annual"},
                "structured_payload": {
                    "method_contract_fingerprint": self.helper.METHOD_CONTRACT_FINGERPRINT,
                    "entity_id": "DNK",
                    "series_a": {"code": "A", "transformation": "raw"},
                    "series_b": {"code": "B", "transformation": "raw"},
                },
            }
            malformed_statement = json.loads(json.dumps(valid_statement))
            del malformed_statement["structured_payload"]["entity_id"]
            package = {
                "status": "accepted",
                "generated_statements": [valid_statement, malformed_statement],
            }
            (Path(td) / "mixed.json").write_text(json.dumps(package))
            with self.assertRaisesRegex(ValueError, "malformed accepted Pearson relationship identity"):
                self.helper.load_current_canonical_pearson_relationship_index(Path(td))

        malformed_variants = [
            ({"statement_type": "derived_relationship", "structured_payload": "malformed"}, "malformed accepted relationship statement"),
            ({"structured_payload": dict(valid_statement["structured_payload"])}, "malformed accepted Pearson relationship statement"),
        ]
        for malformed_statement, expected_error in malformed_variants:
            with self.subTest(expected_error=expected_error), tempfile.TemporaryDirectory() as td:
                package = {
                    "status": "accepted",
                    "generated_statements": [valid_statement, malformed_statement],
                }
                (Path(td) / "mixed.json").write_text(json.dumps(package))
                with self.assertRaisesRegex(ValueError, expected_error):
                    self.helper.load_current_canonical_pearson_relationship_index(Path(td))

    def test_canonical_collision_retains_relationship_identity(self):
        index = self.helper.load_current_canonical_pearson_relationship_index()
        key = next(iter(sorted(index)))
        entity, code_a, code_b = key
        pool = {(s.entity, s.code): s for s in self.helper.load_series_pool()}
        candidate = self.helper.build_candidate(pool[(entity, code_a)], pool[(entity, code_b)])
        classification = self.helper.classify_candidate_for_funnel(candidate, canonical_relationship_index=index)
        self.assertEqual(classification["disposition"], "excluded")
        self.assertIn("current_canonical_relationship", classification["reason_codes"])
        self.assertEqual(classification["contradiction_context"]["canonical_package_ids"], index[key])

    def test_independent_n_plus_one_population_mutation_fails_closed(self):
        outputs = self.helper.build_candidate_funnel_pilot()
        report = json.loads(json.dumps(outputs["funnel_report"]))
        report["candidate_classifications"].append(
            json.loads(json.dumps(report["candidate_classifications"][0]))
        )
        validation = self.helper.validate_candidate_funnel_report(report)
        self.assertFalse(validation["valid"])
        self.assertIn("candidate population does not exactly match declared source identities", validation["errors"])

    def test_duplicate_relationship_and_population_fingerprint_mutations_fail_closed(self):
        outputs = self.helper.build_candidate_funnel_pilot()
        duplicate = json.loads(json.dumps(outputs["funnel_report"]))
        extra = json.loads(json.dumps(duplicate["candidate_classifications"][0]))
        extra["candidate_id"] = "distinct-id-same-relationship"
        duplicate["candidate_classifications"].append(extra)
        duplicate["source_candidate_ids"].append(extra["candidate_id"])
        duplicate["source_candidate_count"] += 1
        duplicate["disposition_counts"][extra["disposition"]] += 1
        validation = self.helper.validate_candidate_funnel_report(duplicate)
        self.assertFalse(validation["valid"])
        self.assertIn("duplicate canonical candidate relationship identity", validation["errors"])

        fingerprint = json.loads(json.dumps(outputs["funnel_report"]))
        fingerprint["source_population_fingerprint"] = "sha256:" + "0" * 64
        fingerprint["report_fingerprint"] = self.helper.sha256_value({
            key: value for key, value in fingerprint.items()
            if key not in {"report_fingerprint", "validation"}
        })
        validation = self.helper.validate_candidate_funnel_report(fingerprint)
        self.assertFalse(validation["valid"])
        self.assertIn("source population fingerprint mismatch", validation["errors"])

    def test_deterministic_dispositions_and_unresolved_membership_are_reconstructed(self):
        outputs = self.helper.build_candidate_funnel_pilot()
        report = json.loads(json.dumps(outputs["funnel_report"]))
        selected = next(item for item in report["candidate_classifications"] if item["disposition"] == "selected")
        selected["disposition"] = "deprioritized"
        selected["reason_codes"] = ["fabricated_reason"]
        report["disposition_counts"]["selected"] -= 1
        report["disposition_counts"]["deprioritized"] += 1
        report["report_fingerprint"] = self.helper.sha256_value({
            key: value for key, value in report.items()
            if key not in {"report_fingerprint", "validation"}
        })
        validation = self.helper.validate_candidate_funnel_report(report)
        self.assertFalse(validation["valid"])
        self.assertIn(
            "candidate classifications do not match deterministic authenticated reconstruction",
            validation["errors"],
        )

        unresolved = json.loads(json.dumps(outputs["funnel_report"]))
        selected = next(item for item in unresolved["candidate_classifications"] if item["disposition"] == "selected")
        selected["disposition"] = "unresolved"
        selected["reason_codes"] = ["fabricated_uncertainty"]
        unresolved["disposition_counts"]["selected"] -= 1
        unresolved["disposition_counts"]["unresolved"] += 1
        unresolved["funnel_stage_counts"]["unresolved_manual_review_count"] += 1
        unresolved["funnel_stage_counts"]["escalation_inclusion_count"] += 1
        unresolved["report_fingerprint"] = self.helper.sha256_value({
            key: value for key, value in unresolved.items()
            if key not in {"report_fingerprint", "validation"}
        })
        validation = self.helper.validate_candidate_funnel_report(unresolved)
        self.assertFalse(validation["valid"])
        self.assertIn(
            "candidate classifications do not match deterministic authenticated reconstruction",
            validation["errors"],
        )

        fabricated_outputs = json.loads(json.dumps(outputs))
        escalation = fabricated_outputs["unresolved_escalation_package"]
        escalation["packages"] = [{
            "profile": self.helper.UNRESOLVED_ESCALATION_PROFILE,
            "fabricated": "missing identity, provenance, qualification, contradiction, statistical, and recovery context",
        }]
        escalation["package_count"] = 1
        escalation["collection_fingerprint"] = self.helper.sha256_value({
            key: value for key, value in escalation.items() if key != "collection_fingerprint"
        })
        validation = self.helper.validate_candidate_funnel_outputs(fabricated_outputs, require_elapsed=False)
        self.assertFalse(validation["valid"])
        self.assertIn(
            "escalation packages do not match deterministic unresolved reconstruction",
            validation["errors"],
        )

    def test_candidate_identity_and_qualification_are_bound_to_authenticated_evidence(self):
        proposals, _ = self.helper.enumerate_proposals(self.helper.load_series_pool())
        original = proposals[0]
        mutations = []
        changed = json.loads(json.dumps(original)); changed["candidate_id"] = "spoofed"; mutations.append(changed)
        changed = json.loads(json.dumps(original)); changed["series_a"]["identity"]["code"] = "SP.DYN.LE00.IN"; mutations.append(changed)
        changed = json.loads(json.dumps(original)); changed["selection_evidence"]["coverage_probe"]["expected_aligned_pairs"] = 999; mutations.append(changed)
        changed = json.loads(json.dumps(original)); changed["thresholds"]["min_aligned_pairs"] = 0; mutations.append(changed)
        changed = json.loads(json.dumps(original)); changed["unexpected_input"] = "not allowlisted"; mutations.append(changed)
        for candidate in mutations:
            classification = self.helper.classify_candidate_for_funnel(candidate, canonical_relationship_index={})
            self.assertEqual(classification["disposition"], "invalid")
            self.assertIn("candidate_contract_mismatch", classification["reason_codes"])

    def test_report_and_run_execution_claims_are_deterministically_bound(self):
        outputs = self.helper.build_candidate_funnel_pilot(
            self.helper.DEFAULT_FIXTURE_ROOT,
            "0.001",
        )
        for key, value in (
            ("frontier_calls", 7),
            ("local_model_calls", 9),
            ("candidate_pair_results_used", True),
            ("dry_run_only", False),
            ("mode", "production"),
        ):
            report = json.loads(json.dumps(outputs["funnel_report"]))
            report[key] = value
            report["report_fingerprint"] = self.helper.sha256_value({
                name: item for name, item in report.items()
                if name not in {"report_fingerprint", "validation"}
            })
            validation = self.helper.validate_candidate_funnel_report(report)
            self.assertFalse(validation["valid"])
            self.assertIn("candidate funnel execution boundary mismatch", validation["errors"])

        report = json.loads(json.dumps(outputs["funnel_report"]))
        report["unexpected_claim"] = True
        report["report_fingerprint"] = self.helper.sha256_value({
            name: item for name, item in report.items()
            if name not in {"report_fingerprint", "validation"}
        })
        self.assertIn(
            "unexpected candidate funnel report schema",
            self.helper.validate_candidate_funnel_report(report)["errors"],
        )

        self.assertNotIn("elapsed_time", outputs["run_evidence"])
        mutations = []
        changed = json.loads(json.dumps(outputs)); changed["run_evidence"]["workflow_identity"] = "forged"; mutations.append(changed)
        changed = json.loads(json.dumps(outputs)); changed["run_evidence"]["source_candidate_count"] = 999; mutations.append(changed)
        changed = json.loads(json.dumps(outputs)); changed["run_evidence"]["human_review_candidate_count"] = 999; mutations.append(changed)
        changed = json.loads(json.dumps(outputs)); changed["run_evidence"]["post_change_funnel_report_canonical_json_bytes"] = 1; mutations.append(changed)
        changed = json.loads(json.dumps(outputs)); changed["run_evidence"]["input_artifact_identities"]["canonical_relationship_index_fingerprint"] = "sha256:" + "0" * 64; mutations.append(changed)
        changed = json.loads(json.dumps(outputs)); changed["run_evidence"]["output_artifact_identities"]["funnel_report"]["fingerprint"] = "sha256:" + "0" * 64; mutations.append(changed)
        changed = json.loads(json.dumps(outputs)); changed["run_evidence"]["candidate_pair_pearson_r"] = "0.999"; mutations.append(changed)
        for changed in mutations:
            run = changed["run_evidence"]
            run["run_fingerprint"] = self.helper.sha256_value({
                name: item for name, item in run.items() if name != "run_fingerprint"
            })
            validation = self.helper.validate_candidate_funnel_outputs(changed)
            self.assertFalse(validation["valid"])
            self.assertTrue(
                {"run evidence does not match deterministic reconstruction"}
                & set(validation["errors"])
            )

    def test_candidate_funnel_writer_mutates_only_declared_outputs(self):
        outputs = self.helper.build_candidate_funnel_pilot(
            self.helper.DEFAULT_FIXTURE_ROOT,
            "0.001",
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            written = self.helper.write_candidate_funnel_outputs(outputs, root, authorized_root=root)
            self.assertEqual(set(written), {"funnel_report", "run_evidence", "unresolved_escalation_package"})
            self.assertEqual(
                sorted(str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()),
                ["funnel_report.json", "run_evidence.json", "unresolved_escalation_package.json"],
            )
            for path in written.values():
                self.assertTrue(Path(path).is_file())
            mutated = json.loads(json.dumps(outputs))
            mutated["run_evidence"]["report_fingerprint"] = "sha256:" + "0" * 64
            self.assertFalse(self.helper.validate_candidate_funnel_outputs(mutated)["valid"])
            with self.assertRaisesRegex(ValueError, "escapes authorized report boundary"):
                self.helper.write_candidate_funnel_outputs(outputs, root / ".." / "escaped", authorized_root=root)


if __name__ == "__main__":
    unittest.main()
