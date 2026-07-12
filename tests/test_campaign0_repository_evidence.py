from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = PROJECT_ROOT / "tools" / "run_campaign0_repository_evidence.py"


def load_campaign_module():
    spec = importlib.util.spec_from_file_location("run_campaign0_repository_evidence", SCRIPT_PATH)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class Campaign0RepositoryEvidenceTest(unittest.TestCase):
    def setUp(self):
        self.module = load_campaign_module()

    def test_campaign0_produces_accepted_and_rejected_catalogues(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign0"
            summary = self.module.run_campaign(PROJECT_ROOT, output)
            self.assertEqual(summary["campaign_id"], self.module.CAMPAIGN_ID)
            self.assertGreaterEqual(summary["accepted"], 8)
            self.assertEqual(summary["rejected"], 3)
            self.assertTrue(summary["determinism_verified"])
            self.assertTrue(summary["fingerprint_stability"])
            self.assertTrue((output / "reports" / "campaign_0_final_report.md").exists())
            self.assertTrue((output / "reports" / "production_quality_report.md").exists())
            self.assertTrue((output / "reports" / "generated_knowledge_object_catalogue.md").exists())
            self.assertTrue((output / "reports" / "rejected_knowledge_object_catalogue.md").exists())

    def test_accepted_objects_pass_stage_validation_and_boundary_checks(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign0"
            self.module.run_campaign(PROJECT_ROOT, output)
            objects = sorted((output / "knowledge_objects").glob("*.json"))
            self.assertGreaterEqual(len(objects), 8)
            forbidden = [term.lower() for term in self.module.FORBIDDEN_TERMS]
            for path in objects:
                obj = json.loads(path.read_text())
                validation = self.module.validator.validate_knowledge_object(obj)
                self.assertTrue(validation["ok"], path.name)
                text = json.dumps(obj).lower()
                self.assertFalse(any(term in text for term in forbidden), path.name)
                statement_type = obj["generated_statements"][0]["statement_type"]
                self.assertIn(statement_type, self.module.constructor.SUPPORTED_KNOWLEDGE_CATEGORIES)

    def test_campaign0_is_replay_stable(self):
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first"
            second = Path(tmp) / "second"
            first_summary = self.module.run_campaign(PROJECT_ROOT, first)
            second_summary = self.module.run_campaign(PROJECT_ROOT, second)
            comparable_keys = ["snapshot_fingerprint", "accepted", "rejected", "determinism_verified", "fingerprint_stability"]
            self.assertEqual({k: first_summary[k] for k in comparable_keys}, {k: second_summary[k] for k in comparable_keys})
            first_quality = json.loads((first / "production_quality_report.json").read_text())
            second_quality = json.loads((second / "production_quality_report.json").read_text())
            self.assertEqual(first_quality, second_quality)

    def test_rejections_preserve_failure_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "campaign0"
            self.module.run_campaign(PROJECT_ROOT, output)
            missing = json.loads((output / "rejected" / "rej-campaign0-missing-provenance.json").read_text())
            boundary = json.loads((output / "rejected" / "rej-campaign0-constitutional-boundary-language.json").read_text())
            self.assertFalse(missing["validator_result"]["ok"])
            self.assertFalse(boundary["validator_result"]["ok"])
            missing_categories = {b["category"] for b in missing["validator_result"]["blockers"]}
            boundary_categories = {b["category"] for b in boundary["validator_result"]["blockers"]}
            self.assertIn("evidence_contract", missing_categories)
            self.assertTrue({"constitutional_boundary", "unsupported_inference"} & boundary_categories)


if __name__ == "__main__":
    unittest.main()
