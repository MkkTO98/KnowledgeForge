from __future__ import annotations

import copy
import importlib
import json
import sys
import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import evidence_portfolio_production as production
admission = importlib.import_module("evidence_portfolio_admission_attempt")


def fixture(mode: str = "canary") -> dict:
    _, manifest = production.build_preregistration()
    selected = [entry for entry in manifest["entries"] if mode == "production" or entry.get("canary") is True]
    outcomes = [production.execute_entry(entry, ROOT) for entry in selected]
    reruns = []
    packages = []
    views = []
    for entry, outcome in zip(selected, outcomes):
        if entry["disposition"] != "execute":
            continue
        reruns.append({
            "candidate_id": entry["candidate_id"],
            "matched": True,
            "first_fingerprint": production.fingerprint(outcome),
            "second_fingerprint": production.fingerprint(outcome),
        })
        if outcome["disposition"] == "valid":
            package = production.build_knowledge_object(entry, outcome, manifest["manifest_fingerprint"])
            packages.append(package)
            views.extend(production.render_operational_views(entry, outcome))
    return {
        "manifest": manifest,
        "manifest_byte_fingerprint": production.manifest_bytes_fingerprint(manifest),
        "manifest_identity_kind": "canonical_in_memory_bytes",
        "mode": mode,
        "outcomes": outcomes,
        "reruns": reruns,
        "blockers": [],
        "packages": packages,
        "views": views,
    }


def build(values: dict, profile_id: str | None = None) -> dict:
    return admission.build_admission_attempt(
        manifest=values["manifest"],
        manifest_byte_fingerprint=values["manifest_byte_fingerprint"],
        manifest_identity_kind=values["manifest_identity_kind"],
        mode=values["mode"],
        outcomes=values["outcomes"],
        reruns=values["reruns"],
        blockers=values["blockers"],
        packages=values["packages"],
        views=values["views"],
        profile_id=admission.PROFILE_ID if profile_id is None else profile_id,
    )


def owner_identity_context(values: dict) -> tuple[dict[str, str], dict[str, list[str]], dict[str, str]]:
    selected = [
        entry for entry in values["manifest"]["entries"]
        if (values["mode"] == "production" or entry.get("canary") is True)
        and entry["disposition"] == "execute"
    ]
    outcome_by_id = {outcome["candidate_id"]: outcome for outcome in values["outcomes"]}
    package_ids = {entry["candidate_id"]: production.stable_object_id(entry) for entry in selected}
    result_ids = {
        entry["candidate_id"]: [
            production.stable_result_id(entry, record["class"], record["metric"])
            for record in outcome_by_id[entry["candidate_id"]].get("result_records", [])
        ]
        for entry in selected
    }
    view_ids = {
        result_id: production.stable_view_id(result_id)
        for values_for_candidate in result_ids.values()
        for result_id in values_for_candidate
    }
    return package_ids, result_ids, view_ids


def reseal(envelope: dict) -> None:
    envelope["attempt_fingerprint"] = admission.fingerprint({key: value for key, value in envelope.items() if key != "attempt_fingerprint"})


class AdmissionAttemptProfileTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.canary = fixture("canary")
        cls.production = fixture("production")

    def validate(self, envelope: dict, values: dict | None = None) -> dict:
        values = values or self.canary
        package_ids, result_ids, view_ids = owner_identity_context(values)
        return admission.dispatch_validate_admission_attempt(
            admission.PROFILE_ID,
            envelope,
            expected_manifest=values["manifest"],
            expected_manifest_byte_fingerprint=values["manifest_byte_fingerprint"],
            expected_manifest_identity_kind=values["manifest_identity_kind"],
            expected_package_ids=package_ids,
            expected_result_ids=result_ids,
            expected_view_ids=view_ids,
        )

    def test_owner_derived_result_and_view_identities_cannot_be_resealed(self) -> None:
        envelope = build(self.canary)
        outcome = next(row for row in envelope["outcomes"] if row["disposition"] == "valid")
        package = envelope["packages"][0]
        outcome_record = outcome["result_records"][0]
        package_record = admission._package_result_records(package)[0]
        view = envelope["views"][0]
        spoofed_result_id = outcome_record["result_id"] + "-spoofed"
        outcome_record["result_id"] = spoofed_result_id
        package_record["result_id"] = spoofed_result_id
        view["result_record_id"] = spoofed_result_id
        view["view_id"] = view["view_id"] + "-spoofed"
        view["view_fingerprint"] = admission.fingerprint({key: value for key, value in view.items() if key != "view_fingerprint"})
        outcome_fingerprint = admission.fingerprint(outcome)
        rerun = next(row for row in envelope["reruns"] if row["candidate_id"] == outcome["candidate_id"])
        rerun["first_fingerprint"] = outcome_fingerprint
        rerun["second_fingerprint"] = outcome_fingerprint
        envelope["result_fingerprints"] = [admission.fingerprint(row) for row in envelope["outcomes"]]
        envelope["package_fingerprints"] = [admission.fingerprint(row) for row in envelope["packages"]]
        envelope["view_fingerprints"] = [row["view_fingerprint"] for row in envelope["views"]]
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "result identity|view identity"):
            self.validate(envelope)

    def test_package_outcome_binding_preserves_json_number_types(self) -> None:
        envelope = build(self.canary)
        package_records = admission._package_result_records(envelope["packages"][0])
        package_record = next(record for record in package_records if isinstance(record.get("value"), (int, float)) and not isinstance(record.get("value"), bool) and float(record["value"]).is_integer())
        original = package_record["value"]
        replacement = float(original) if isinstance(original, int) else int(original)
        self.assertEqual(replacement, original)
        self.assertIsNot(type(replacement), type(original))
        package_record["value"] = replacement
        envelope["package_fingerprints"] = [admission.fingerprint(row) for row in envelope["packages"]]
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "exactly match|detached"):
            self.validate(envelope)

    def test_exact_identity_and_canary_scope_are_admissible(self) -> None:
        envelope = build(self.canary)
        result = self.validate(envelope)
        self.assertTrue(result["admission_authorized"])
        self.assertEqual(envelope["profile_id"], "knowledgeforge.evidence_portfolio.admission_attempt.v1@1.0")
        self.assertEqual(len(envelope["evaluated_candidate_ids"]), 2)
        self.assertEqual(len(envelope["unevaluated_candidate_ids"]), 1)
        self.assertEqual(len(envelope["packages"]), 1)
        self.assertEqual(len(envelope["views"]), 28)

    def test_complete_positive_production_is_admissible(self) -> None:
        envelope = build(self.production)
        result = self.validate(envelope, self.production)
        self.assertTrue(result["admission_authorized"])
        self.assertEqual(envelope["unevaluated_candidate_ids"], [])
        self.assertEqual(len(envelope["outcomes"]), 3)
        self.assertEqual(len(envelope["packages"]), 2)
        self.assertEqual(len(envelope["views"]), 56)

    def _negative(self, disposition: str, stage: str) -> dict:
        values = copy.deepcopy(self.canary)
        executable_id = values["reruns"][0]["candidate_id"]
        negative = {
            "candidate_id": executable_id,
            "disposition": disposition,
            "stage": stage,
            "reason": f"bounded {disposition}",
            "raw_result_count": 0,
        }
        values["outcomes"][0] = negative
        values["reruns"][0].update({
            "first_fingerprint": production.fingerprint(negative),
            "second_fingerprint": production.fingerprint(negative),
        })
        values["packages"] = []
        values["views"] = []
        values["blockers"] = ["execution failure"] if disposition == "failed" else ["canary valid-candidate count mismatch"]
        return values

    def test_null_is_a_validly_recorded_non_admission_without_package(self) -> None:
        values = self._negative("null", "calculation")
        result = self.validate(build(values), values)
        self.assertFalse(result["admission_authorized"])
        self.assertEqual(result["decision"], "reject")

    def test_invented_execution_rejection_is_not_an_owner_transition(self) -> None:
        values = self._negative("rejected", "execution")
        with self.assertRaisesRegex(ValueError, "not emitted by this owner"):
            build(values)

    def test_input_validation_failure_is_representable_but_not_admissible(self) -> None:
        values = self._negative("failed", "input_validation")
        self.assertFalse(self.validate(build(values), values)["admission_authorized"])

    def test_calculation_failure_is_representable_but_not_admissible(self) -> None:
        values = self._negative("failed", "calculation")
        self.assertFalse(self.validate(build(values), values)["admission_authorized"])

    def test_invented_post_execution_failure_is_not_an_owner_transition(self) -> None:
        values = self._negative("failed", "post_execution_validation")
        with self.assertRaisesRegex(ValueError, "not emitted by this owner"):
            build(values)

    def test_mixed_positive_and_negative_production_is_rejected_as_a_run(self) -> None:
        values = copy.deepcopy(self.production)
        second_id = values["reruns"][1]["candidate_id"]
        negative = {"candidate_id": second_id, "disposition": "null", "stage": "calculation", "reason": "bounded null", "raw_result_count": 0}
        values["outcomes"][1] = negative
        values["reruns"][1].update({"first_fingerprint": production.fingerprint(negative), "second_fingerprint": production.fingerprint(negative)})
        values["packages"] = []
        values["views"] = []
        values["blockers"] = ["production valid-candidate count mismatch"]
        envelope = build(values)
        result = admission.dispatch_validate_admission_attempt(
            admission.PROFILE_ID, envelope,
            expected_manifest=values["manifest"],
            expected_manifest_byte_fingerprint=values["manifest_byte_fingerprint"],
            expected_manifest_identity_kind=values["manifest_identity_kind"],
            expected_package_ids={
                entry["candidate_id"]: production.stable_object_id(entry)
                for entry in values["manifest"]["entries"] if entry["disposition"] == "execute"
            },
        )
        self.assertFalse(result["admission_authorized"])
        self.assertEqual(envelope["packages"], [])

    def test_canary_does_not_invent_outcome_for_unevaluated_candidate(self) -> None:
        envelope = build(self.canary)
        outcome_ids = {row["candidate_id"] for row in envelope["outcomes"]}
        self.assertTrue(outcome_ids.isdisjoint(envelope["unevaluated_candidate_ids"]))
        bad = copy.deepcopy(envelope)
        missing = bad["unevaluated_candidate_ids"][0]
        bad["outcomes"].append({"candidate_id": missing, "disposition": "failed", "stage": "execution", "reason": "invented", "raw_result_count": 0})
        reseal(bad)
        with self.assertRaisesRegex(ValueError, "outcome population"):
            self.validate(bad)

    def test_package_population_must_match_valid_admitted_outcomes(self) -> None:
        envelope = build(self.canary)
        envelope["packages"] = []
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "package population|constructed proposal"):
            self.validate(envelope)

    def test_negative_outcome_cannot_carry_invented_empty_package(self) -> None:
        values = self._negative("null", "calculation")
        envelope = build(values)
        envelope["packages"] = [copy.deepcopy(self.canary["packages"][0])]
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "rejected attempt.*packages|package population"):
            self.validate(envelope, values)

    def test_view_population_must_exactly_cover_package_records(self) -> None:
        envelope = build(self.canary)
        envelope["views"].pop()
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "view population"):
            self.validate(envelope)

    def test_manifest_candidate_scope_is_exact_and_ordered(self) -> None:
        envelope = build(self.canary)
        envelope["evaluated_candidate_ids"].reverse()
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "evaluated candidate scope"):
            self.validate(envelope)

    def test_exact_manifest_semantics_and_invocation_bytes_are_bound(self) -> None:
        envelope = build(self.canary)
        expected_package_ids = {
            entry["candidate_id"]: production.stable_object_id(entry)
            for entry in self.canary["manifest"]["entries"]
            if entry.get("canary") is True and entry["disposition"] == "execute"
        }
        changed = copy.deepcopy(self.canary["manifest"])
        changed["manifest_id"] += "-tampered"
        with self.assertRaisesRegex(ValueError, "manifest identity|expected manifest"):
            admission.dispatch_validate_admission_attempt(
                admission.PROFILE_ID, envelope,
                expected_manifest=changed,
                expected_manifest_byte_fingerprint=self.canary["manifest_byte_fingerprint"],
                expected_manifest_identity_kind=self.canary["manifest_identity_kind"],
                expected_package_ids=expected_package_ids,
            )
        with self.assertRaisesRegex(ValueError, "manifest byte fingerprint"):
            admission.dispatch_validate_admission_attempt(
                admission.PROFILE_ID, envelope,
                expected_manifest=self.canary["manifest"],
                expected_manifest_byte_fingerprint="sha256:" + "0" * 64,
                expected_manifest_identity_kind=self.canary["manifest_identity_kind"],
                expected_package_ids=expected_package_ids,
            )

    def test_manifest_tampering_fails_even_when_attempt_is_resealed(self) -> None:
        envelope = build(self.canary)
        envelope["manifest"]["portfolio_kind"] = "spoofed"
        envelope["manifest"]["manifest_fingerprint"] = production.fingerprint({key: value for key, value in envelope["manifest"].items() if key != "manifest_fingerprint"})
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "manifest identity|expected manifest"):
            self.validate(envelope)

    def test_package_byte_tampering_fails_even_when_attempt_is_resealed(self) -> None:
        envelope = build(self.canary)
        envelope["packages"][0]["status"] = "tampered"
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "package.*outcome|package fingerprint|package validation"):
            self.validate(envelope)

    def test_result_fingerprint_population_is_explicit_and_tamper_evident(self) -> None:
        envelope = build(self.canary)
        self.assertEqual(
            envelope["result_fingerprints"],
            [admission.fingerprint(outcome) for outcome in envelope["outcomes"]],
        )
        envelope["result_fingerprints"][0] = "sha256:" + "0" * 64
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "result fingerprint"):
            self.validate(envelope)

    def test_owner_derived_package_identity_is_required(self) -> None:
        envelope = build(self.canary)
        selected = next(
            entry for entry in self.canary["manifest"]["entries"]
            if entry.get("canary") is True and entry["disposition"] == "execute"
        )
        with self.assertRaisesRegex(ValueError, "package identity"):
            admission.dispatch_validate_admission_attempt(
                admission.PROFILE_ID,
                envelope,
                expected_manifest=self.canary["manifest"],
                expected_manifest_byte_fingerprint=self.canary["manifest_byte_fingerprint"],
                expected_manifest_identity_kind=self.canary["manifest_identity_kind"],
                expected_package_ids={selected["candidate_id"]: "pkg-object-spoofed"},
            )

    def test_dispatch_cannot_authorize_without_owner_package_identity_context(self) -> None:
        envelope = build(self.canary)
        with self.assertRaisesRegex(ValueError, "owner-derived package identity"):
            admission.dispatch_validate_admission_attempt(
                admission.PROFILE_ID,
                envelope,
                expected_manifest=self.canary["manifest"],
                expected_manifest_byte_fingerprint=self.canary["manifest_byte_fingerprint"],
                expected_manifest_identity_kind=self.canary["manifest_identity_kind"],
            )
        structural = admission.validate_admission_attempt(
            envelope,
            expected_manifest=self.canary["manifest"],
            expected_manifest_byte_fingerprint=self.canary["manifest_byte_fingerprint"],
            expected_manifest_identity_kind=self.canary["manifest_identity_kind"],
        )
        self.assertTrue(structural["valid"])
        self.assertFalse(structural["admission_authorized"])

    def test_owner_derived_package_identity_population_is_complete(self) -> None:
        envelope = build(self.canary)
        with self.assertRaisesRegex(ValueError, "package identity population"):
            admission.dispatch_validate_admission_attempt(
                admission.PROFILE_ID,
                envelope,
                expected_manifest=self.canary["manifest"],
                expected_manifest_byte_fingerprint=self.canary["manifest_byte_fingerprint"],
                expected_manifest_identity_kind=self.canary["manifest_identity_kind"],
                expected_package_ids={},
            )

    def test_spoofed_admit_decision_fails(self) -> None:
        values = self._negative("failed", "input_validation")
        envelope = build(values)
        envelope["decision"] = "admit"
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "derived decision"):
            self.validate(envelope, values)

    def test_unmatched_rerun_cannot_be_admitted(self) -> None:
        values = copy.deepcopy(self.canary)
        values["reruns"][0]["matched"] = False
        values["reruns"][0]["second_fingerprint"] = "sha256:" + "0" * 64
        values["blockers"] = ["deterministic rerun mismatch"]
        values["packages"] = []
        values["views"] = []
        result = self.validate(build(values), values)
        self.assertFalse(result["admission_authorized"])

    def test_missing_malformed_latest_range_alias_and_unknown_profile_fail_closed(self) -> None:
        envelope = build(self.canary)
        for identity in [None, "", admission.SCHEMA_NAME, "latest", "knowledgeforge.evidence_portfolio.admission_attempt.v1@latest", "knowledgeforge.evidence_portfolio.admission_attempt.v1@>=1.0", "admission-attempt-v1", "knowledgeforge.evidence_portfolio.admission_attempt.v2@2.0"]:
            with self.subTest(identity=identity):
                with self.assertRaisesRegex(ValueError, "exact admission-attempt profile"):
                    admission.dispatch_validate_admission_attempt(
                        identity, envelope,
                        expected_manifest=self.canary["manifest"],
                        expected_manifest_byte_fingerprint=self.canary["manifest_byte_fingerprint"],
                    )

    def test_envelope_identity_conflict_fails(self) -> None:
        envelope = build(self.canary)
        envelope["profile_id"] = "knowledgeforge.evidence_portfolio.admission_attempt.v1@latest"
        reseal(envelope)
        with self.assertRaisesRegex(ValueError, "schema/version/profile"):
            self.validate(envelope)

    def test_deterministic_repetition(self) -> None:
        one = build(self.canary)
        two = build(copy.deepcopy(self.canary))
        self.assertEqual(one, two)
        self.assertEqual(one["attempt_fingerprint"], two["attempt_fingerprint"])

    def test_published_historical_profile_identity_remains_distinct(self) -> None:
        historical = importlib.import_module("evidence_portfolio_conformance")
        self.assertEqual(historical.PROFILE_ID, "knowledgeforge.evidence_portfolio.conformance.v1@1.0")
        self.assertNotEqual(historical.PROFILE_ID, admission.PROFILE_ID)


class AdmissionOwnerIntegrationTest(unittest.TestCase):
    def test_public_persistence_helpers_expose_no_lock_bypass(self) -> None:
        import inspect
        self.assertNotIn("_lock_held", inspect.signature(production.persist_packages).parameters)
        self.assertNotIn("_lock_held", inspect.signature(production.knowledge_repository.persist_knowledge_object_packages).parameters)

    def test_repository_root_inside_output_root_is_rejected_before_execution(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / "attempt-output"
            with mock.patch.object(production, "_rerun_match", side_effect=AssertionError("execution reached")):
                with self.assertRaisesRegex(ValueError, "output root.*repository"):
                    production.run_portfolio(manifest, "canary", output, output / "repository", project_root=ROOT)

    def test_hard_linked_output_target_is_rejected_before_execution_or_persistence(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            output = root / "output"
            output.mkdir()
            external = root / "external.json"
            external.write_text("protected", encoding="utf-8")
            (output / "canary_gate.json").hardlink_to(external)
            with mock.patch.object(production, "_rerun_match", side_effect=AssertionError("execution reached")), mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(ValueError, "output target"):
                    production.run_portfolio(manifest, "canary", output, root / "repository", project_root=ROOT)
                persist.assert_not_called()
            self.assertEqual(external.read_text(encoding="utf-8"), "protected")

    def test_unwritable_existing_output_target_is_rejected_before_execution_or_persistence(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            output = root / "output"
            output.mkdir()
            target = output / "canary_admission_attempt.json"
            target.write_text("protected", encoding="utf-8")
            target.chmod(0o444)
            with mock.patch.object(production, "_rerun_match", side_effect=AssertionError("execution reached")), mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(ValueError, "output target"):
                    production.run_portfolio(manifest, "canary", output, root / "repository", project_root=ROOT)
                persist.assert_not_called()
            self.assertEqual(target.read_text(encoding="utf-8"), "protected")

    def test_direct_persist_helper_acquires_shared_writer_lock(self) -> None:
        _, manifest = production.build_preregistration()
        entry = next(entry for entry in manifest["entries"] if entry["disposition"] == "execute" and entry.get("canary") is True)
        result = production.calculate_candidate(entry, production.read_json(ROOT / entry["input"]["path"]))
        package = production.build_knowledge_object(entry, result, manifest["manifest_fingerprint"])
        expected = {"exists": False, "object_count": 0, "repository_fingerprint": None}
        authenticated = {"object_count": 1, "repository_fingerprint": "sha256:" + "1" * 64}
        @contextmanager
        def observed_lock(_root):
            yield Path("/tmp/shared.lock")
        with tempfile.TemporaryDirectory() as td, \
                mock.patch.object(production, "production_repository_lock", side_effect=observed_lock) as lock, \
                mock.patch.object(production.knowledge_repository, "_persist_knowledge_object_packages_locked"), \
                mock.patch.object(production.knowledge_repository, "authenticate_repository", return_value=authenticated):
            production.persist_packages([package], Path(td) / "repository", expected)
        lock.assert_called_once()

    def test_output_root_file_is_rejected_before_execution_or_persistence(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            output = root / "output"
            output.write_text("not a directory", encoding="utf-8")
            with mock.patch.object(production, "_rerun_match", side_effect=AssertionError("execution reached")), \
                    mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(ValueError, "output root"):
                    production.run_portfolio(manifest, "canary", output, root / "repository", project_root=ROOT)
                persist.assert_not_called()

    def test_output_target_directory_is_rejected_before_repository_persistence(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            output = root / "output"
            output.mkdir()
            (output / "canary_gate.json").mkdir()
            with mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(ValueError, "output target"):
                    production.run_portfolio(manifest, "canary", output, root / "repository", project_root=ROOT)
                persist.assert_not_called()

    def test_output_root_inside_repository_is_rejected_before_execution(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            repository = Path(td) / "repository"
            with mock.patch.object(production, "_rerun_match", side_effect=AssertionError("execution reached")):
                with self.assertRaisesRegex(ValueError, "output root.*repository"):
                    production.run_portfolio(manifest, "canary", repository / "attempt-output", repository, project_root=ROOT)

    def test_existing_canary_repository_must_authenticate_before_execution(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            repository = root / "repository"
            repository.mkdir()
            (repository / "junk").write_text("not canonical", encoding="utf-8")
            with mock.patch.object(production, "_rerun_match", side_effect=AssertionError("execution reached")):
                with self.assertRaisesRegex(ValueError, "canary repository authentication"):
                    production.run_portfolio(manifest, "canary", root / "output", repository, project_root=ROOT)

    def test_clean_validator_rejection_is_a_contradiction_not_a_resealed_rejection(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            rejected = {"valid": True, "profile_id": admission.PROFILE_ID, "decision": "reject", "admission_authorized": False}
            with mock.patch.object(production.admission_attempt, "dispatch_validate_admission_attempt", return_value=rejected), mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(RuntimeError, "contradicts owner decision"):
                    production.run_portfolio(manifest, "canary", root / "out", root / "repository", project_root=ROOT)
                persist.assert_not_called()
                self.assertFalse((root / "out" / "canary_admission_attempt.json").exists())

    def test_direct_owner_uses_canonical_in_memory_identity_and_accepts_no_claimed_hash(self) -> None:
        import inspect
        self.assertNotIn("manifest_file_fingerprint", inspect.signature(production.run_portfolio).parameters)
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            production.run_portfolio(manifest, "canary", root / "out", root / "repository", project_root=ROOT)
            attempt = json.loads((root / "out" / "canary_admission_attempt.json").read_text())
            self.assertEqual(attempt["manifest_identity_kind"], "canonical_in_memory_bytes")
            self.assertEqual(attempt["manifest_byte_fingerprint"], production.manifest_bytes_fingerprint(manifest))

    def test_file_source_comparison_preserves_json_number_types(self) -> None:
        _, manifest = production.build_preregistration()
        invoked = copy.deepcopy(manifest)
        invoked["canonical_ontology_change"] = 0
        invoked["manifest_fingerprint"] = production.fingerprint({
            key: value for key, value in invoked.items() if key != "manifest_fingerprint"
        })
        self.assertEqual(invoked["canonical_ontology_change"], manifest["canonical_ontology_change"])
        self.assertIsNot(type(invoked["canonical_ontology_change"]), type(manifest["canonical_ontology_change"]))
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            path = root / "manifest.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            with mock.patch.object(production, "_rerun_match", side_effect=AssertionError("execution reached")):
                with self.assertRaisesRegex(ValueError, "source bytes"):
                    production.run_portfolio(invoked, "canary", root / "out", root / "repo", manifest_source_path=path, project_root=ROOT)

    def test_manifest_source_identity_hashes_the_same_bytes_it_decodes(self) -> None:
        _, manifest = production.build_preregistration()
        source_bytes = json.dumps(manifest, separators=(",", ":"), sort_keys=True).encode("utf-8")
        with mock.patch.object(Path, "read_bytes", return_value=source_bytes) as read_bytes:
            decoded, observed = production.read_manifest_source_identity(Path("ignored.json"))
        read_bytes.assert_called_once()
        self.assertEqual(decoded, manifest)
        self.assertEqual(observed, "sha256:" + __import__("hashlib").sha256(source_bytes).hexdigest())

    def test_file_backed_manifest_source_must_decode_to_invoked_manifest(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            manifest_path = root / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            changed = copy.deepcopy(manifest)
            changed["manifest_id"] += "-spoofed"
            changed["manifest_fingerprint"] = production.fingerprint({
                key: value for key, value in changed.items() if key != "manifest_fingerprint"
            })
            with mock.patch.object(production, "_rerun_match", side_effect=AssertionError("execution reached")):
                with self.assertRaisesRegex(ValueError, "source bytes"):
                    production.run_portfolio(changed, "canary", root / "out", root / "repository", manifest_source_path=manifest_path, project_root=ROOT)
            self.assertFalse((root / "out").exists())

    def test_profile_failure_occurs_before_first_persistence_call(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with mock.patch.object(production.admission_attempt, "dispatch_validate_admission_attempt", side_effect=ValueError("profile rejected")) as validator, mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(ValueError, "profile rejected"):
                    production.run_portfolio(manifest, "canary", root / "out", root / "repository", project_root=ROOT)
                validator.assert_called_once()
                persist.assert_not_called()
                self.assertFalse((root / "repository").exists())

    def test_rejected_attempt_leaves_repository_unchanged_and_records_non_admission(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            negative = {"candidate_id": manifest["entries"][0]["candidate_id"], "disposition": "null", "stage": "calculation", "reason": "bounded null", "raw_result_count": 0}
            with mock.patch.object(production, "_rerun_match", return_value=(negative, copy.deepcopy(negative), True)), mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(RuntimeError, "canary gate failed"):
                    production.run_portfolio(manifest, "canary", root / "out", root / "repository", project_root=ROOT)
                persist.assert_not_called()
                self.assertFalse((root / "repository").exists())
                attempt = json.loads((root / "out" / "canary_admission_attempt.json").read_text())
                self.assertEqual(attempt["decision"], "reject")
                self.assertFalse(admission.validate_admission_attempt(attempt)["admission_authorized"])

    def test_owner_rejects_non_boolean_validator_authorization_before_persistence(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            malformed = {"valid": True, "decision": "admit", "admission_authorized": "false"}
            with mock.patch.object(
                production.admission_attempt,
                "dispatch_validate_admission_attempt",
                return_value=malformed,
            ), mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(RuntimeError, "malformed admission-attempt validation"):
                    production.run_portfolio(
                        manifest,
                        "canary",
                        root / "out",
                        root / "repository",
                        project_root=ROOT,
                    )
                persist.assert_not_called()

    def test_exact_bound_packages_from_validated_envelope_are_persisted(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            captured = {}
            real_dispatch = admission.dispatch_validate_admission_attempt
            def spy(profile_id, envelope, **kwargs):
                result = real_dispatch(profile_id, envelope, **kwargs)
                captured["package_ids"] = [row["package_id"] for row in envelope["packages"]]
                return result
            real_persist = production._persist_packages_locked
            def persist_spy(packages, repository_root, expected_repository_state):
                captured["persisted_ids"] = [row["package_id"] for row in copy.deepcopy(packages)]
                return real_persist(packages, repository_root, expected_repository_state)
            with mock.patch.object(production.admission_attempt, "dispatch_validate_admission_attempt", side_effect=spy), mock.patch.object(production, "_persist_packages_locked", side_effect=persist_spy):
                gate = production.run_portfolio(manifest, "canary", root / "out", root / "repository", project_root=ROOT)
            self.assertEqual(gate["publication"]["admitted_object_count"], 1)
            self.assertEqual(captured["persisted_ids"], captured["package_ids"])

    def test_direct_owner_rejects_missing_latest_and_unknown_profile_identity(self) -> None:
        _, manifest = production.build_preregistration()
        for identity in [None, "latest", "knowledgeforge.evidence_portfolio.admission_attempt.v2@2.0"]:
            with self.subTest(identity=identity), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                with mock.patch.object(production, "_persist_packages_locked") as persist:
                    with self.assertRaisesRegex(ValueError, "exact admission-attempt profile"):
                        production.run_portfolio(manifest, "canary", root / "out", root / "repository", project_root=ROOT, admission_profile_id=identity)
                    persist.assert_not_called()

    def test_sweden_cli_and_shared_cli_converge_on_same_owner(self) -> None:
        sweden = importlib.import_module("evidence_portfolio_sweden_infrastructure")
        self.assertIs(sweden.portfolio.run_portfolio, production.run_portfolio)
        self.assertIn("run_portfolio(", Path(production.__file__).read_text())
        self.assertIn("portfolio.run_portfolio(", Path(sweden.__file__).read_text())

    def test_private_locked_helper_still_enforces_profile_before_persistence(self) -> None:
        _, manifest = production.build_preregistration()
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with mock.patch.object(production, "_persist_packages_locked") as persist:
                with self.assertRaisesRegex(ValueError, "exact admission-attempt profile"):
                    production._run_portfolio_locked(
                        manifest, "canary", root / "out", root / "repository",
                        project_root=ROOT, admission_profile_id="latest",
                    )
                persist.assert_not_called()

    def test_owner_accepts_no_caller_supplied_stale_validation_result(self) -> None:
        import inspect
        parameters = inspect.signature(production.run_portfolio).parameters
        self.assertNotIn("validation_result", parameters)
        self.assertNotIn("conformance_result", parameters)

    def test_lower_level_persistence_is_per_file_not_whole_portfolio_atomic(self) -> None:
        repository = importlib.import_module("knowledge_repository")
        values = fixture("canary")
        package = values["packages"][0]
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "repository"
            real_write = repository.write_json
            calls = 0
            def fail_second(path, value):
                nonlocal calls
                calls += 1
                if calls == 2:
                    raise OSError("injected write interruption")
                return real_write(path, value)
            with mock.patch.object(repository, "write_json", side_effect=fail_second):
                with self.assertRaisesRegex(OSError, "injected write interruption"):
                    repository.persist_knowledge_object_packages([package], root)
            self.assertTrue((root / "objects" / f"{package['package_id']}.json").is_file())
            self.assertFalse((root / "manifest.json").exists())

    def test_owner_persistence_reauthenticates_expected_state_under_shared_lock(self) -> None:
        _, manifest = production.build_preregistration()
        entry = next(entry for entry in manifest["entries"] if entry["disposition"] == "execute" and entry.get("canary") is True)
        result = production.calculate_candidate(entry, production.read_json(ROOT / entry["input"]["path"]))
        package = production.build_knowledge_object(entry, result, manifest["manifest_fingerprint"])
        expected = {"exists": False, "object_count": 0, "repository_fingerprint": None}
        authenticated = {"object_count": 1, "repository_fingerprint": "sha256:" + "1" * 64}
        with tempfile.TemporaryDirectory() as td,                 mock.patch.object(production.knowledge_repository, "_persist_knowledge_object_packages_locked") as lower,                 mock.patch.object(production.knowledge_repository, "authenticate_repository", return_value=authenticated):
            result = production.persist_packages([package], Path(td) / "repository", expected)
        lower.assert_called_once_with([package], Path(td) / "repository", expected_repository_state=expected)
        self.assertEqual(result, authenticated)

    def test_lower_level_persistence_is_not_an_admission_attempt_api(self) -> None:
        repository = importlib.import_module("knowledge_repository")
        self.assertFalse(hasattr(repository, "build_admission_attempt"))
        self.assertFalse(hasattr(repository, "dispatch_validate_admission_attempt"))


if __name__ == "__main__":
    unittest.main()
