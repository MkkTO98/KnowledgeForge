from __future__ import annotations

import contextlib
import io
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "release_automation_alignment_v1.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("release_automation_alignment_v1", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseAutomationAlignmentV1Test(unittest.TestCase):
    def setUp(self):
        self.tool = load_tool()

    def test_synthetic_release_contracts_validate(self):
        v1, v2 = self.tool.synthetic_releases()
        self.assertEqual([], self.tool.validate_release(v1))
        self.assertEqual([], self.tool.validate_release(v2))
        self.assertNotEqual(v1["release_content_fingerprint"], v2["release_content_fingerprint"])

    def test_change_detection_is_exact(self):
        v1, v2 = self.tool.synthetic_releases()
        change = self.tool.detect_changes(v1, v2)
        self.assertEqual(["obs:A:DNK:2022"], change["added_item_ids"])
        self.assertEqual([], change["removed_item_ids"])
        self.assertEqual(["obs:A:DNK:2021"], change["changed_item_ids"])
        self.assertEqual(["obs:A:DNK:2020", "obs:B:DNK:2020"], change["unchanged_item_ids"])

    def test_impact_analysis_affects_only_matching_derivations(self):
        v1, v2 = self.tool.synthetic_releases()
        reg = self.tool.derivation_registry()
        impact = self.tool.affected_derivations(self.tool.detect_changes(v1, v2), v2, reg)
        self.assertEqual(
            ["synthetic_growth_SYN.A_DNK_annual", "synthetic_relationship_SYN.A_SYN.B_DNK_annual"],
            [d["derivation_id"] for d in impact["affected_derivations"]],
        )
        self.assertEqual(["synthetic_unaffected_SYN.C_DNK_annual"], impact["unaffected_derivation_ids"])
        self.assertTrue(impact["minimal_recompute"])

    def test_prototype_preserves_boundaries(self):
        result = self.tool.build_run()
        self.assertFalse(result["automation_capability_audit"]["boundary_findings"]["direct_macroforge_dependency_required"])
        self.assertFalse(result["incremental_postgresql_publication"]["schema_expansion_required"])
        self.assertFalse(result["incremental_postgresql_publication"]["executed_postgresql_write"])
        self.assertFalse(result["supersession_model"]["canonical_package_mutation"])
        self.assertFalse(result["compact_ai_retrieval_assessment"]["frontier_llm_required"])

    def test_cli_verify_rejects_invalid_impact(self):
        result = self.tool.build_run()
        result["dependency_impact_analysis"]["affected_derivations"] = []
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            self.tool.write_json(path, result)
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(2, self.tool.main(["verify", "--output", str(path)]))


if __name__ == "__main__":
    unittest.main()
