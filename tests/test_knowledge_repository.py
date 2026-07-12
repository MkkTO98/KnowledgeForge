from __future__ import annotations

import importlib.util
import json
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


if __name__ == "__main__":
    unittest.main()
