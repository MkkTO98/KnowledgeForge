from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate_knowledge_pipeline_v1.py"
FIXTURES = PROJECT_ROOT / "tests" / "fixtures" / "validation_framework_v1"


def load_validator_module():
    spec = importlib.util.spec_from_file_location("validate_knowledge_pipeline_v1", VALIDATOR_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture(name: str):
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


class ValidationFrameworkV1Test(unittest.TestCase):
    def setUp(self):
        self.validator = load_validator_module()

    def assert_valid(self, report):
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["blockers"], [])

    def assert_blocks(self, report, category: str, message_part: str):
        self.assertFalse(report["ok"], report)
        categories = [finding["category"] for finding in report["blockers"]]
        self.assertIn(category, categories, report)
        self.assertTrue(any(message_part in finding["message"] for finding in report["blockers"]), report)

    def test_positive_fixtures_validate_independently_at_each_pipeline_stage(self):
        self.assert_valid(self.validator.validate_evidence(fixture("positive_evidence")))
        self.assert_valid(self.validator.validate_evidence_evaluation(fixture("positive_evidence_evaluation")))
        self.assert_valid(self.validator.validate_knowledge_candidate(fixture("positive_candidate")))
        self.assert_valid(self.validator.validate_knowledge_object(fixture("positive_knowledge_object")))
        self.assert_valid(self.validator.validate_knowledge_change(fixture("positive_knowledge_change")))

    def test_evidence_validation_rejects_malformed_inputs_before_processing(self):
        self.assert_blocks(
            self.validator.validate_evidence(fixture("negative_evidence_missing_source_identity")),
            "evidence_contract",
            "source_identity",
        )
        self.assert_blocks(
            self.validator.validate_evidence(fixture("negative_evidence_missing_fingerprint")),
            "provenance",
            "fingerprint",
        )
        self.assert_blocks(
            self.validator.validate_evidence(fixture("negative_evidence_llm_direct_evidence")),
            "constitutional_boundary",
            "LLM output cannot be direct evidence",
        )

    def test_evidence_evaluation_validation_enforces_separation_and_no_interpretation(self):
        self.assert_blocks(
            self.validator.validate_evidence_evaluation(fixture("negative_evaluation_collapsed_evidence")),
            "evidence_contract",
            "must not embed evidence",
        )
        self.assert_blocks(
            self.validator.validate_evidence_evaluation(fixture("negative_evaluation_forbidden_interpretation")),
            "unsupported_inference",
            "forbidden interpretation language",
        )
        self.assert_blocks(
            self.validator.validate_evidence_evaluation(fixture("negative_evaluation_missing_uncertainty")),
            "evidence_contract",
            "uncertainty",
        )

    def test_candidate_validation_enforces_package_contract_and_insightforge_boundary(self):
        self.assert_blocks(
            self.validator.validate_knowledge_candidate(fixture("negative_candidate_unsupported_inference")),
            "unsupported_inference",
            "forbidden interpretation language",
        )
        self.assert_blocks(
            self.validator.validate_knowledge_candidate(fixture("negative_candidate_missing_fingerprints")),
            "lineage_fingerprint",
            "fingerprints",
        )
        self.assert_blocks(
            self.validator.validate_knowledge_candidate(fixture("negative_candidate_maturity_overclaim")),
            "maturity_state",
            "candidate package cannot be accepted",
        )

    def test_knowledge_object_validation_enforces_promotion_integrity(self):
        self.assert_blocks(
            self.validator.validate_knowledge_object(fixture("negative_object_missing_validation_history")),
            "maturity_state",
            "validation_history",
        )
        self.assert_blocks(
            self.validator.validate_knowledge_object(fixture("negative_object_invalid_lineage")),
            "lineage_fingerprint",
            "previous package",
        )
        self.assert_blocks(
            self.validator.validate_knowledge_object(fixture("negative_object_maturity_overclaim")),
            "maturity_state",
            "production-governed maturity",
        )

    def test_knowledge_change_validation_enforces_version_and_fingerprint_evolution(self):
        self.assert_blocks(
            self.validator.validate_knowledge_change(fixture("negative_change_missing_previous_ref")),
            "package_schema",
            "previous_package_ref",
        )
        self.assert_blocks(
            self.validator.validate_knowledge_change(fixture("negative_change_missing_fingerprint_evolution")),
            "lineage_fingerprint",
            "fingerprint_evolution",
        )
        self.assert_blocks(
            self.validator.validate_knowledge_change(fixture("negative_change_malformed_history")),
            "lineage_fingerprint",
            "version lineage",
        )

    def test_fixture_catalogue_covers_all_required_positive_and_negative_cases(self):
        fixture_names = {path.stem for path in FIXTURES.glob("*.json")}
        expected = {
            "positive_evidence", "positive_evidence_evaluation", "positive_candidate",
            "positive_knowledge_object", "positive_knowledge_change",
            "negative_evidence_missing_source_identity", "negative_evidence_missing_fingerprint",
            "negative_evidence_llm_direct_evidence", "negative_evaluation_collapsed_evidence",
            "negative_evaluation_forbidden_interpretation", "negative_evaluation_missing_uncertainty",
            "negative_candidate_unsupported_inference", "negative_candidate_missing_fingerprints",
            "negative_candidate_maturity_overclaim", "negative_object_missing_validation_history",
            "negative_object_invalid_lineage", "negative_object_maturity_overclaim",
            "negative_change_missing_previous_ref", "negative_change_missing_fingerprint_evolution",
            "negative_change_malformed_history",
        }
        self.assertEqual(fixture_names, expected)


if __name__ == "__main__":
    unittest.main()
