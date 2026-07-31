from __future__ import annotations

import copy
import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "knowledge_repository.py"
CAMPAIGN12_OBJECTS = PROJECT_ROOT / "artifacts" / "production" / "campaign-12-wdi-environment-provenance-lineage-closeout" / "knowledge_object_packages.json"


def load_repository_module():
    spec = importlib.util.spec_from_file_location("knowledge_repository", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class KnowledgeRepositoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_repository_module()
        self.sample_package = json.loads(CAMPAIGN12_OBJECTS.read_text())[0]

    def assert_hard_linked_output_is_rejected(self, relative_path: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            self.module.persist_knowledge_object_packages([self.sample_package], repo)
            destination = repo / relative_path
            outside = base / "outside.json"
            outside.write_text(json.dumps(json.loads(destination.read_text())))
            destination.unlink()
            os.link(outside, destination)
            before = {
                path.relative_to(repo): path.read_bytes()
                for path in repo.rglob("*")
                if path.is_file()
            }
            outside_before = outside.read_bytes()

            with self.assertRaisesRegex(ValueError, "hard.?link|multiple links"):
                self.module.persist_knowledge_object_packages([self.sample_package], repo)

            self.assertEqual(outside.read_bytes(), outside_before)
            self.assertEqual(
                {
                    path.relative_to(repo): path.read_bytes()
                    for path in repo.rglob("*")
                    if path.is_file()
                },
                before,
            )

    def test_persist_validated_knowledge_object_package_without_rewriting_package_model(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            result = self.module.persist_knowledge_object_packages([self.sample_package], repo)

            object_path = repo / "objects" / f"{self.sample_package['package_id']}.json"
            self.assertTrue(object_path.exists())
            persisted = json.loads(object_path.read_text())
            self.assertEqual(persisted, self.sample_package)
            self.assertEqual(result["persisted_count"], 1)
            self.assertEqual(result["rejected_count"], 0)
            self.assertEqual(result["repository_root"], str(repo))

            self.assertEqual(persisted["package_kind"], "KnowledgeObjectPackage")
            self.assertEqual(persisted["provenance_envelope"], self.sample_package["provenance_envelope"])
            self.assertEqual(persisted["fingerprints"], self.sample_package["fingerprints"])
            self.assertEqual(persisted["validation_state"], self.sample_package["validation_state"])
            self.assertEqual(persisted["confidence_quality"]["lifecycle_state"], "accepted")
            self.assertEqual(persisted["confidence_quality"]["reproducibility_state"], "reproducible")

    def test_indexes_make_persisted_knowledge_retrievable_by_owned_knowledgeforge_identity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            self.module.persist_knowledge_object_packages([self.sample_package], repo)

            indexes = repo / "indexes"
            package_id = self.sample_package["package_id"]
            statement_id = self.sample_package["generated_statements"][0]["statement_id"]
            evidence_family = self.sample_package["scope"]["evidence_family"]
            statement_type = self.sample_package["generated_statements"][0]["statement_type"]
            lifecycle = self.sample_package["confidence_quality"]["lifecycle_state"]
            package_manifest = self.sample_package["fingerprints"]["package_manifest"]

            by_package = json.loads((indexes / "by_package_id.json").read_text())
            by_knowledge = json.loads((indexes / "by_knowledge_identity.json").read_text())
            by_family = json.loads((indexes / "by_evidence_family.json").read_text())
            by_type = json.loads((indexes / "by_statement_type.json").read_text())
            by_lifecycle = json.loads((indexes / "by_lifecycle_state.json").read_text())
            by_fingerprint = json.loads((indexes / "by_package_manifest_fingerprint.json").read_text())

            self.assertEqual(by_package[package_id], f"objects/{package_id}.json")
            self.assertEqual(by_knowledge[statement_id], [package_id])
            self.assertEqual(by_family[evidence_family], [package_id])
            self.assertEqual(by_type[statement_type], [package_id])
            self.assertEqual(by_lifecycle[lifecycle], [package_id])
            self.assertEqual(by_fingerprint[package_manifest], [package_id])

    def test_repository_manifest_records_version_evolution_provenance_and_deterministic_fingerprint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            first = self.module.persist_knowledge_object_packages([self.sample_package], repo)
            second = self.module.persist_knowledge_object_packages([self.sample_package], repo)
            manifest = json.loads((repo / "manifest.json").read_text())
            evolution = json.loads((repo / "evolution" / f"{self.sample_package['package_id']}.json").read_text())

            self.assertEqual(first["repository_fingerprint"], second["repository_fingerprint"])
            self.assertEqual(manifest["repository_kind"], "KnowledgeForgeKnowledgeRepository")
            self.assertEqual(manifest["schema_version"], "1.0")
            self.assertEqual(manifest["object_count"], 1)
            self.assertEqual(manifest["package_ids"], [self.sample_package["package_id"]])
            self.assertEqual(manifest["repository_fingerprint"], first["repository_fingerprint"])
            self.assertEqual(evolution["package_id"], self.sample_package["package_id"])
            self.assertEqual(evolution["lineage"], self.sample_package["lineage"])
            self.assertEqual(evolution["evolution_metadata"], self.sample_package["evolution_metadata"])
            self.assertEqual(evolution["provenance_envelope"], self.sample_package["provenance_envelope"])

    def test_rejects_packages_that_are_not_validated_knowledge_objects(self) -> None:
        invalid = dict(self.sample_package)
        invalid["package_kind"] = "KnowledgeCandidatePackage"
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            with self.assertRaises(ValueError) as ctx:
                self.module.persist_knowledge_object_packages([invalid], repo)
            self.assertIn("KnowledgeObjectPackage", str(ctx.exception))

        blocked = json.loads(json.dumps(self.sample_package))
        blocked["validation_state"] = {"validation_result": "blocked", "blockers": [{"category": "provenance"}]}
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            with self.assertRaises(ValueError) as ctx:
                self.module.persist_knowledge_object_packages([blocked], repo)
            self.assertIn("validation blockers", str(ctx.exception))

    def test_rejects_non_identical_overwrite_of_existing_canonical_package(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            self.module.persist_knowledge_object_packages([self.sample_package], repo)
            object_path = repo / "objects" / f"{self.sample_package['package_id']}.json"
            before = object_path.read_bytes()

            mutated = json.loads(json.dumps(self.sample_package))
            mutated["confidence_quality"]["lifecycle_state"] = "superseded"
            with self.assertRaises(ValueError) as ctx:
                self.module.persist_knowledge_object_packages([mutated], repo)

            self.assertIn("canonical package overwrite is forbidden", str(ctx.exception))
            self.assertEqual(object_path.read_bytes(), before)

    def test_rejects_malicious_package_ids_before_any_repository_persistence(self) -> None:
        probes = ["x/../../../../tmp/knowledgeforge-escape", "/tmp/knowledgeforge-escape", r"x\\..\\escape", "..", ".hidden", "unsafe value"]
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            for index, package_id in enumerate(probes):
                repo = base / f"repo-{index}"
                outside = base / "knowledgeforge-escape.json"
                package = copy.deepcopy(self.sample_package)
                package["package_id"] = package_id
                with self.subTest(package_id=package_id), self.assertRaisesRegex(ValueError, "package_id"):
                    self.module.persist_knowledge_object_packages([package], repo)
                self.assertFalse(repo.exists())
                self.assertFalse(outside.exists())

    def test_rejects_symlinked_repository_root_before_any_external_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            outside = base / "outside"
            outside.mkdir()
            (outside / "sentinel").write_bytes(b"unchanged\n")
            repo.symlink_to(outside, target_is_directory=True)
            before = {path.name: path.read_bytes() for path in outside.iterdir()}

            with self.assertRaisesRegex(ValueError, "root.*symlink|symlink.*root"):
                self.module.persist_knowledge_object_packages([self.sample_package], repo)

            self.assertEqual({path.name: path.read_bytes() for path in outside.iterdir()}, before)
            self.assertTrue(repo.is_symlink())

    def test_authenticate_repository_rejects_symlinked_repository_root_read_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            real_repo = base / "real-repo"
            expected = self.module.persist_knowledge_object_packages([self.sample_package], real_repo)
            before = {
                path.relative_to(real_repo): path.read_bytes()
                for path in real_repo.rglob("*")
                if path.is_file()
            }
            repo = base / "repo"
            repo.symlink_to(real_repo, target_is_directory=True)

            with self.assertRaisesRegex(ValueError, "root.*symlink|symlink.*root"):
                self.module.authenticate_repository(repo)

            self.assertEqual(
                {
                    path.relative_to(real_repo): path.read_bytes()
                    for path in real_repo.rglob("*")
                    if path.is_file()
                },
                before,
            )
            self.assertTrue(expected["repository_fingerprint"])

    def test_rejects_symlinked_object_directory_that_escapes_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = base / "repo"
            outside = base / "outside"
            repo.mkdir()
            outside.mkdir()
            (repo / "objects").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "escapes repository"):
                self.module.persist_knowledge_object_packages([self.sample_package], repo)
            self.assertEqual(list(outside.iterdir()), [])


    def test_rejects_symlinked_indexes_directory_before_any_canonical_write(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); repo = base / "repo"; outside = base / "outside"
            repo.mkdir(); outside.mkdir()
            (repo / "indexes").symlink_to(outside, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "indexes.*symlink|symlink.*indexes"):
                self.module.persist_knowledge_object_packages([self.sample_package], repo)
            self.assertEqual(list(outside.iterdir()), [])
            self.assertFalse((repo / "objects").exists())
            self.assertFalse((repo / "evolution").exists())
            self.assertFalse((repo / "manifest.json").exists())

    def test_rejects_symlinked_manifest_before_any_canonical_write_or_outside_change(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp); repo = base / "repo"; outside = base / "outside-manifest.json"
            repo.mkdir(); outside.write_bytes(b"outside sentinel\n")
            (repo / "manifest.json").symlink_to(outside)
            before = outside.read_bytes()
            with self.assertRaisesRegex(ValueError, "manifest.*symlink|symlink.*manifest"):
                self.module.persist_knowledge_object_packages([self.sample_package], repo)
            self.assertEqual(outside.read_bytes(), before)
            self.assertFalse((repo / "objects").exists())
            self.assertFalse((repo / "indexes").exists())
            self.assertFalse((repo / "evolution").exists())

    def test_rejects_hard_linked_manifest_before_any_canonical_write_or_outside_change(self) -> None:
        self.assert_hard_linked_output_is_rejected("manifest.json")

    def test_rejects_hard_linked_index_before_any_canonical_write_or_outside_change(self) -> None:
        self.assert_hard_linked_output_is_rejected("indexes/by_package_id.json")

    def test_rejects_hard_linked_evolution_before_any_canonical_write_or_outside_change(self) -> None:
        package_id = self.sample_package["package_id"]
        self.assert_hard_linked_output_is_rejected(f"evolution/{package_id}.json")

    def test_rejects_hard_linked_object_before_any_canonical_write_or_outside_change(self) -> None:
        package_id = self.sample_package["package_id"]
        self.assert_hard_linked_output_is_rejected(f"objects/{package_id}.json")

    def test_authenticate_repository_rejects_each_tampered_canonical_component(self) -> None:
        mutations = {
            "object": lambda repo, pid: (repo / "objects" / f"{pid}.json").write_text("{}\n"),
            "index": lambda repo, _pid: (repo / "indexes" / "by_package_id.json").write_text("{}\n"),
            "evolution": lambda repo, pid: (repo / "evolution" / f"{pid}.json").write_text("{}\n"),
            "manifest": lambda repo, _pid: (repo / "manifest.json").write_text(json.dumps({"object_count": 1, "repository_fingerprint": "sha256:" + "6" * 64})),
        }
        for component, mutate in mutations.items():
            with self.subTest(component=component), tempfile.TemporaryDirectory() as tmp:
                repo = Path(tmp) / "repo"
                expected = self.module.persist_knowledge_object_packages([self.sample_package], repo)
                self.assertEqual(
                    self.module.authenticate_repository(repo),
                    {"object_count": 1, "repository_fingerprint": expected["repository_fingerprint"]},
                )
                mutate(repo, self.sample_package["package_id"])
                with self.assertRaisesRegex(ValueError, "repository"):
                    self.module.authenticate_repository(repo)

    def test_authenticate_valid_empty_repository(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            expected = self.module.persist_knowledge_object_packages([], repo)
            self.assertEqual(self.module.authenticate_repository(repo), {
                "object_count": 0,
                "repository_fingerprint": expected["repository_fingerprint"],
            })

    def test_authenticate_allows_governed_summaries_beside_canonical_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            expected = self.module.persist_knowledge_object_packages([self.sample_package], repo)
            for directory in ("objects", "evolution", "indexes"):
                (repo / directory / "_SUMMARY.md").write_text(f"# Curated {directory} summary\n")

            self.assertEqual(
                self.module.authenticate_repository(repo),
                {"object_count": 1, "repository_fingerprint": expected["repository_fingerprint"]},
            )

    def test_authenticate_exact_byte_copy_with_portable_root_at_another_location(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            previous_cwd = Path.cwd()
            try:
                os.chdir(base)
                source = Path("knowledge_repository")
                expected = self.module.persist_knowledge_object_packages([self.sample_package], source)
                self.assertEqual(json.loads((source / "manifest.json").read_text())["repository_root"], "knowledge_repository")
                clone = Path("detached-clone")
                shutil.copytree(source, clone)
                before = {
                    path.relative_to(clone): path.read_bytes()
                    for path in clone.rglob("*")
                    if path.is_file()
                }
                result = self.module.authenticate_repository(clone)
                after = {
                    path.relative_to(clone): path.read_bytes()
                    for path in clone.rglob("*")
                    if path.is_file()
                }
            finally:
                os.chdir(previous_cwd)

            self.assertEqual(result, {"object_count": 1, "repository_fingerprint": expected["repository_fingerprint"]})
            self.assertEqual(after, before)

    def test_authenticate_rejects_unexpected_json_in_each_canonical_directory(self) -> None:
        for directory in ("objects", "evolution", "indexes"):
            with self.subTest(directory=directory), tempfile.TemporaryDirectory() as tmp:
                repo = Path(tmp) / "repo"
                self.module.persist_knowledge_object_packages([self.sample_package], repo)
                (repo / directory / "unexpected.json").write_text("{}\n")
                with self.assertRaisesRegex(ValueError, "repository authentication failed"):
                    self.module.authenticate_repository(repo)

    def test_authenticate_rejects_non_governed_extra_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "repo"
            self.module.persist_knowledge_object_packages([self.sample_package], repo)
            (repo / "objects" / "NOTES.md").write_text("not governed\n")
            with self.assertRaisesRegex(ValueError, "population mismatch"):
                self.module.authenticate_repository(repo)

    def test_authenticate_rejects_symlinked_or_hard_linked_governed_summary(self) -> None:
        for link_kind in ("symlink", "hardlink"):
            with self.subTest(link_kind=link_kind), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                repo = base / "repo"
                self.module.persist_knowledge_object_packages([self.sample_package], repo)
                outside = base / "summary.md"
                outside.write_text("# Summary\n")
                summary = repo / "objects" / "_SUMMARY.md"
                if link_kind == "symlink":
                    summary.symlink_to(outside)
                else:
                    os.link(outside, summary)
                with self.assertRaisesRegex(ValueError, "symlink|hard.?link|multiple links"):
                    self.module.authenticate_repository(repo)

    def test_authenticate_rejects_symlinked_or_hard_linked_canonical_json(self) -> None:
        for link_kind in ("symlink", "hardlink"):
            with self.subTest(link_kind=link_kind), tempfile.TemporaryDirectory() as tmp:
                base = Path(tmp)
                repo = base / "repo"
                self.module.persist_knowledge_object_packages([self.sample_package], repo)
                canonical = repo / "objects" / f"{self.sample_package['package_id']}.json"
                outside = base / "object.json"
                outside.write_bytes(canonical.read_bytes())
                canonical.unlink()
                if link_kind == "symlink":
                    canonical.symlink_to(outside)
                else:
                    os.link(outside, canonical)
                with self.assertRaisesRegex(ValueError, "symlink|hard.?link|multiple links"):
                    self.module.authenticate_repository(repo)


if __name__ == "__main__":
    unittest.main()
