from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "relationship_export_v1.py"
SIM = ROOT / "tools" / "relationship_export_consumer_simulator_v1.py"
PROJECTION = ROOT / "tools" / "postgresql_operational_projection.py"
QUERY_DIR = ROOT / "specs" / "relationship_exports" / "queries"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RelationshipExportContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not all(shutil.which(name) for name in ("psql", "createdb", "dropdb")):
            raise unittest.SkipTest("PostgreSQL CLI unavailable")
        cls.export_tool = load_module(TOOL, "relationship_export_v1")
        cls.consumer = load_module(SIM, "relationship_export_consumer_simulator_v1")
        cls.projection = load_module(PROJECTION, "postgresql_operational_projection_relationship_test")
        cls.database = f"knowledgeforge_relationship_export_test_{os.getpid()}"
        subprocess.run(["dropdb", "--if-exists", cls.database], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["createdb", cls.database], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cls.projection.rebuild_projection(ROOT / "knowledge_repository", cls.database)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "database"):
            subprocess.run(["dropdb", "--if-exists", cls.database], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def test_query_validation_rejects_interpretive_filter(self):
        q = json.loads((QUERY_DIR / "malformed_unsupported_filter.json").read_text())
        with self.assertRaises(Exception):
            self.export_tool.validate_query(q)

    def test_query_validation_rejects_unbounded_results(self):
        q = json.loads((QUERY_DIR / "unbounded_result_probe.json").read_text())
        with self.assertRaises(Exception):
            self.export_tool.validate_query(q)

    def test_sql_injection_probe_is_literal_filter(self):
        q = json.loads((QUERY_DIR / "sql_injection_probe.json").read_text())
        qv = self.export_tool.validate_query(q)
        sql, shapes = self.export_tool.build_sql(qv, "projection-test")
        self.assertIn("DROP TABLE", sql)
        self.assertIn("''; DROP TABLE", sql)
        self.assertGreaterEqual(shapes["jsonb_payload_scans"], 1)

    def test_export_verification_detects_tampering(self):
        q = json.loads((QUERY_DIR / "zero_results.json").read_text())
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "zero.json"
            self.export_tool.export(q, path, db=self.database)
            self.assertTrue(self.export_tool.verify_export(path)["valid"])
            obj = json.loads(path.read_text())
            obj["deterministic_content"]["result_count"] = 999
            path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
            with self.assertRaises(Exception):
                self.export_tool.verify_export(path)

    def test_consumer_simulation_uses_export_only(self):
        q = json.loads((QUERY_DIR / "exact_package_id.json").read_text())
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "exact.json"
            self.export_tool.export(q, path, db=self.database)
            result = self.consumer.verify(path)
            self.assertTrue(result["valid"])
            self.assertFalse(result["independence"]["used_postgresql"])
            self.assertFalse(result["independence"]["read_canonical_repository"])
            self.assertEqual(result["result_count"], 1)

    def test_stale_projection_simulation_fails_closed(self):
        q = json.loads((QUERY_DIR / "zero_results.json").read_text())
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(Exception):
                self.export_tool.export(q, Path(td) / "stale.json", db=self.database, simulate_stale=True)


if __name__ == "__main__":
    unittest.main()
