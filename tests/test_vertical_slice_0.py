from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate_vertical_slice_0.py"
OBJECTS_DIR = PROJECT_ROOT / "knowledge" / "objects"
CLAIM_FILE = "claim-gdp-measures-aggregate-economic-output.json"
CONCEPT_FILE = "concept-gdp.json"
EVIDENCE_FILE = "evidence-ref-gdp-source-documentation.json"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_vertical_slice_0", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class VerticalSlice0Test(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator_module()

    def make_temp_project(self) -> Path:
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        root = Path(temp_dir.name)
        target = root / "knowledge" / "objects"
        target.mkdir(parents=True)
        for source in OBJECTS_DIR.glob("*.json"):
            shutil.copy2(source, target / source.name)
        return root

    def mutate_object(self, project_root: Path, file_name: str, mutator) -> None:
        path = project_root / "knowledge" / "objects" / file_name
        data = json.loads(path.read_text(encoding="utf-8"))
        mutator(data)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def assert_validation_fails(self, project_root: Path, expected_message_part: str) -> None:
        with self.assertRaises(self.validator.ValidationError) as raised:
            self.validator.validate_vertical_slice_0(project_root)
        self.assertIn(expected_message_part, str(raised.exception))

    def test_four_object_ecosystem_validates_core_architecture(self):
        result = self.validator.validate_vertical_slice_0(PROJECT_ROOT)

        self.assertTrue(result["ok"])
        self.assertEqual(result["object_count"], 4)
        self.assertEqual(
            result["object_ids"],
            [
                "claim-gdp-measures-aggregate-economic-output",
                "concept-aggregate-economic-output",
                "concept-gdp",
                "evidence-ref-gdp-source-documentation",
            ],
        )
        self.assertEqual(
            result["claim_dependencies"],
            [
                "concept-gdp",
                "concept-aggregate-economic-output",
                "evidence-ref-gdp-source-documentation",
            ],
        )
        self.assertTrue(result["representation_neutral"])

    def test_fixtures_do_not_add_excluded_object_types(self):
        self.assertTrue(OBJECTS_DIR.exists())
        object_files = sorted(p.name for p in OBJECTS_DIR.glob("*.json"))

        self.assertEqual(
            object_files,
            [
                "claim-gdp-measures-aggregate-economic-output.json",
                "concept-aggregate-economic-output.json",
                "concept-gdp.json",
                "evidence-ref-gdp-source-documentation.json",
            ],
        )
        self.assertFalse(any(name.startswith("dependency-") for name in object_files))
        self.assertFalse(any(name.startswith("relationship-") for name in object_files))
        self.assertFalse(any(name.startswith("mapping-") for name in object_files))

    def test_claim_owns_dependency_posture_and_revision_history(self):
        claim_path = OBJECTS_DIR / CLAIM_FILE
        claim = json.loads(claim_path.read_text(encoding="utf-8"))

        self.assertEqual(claim["stable_id"], "claim-gdp-measures-aggregate-economic-output")
        self.assertEqual(claim["object_kind"], "claim")
        self.assertEqual(claim["dependency_posture"]["state"], "dependencies listed")
        self.assertEqual(
            [item["object_id"] for item in claim["dependency_posture"]["dependencies"]],
            [
                "concept-gdp",
                "concept-aggregate-economic-output",
                "evidence-ref-gdp-source-documentation",
            ],
        )
        self.assertGreaterEqual(len(claim["revision_history"]), 2)
        self.assertEqual(
            {revision["stable_id"] for revision in claim["revision_history"]},
            {"claim-gdp-measures-aggregate-economic-output"},
        )

    def test_missing_required_durable_object_kernel_field_fails(self):
        project = self.make_temp_project()
        self.mutate_object(project, CONCEPT_FILE, lambda data: data.pop("provenance"))

        self.assert_validation_fails(project, "missing kernel fields")

    def test_unresolved_claim_dependency_fails(self):
        project = self.make_temp_project()

        def mutate(data):
            data["dependency_posture"]["dependencies"][0]["object_id"] = "concept-missing"

        self.mutate_object(project, CLAIM_FILE, mutate)

        self.assert_validation_fails(project, "points to unknown object")

    def test_duplicated_observational_values_fail(self):
        project = self.make_temp_project()

        def mutate(data):
            data["observational_values"] = [100.0, 101.5, 103.2]

        self.mutate_object(project, EVIDENCE_FILE, mutate)

        self.assert_validation_fails(project, "observational dataset values")

    def test_representation_specific_fields_fail(self):
        project = self.make_temp_project()

        def mutate(data):
            data["graph_node_id"] = "node:concept-gdp"

        self.mutate_object(project, CONCEPT_FILE, mutate)

        self.assert_validation_fails(project, "representation-specific field")


if __name__ == "__main__":
    unittest.main()
