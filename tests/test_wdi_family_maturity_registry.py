from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class WDIFamilyMaturityRegistryTest(unittest.TestCase):
    def test_all_currently_mature_wdi_families_are_loaded_from_authoritative_closeouts(self):
        registry = load_module(ROOT / "tools/wdi_family_maturity_registry.py", "wdi_family_maturity_registry_test")
        mature = registry.mature_wdi_family_registry(ROOT)
        expected = {
            "Demographic",
            "Environment",
            "Infrastructure",
            "Energy & Mining",
            "Agriculture & Rural Development",
            "Health",
            "Education",
            "Trade",
            "Financial Sector",
        }
        self.assertEqual(set(mature), expected)
        for family, record in mature.items():
            self.assertEqual(record["classification"], "Mature")
            self.assertTrue((ROOT / record["authoritative_source"]).exists(), family)
            self.assertIn("family maturity", record["evidence_text"].lower())

    def test_campaign39_candidates_consume_registry_not_hardcoded_stable_state(self):
        registry = load_module(ROOT / "tools/wdi_family_maturity_registry.py", "wdi_family_maturity_registry_test2")
        self.assertTrue(registry.is_mature_wdi_family("Education", ROOT))
        self.assertTrue(registry.is_mature_wdi_family("Financial Sector", ROOT))
        self.assertFalse(registry.is_mature_wdi_family("Unknown", ROOT))


if __name__ == "__main__":
    unittest.main()
