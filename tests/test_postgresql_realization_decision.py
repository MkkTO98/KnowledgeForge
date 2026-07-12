from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "postgresql_realization_decision.py"


def load_module():
    spec = importlib.util.spec_from_file_location("postgresql_realization_decision", MODULE_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class PostgreSQLRealizationDecisionTests(unittest.TestCase):
    def test_decision_selects_option_b_without_canonical_authority_transfer(self) -> None:
        module = load_module()
        repo = PROJECT_ROOT / "knowledge_repository"
        packages = module.load_packages(repo)
        result = module.build_decision(packages, repo, repeat=1)
        self.assertEqual(result["selected_option"], "B")
        self.assertTrue(result["decision_answers"]["is_postgresql_justified_now"])
        self.assertFalse(result["scale_and_performance"]["performance_conclusion"]["postgresql_required_today_for_performance"])
        self.assertFalse(result["authority_and_consistency_model"]["may_postgresql_originate_or_mutate_canonical_knowledge"])
        self.assertTrue(result["authority_and_consistency_model"]["fully_rebuildable_from_packages"])
        self.assertFalse(result["authority_and_consistency_model"]["postgresql_in_canonical_fingerprints"])
        self.assertIn("Full KnowledgeObjectPackage JSON", result["authority_and_consistency_model"]["canonical_authority"])

    def test_option_matrix_rejects_coauthoritative_and_new_canonical_roles(self) -> None:
        module = load_module()
        result = module.build_option_matrix()
        self.assertEqual(result["selected_option"], "B")
        self.assertEqual(result["options"]["C"]["decision"], "reject")
        self.assertEqual(result["options"]["D"]["decision"], "reject")
        self.assertEqual(result["options"]["E"]["decision"], "reject")
        self.assertEqual(result["options"]["D"]["classification"], "unsupported expansion")

    def test_required_operational_requirements_are_evidence_backed(self) -> None:
        module = load_module()
        repo = PROJECT_ROOT / "knowledge_repository"
        packages = module.load_packages(repo)
        req = module.derive_supported_requirements(packages, repo)
        requirements = {item["requirement"]: item for item in req["requirements"]}
        for key in [
            "lookup_by_package_id",
            "filter_by_family",
            "fingerprint_lookup_and_verification",
            "provenance_and_lineage_traversal",
            "reproducible_repository_snapshots",
            "bulk_retrieval_for_downstream_analysis",
        ]:
            self.assertTrue(requirements[key]["supported_by_current_evidence"], key)

    def test_writes_machine_matrix_and_report_without_sql_ddl(self) -> None:
        module = load_module()
        repo = PROJECT_ROOT / "knowledge_repository"
        packages = module.load_packages(repo)
        result = module.build_decision(packages, repo, repeat=1)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "decision"
            module.write_report(out, result)
            matrix = json.loads((out / "postgresql_realization_options_evidence_matrix.json").read_text())
            report = (out / "bounded_postgresql_realization_decision_report.md").read_text()
        self.assertEqual(matrix["selected_option"], "B")
        for forbidden in ["CREATE TABLE", "ALTER TABLE", "CREATE INDEX", "INSERT INTO", "CREATE SCHEMA"]:
            self.assertNotIn(forbidden, report.upper())
            self.assertNotIn(forbidden, json.dumps(matrix).upper())


if __name__ == "__main__":
    unittest.main()
