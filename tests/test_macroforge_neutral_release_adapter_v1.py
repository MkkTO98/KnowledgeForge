from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "tools" / "macroforge_neutral_release_adapter_v1.py"
HANDOFF = ROOT / "artifacts/external-release-handoffs/macroforge/task-210-wdi-trade-share-dnk-swe-nor-1990-2024"
EXPORT = HANDOFF / "macroforge-wdi-trade-share-dnk-swe-nor-1990-2024.neutral-release.json"
MANIFEST = HANDOFF / "manifest.json"


def load_adapter():
    spec = importlib.util.spec_from_file_location("macroforge_adapter", ADAPTER)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class MacroForgeNeutralReleaseAdapterV1Test(unittest.TestCase):
    def setUp(self):
        self.adapter = load_adapter()

    def test_validates_macroforge_producer_envelope_from_transferred_copy(self):
        result = self.adapter.validate_macroforge_release(EXPORT, MANIFEST)
        self.assertTrue(result["valid"], result)
        self.assertEqual(210, result["item_count"])
        self.assertEqual("macroforge.neutral_evidence_release_export.v1", result["contract_identity"])
        self.assertEqual("1.0", result["contract_version"])
        self.assertEqual("sha256:def8c318100cf14526cbdac87335e6b1646681b2176fd684c66ac7cc9d7add67", result["release_fingerprint"])
        self.assertEqual("sha256:2b1a1c3d9e65b182f073e0171c59627c8298740ee9cb7c1418dfbae3ae196e0a", result["selection_fingerprint"])
        self.assertEqual("1906821add91de87538f29bbbc254c8d52d5f6734ba7f00aced45fe2c5358f86", result["export_sha256"])
        self.assertFalse(result["leakage"]["leaks"])

    def test_adapter_maps_macroforge_release_to_knowledgeforge_internal_release(self):
        adapted = self.adapter.adapt_macroforge_release(EXPORT, MANIFEST)
        release = adapted["knowledgeforge_release"]
        self.assertEqual("knowledgeforge_neutral_evidence_release_contract_v1", release["contract_id"])
        self.assertEqual("1.0", release["contract_version"])
        self.assertEqual("macroforge-wdi-1990-2024-2b1a1c3d9e65b182", release["release_id"])
        self.assertEqual("World Bank", release["provider"]["name"])
        self.assertEqual("World Development Indicators", release["dataset"]["name"])
        self.assertEqual("WDI:2026-07-01:1990:2024", release["source_release_vintage"])
        self.assertEqual(210, len(release["evidence_items"]))
        self.assertEqual("macroforge.neutral_evidence_release_export.v1", release["producer_metadata"]["producer_contract_identity"])
        self.assertEqual("sha256:def8c318100cf14526cbdac87335e6b1646681b2176fd684c66ac7cc9d7add67", release["producer_metadata"]["producer_release_fingerprint"])
        self.assertRegex(adapted["normalized_release_fingerprint"], r"^sha256:[0-9a-f]{64}$")

    def test_adapter_fail_closed_on_changed_producer_fingerprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp) / EXPORT.name
            data = json.loads(EXPORT.read_text())
            data["items"][0]["value"] = "999"
            tmp_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
            result = self.adapter.validate_macroforge_release(tmp_path, MANIFEST)
            self.assertFalse(result["valid"])
            self.assertIn("item_fingerprint_mismatch", "\n".join(result["errors"]))
            self.assertIn("release_fingerprint_mismatch", "\n".join(result["errors"]))

    def test_process_transferred_release_twice_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state"
            result = self.adapter.process_adapted_release(EXPORT, MANIFEST, state)
            self.assertEqual("successfully_processed_no_promote", result["first_processing"]["processing_status"])
            duplicate = self.adapter.process_adapted_release(EXPORT, MANIFEST, state)
            self.assertEqual("already_processed_identical_release", duplicate["first_processing"]["received_status"])
            self.assertEqual(0, duplicate["first_processing"]["recomputation_summary"]["incremental_recompute_count"])


if __name__ == "__main__":
    unittest.main()
