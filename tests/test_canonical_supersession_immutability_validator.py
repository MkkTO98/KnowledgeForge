from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/canonical_supersession_immutability_validator.py"


class CanonicalSupersessionImmutabilityValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("validator", TOOL)
        cls.module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(cls.module)

    def test_validator_detects_previous_predecessor_mutation_and_corrects_model(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.module.validate(Path(tmp), create_postgres=False)
        self.assertFalse(result["byte_identical_predecessor_in_flawed_prototype"])
        self.assertTrue(result["corrected_predecessor_byte_identical"])
        self.assertTrue(result["exactly_one_current"])
        self.assertIn("external", result["changed_packages_meaning"])

    def test_corrected_state_keeps_current_state_outside_package_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            report = Path(tmp)
            result = self.module.validate(report, create_postgres=False)
            state_path = ROOT / result["current_state_identity"] if not Path(result["current_state_identity"]).is_absolute() else Path(result["current_state_identity"])
            # In temp mode, result path is relative to project only for normal report; use report fallback.
            if not state_path.exists():
                state_path = report / "corrected_isolated_model/state/current_state_registry.json"
            state = json.loads(state_path.read_text())
        current = [k for k, v in state["current_state_by_package"].items() if v["current"]]
        self.assertEqual(current, [self.module.SUCC_ID])
        self.assertFalse(state["current_state_by_package"][self.module.PRED_ID]["current"])

    def test_failed_validation_does_not_change_current_state_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = self.module.validate(Path(tmp), create_postgres=False)
        rollback = result["rollback_idempotence"]
        self.assertTrue(rollback["state_unchanged_after_failed_validation"])
        self.assertEqual(rollback["state_hash_before"], rollback["state_hash_after_failed_validation"])


if __name__ == "__main__":
    unittest.main()
