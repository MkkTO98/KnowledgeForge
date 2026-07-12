from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONSTRUCTOR_PATH = PROJECT_ROOT / "tools" / "construct_knowledge_package_v1.py"
VALIDATOR_PATH = PROJECT_ROOT / "tools" / "validate_knowledge_pipeline_v1.py"
FIXTURES = PROJECT_ROOT / "tests" / "fixtures" / "package_construction_v1"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixture(name: str):
    return json.loads((FIXTURES / f"{name}.json").read_text(encoding="utf-8"))


class PackageConstructionValidationV1Test(unittest.TestCase):
    def setUp(self):
        self.constructor = load_module(CONSTRUCTOR_PATH, "construct_knowledge_package_v1")
        self.validator = load_module(VALIDATOR_PATH, "validate_knowledge_pipeline_v1")
        self.source_package = fixture("valid_source_evidence_package")

    def assert_ok(self, report):
        self.assertTrue(report["ok"], report)
        self.assertEqual(report["blockers"], [])

    def assert_blocks(self, report, category: str, message_part: str):
        self.assertFalse(report["ok"], report)
        self.assertTrue(any(f["category"] == category and message_part in f["message"] for f in report["blockers"]), report)

    def test_constructs_complete_pipeline_from_immutable_source_evidence_package(self):
        result = self.constructor.construct_pipeline(self.source_package)

        self.assert_ok(result["source_validation"])
        self.assert_ok(self.validator.validate_evidence(result["evidence"]))
        self.assert_ok(self.validator.validate_evidence_evaluation(result["evidence_evaluation"]))
        self.assert_ok(self.validator.validate_knowledge_candidate(result["knowledge_candidate_package"]))
        self.assert_ok(self.validator.validate_knowledge_object(result["knowledge_object_package"]))

        self.assertEqual(result["evidence"]["evidence_ref_id"], "ev-srcpkg-demographic-coverage-fixture-v1")
        self.assertEqual(result["knowledge_candidate_package"]["package_kind"], "KnowledgeCandidatePackage")
        self.assertEqual(result["knowledge_object_package"]["package_kind"], "KnowledgeObjectPackage")
        self.assertEqual(
            result["knowledge_object_package"]["promotion"]["from_candidate_package_id"],
            result["knowledge_candidate_package"]["package_id"],
        )

    def test_construction_is_deterministic_and_replayable(self):
        first = self.constructor.construct_pipeline(self.source_package)
        second = self.constructor.construct_pipeline(copy.deepcopy(self.source_package))

        self.assertEqual(first, second)
        self.assertEqual(
            first["determinism"]["pipeline_fingerprint"],
            second["determinism"]["pipeline_fingerprint"],
        )
        self.assertTrue(first["determinism"]["identical_replay"])
        self.assertEqual(first["knowledge_object_package"]["status"], "accepted-for-controlled-production-readiness")

    def test_generated_object_stays_inside_constitutional_knowledge_boundary(self):
        result = self.constructor.construct_pipeline(self.source_package)
        obj = result["knowledge_object_package"]
        boundary = self.constructor.verify_knowledge_boundary(obj)

        self.assert_ok(boundary)
        serialized = json.dumps(obj, sort_keys=True).lower()
        forbidden_terms = [
            "investors should",
            "forecast",
            "hypothesis",
            "causes",
            "recommend",
            "policy implication",
            "presentation narrative",
            "investment meaning",
            "this means",
        ]
        for term in forbidden_terms:
            self.assertNotIn(term, serialized)

    def test_negative_source_package_cases_block_before_construction(self):
        malformed = copy.deepcopy(self.source_package)
        del malformed["source_evidence_package_id"]
        self.assert_blocks(
            self.constructor.validate_source_evidence_package(malformed),
            "evidence_contract",
            "source_evidence_package_id",
        )

        missing_provenance = copy.deepcopy(self.source_package)
        missing_provenance["provenance"] = {}
        self.assert_blocks(
            self.constructor.validate_source_evidence_package(missing_provenance),
            "provenance",
            "provenance",
        )

        invalid_fingerprint = copy.deepcopy(self.source_package)
        invalid_fingerprint["fingerprints"]["source_payload"] = "sha256:not-the-real-fingerprint"
        self.assert_blocks(
            self.constructor.validate_source_evidence_package(invalid_fingerprint),
            "lineage_fingerprint",
            "source_payload",
        )

        broken_repro = copy.deepcopy(self.source_package)
        broken_repro["reproducibility"]["rerun_method"] = "manual memory"
        self.assert_blocks(
            self.constructor.validate_source_evidence_package(broken_repro),
            "reproducibility",
            "deterministic",
        )

    def test_negative_constructed_package_cases_block_independently(self):
        result = self.constructor.construct_pipeline(self.source_package)

        bad_candidate = copy.deepcopy(result["knowledge_candidate_package"])
        bad_candidate["generated_statements"][0]["text"] = "Investors should treat this as bullish."
        self.assert_blocks(
            self.validator.validate_knowledge_candidate(bad_candidate),
            "unsupported_inference",
            "forbidden interpretation language",
        )

        incomplete_candidate = copy.deepcopy(result["knowledge_candidate_package"])
        del incomplete_candidate["provenance_envelope"]
        self.assert_blocks(
            self.validator.validate_knowledge_candidate(incomplete_candidate),
            "package_schema",
            "provenance_envelope",
        )

        invalid_object = copy.deepcopy(result["knowledge_object_package"])
        invalid_object["promotion"]["maturity_state"] = "M5 production governed"
        self.assert_blocks(
            self.validator.validate_knowledge_object(invalid_object),
            "maturity_state",
            "production-governed maturity",
        )


if __name__ == "__main__":
    unittest.main()
