from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "repository_scale_doctrine_review.py"
SAMPLE_PACKAGES = PROJECT_ROOT / "artifacts" / "production" / "campaign-32-wdi-financial-sector-indicator-family-coverage-maturation" / "knowledge_object_packages.json"


def load_module():
    spec = importlib.util.spec_from_file_location("repository_scale_doctrine_review", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RepositoryScaleDoctrineReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.module = load_module()
        self.packages = json.loads(SAMPLE_PACKAGES.read_text())

    def test_primary_type_classification_is_non_overlapping_and_complete(self) -> None:
        metrics = self.module.composition_metrics(self.packages)
        self.assertEqual(metrics["object_count"], 36)
        self.assertEqual(metrics["primary_type_count_sum"], 36)
        self.assertGreater(metrics["primary_type_counts_no_double_count"]["coverage"], 0)
        self.assertGreater(metrics["primary_type_counts_no_double_count"]["deterministic_derived_indicators"], 0)
        self.assertGreater(metrics["primary_type_counts_no_double_count"]["classifications"], 0)
        self.assertIn("category_flag_counts_with_overlap", metrics)

    def test_duplicate_detection_flags_exact_and_normalised_duplicate_statement_text(self) -> None:
        a = json.loads(json.dumps(self.packages[0]))
        b = json.loads(json.dumps(self.packages[0]))
        b["package_id"] = b["package_id"] + "-copy"
        b["generated_statements"][0]["statement_id"] = b["generated_statements"][0]["statement_id"] + "-copy"
        result = self.module.duplicate_metrics([a, b])
        self.assertFalse(result["duplication_pass"])
        self.assertEqual(result["exact_duplicate_statement_text_groups"], 1)
        self.assertEqual(result["semantic_recurrence_statement_text_groups"], 1)

    def test_review_on_temp_repository_rebuilds_deterministically_and_preserves_doctrine_verdict(self) -> None:
        repo_module_path = PROJECT_ROOT / "tools" / "knowledge_repository.py"
        spec = importlib.util.spec_from_file_location("knowledge_repository", repo_module_path)
        assert spec is not None and spec.loader is not None
        repo_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(repo_module)
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "knowledge_repository"
            repo_module.persist_knowledge_object_packages(self.packages, repo)
            metrics = self.module.run_review(repo, repeat=1)
        self.assertTrue(metrics["repository_health"]["repository_health_pass"])
        self.assertTrue(metrics["index_determinism"]["index_determinism_pass"])
        self.assertTrue(metrics["deterministic_rebuild"]["deterministic_rebuild_pass"])
        self.assertEqual(metrics["decision"]["recommendation"], "B")
        self.assertIn("doctrine", metrics["decision"]["doctrine_sufficiency_verdict"].lower())


if __name__ == "__main__":
    unittest.main()
