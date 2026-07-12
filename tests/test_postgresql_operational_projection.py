from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "postgresql_operational_projection.py"
REPOSITORY_ROOT = PROJECT_ROOT / "knowledge_repository"
EXPECTED_REPOSITORY_MANIFEST = json.loads((REPOSITORY_ROOT / "manifest.json").read_text())
EXPECTED_OBJECT_COUNT = EXPECTED_REPOSITORY_MANIFEST["object_count"]
EXPECTED_REPOSITORY_FINGERPRINT = EXPECTED_REPOSITORY_MANIFEST["repository_fingerprint"]


def load_module():
    spec = importlib.util.spec_from_file_location("postgresql_operational_projection", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def have_postgres_tools() -> bool:
    return all(shutil.which(cmd) for cmd in ("psql", "createdb", "dropdb"))


class PostgreSQLOperationalProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not have_postgres_tools():
            raise unittest.SkipTest("PostgreSQL CLI tools unavailable; integration test explicitly skipped")
        probe = subprocess.run(
            ["psql", "-d", "postgres", "-Atc", "SELECT 1"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if probe.returncode != 0:
            raise unittest.SkipTest(f"PostgreSQL unavailable: {probe.stderr.strip()}")

    def setUp(self):
        self.module = load_module()
        self.database = f"knowledgeforge_projection_test_{os.getpid()}_{self._testMethodName.lower()}"
        subprocess.run(["createdb", self.database], check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def tearDown(self):
        subprocess.run(["dropdb", "--if-exists", self.database], check=False, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_full_rebuild_loads_current_packages_with_payload_fidelity_and_fresh_retrieval(self):
        before = self.module.snapshot_canonical_package_bytes(REPOSITORY_ROOT)
        rebuild = self.module.rebuild_projection(REPOSITORY_ROOT, self.database)
        self.assertTrue(rebuild["valid"])
        self.assertEqual(EXPECTED_OBJECT_COUNT, rebuild["object_count"])
        self.assertEqual(EXPECTED_REPOSITORY_FINGERPRINT, rebuild["repository_fingerprint"])

        verification = self.module.verify_projection(REPOSITORY_ROOT, self.database)
        self.assertTrue(verification["valid"])
        self.assertEqual(EXPECTED_OBJECT_COUNT, verification["projected_object_count"])
        self.assertEqual([], verification["missing_package_ids"])
        self.assertEqual([], verification["extra_package_ids"])
        self.assertEqual(0, verification["payload_fidelity_failures"])
        self.assertEqual(0, verification["package_fingerprint_failures"])
        self.assertEqual(before, self.module.snapshot_canonical_package_bytes(REPOSITORY_ROOT))

        lookup = self.module.lookup_package(
            REPOSITORY_ROOT,
            self.database,
            "pkg-object-srcpkg-campaign33-architectural-continuity-review",
        )
        self.assertTrue(lookup["valid"])
        self.assertEqual("pkg-object-srcpkg-campaign33-architectural-continuity-review", lookup["package"]["package_id"])
        self.assertTrue(lookup["package"]["canonical_path"].endswith("objects/pkg-object-srcpkg-campaign33-architectural-continuity-review.json"))

    def test_rebuild_is_idempotent_and_order_independent_and_removes_stale_rows(self):
        first = self.module.rebuild_projection(REPOSITORY_ROOT, self.database)
        self.assertTrue(first["valid"])
        self.module.inject_stale_test_row(self.database, "pkg-object-stale-test-row")
        second = self.module.rebuild_projection(REPOSITORY_ROOT, self.database)
        reverse = self.module.rebuild_projection(REPOSITORY_ROOT, self.database, traversal_order="reverse")
        self.assertTrue(second["valid"])
        self.assertTrue(reverse["valid"])
        self.assertEqual(first["logical_projection_fingerprint"], second["logical_projection_fingerprint"])
        self.assertEqual(first["logical_projection_fingerprint"], reverse["logical_projection_fingerprint"])
        self.assertEqual(EXPECTED_OBJECT_COUNT, second["object_count"])
        self.assertFalse(self.module.package_exists_in_projection(self.database, "pkg-object-stale-test-row"))

    def test_stale_or_failed_projection_fails_closed_for_retrieval(self):
        rebuild = self.module.rebuild_projection(REPOSITORY_ROOT, self.database)
        self.assertTrue(rebuild["valid"])
        self.module.mark_projection_invalid_for_test(self.database, repository_fingerprint="sha256:deliberately-wrong")
        result = self.module.lookup_package(
            REPOSITORY_ROOT,
            self.database,
            "pkg-object-srcpkg-campaign33-architectural-continuity-review",
        )
        self.assertFalse(result["valid"])
        self.assertEqual("stale_or_invalid_projection", result["error"])
        self.assertNotIn("package", result)

        self.module.create_failed_build_marker_for_test(self.database)
        failed_build_result = self.module.lookup_package(
            REPOSITORY_ROOT,
            self.database,
            "pkg-object-srcpkg-campaign33-architectural-continuity-review",
        )
        self.assertFalse(failed_build_result["valid"])
        self.assertEqual("stale_or_invalid_projection", failed_build_result["error"])
        self.assertNotIn("package", failed_build_result)

    def test_supported_filter_operations_are_deterministic(self):
        self.assertTrue(self.module.rebuild_projection(REPOSITORY_ROOT, self.database)["valid"])
        by_family_1 = self.module.filter_packages(
            REPOSITORY_ROOT,
            self.database,
            evidence_family="external_wdi_annual_scalar_financial_sector_provenance_lineage",
        )
        by_family_2 = self.module.filter_packages(
            REPOSITORY_ROOT,
            self.database,
            evidence_family="external_wdi_annual_scalar_financial_sector_provenance_lineage",
        )
        self.assertTrue(by_family_1["valid"])
        self.assertEqual(by_family_1, by_family_2)
        self.assertEqual(17, len(by_family_1["package_ids"]))
        by_statement = self.module.filter_packages(REPOSITORY_ROOT, self.database, statement_type="methodological")
        self.assertTrue(by_statement["valid"])
        self.assertEqual(sorted(by_statement["package_ids"]), by_statement["package_ids"])
        by_lifecycle = self.module.filter_packages(REPOSITORY_ROOT, self.database, lifecycle_state="accepted")
        self.assertTrue(by_lifecycle["valid"])
        self.assertEqual(EXPECTED_OBJECT_COUNT, len(by_lifecycle["package_ids"]))
        provenance = self.module.provenance_lineage(REPOSITORY_ROOT, self.database, "pkg-object-srcpkg-campaign33-architectural-continuity-review")
        self.assertTrue(provenance["valid"])
        self.assertTrue(any(row["relation_type"] == "evidence_ref" for row in provenance["relationships"]))
        self.assertTrue(any(row["relation_type"] == "previous_package_id" for row in provenance["relationships"]))

    def test_database_isolation_targets_only_named_knowledgeforge_database(self):
        self.assertTrue(self.module.rebuild_projection(REPOSITORY_ROOT, self.database)["valid"])
        isolation = self.module.inspect_database_isolation(self.database)
        self.assertEqual(self.database, isolation["database"])
        self.assertEqual("knowledgeforge_projection", isolation["schema"])
        self.assertEqual([], isolation["non_knowledgeforge_schemas_with_projection_tables"])
        self.assertNotIn("macroforge", self.database)


if __name__ == "__main__":
    unittest.main()
