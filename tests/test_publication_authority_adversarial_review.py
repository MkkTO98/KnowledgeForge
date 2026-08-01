from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "publication_authority_review", ROOT / "tools" / "publication_authority.py"
)
pa = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(pa)


def fp(value: dict, field: str) -> str:
    payload = {key: item for key, item in value.items() if key != field}
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class Environment:
    def __init__(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.complete_root = self.root / "complete"
        self.mixed_root = self.root / "mixed"
        self.authority_root = self.root / "authority"
        self.registry_path = self.root / "publication_authority_registry.json"
        for path in [self.repo, self.complete_root, self.mixed_root, self.authority_root]:
            path.mkdir()
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.name", "Test"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "config", "user.email", "test@example.invalid"], check=True)
        self.durable_path = "artifacts/reports/R-test-publication-authority.md"
        self._write(self.repo, self.durable_path, b"old durable record\n", 0o644)
        self._write(self.repo, "state/mixed.md", b"mixed\n", 0o644)
        self._write(self.repo, "tools/audit.py", b"audit\n", 0o644)
        subprocess.run(["git", "-C", str(self.repo), "add", "--all"], check=True)
        subprocess.run(["git", "-C", str(self.repo), "commit", "-qm", "parent"], check=True)
        self.parent = subprocess.run(
            ["git", "-C", str(self.repo), "rev-parse", "HEAD"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        self.mixed_bytes = b"mixed\n"
        self.authority_bytes = b"audit\n"
        self._write(self.mixed_root, "state/mixed.md", self.mixed_bytes, 0o644)
        self._write(self.authority_root, "tools/audit.py", self.authority_bytes, 0o755)
        self.mixed = {
            "apply_policy": "do not copy; preserve as external candidate representations",
            "parent_head": self.parent,
            "path_count": 1,
            "paths": [{"path": "state/mixed.md", "mode": "100644", "sha256": sha(self.mixed_bytes), "size": len(self.mixed_bytes)}],
            "schema_name": "knowledgeforge.evidence_portfolio.mixed_representation_candidate.v1",
            "schema_version": "1.0",
        }
        self.mixed["manifest_fingerprint"] = fp(self.mixed, "manifest_fingerprint")
        self.complete_bytes = (
            "# Publication authority continuity\n\n"
            "Publication-Authority-Schema: knowledgeforge.publication_authority.v1@1.0\n"
            f"Publication-Authority-Parent: {self.parent}\n"
            f"Publication-Authority-Audit-Subject: sha256:{'4' * 64}\n"
            f"Publication-Authority-Mixed-Manifest: {self.mixed['manifest_fingerprint']}\n"
            "Publication-Authority-Complete-Path-Count: 1\n"
            "Publication-Authority-Only-Path-Count: 1\n"
            "Publication-Authority-External-Evidence: /tmp/test/publication_authority.json\n"
        ).encode("utf-8")
        self._write(self.complete_root, self.durable_path, self.complete_bytes, 0o644)
        self.complete = {
            "apply_policy": "copy complete bytes only; zero staging; no mixed paths",
            "parent_head": self.parent,
            "path_count": 1,
            "paths": [{"path": self.durable_path, "mode": "100644", "sha256": sha(self.complete_bytes), "size": len(self.complete_bytes)}],
            "schema_name": "knowledgeforge.evidence_portfolio.complete_file_candidate.v1",
            "schema_version": "1.0",
        }
        self.complete["manifest_fingerprint"] = fp(self.complete, "manifest_fingerprint")
        self.extra = [{"path": "tools/audit.py", "mode": "100755", "blob_sha256": "sha256:" + sha(self.authority_bytes), "reason": "frozen audit tool authority"}]
        self.roots = {"complete": self.complete_root, "mixed": self.mixed_root, "authority_only": self.authority_root}
        self.original_evidence_root = self.root / "original-evidence"
        self._write(
            self.original_evidence_root / "files",
            "state/mixed.md",
            self.mixed_bytes,
            0o644,
        )
        self.original_evidence_manifest = {
            "schema_name": pa.MIXED_SNAPSHOT_SCHEMA,
            "schema_version": pa.MIXED_SNAPSHOT_VERSION,
            "parent_head": self.parent,
            "mixed_manifest_fingerprint": self.mixed["manifest_fingerprint"],
            "path_count": 1,
            "paths": [
                {
                    "path": "state/mixed.md",
                    "filesystem_mode": "0o644",
                    "size": len(self.mixed_bytes),
                    "sha256": sha(self.mixed_bytes),
                }
            ],
        }
        self.original_evidence_manifest["snapshot_fingerprint"] = fp(
            self.original_evidence_manifest, "snapshot_fingerprint"
        )
        (self.original_evidence_root / "protected_mixed_manifest.json").write_text(
            json.dumps(self.original_evidence_manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        self.protected_mixed_root = self.root / "protected-mixed"
        self.protected_mixed_manifest = pa.capture_mixed_snapshot(
            self.mixed,
            repository_root=self.repo,
            output_root=self.protected_mixed_root,
            original_evidence_manifest=self.original_evidence_manifest,
            original_evidence_root=self.original_evidence_root,
        )

    @staticmethod
    def _write(root: Path, relative: str, data: bytes, mode: int):
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        path.chmod(mode)

    def build(self, durable=None):
        return pa.build_publication_authority(
            self.complete,
            self.mixed,
            self.extra,
            repository_root=self.repo,
            registry_path=self.registry_path,
            audit_subject_manifest_fingerprint="sha256:" + "4" * 64,
            durable_record_path=durable or self.durable_path,
        )

    def activate_registry(self, authority, superseded=None):
        return pa.install_authority_registry(
            authority, superseded=superseded or []
        )

    def close(self):
        self.temp.cleanup()


class IndependentReviewRegressionTests(unittest.TestCase):
    def setUp(self):
        self.env = Environment()

    def tearDown(self):
        self.env.close()

    def test_parent_delta_is_derived_from_authenticated_git_tree(self):
        authority = self.env.build()
        self.assertIn("artifacts/reports/R-test-publication-authority.md", authority["changed_paths"])
        self.assertIn("state/mixed.md", authority["parent_identical_paths"])
        self.assertEqual(authority["parent_head"], self.env.parent)
        self.assertIsInstance(authority["parent_tree_oid"], str)
        self.assertEqual(len(authority["parent_tree_oid"]), 40)

    def test_source_parent_must_equal_current_repository_head(self):
        self.env._write(self.env.repo, "unrelated.txt", b"later\n", 0o644)
        subprocess.run(["git", "-C", str(self.env.repo), "add", "--all"], check=True)
        subprocess.run(["git", "-C", str(self.env.repo), "commit", "-qm", "later"], check=True)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "current|HEAD|parent"):
            self.env.build()

    def test_git_replacement_refs_cannot_change_authenticated_parent(self):
        self.env._write(self.env.repo, "state/mixed.md", b"replacement bytes\n", 0o644)
        subprocess.run(["git", "-C", str(self.env.repo), "add", "--all"], check=True)
        subprocess.run(["git", "-C", str(self.env.repo), "commit", "-qm", "replacement"], check=True)
        alternate = subprocess.run(
            ["git", "-C", str(self.env.repo), "rev-parse", "HEAD"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        subprocess.run(
            ["git", "-C", str(self.env.repo), "reset", "--hard", "-q", self.env.parent],
            check=True,
        )
        subprocess.run(
            ["git", "-C", str(self.env.repo), "replace", self.env.parent, alternate],
            check=True,
        )
        authority = self.env.build()
        self.assertIn("state/mixed.md", authority["parent_identical_paths"])

    def test_gate_fails_without_current_source_roots(self):
        authority = self.env.build()
        self.env.activate_registry(authority)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "source|root|representation"):
            pa.build_staging_gate(
                authority,
                self.env.complete,
                self.env.mixed,
                self.env.extra,
                repository_root=self.env.repo,
                source_roots=None,
                validation_passed=True,
            )

    def test_source_byte_mutation_after_gate_construction_fails(self):
        authority = self.env.build()
        self.env.activate_registry(authority)
        gate = pa.build_staging_gate(
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
            validation_passed=True,
        )
        (self.env.complete_root / "artifacts/reports/R-test-publication-authority.md").write_bytes(b"mutated\n")
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "source|identity|representation"):
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

    def test_symlinked_source_root_fails(self):
        authority = self.env.build()
        linked = self.env.root / "complete-link"
        linked.symlink_to(self.env.complete_root, target_is_directory=True)
        roots = dict(self.env.roots)
        roots["complete"] = linked
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "symlink"):
            pa.verify_source_representations(
                authority,
                self.env.complete,
                self.env.mixed,
                self.env.extra,
                repository_root=self.env.repo,
                roots=roots,
            )

    def test_source_root_with_symlinked_ancestor_fails(self):
        authority = self.env.build()
        real_parent = self.env.root / "real-parent"
        real_parent.mkdir()
        moved = real_parent / "complete"
        self.env.complete_root.rename(moved)
        alias = self.env.root / "alias-parent"
        alias.symlink_to(real_parent, target_is_directory=True)
        roots = dict(self.env.roots)
        roots["complete"] = alias / "complete"
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "symlink"):
            pa.verify_source_representations(
                authority,
                self.env.complete,
                self.env.mixed,
                self.env.extra,
                repository_root=self.env.repo,
                roots=roots,
            )

    def test_registry_locator_with_symlinked_ancestor_fails(self):
        real_parent = self.env.root / "registry-parent"
        real_parent.mkdir()
        alias = self.env.root / "registry-alias"
        alias.symlink_to(real_parent, target_is_directory=True)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "symlink"):
            pa.build_publication_authority(
                self.env.complete,
                self.env.mixed,
                self.env.extra,
                repository_root=self.env.repo,
                registry_path=alias / "publication_authority_registry.json",
                audit_subject_manifest_fingerprint="sha256:" + "4" * 64,
                durable_record_path="artifacts/reports/R-test-publication-authority.md",
            )

    def test_cli_has_no_arbitrary_registry_input(self):
        tool = ROOT / "tools" / "publication_authority.py"
        gate_help = subprocess.run(
            ["python3", str(tool), "gate", "--help"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        build_help = subprocess.run(
            ["python3", str(tool), "build", "--help"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout
        self.assertNotIn("--authority-registry", gate_help)
        self.assertIn("--registry-path", build_help)

    def test_cli_executes_build_registry_gate_and_verify_gate(self):
        tool = ROOT / "tools" / "publication_authority.py"
        documents = {
            "complete": self.env.complete,
            "mixed": self.env.mixed,
            "authority-only": self.env.extra,
        }
        paths = {}
        for name, value in documents.items():
            path = self.env.root / f"{name}.json"
            path.write_text(json.dumps(value, sort_keys=True) + "\n", encoding="utf-8")
            paths[name] = path
        authority_path = self.env.root / "authority.json"
        gate_path = self.env.root / "gate.json"
        plan_path = self.env.root / "plan.json"
        common = [
            "--complete", str(paths["complete"]),
            "--mixed", str(paths["mixed"]),
            "--authority-only", str(paths["authority-only"]),
            "--repository", str(self.env.repo),
        ]
        subprocess.run(
            [
                "python3", str(tool), "build", *common,
                "--registry-path", str(self.env.registry_path),
                "--audit-subject-fingerprint", "sha256:" + "4" * 64,
                "--durable-record-path", "artifacts/reports/R-test-publication-authority.md",
                "--output", str(authority_path),
            ],
            check=True,
        )
        subprocess.run(
            ["python3", str(tool), "registry", "--authority", str(authority_path)],
            check=True,
        )
        roots = [
            "--complete-root", str(self.env.complete_root),
            "--mixed-root", str(self.env.mixed_root),
            "--authority-root", str(self.env.authority_root),
            "--protected-mixed-manifest", str(self.env.protected_mixed_root / "protected_mixed_manifest.json"),
            "--protected-mixed-root", str(self.env.protected_mixed_root),
            "--original-evidence-manifest", str(self.env.original_evidence_root / "protected_mixed_manifest.json"),
            "--original-evidence-root", str(self.env.original_evidence_root),
        ]
        subprocess.run(
            [
                "python3", str(tool), "gate", *common,
                "--authority", str(authority_path), *roots,
                "--output", str(gate_path),
            ],
            check=True,
        )
        subprocess.run(
            [
                "python3", str(tool), "verify-gate", *common,
                "--authority", str(authority_path), *roots,
                "--staging-gate", str(gate_path),
                "--output", str(plan_path),
            ],
            check=True,
        )
        plan = json.loads(plan_path.read_text(encoding="utf-8"))
        self.assertIs(plan["staging_authorized"], True)
        self.assertEqual(plan["changed_path_count"], 2)

    def test_successor_registry_invalidates_old_gate_without_optional_list(self):
        authority = self.env.build()
        self.env.activate_registry(authority)
        gate = pa.build_staging_gate(
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
            validation_passed=True,
        )
        successor = dict(authority)
        successor["supersedes"] = [authority["authority_fingerprint"]]
        successor["authority_fingerprint"] = pa.authority_fingerprint(successor)
        self.env.activate_registry(
            successor, superseded=[authority["authority_fingerprint"]]
        )
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "superseded|active|stale"):
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

    def test_registry_history_detects_canonical_rollback(self):
        authority = self.env.build()
        first = pa.install_authority_registry(authority)
        old_bytes = self.env.registry_path.read_bytes()
        gate = pa.build_staging_gate(
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
            validation_passed=True,
        )
        successor = dict(authority)
        successor["supersedes"] = [authority["authority_fingerprint"]]
        successor["authority_fingerprint"] = pa.authority_fingerprint(successor)
        second = pa.install_authority_registry(
            successor, superseded=[authority["authority_fingerprint"]]
        )
        self.assertNotEqual(first["registry_fingerprint"], second["registry_fingerprint"])
        self.env.registry_path.write_bytes(old_bytes)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "history|rollback|latest"):
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

    def test_successor_must_explicitly_name_active_predecessor(self):
        predecessor = self.env.build()
        pa.install_authority_registry(predecessor)
        successor = dict(predecessor)
        successor["supersedes"] = []
        successor["audit_subject_manifest_fingerprint"] = "sha256:" + "5" * 64
        successor["authority_fingerprint"] = pa.authority_fingerprint(successor)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "explicit|predecessor|supersed"):
            pa.install_authority_registry(successor)

    def test_registry_install_rejects_inactive_or_self_invalid_authority(self):
        authority = self.env.build()
        inactive = dict(authority)
        inactive["status"] = "superseded"
        inactive["authority_fingerprint"] = pa.authority_fingerprint(inactive)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "active|status"):
            pa.install_authority_registry(inactive)
        tampered = dict(authority)
        tampered["path_count"] += 1
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "fingerprint|authority"):
            pa.install_authority_registry(tampered)

    def test_declared_source_size_must_match_physical_file(self):
        self.env.complete["paths"][0]["size"] += 1
        self.env.complete["manifest_fingerprint"] = fp(
            self.env.complete, "manifest_fingerprint"
        )
        authority = self.env.build()
        self.env.activate_registry(authority)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "size|identity"):
            pa.build_staging_gate(
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
                validation_passed=True,
            )

    def test_registry_schema_rejects_extra_fields(self):
        authority = self.env.build()
        registry = pa.build_authority_registry(authority)
        registry["unexpected"] = True
        registry["registry_fingerprint"] = pa.registry_fingerprint(registry)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "schema|field|exact"):
            pa.verify_authority_registry(registry, authority)

    def test_arbitrary_complete_file_cannot_be_designated_durable_record(self):
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "durable"):
            self.env.build(durable="docs/complete.txt")

    def test_report_shaped_durable_record_without_semantic_markers_fails_gate(self):
        bad = b"# Ordinary report without authority continuity\n"
        durable = self.env.complete_root / self.env.durable_path
        durable.write_bytes(bad)
        self.env.complete["paths"][0]["sha256"] = sha(bad)
        self.env.complete["paths"][0]["size"] = len(bad)
        self.env.complete["manifest_fingerprint"] = fp(
            self.env.complete, "manifest_fingerprint"
        )
        authority = self.env.build()
        self.env.activate_registry(authority)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "semantic markers"):
            pa.build_staging_gate(
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
                validation_passed=True,
            )

    def test_parent_identical_or_mixed_path_cannot_be_durable_record(self):
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "durable"):
            self.env.build(durable="state/mixed.md")


if __name__ == "__main__":
    unittest.main()
