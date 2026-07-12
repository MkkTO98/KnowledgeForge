from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "release_inbox_v1.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("release_inbox_v1", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseInboxRealEvidenceV1Test(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.state = self.root / "state"
        self.out = self.root / "out"
        self.tool.initialize_operational_state(self.state)
        self.tool.write_real_evidence_pilot_fixtures(self.out)
        self.v1 = self.out / "real_wdi_exports_imports_release_v1.json"
        self.v2 = self.out / "controlled_successor_release_v2.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_real_v1_validates_and_records_real_wdi_scope(self):
        release = self.tool.read_json(self.v1)
        validation = self.tool.validate_release(release)
        self.assertTrue(validation["valid"])
        self.assertEqual("World Bank", release["provider"]["name"])
        self.assertEqual("World Development Indicators", release["dataset"]["name"])
        self.assertIn("KnowledgeForge conformance fixture", release["provenance_note"])
        scopes = {(i["entity_id"], i["indicator_code"]) for i in release["evidence_items"]}
        self.assertIn(("DNK", "NE.EXP.GNFS.ZS"), scopes)
        self.assertIn(("SWE", "NE.IMP.GNFS.ZS"), scopes)
        self.assertEqual(210, len(release["evidence_items"]))

    def test_process_v1_idempotence_conflict_successor_out_of_order_and_quarantine(self):
        r1 = self.tool.process_release_path(self.v1, self.state, no_promote=True)
        self.assertEqual("successfully_processed_no_promote", r1["processing_status"])
        r1_again = self.tool.process_release_path(self.v1, self.state, no_promote=True)
        self.assertEqual("already_processed_identical_release", r1_again["received_status"])
        self.assertEqual(0, r1_again["recomputation_summary"]["incremental_recompute_count"])

        altered = self.tool.read_json(self.v1)
        altered["evidence_items"][0]["value_canonical"] = "999"
        self.tool.refresh_release_fingerprints(altered, keep_release_id=True)
        conflict_path = self.out / "conflicting_v1.json"
        self.tool.write_json(conflict_path, altered)
        conflict = self.tool.process_release_path(conflict_path, self.state, no_promote=True)
        self.assertEqual("conflicting_reuse_of_release_id", conflict["received_status"])
        self.assertEqual("quarantined_release", conflict["processing_status"])

        r2 = self.tool.process_release_path(self.v2, self.state, no_promote=True)
        self.assertEqual("valid_successor_release", r2["received_status"])
        self.assertEqual(["pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1"], r2["impact"]["affected_derivation_ids"])
        self.assertEqual(1, r2["recomputation_summary"]["incremental_recompute_count"])
        self.assertEqual(2, r2["recomputation_summary"]["avoided_recompute_count"])

        r2_again = self.tool.process_release_path(self.v2, self.state, no_promote=True)
        self.assertEqual("already_processed_identical_release", r2_again["received_status"])
        late_v1 = self.tool.process_release_path(self.v1, self.state, no_promote=True)
        self.assertEqual("out_of_order_release", late_v1["received_status"])

        malformed = self.out / "malformed.json"
        malformed.write_text("{not-json")
        bad = self.tool.process_release_path(malformed, self.state, no_promote=True)
        self.assertEqual("invalid_release", bad["received_status"])
        self.assertEqual("quarantined_release", bad["processing_status"])

    def test_failure_and_resume_are_auditable_and_do_not_duplicate_success(self):
        self.tool.process_release_path(self.v1, self.state, no_promote=True)
        failed = self.tool.process_release_path(self.v2, self.state, no_promote=True, simulate_recompute_failure=True)
        self.assertEqual("processing_failed", failed["processing_status"])
        resumed = self.tool.process_release_path(self.v2, self.state, no_promote=True)
        self.assertEqual("successfully_processed_no_promote", resumed["processing_status"])
        registry = self.tool.load_registry(self.state)
        statuses = [e["processing_status"] for e in registry["entries"] if e.get("release_id") == "wdi-trade-exports-imports-controlled-test-v2"]
        self.assertIn("processing_failed", statuses)
        self.assertIn("successfully_processed_no_promote", statuses)

    def test_incremental_result_matches_full_no_promote_recompute_and_delta_is_consumable(self):
        self.tool.process_release_path(self.v1, self.state, no_promote=True)
        result = self.tool.process_release_path(self.v2, self.state, no_promote=True)
        self.assertEqual(result["recomputation_summary"]["incremental_results"], result["recomputation_summary"]["full_comparison_results_for_affected"])
        delta_path = Path(result["downstream_delta_path"])
        delta = self.tool.read_json(delta_path)
        consumer = self.tool.consumer_assess_delta(delta)
        self.assertTrue(consumer["can_determine_what_changed"])
        self.assertTrue(consumer["can_determine_which_relationship_would_change"])
        self.assertTrue(consumer["can_determine_which_relationships_remain_valid"])
        self.assertFalse(consumer["canonical_promotion_occurred"])
        self.assertEqual("wdi-trade-exports-imports-controlled-test-v2", consumer["evidence_release_id"])

    def test_conformance_fixture_has_no_macroforge_or_private_schema_coupling(self):
        package = self.tool.write_producer_conformance_package(self.out / "conformance")
        text = json.dumps(package, sort_keys=True)
        forbidden = ["MacroForge table", "macroforge.", "database credentials", "KnowledgeForge private PostgreSQL schema"]
        for term in forbidden:
            self.assertNotIn(term, text)
        results = self.tool.verify_conformance_package(self.out / "conformance")
        self.assertTrue(results["valid"])
        self.assertGreaterEqual(len(results["controlled_invalid_results"]), 3)


if __name__ == "__main__":
    unittest.main()
