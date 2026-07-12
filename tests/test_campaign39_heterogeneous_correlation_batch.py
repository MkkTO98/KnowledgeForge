from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELECTION = ROOT / "artifacts/reports/campaign39-heterogeneous-wdi-pearson-batch-20260711/selection/campaign39_frozen_batch_selection_decision.json"
FIXTURE = ROOT / "artifacts/evidence-fixtures/campaign39-heterogeneous-wdi-pearson-batch-1990-2024-https"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Campaign39HeterogeneousBatchTest(unittest.TestCase):
    def test_batch_scope_uses_authoritative_mature_family_registry(self):
        campaign = load_module(ROOT / "tools/run_campaign39_heterogeneous_correlation_batch.py", "campaign39_test")
        scope = campaign.batch_scope()
        self.assertEqual(scope["expected_package_count_max"], 3)
        self.assertEqual(scope["method_contract_fingerprint"], "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476")
        mature = scope["verified_mature_families"]
        self.assertEqual(mature["Education"]["classification"], "Mature")
        self.assertEqual(mature["Financial Sector"]["classification"], "Mature")

    def test_frozen_batch_selection_is_coefficient_free_and_three_pairs(self):
        self.assertTrue(SELECTION.exists())
        selection = json.loads(SELECTION.read_text())
        serialized = json.dumps(selection, sort_keys=True).lower()
        self.assertFalse(selection["coefficient_calculation_performed_during_selection"])
        self.assertNotIn("pearson_coefficient", serialized)
        self.assertNotIn("coefficient_value", serialized)
        self.assertEqual(len(selection["selected_pairs"]), 3)
        self.assertGreaterEqual(len({p["family"] for p in selection["selected_pairs"]}), 2)
        self.assertGreaterEqual(len({p["entity"] for p in selection["selected_pairs"]}), 2)

    def test_https_downgrade_rejected(self):
        campaign = load_module(ROOT / "tools/run_campaign39_heterogeneous_correlation_batch.py", "campaign39_test2")
        with self.assertRaises(ValueError):
            campaign.acquire_url("http://api.worldbank.org/v2/indicator/SP.DYN.CBRT.IN?format=json")

    def test_fixture_outputs_are_deterministic_after_acquisition(self):
        if not (FIXTURE / "batch_alignment_results.json").exists():
            self.skipTest("Campaign 39 fixture not acquired yet")
        alignments = json.loads((FIXTURE / "batch_alignment_results.json").read_text())
        self.assertEqual(len(alignments), 3)
        for item in alignments:
            self.assertGreaterEqual(item["aligned_pair_count"], 30)
            self.assertGreaterEqual(float(item["aligned_coverage"]), 0.85)
            self.assertIn("combined_aligned_evidence_fingerprint", item)


if __name__ == "__main__":
    unittest.main()
