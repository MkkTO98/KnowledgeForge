from __future__ import annotations

import copy
import json
import os
import subprocess
import unittest
from pathlib import Path
from unittest import mock

from tests.test_publication_authority_adversarial_review import Environment, ROOT, fp, pa, sha


class MixedRestorationProtectionTests(unittest.TestCase):
    def setUp(self):
        self.env = Environment()
        self.snapshot_root = self.env.root / "focused-protected-mixed"

    def tearDown(self):
        self.env.close()

    def original_evidence_for_mode(self, mode):
        root = self.env.root / f"original-evidence-{mode:o}"
        self.env._write(root / "files", "state/mixed.md", self.env.mixed_bytes, mode)
        manifest = copy.deepcopy(self.env.original_evidence_manifest)
        manifest["paths"][0]["filesystem_mode"] = f"0o{mode:o}"
        manifest["snapshot_fingerprint"] = fp(manifest, "snapshot_fingerprint")
        (root / "protected_mixed_manifest.json").write_text(
            json.dumps(manifest, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return manifest, root

    def capture(self):
        return pa.capture_mixed_snapshot(
            self.env.mixed,
            repository_root=self.env.repo,
            output_root=self.snapshot_root,
            original_evidence_manifest=self.env.original_evidence_manifest,
            original_evidence_root=self.env.original_evidence_root,
        )

    def proof(self, manifest=None, root=None, candidate_root=None):
        return pa.verify_mixed_preservation(
            self.env.mixed,
            repository_root=self.env.repo,
            candidate_root=candidate_root or self.env.mixed_root,
            protected_manifest=manifest or self.capture(),
            protected_root=root or self.snapshot_root,
            original_evidence_manifest=self.env.original_evidence_manifest,
            original_evidence_root=self.env.original_evidence_root,
        )

    def gate(self, authority, manifest):
        return pa.build_staging_gate(
            authority,
            self.env.complete,
            self.env.mixed,
            self.env.extra,
            repository_root=self.env.repo,
            source_roots=self.env.roots,
            protected_mixed_manifest=manifest,
            protected_mixed_root=self.snapshot_root,
            original_evidence_manifest=self.env.original_evidence_manifest,
            original_evidence_root=self.env.original_evidence_root,
            validation_passed=True,
        )

    def test_capture_is_external_exact_immutable_source_copy(self):
        before = (self.env.repo / "state/mixed.md").read_bytes()
        manifest = self.capture()
        self.assertEqual((self.env.repo / "state/mixed.md").read_bytes(), before)
        self.assertEqual(manifest["parent_head"], self.env.parent)
        self.assertEqual(manifest["path_count"], 1)
        self.assertEqual({row["path"] for row in manifest["paths"]}, {"state/mixed.md"})
        row = manifest["paths"][0]
        self.assertEqual(row["filesystem_mode"], "0o644")
        self.assertEqual(row["size"], len(before))
        self.assertEqual(row["sha256"], sha(before))
        self.assertEqual(manifest["snapshot_fingerprint"], pa.mixed_snapshot_fingerprint(manifest))
        self.assertEqual((self.snapshot_root / "files/state/mixed.md").read_bytes(), before)
        on_disk = json.loads((self.snapshot_root / "protected_mixed_manifest.json").read_text())
        self.assertEqual(on_disk, manifest)

    def test_capture_copies_from_retained_evidence_and_rejects_mid_copy_live_mutation(self):
        real_copy = pa.shutil.copyfileobj
        observed_sources = []

        def mutate_live_after_copy(source_handle, target_handle):
            observed_sources.append(Path(source_handle.name))
            real_copy(source_handle, target_handle)
            (self.env.repo / "state/mixed.md").write_bytes(b"mutated during capture\n")

        with mock.patch.object(pa.shutil, "copyfileobj", mutate_live_after_copy):
            with self.assertRaisesRegex(
                pa.PublicationAuthorityError,
                "live mixed source after snapshot capture",
            ):
                self.capture()
        self.assertEqual(len(observed_sources), 1)
        self.assertTrue(
            observed_sources[0].is_relative_to(self.env.original_evidence_root / "files")
        )
        self.assertFalse(self.snapshot_root.exists())

    def test_capture_refuses_inside_repository_or_existing_output(self):
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "outside|repository"):
            pa.capture_mixed_snapshot(
                self.env.mixed,
                repository_root=self.env.repo,
                output_root=self.env.repo / "snapshot",
                original_evidence_manifest=self.env.original_evidence_manifest,
                original_evidence_root=self.env.original_evidence_root,
            )
        self.snapshot_root.mkdir()
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "exist"):
            self.capture()

    def test_capture_rejects_partial_or_extra_live_population(self):
        (self.env.repo / "state/mixed.md").unlink()
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "missing|path|population"):
            self.capture()
        self.env._write(self.env.repo, "state/mixed.md", self.env.mixed_bytes, 0o644)
        mixed = copy.deepcopy(self.env.mixed)
        mixed["paths"].append({"path": "state/absent.md", "mode": "100644", "sha256": sha(b"x"), "size": 1})
        mixed["paths"].sort(key=lambda row: row["path"])
        mixed["path_count"] = 2
        mixed["manifest_fingerprint"] = fp(mixed, "manifest_fingerprint")
        with self.assertRaises(pa.PublicationAuthorityError):
            pa.capture_mixed_snapshot(
                mixed,
                repository_root=self.env.repo,
                output_root=self.snapshot_root,
                original_evidence_manifest=self.env.original_evidence_manifest,
                original_evidence_root=self.env.original_evidence_root,
            )

    def test_capture_rejects_symlink_and_non_regular_source(self):
        live = self.env.repo / "state/mixed.md"
        outside = self.env.root / "outside"
        outside.write_bytes(self.env.mixed_bytes)
        live.unlink()
        live.symlink_to(outside)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "symlink|regular"):
            self.capture()
        live.unlink()
        live.mkdir()
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "regular"):
            self.capture()

    def test_capture_preserves_exact_non_git_filesystem_modes(self):
        live = self.env.repo / "state/mixed.md"
        for mode in (0o600, 0o640, 0o664):
            with self.subTest(mode=oct(mode)):
                os.chmod(live, mode)
                root = self.env.root / f"snapshot-{mode:o}"
                original_manifest, original_root = self.original_evidence_for_mode(mode)
                manifest = pa.capture_mixed_snapshot(
                    self.env.mixed,
                    repository_root=self.env.repo,
                    output_root=root,
                    original_evidence_manifest=original_manifest,
                    original_evidence_root=original_root,
                )
                self.assertEqual(manifest["paths"][0]["filesystem_mode"], f"0o{mode:o}")
                self.assertEqual(os.stat(root / "files/state/mixed.md").st_mode & 0o777, mode)

    def test_candidate_root_may_be_a_full_workspace(self):
        manifest = self.capture()
        (self.env.mixed_root / "unrelated.txt").write_bytes(b"not part of mixed population\n")
        proof = self.proof(manifest)
        self.assertIs(proof["valid"], True)

    def test_verifies_live_snapshot_and_candidate_manifest_separately(self):
        manifest = self.capture()
        proof = self.proof(manifest)
        self.assertIs(proof["valid"], True)
        self.assertIn("protected_population_fingerprint", proof)
        self.assertIn("candidate_population_fingerprint", proof)
        self.assertNotEqual(
            proof["protected_population_fingerprint"],
            proof["candidate_population_fingerprint"],
        )

    def test_m1_overwrite_and_live_mutation_fail(self):
        candidate = b"external candidate bytes\n"
        candidate_path = self.env.mixed_root / "state/mixed.md"
        candidate_path.write_bytes(candidate)
        self.env.mixed["paths"][0]["sha256"] = sha(candidate)
        self.env.mixed["paths"][0]["size"] = len(candidate)
        self.env.mixed["manifest_fingerprint"] = fp(self.env.mixed, "manifest_fingerprint")
        manifest = self.capture()
        live = self.env.repo / "state/mixed.md"
        live.write_bytes(candidate)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "live|snapshot|identity|size"):
            self.proof(manifest)

    def test_capture_rejects_late_snapshot_after_m1_overwrite(self):
        candidate = b"candidate applied before snapshot\n"
        (self.env.mixed_root / "state/mixed.md").write_bytes(candidate)
        self.env.mixed["paths"][0]["sha256"] = sha(candidate)
        self.env.mixed["paths"][0]["size"] = len(candidate)
        self.env.mixed["manifest_fingerprint"] = fp(self.env.mixed, "manifest_fingerprint")
        (self.env.repo / "state/mixed.md").write_bytes(candidate)
        with self.assertRaisesRegex(
            pa.PublicationAuthorityError,
            "original|evidence|late|overwrite|live mixed source before snapshot capture",
        ):
            pa.capture_mixed_snapshot(
                self.env.mixed,
                repository_root=self.env.repo,
                output_root=self.env.root / "late-snapshot",
                original_evidence_manifest=self.env.original_evidence_manifest,
                original_evidence_root=self.env.original_evidence_root,
            )

    def test_missing_snapshot_bytes_or_hash_only_evidence_fails(self):
        manifest = self.capture()
        (self.snapshot_root / "files/state/mixed.md").unlink()
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "missing|snapshot|bytes"):
            self.proof(manifest)

    def test_mutated_snapshot_candidate_or_stale_parent_fails(self):
        manifest = self.capture()
        (self.snapshot_root / "files/state/mixed.md").write_bytes(b"mutated snapshot\n")
        with self.assertRaises(pa.PublicationAuthorityError):
            self.proof(manifest)
        (self.snapshot_root / "files/state/mixed.md").write_bytes(self.env.mixed_bytes)
        (self.env.mixed_root / "state/mixed.md").write_bytes(b"mutated candidate\n")
        with self.assertRaises(pa.PublicationAuthorityError):
            self.proof(manifest)
        (self.env.mixed_root / "state/mixed.md").write_bytes(self.env.mixed_bytes)
        self.env._write(self.env.repo, "later", b"later", 0o644)
        subprocess.run(["git", "-C", str(self.env.repo), "add", "later"], check=True)
        subprocess.run(["git", "-C", str(self.env.repo), "commit", "-qm", "later"], check=True)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "parent|HEAD|stale"):
            self.proof(manifest)

    def test_manifest_path_mode_size_hash_and_fingerprint_tampering_fails(self):
        manifest = self.capture()
        mutations = (
            lambda value: value["paths"].append({"path": "extra", "filesystem_mode": "0o644", "size": 0, "sha256": sha(b"")}),
            lambda value: value["paths"][0].__setitem__("filesystem_mode", "0o755"),
            lambda value: value["paths"][0].__setitem__("size", 99),
            lambda value: value["paths"][0].__setitem__("sha256", "0" * 64),
            lambda value: value.__setitem__("snapshot_fingerprint", "sha256:" + "0" * 64),
        )
        for mutate in mutations:
            bad = copy.deepcopy(manifest)
            mutate(bad)
            with self.subTest(bad=bad):
                with self.assertRaises(pa.PublicationAuthorityError):
                    self.proof(bad)

    def test_gate_requires_and_binds_preservation_proof(self):
        authority = self.env.build()
        self.env.activate_registry(authority)
        with self.assertRaisesRegex(pa.PublicationAuthorityError, "protected|preservation|snapshot"):
            pa.build_staging_gate(
                authority,
                self.env.complete,
                self.env.mixed,
                self.env.extra,
                repository_root=self.env.repo,
                source_roots=self.env.roots,
                validation_passed=True,
            )
        manifest = self.capture()
        gate = self.gate(authority, manifest)
        self.assertEqual(gate["mixed_snapshot_fingerprint"], manifest["snapshot_fingerprint"])
        self.assertIn("mixed_live_population_fingerprint", gate)
        self.assertIn("mixed_candidate_population_fingerprint", gate)
        (self.env.repo / "state/mixed.md").write_bytes(b"overwritten\n")
        with self.assertRaises(pa.PublicationAuthorityError):
            pa.verify_staging_gate(
                gate,
                authority,
                self.env.complete,
                self.env.mixed,
                self.env.extra,
                repository_root=self.env.repo,
                source_roots=self.env.roots,
                protected_mixed_manifest=manifest,
                protected_mixed_root=self.snapshot_root,
                original_evidence_manifest=self.env.original_evidence_manifest,
                original_evidence_root=self.env.original_evidence_root,
            )

    def test_cli_snapshot_and_protected_gate_options(self):
        tool = ROOT / "tools/publication_authority.py"
        mixed_path = self.env.root / "mixed.json"
        mixed_path.write_text(json.dumps(self.env.mixed) + "\n")
        subprocess.run(
            [
                "python3", "-B", str(tool), "snapshot-mixed",
                "--mixed", str(mixed_path),
                "--repository", str(self.env.repo),
                "--output-root", str(self.snapshot_root),
                "--original-evidence-manifest",
                str(self.env.original_evidence_root / "protected_mixed_manifest.json"),
                "--original-evidence-root", str(self.env.original_evidence_root),
            ],
            check=True,
        )
        self.assertTrue((self.snapshot_root / "protected_mixed_manifest.json").is_file())
        for command in ("gate", "verify-gate"):
            help_text = subprocess.run(
                ["python3", "-B", str(tool), command, "--help"], check=True,
                text=True, capture_output=True,
            ).stdout
            self.assertIn("--protected-mixed-manifest", help_text)
            self.assertIn("--protected-mixed-root", help_text)
            self.assertIn("--original-evidence-manifest", help_text)
            self.assertIn("--original-evidence-root", help_text)


if __name__ == "__main__":
    unittest.main()
