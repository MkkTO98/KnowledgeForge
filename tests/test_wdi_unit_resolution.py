from __future__ import annotations

import copy
import importlib.util
import json
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "wdi_observation_evidence_fixture.py"


def load_module():
    spec = importlib.util.spec_from_file_location("wdi_observation_evidence_fixture", MODULE_PATH)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def provider_payload(records):
    return [{"page": 1, "pages": 1, "per_page": 100, "total": len(records), "sourceid": "2", "lastupdated": "2026-07-01"}, records]


def metadata(indicator_id, name, unit="", note="", source_org="World Bank"):
    return [{"page": 1, "pages": 1, "per_page": "1", "total": 1}, [{"id": indicator_id, "name": name, "unit": unit, "sourceNote": note, "sourceOrganization": source_org, "topics": []}]]


def row(indicator_id, indicator_name, year, value, unit="", entity="DNK"):
    return {"indicator": {"id": indicator_id, "value": indicator_name}, "country": {"id": "DK", "value": "Denmark"}, "countryiso3code": entity, "date": str(year), "value": value, "unit": unit, "obs_status": "", "decimal": 2}


class WDIUnitResolutionTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()

    def build_raw(self, indicator_id, name, meta_unit, note, row_unit="", value=1):
        contract = self.module.build_selection_contract(indicator_code=indicator_id, entities=["DNK"], start_year=2020, end_year=2020)
        return self.module.raw_fixture_from_provider_payloads(
            selection_contract=contract,
            observation_payload=provider_payload([row(indicator_id, name, 2020, value, row_unit)]),
            indicator_metadata_payload=metadata(indicator_id, name, meta_unit, note),
            observation_response_bytes=b"obs",
            indicator_metadata_response_bytes=b"meta",
            access_timestamp_utc="2026-07-10T00:00:00Z",
        )

    def test_population_persons_is_definition_derived_not_generic_fallback(self):
        raw = self.build_raw("SP.POP.TOTL", "Population, total", "", "Total population is based on the de facto definition of population.")
        normalized = self.module.normalize_raw_fixture(raw)
        self.assertEqual(normalized["indicator_metadata"]["unit_resolution"]["state"], "definition-derived unit")
        self.assertEqual(normalized["indicator_metadata"]["unit"], "persons")
        self.assertEqual(normalized["observations"][0]["unit"], "persons")

    def test_exports_share_resolves_to_percent_of_gdp_from_name_and_definition(self):
        raw = self.build_raw("NE.EXP.GNFS.ZS", "Exports of goods and services (% of GDP)", "", "Exports of goods and services represent the value of all goods and other market services provided to the rest of the world. This indicator is expressed as a percentage of Gross Domestic Product (GDP).")
        normalized = self.module.normalize_raw_fixture(raw)
        unit = normalized["indicator_metadata"]["unit_resolution"]
        self.assertEqual(unit["state"], "definition-derived unit")
        self.assertEqual(unit["resolved_unit"], "percent of GDP")
        self.assertIn("metadata_fingerprint", unit)
        self.assertEqual(normalized["observations"][0]["unit"], "percent of GDP")

    def test_missing_ambiguous_unit_cannot_inherit_persons(self):
        raw = self.build_raw("CUSTOM.UNKNOWN", "Ambiguous indicator", "", "This indicator has no unit semantics.")
        with self.assertRaisesRegex(ValueError, "unresolved unit"):
            self.module.normalize_raw_fixture(raw)

    def test_unknown_indicator_fails_closed(self):
        raw = self.build_raw("XX.UNKNOWN", "Unknown", "", "No useful unit text")
        with self.assertRaisesRegex(ValueError, "unresolved unit"):
            self.module.normalize_raw_fixture(raw)

    def test_metadata_change_changes_unit_resolution_fingerprint(self):
        raw = self.build_raw("NE.EXP.GNFS.ZS", "Exports of goods and services (% of GDP)", "", "Exports of goods and services represent the value of all goods and other market services provided to the rest of the world. This indicator is expressed as a percentage of Gross Domestic Product (GDP).")
        first = self.module.normalize_raw_fixture(raw)["indicator_metadata"]["unit_resolution"]["unit_resolution_fingerprint"]
        changed = copy.deepcopy(raw)
        changed["provider_payloads"]["indicator_metadata"][1][0]["sourceNote"] += " Metadata revision."
        changed["raw_fixture_fingerprint"] = self.module.sha256_value({k: v for k, v in changed.items() if k != "raw_fixture_fingerprint"})
        second = self.module.normalize_raw_fixture(changed)["indicator_metadata"]["unit_resolution"]["unit_resolution_fingerprint"]
        self.assertNotEqual(first, second)

    def test_historical_campaign34_and_campaign35_packages_remain_unchanged(self):
        expected = {
            "pkg-object-srcpkg-campaign34-denmark-population-statistical-summary.json": "ee124afc43b6db03c9ceacb9905864caa8abe15057d1bac507ba1a9db6e913eb",
            "pkg-object-srcpkg-campaign35-dnk-exports-share-statistical-summary-v2.json": "73e834695d90e2980eb594d902cd3bc56a4f10dbca4457602c5e8cdbcfc9aa9b",
            "pkg-object-srcpkg-campaign35-swe-exports-share-statistical-summary-v2.json": "69cb3b0e6e75c148470000bd0e3bd31e70b5f627562ee0d9d6d934dcd06c6f8e",
            "pkg-object-srcpkg-campaign35-nor-exports-share-statistical-summary-v2.json": "097c9c1bcfe90d07c76295ef4d514750e71ffe027620f89ce75f50ec579cf3ca",
        }
        for name, digest in expected.items():
            self.assertEqual(__import__('hashlib').sha256((PROJECT_ROOT / "knowledge_repository" / "objects" / name).read_bytes()).hexdigest(), digest)


if __name__ == "__main__":
    unittest.main()
