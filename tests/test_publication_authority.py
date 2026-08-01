from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "publication_authority", ROOT / "tools" / "publication_authority.py"
)
pa = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(pa)

FIXTURE_PATH = (
    ROOT
    / "tests"
    / "fixtures"
    / "publication_authority"
    / "sweden_infrastructure_regression.json"
)


def canonical_fingerprint(value: dict, field: str) -> str:
    payload = {key: item for key, item in value.items() if key != field}
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def load_fixture() -> dict:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def refingerprint(manifest: dict, field: str) -> dict:
    manifest[field] = canonical_fingerprint(manifest, field)
    return manifest


class SwedenRegressionTests(unittest.TestCase):
    def test_exact_defective_59_path_authority_is_rejected(self):
        fixture = load_fixture()
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "missing|exact|mixed"):
            pa.validate_legacy_publication_authority(
                fixture["defective_authority"],
                fixture["complete_manifest"],
                fixture["mixed_manifest"],
                fixture["authority_only_entries"],
                fixture["parent_entries"],
            )

    def test_corrected_64_path_authority_is_accepted_with_58_changes(self):
        fixture = load_fixture()
        result = pa.validate_legacy_publication_authority(
            fixture["corrected_authority"],
            fixture["complete_manifest"],
            fixture["mixed_manifest"],
            fixture["authority_only_entries"],
            fixture["parent_entries"],
        )
        self.assertIs(result["valid"], True)
        self.assertEqual(result["authority_path_count"], 64)
        self.assertEqual(result["changed_path_count"], 58)
        self.assertEqual(result["parent_identical_path_count"], 6)
        self.assertEqual(result["changed_paths"], fixture["expected"]["changed_paths"])
        self.assertEqual(
            result["parent_identical_paths"],
            fixture["expected"]["parent_identical_paths"],
        )

    def test_parent_identical_authorities_are_not_false_commit_changes(self):
        fixture = load_fixture()
        result = pa.validate_legacy_publication_authority(
            fixture["corrected_authority"],
            fixture["complete_manifest"],
            fixture["mixed_manifest"],
            fixture["authority_only_entries"],
            fixture["parent_entries"],
        )
        self.assertTrue(
            set(result["changed_paths"]).isdisjoint(result["parent_identical_paths"])
        )
        self.assertEqual(
            set(result["changed_paths"]) | set(result["parent_identical_paths"]),
            {row["path"] for row in fixture["corrected_authority"]["paths"]},
        )

    def test_omission_of_any_one_mixed_path_fails(self):
        fixture = load_fixture()
        for omitted in fixture["mixed_manifest"]["paths"]:
            bad = copy.deepcopy(fixture["corrected_authority"])
            bad["paths"] = [r for r in bad["paths"] if r["path"] != omitted["path"]]
            bad["path_count"] = len(bad["paths"])
            refingerprint(bad, "final_manifest_fingerprint")
            with self.subTest(path=omitted["path"]):
                with self.assertRaises(pa.PublicationAuthorityError):
                    pa.validate_legacy_publication_authority(
                        bad,
                        fixture["complete_manifest"],
                        fixture["mixed_manifest"],
                        fixture["authority_only_entries"],
                        fixture["parent_entries"],
                    )

    def test_omission_of_any_one_complete_path_fails(self):
        fixture = load_fixture()
        for omitted in fixture["complete_manifest"]["paths"]:
            bad = copy.deepcopy(fixture["corrected_authority"])
            bad["paths"] = [r for r in bad["paths"] if r["path"] != omitted["path"]]
            bad["path_count"] = len(bad["paths"])
            refingerprint(bad, "final_manifest_fingerprint")
            with self.subTest(path=omitted["path"]):
                with self.assertRaises(pa.PublicationAuthorityError):
                    pa.validate_legacy_publication_authority(
                        bad,
                        fixture["complete_manifest"],
                        fixture["mixed_manifest"],
                        fixture["authority_only_entries"],
                        fixture["parent_entries"],
                    )

    def test_undeclared_extra_authority_path_fails(self):
        fixture = load_fixture()
        bad = copy.deepcopy(fixture["corrected_authority"])
        bad["paths"].append(
            {
                "path": "unexpected.txt",
                "mode": "100644",
                "blob_sha256": "sha256:" + "f" * 64,
            }
        )
        bad["paths"].sort(key=lambda row: row["path"])
        bad["path_count"] = len(bad["paths"])
        refingerprint(bad, "final_manifest_fingerprint")
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "extra|exact"):
            pa.validate_legacy_publication_authority(
                bad,
                fixture["complete_manifest"],
                fixture["mixed_manifest"],
                fixture["authority_only_entries"],
                fixture["parent_entries"],
            )

    def test_audit_subject_population_cannot_substitute_for_publication_sources(self):
        fixture = load_fixture()
        audit_subject = {
            row["path"] for row in fixture["corrected_authority"]["paths"]
        }
        self.assertEqual(len(audit_subject), 64)
        with self.assertRaises(pa.PublicationAuthorityError):
            pa.validate_legacy_publication_authority(
                fixture["defective_authority"],
                fixture["complete_manifest"],
                fixture["mixed_manifest"],
                fixture["authority_only_entries"],
                fixture["parent_entries"],
                audit_subject_paths=audit_subject,
            )


class GenericAuthorityTests(unittest.TestCase):
    def setUp(self):
        from tests.test_publication_authority_adversarial_review import Environment

        self.env = Environment()

    def tearDown(self):
        self.env.close()

    def build(self):
        authority = self.env.build()
        registry = self.env.activate_registry(authority)
        return authority, registry

    def gate(self, authority, registry, validation_passed=True):
        return pa.build_staging_gate(
            authority,
            self.env.complete,
            self.env.mixed,
            self.env.extra,
            repository_root=self.env.repo,
            source_roots=self.env.roots,
            protected_mixed_manifest=self.env.protected_mixed_manifest,
            protected_mixed_root=self.env.protected_mixed_root,
            original_evidence_manifest=self.env.original_evidence_manifest,
            original_evidence_root=self.env.original_evidence_root,
            validation_passed=validation_passed,
        )

    def test_build_and_verify_are_canonical_and_deterministic(self):
        first, _ = self.build()
        second = self.env.build()
        self.assertEqual(first, second)
        result = pa.verify_publication_authority(
            first,
            self.env.complete,
            self.env.mixed,
            self.env.extra,
            repository_root=self.env.repo,
        )
        self.assertIs(result["valid"], True)
        self.assertEqual(result["changed_path_count"], 2)
        self.assertEqual(result["parent_identical_path_count"], 1)

    def test_conflicting_duplicate_representations_fail(self):
        mixed = copy.deepcopy(self.env.mixed)
        mixed["paths"][0] = copy.deepcopy(self.env.complete["paths"][0])
        refingerprint(mixed, "manifest_fingerprint")
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "representation|duplicate"):
            pa.build_publication_authority(
                self.env.complete,
                mixed,
                self.env.extra,
                repository_root=self.env.repo,
                registry_path=self.env.registry_path,
                audit_subject_manifest_fingerprint="sha256:" + "4" * 64,
                durable_record_path="artifacts/reports/R-test-publication-authority.md",
            )

    def test_identical_duplicate_authority_only_declarations_are_deduplicated(self):
        authority = pa.build_publication_authority(
            self.env.complete,
            self.env.mixed,
            self.env.extra + copy.deepcopy(self.env.extra),
            repository_root=self.env.repo,
            registry_path=self.env.registry_path,
            audit_subject_manifest_fingerprint="sha256:" + "4" * 64,
            durable_record_path="artifacts/reports/R-test-publication-authority.md",
        )
        self.assertEqual(authority["authority_only_path_count"], 1)
        self.assertEqual(authority["path_count"], 3)

    def test_mode_only_change_is_a_real_change(self):
        authority, _ = self.build()
        self.assertIn("tools/audit.py", authority["changed_paths"])
        row = next(r for r in authority["paths"] if r["path"] == "tools/audit.py")
        self.assertEqual(row["change_kind"], "mode_only")

    def test_malformed_absolute_traversal_and_backslash_paths_fail(self):
        for bad_path in ["", "/absolute", "../escape", "a/../escape", "a\\b", "./dot", "a//b"]:
            complete = copy.deepcopy(self.env.complete)
            complete["paths"][0]["path"] = bad_path
            refingerprint(complete, "manifest_fingerprint")
            with self.subTest(path=bad_path):
                with self.assertRaises(pa.PublicationAuthorityError):
                    pa.build_publication_authority(
                        complete,
                        self.env.mixed,
                        self.env.extra,
                        repository_root=self.env.repo,
                        registry_path=self.env.registry_path,
                        audit_subject_manifest_fingerprint="sha256:" + "4" * 64,
                        durable_record_path="artifacts/reports/R-test-publication-authority.md",
                    )

    def test_unsupported_modes_and_malformed_hashes_fail(self):
        for field, value in [("mode", "120000"), ("sha256", "not-a-hash")]:
            complete = copy.deepcopy(self.env.complete)
            complete["paths"][0][field] = value
            refingerprint(complete, "manifest_fingerprint")
            with self.subTest(field=field):
                with self.assertRaises(pa.PublicationAuthorityError):
                    pa.build_publication_authority(
                        complete,
                        self.env.mixed,
                        self.env.extra,
                        repository_root=self.env.repo,
                        registry_path=self.env.registry_path,
                        audit_subject_manifest_fingerprint="sha256:" + "4" * 64,
                        durable_record_path="artifacts/reports/R-test-publication-authority.md",
                    )

    def test_unsafe_final_symlink_fails(self):
        authority, _ = self.build()
        path = self.env.complete_root / "artifacts/reports/R-test-publication-authority.md"
        path.unlink()
        path.symlink_to(self.env.root / "outside")
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "symlink|escape|regular"):
            pa.verify_source_representations(
                authority,
                self.env.complete,
                self.env.mixed,
                self.env.extra,
                repository_root=self.env.repo,
                roots=self.env.roots,
            )

    def test_source_manifest_mutation_after_authority_construction_fails(self):
        authority, _ = self.build()
        mixed = copy.deepcopy(self.env.mixed)
        mixed["paths"][0]["sha256"] = "9" * 64
        refingerprint(mixed, "manifest_fingerprint")
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "source|exact|fingerprint"):
            pa.verify_publication_authority(
                authority,
                self.env.complete,
                mixed,
                self.env.extra,
                repository_root=self.env.repo,
            )

    def test_authority_mutation_after_gate_validation_fails(self):
        authority, registry = self.build()
        gate = self.gate(authority, registry)
        authority["paths"][0]["blob_sha256"] = "sha256:" + "9" * 64
        authority["authority_fingerprint"] = pa.authority_fingerprint(authority)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "gate|authority|fingerprint|active"):
            pa.verify_staging_gate(
                gate,
                authority,
                self.env.complete,
                self.env.mixed,
                self.env.extra,
                repository_root=self.env.repo,
                source_roots=self.env.roots,
                protected_mixed_manifest=self.env.protected_mixed_manifest,
                protected_mixed_root=self.env.protected_mixed_root,
            original_evidence_manifest=self.env.original_evidence_manifest,
            original_evidence_root=self.env.original_evidence_root,
            )

    def test_truthy_non_boolean_gate_results_fail(self):
        authority, registry = self.build()
        for truthy in [1, "true", [True], {"valid": True}]:
            with self.subTest(value=truthy):
                with self.assertRaisesRegex(pa.PublicationAuthorityError, "Boolean"):
                    self.gate(authority, registry, validation_passed=truthy)

    def test_stale_authority_cannot_authorize_staging(self):
        authority, registry = self.build()
        stale = copy.deepcopy(authority)
        stale["status"] = "superseded"
        stale["authority_fingerprint"] = pa.authority_fingerprint(stale)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "active|superseded"):
            self.gate(stale, registry)

    def test_staging_plan_contains_only_authenticated_parent_delta(self):
        authority, registry = self.build()
        gate = self.gate(authority, registry)
        plan = pa.verify_staging_gate(
            gate,
            authority,
            self.env.complete,
            self.env.mixed,
            self.env.extra,
            repository_root=self.env.repo,
            source_roots=self.env.roots,
            protected_mixed_manifest=self.env.protected_mixed_manifest,
            protected_mixed_root=self.env.protected_mixed_root,
            original_evidence_manifest=self.env.original_evidence_manifest,
            original_evidence_root=self.env.original_evidence_root,
        )
        self.assertIs(plan["staging_authorized"], True)
        self.assertEqual(plan["changed_paths"], authority["changed_paths"])
        self.assertNotIn("state/mixed.md", plan["changed_paths"])

    def test_durable_record_must_be_an_authorized_changed_complete_path(self):
        for bad_path in ["not/authorized.md", "state/mixed.md"]:
            with self.subTest(path=bad_path):
                with self.assertRaisesRegex(pa.PublicationAuthorityError, "durable"):
                    pa.build_publication_authority(
                        self.env.complete,
                        self.env.mixed,
                        self.env.extra,
                        repository_root=self.env.repo,
                        registry_path=self.env.registry_path,
                        audit_subject_manifest_fingerprint="sha256:" + "4" * 64,
                        durable_record_path=bad_path,
                    )


if __name__ == "__main__":
    unittest.main()
