from __future__ import annotations

import importlib.util
import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "external_outbox_poller_v1.py"
DEFAULT_MACROFORGE_OUTBOX = ROOT.parent / "MacroForge" / "artifacts" / "exports" / "neutral-evidence-release" / "outbox" / "macroforge-wdi-trade-share-dnk-swe-nor-annual-v1" / "macroforge-wdi-1990-2024-2b1a1c3d9e65b182"
MACROFORGE_OUTBOX = Path(os.environ.get("KNOWLEDGEFORGE_TEST_MACROFORGE_OUTBOX", DEFAULT_MACROFORGE_OUTBOX))


def load_tool():
    spec = importlib.util.spec_from_file_location("external_outbox_poller_v1", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ExternalOutboxPollingSupersessionV1Test(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool()
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source_root = self.root / "producer-outbox"
        shutil.copytree(MACROFORGE_OUTBOX, self.source_root / "release")
        self.config_path = self.root / "external_sources.json"
        self.config_path.write_text(json.dumps({
            "sources": [{
                "source_identity": "test-macroforge-outbox",
                "root_location": str(self.source_root),
                "supported_contracts": [{"contract_identity": "macroforge.neutral_evidence_release_export.v1", "contract_version": "1.0"}],
                "discovery_pattern": "**/manifest.json",
                "enabled": True,
                "polling_mode": "manual_once",
                "transfer_destination": str(self.root / "state" / "inbound"),
                "max_files_per_scan": 10,
                "max_bytes_per_scan": 1_000_000
            }]
        }))
        self.state = self.root / "state"

    def tearDown(self):
        self.tmp.cleanup()

    def test_poll_once_transfers_real_outbox_artifact_and_processes_duplicate_without_recompute(self):
        first = self.tool.poll_once(self.config_path, self.state, max_releases=1, process=True)
        self.assertEqual(1, first["transferred_count"])
        record = first["records"][0]
        self.assertEqual("processed", record["transport_status"])
        self.assertEqual("macroforge-wdi-1990-2024-2b1a1c3d9e65b182", record["producer_release_id"])
        self.assertEqual("sha256:def8c318100cf14526cbdac87335e6b1646681b2176fd684c66ac7cc9d7add67", record["producer_fingerprint"])
        self.assertEqual("1906821add91de87538f29bbbc254c8d52d5f6734ba7f00aced45fe2c5358f86", record["export_hash"])
        self.assertTrue(Path(record["destination_export_path"]).exists())
        self.assertTrue(Path(record["destination_manifest_path"]).exists())
        self.assertEqual("knowledgeforge_macroforge_neutral_release_adapter_v1@1.0", record["adapter_identity_version"])
        self.assertEqual("already_processed_identical_release", record["seen_release_result"])
        self.assertEqual(0, record["incremental_recompute_count"])
        self.assertEqual("75a2b2a586df56523e3a5f81435b159f078af767d67de5adbda667e47c755060", record["normalized_release_fingerprint"].removeprefix("sha256:"))

        second = self.tool.poll_once(self.config_path, self.state, max_releases=1, process=True)
        self.assertEqual("already_transferred_identical", second["records"][0]["transport_status"])
        self.assertEqual(0, second["records"][0]["incremental_recompute_count"])

    def test_dry_run_and_list_discovered_do_not_copy_or_process(self):
        discovered = self.tool.list_discovered(self.config_path)
        self.assertEqual(1, len(discovered["releases"]))
        dry = self.tool.poll_once(self.config_path, self.state, max_releases=1, dry_run=True, process=True)
        self.assertEqual("discovered", dry["records"][0]["transport_status"])
        self.assertFalse((self.state / "inbound").exists())
        self.assertFalse((self.state / "transport-registry.jsonl").exists())

    def test_incomplete_and_hash_mismatch_are_quarantined_without_touching_source(self):
        incomplete = self.source_root / "_staging" / "incomplete"
        incomplete.mkdir(parents=True)
        (incomplete / "manifest.json").write_text("{}")
        source_export = self.source_root / "release" / "macroforge-wdi-1990-2024-2b1a1c3d9e65b182.neutral-release.json"
        before = self.tool.file_sha256(source_export)
        bad_manifest = json.loads((self.source_root / "release" / "manifest.json").read_text())
        bad_manifest["export_sha256"] = "0" * 64
        (self.source_root / "release" / "manifest.json").write_text(json.dumps(bad_manifest))
        result = self.tool.poll_once(self.config_path, self.state, max_releases=10, process=True)
        self.assertEqual("quarantined", result["records"][0]["transport_status"])
        self.assertEqual("manifest_export_hash_mismatch", result["records"][0]["failure_reason"])
        self.assertEqual(before, self.tool.file_sha256(source_export))
        self.assertFalse(any("_staging" in r.get("source_manifest_path", "") for r in result["records"]))

    def test_registry_inventory_classification_and_metadata_gate(self):
        inventory = self.tool.inventory_release_registries(ROOT)
        classifications = {i["classification"] for i in inventory["registries"]}
        self.assertIn("producer_stream_operational", classifications)
        self.assertEqual("artifacts/release-inbox-unified-v1/seen-release-registry.jsonl", inventory["production_registry_authority"])
        gate = self.tool.metadata_sufficiency_gate({"indicator_code":"NE.EXP.GNFS.ZS","indicator_name":"Exports of goods and services (% of GDP)","unit":"percent of GDP"})
        self.assertEqual("automatic_deterministic_recomputation_permitted", gate["decision"])
        new_short_only = self.tool.metadata_sufficiency_gate({"indicator_code":"NEW.TEST","indicator_name":"Short label","unit":"x"})
        self.assertEqual("candidate_registry_proposal_only", new_short_only["decision"])
        changed_unit = self.tool.metadata_sufficiency_gate({"indicator_code":"NE.EXP.GNFS.ZS","indicator_name":"Exports of goods and services (% of GDP)","unit":"changed"})
        self.assertEqual("semantic_review_required", changed_unit["decision"])

    def test_controlled_successor_supersession_and_isolated_repository_are_idempotent(self):
        release = self.tool.load_json(MACROFORGE_OUTBOX / "macroforge-wdi-1990-2024-2b1a1c3d9e65b182.neutral-release.json")
        normalized = self.tool.adapt_external_release(MACROFORGE_OUTBOX / "macroforge-wdi-1990-2024-2b1a1c3d9e65b182.neutral-release.json", MACROFORGE_OUTBOX / "manifest.json")
        successor = self.tool.build_controlled_successor_release(normalized["knowledgeforge_release"])
        self.assertEqual("controlled_test_successor_not_provider_evidence", successor["source_metadata"]["controlled_fixture_label"])
        self.assertEqual(normalized["knowledgeforge_release"]["release_id"], successor["prior_release_id"])
        self.assertEqual(212, len(successor["evidence_items"]))
        predecessor_path = ROOT / "knowledge_repository" / "objects" / f"{self.tool.DNK_PACKAGE_ID}.json"
        before = self.tool.file_sha256(predecessor_path)
        writes = []
        original_write_text = Path.write_text

        def guarded_write_text(path, *args, **kwargs):
            if Path(path).resolve() == predecessor_path.resolve():
                writes.append(str(path))
                raise AssertionError("predecessor package opened for writing")
            return original_write_text(path, *args, **kwargs)

        with mock.patch.object(Path, "write_text", guarded_write_text):
            supersession = self.tool.run_isolated_supersession_prototype(successor, self.root / "isolated")
        self.assertFalse(writes)
        self.assertTrue(supersession["valid"])
        self.assertEqual(before, self.tool.file_sha256(predecessor_path))
        self.assertEqual(before, supersession["predecessor_pre_sha256"])
        self.assertEqual(before, supersession["predecessor_post_sha256"])
        self.assertTrue(supersession["predecessor_byte_identical"])
        self.assertEqual("accepted", supersession["predecessor_package"]["confidence_quality"]["lifecycle_state"])
        self.assertEqual("accepted", supersession["successor_package"]["confidence_quality"]["lifecycle_state"])
        self.assertNotEqual(supersession["predecessor_package"]["package_id"], supersession["successor_package"]["package_id"])
        self.assertEqual(supersession["successor_package"]["package_id"], supersession["current_state_registry"]["current_package_id"])
        self.assertFalse(supersession["current_state_registry"]["packages"][self.tool.DNK_PACKAGE_ID]["current"])
        self.assertEqual("supersession", supersession["supersession_record"]["record_type"])
        self.assertEqual(1, supersession["changed_package_count"])
        self.assertEqual(2, supersession["unchanged_package_count"])
        self.assertTrue((self.root / "isolated" / "repository" / "objects" / f"{self.tool.DNK_PACKAGE_ID}.json").exists())
        self.assertTrue((self.root / "isolated" / "repository" / "objects" / f"{supersession['successor_package']['package_id']}.json").exists())
        rerun = self.tool.run_isolated_supersession_prototype(successor, self.root / "isolated")
        self.assertEqual(supersession["repository_fingerprint"], rerun["repository_fingerprint"])

    def test_failure_recovery_cases_are_auditable(self):
        cases = self.tool.run_failure_recovery_fixtures(self.config_path, self.root / "failure-state")
        statuses = {case["case"]: case["status"] for case in cases["cases"]}
        self.assertEqual("quarantined", statuses["missing_manifest"])
        self.assertEqual("unsupported_contract", statuses["unsupported_contract"])
        self.assertEqual("processing_failed", statuses["adapter_failure"])
        self.assertEqual("retry_succeeded", statuses["retry_after_failure"])
        self.assertTrue(cases["producer_files_untouched"])


if __name__ == "__main__":
    unittest.main()
