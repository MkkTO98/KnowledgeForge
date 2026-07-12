from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = PROJECT_ROOT / "tools" / "wdi_observation_evidence_fixture.py"


def load_module():
    spec = importlib.util.spec_from_file_location("wdi_observation_evidence_fixture", MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load module: {MODULE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def provider_payload(records: list[dict]) -> list:
    return [
        {"page": 1, "pages": 1, "per_page": 100, "total": len(records), "sourceid": "2", "lastupdated": "2026-07-01"},
        records,
    ]


def metadata_payload() -> list:
    return [
        {"page": 1, "pages": 1, "per_page": "1", "total": 1},
        [
            {
                "id": "SP.POP.TOTL",
                "name": "Population, total",
                "unit": "",
                "source": {"id": "2", "value": "World Development Indicators"},
                "sourceNote": "Total population is based on the de facto definition of population.",
                "sourceOrganization": "World Population Prospects, United Nations (UN)",
                "topics": [{"id": "8", "value": "Health "}],
            }
        ],
    ]


def record(year: int, value):
    return {
        "indicator": {"id": "SP.POP.TOTL", "value": "Population, total"},
        "country": {"id": "DK", "value": "Denmark"},
        "countryiso3code": "DNK",
        "date": str(year),
        "value": value,
        "unit": "",
        "obs_status": "",
        "decimal": 0,
    }


class WDIObservationEvidenceFixtureTest(unittest.TestCase):
    def setUp(self):
        self.module = load_module()
        self.contract = self.module.build_selection_contract(
            indicator_code="SP.POP.TOTL",
            entities=["DNK"],
            start_year=2020,
            end_year=2022,
        )
        self.raw = self.module.raw_fixture_from_provider_payloads(
            selection_contract=self.contract,
            observation_payload=provider_payload([
                record(2022, 5946952),
                record(2021, None),
                record(2020, 5831404),
            ]),
            indicator_metadata_payload=metadata_payload(),
            observation_response_bytes=b"observation-bytes",
            indicator_metadata_response_bytes=b"metadata-bytes",
            access_timestamp_utc="2026-07-10T00:00:00Z",
        )

    def test_normalization_is_deterministic_and_preserves_missingness(self):
        normalized = self.module.normalize_raw_fixture(self.raw)
        repeated = self.module.normalize_raw_fixture(self.raw)

        self.assertEqual(normalized["normalized_fingerprint"], repeated["normalized_fingerprint"])
        self.assertEqual([obs["period"] for obs in normalized["observations"]], [2020, 2021, 2022])
        self.assertEqual([obs["observed"] for obs in normalized["observations"]], [True, False, True])
        self.assertEqual(normalized["observed_count"], 2)
        self.assertEqual(normalized["missing_count"], 1)
        self.assertEqual(normalized["observations"][0]["value_canonical"], "5831404")
        self.assertIsNone(normalized["observations"][1]["value_canonical"])

    def test_order_independence_of_normalized_fingerprint(self):
        reversed_raw = dict(self.raw)
        reversed_raw["provider_payloads"] = dict(self.raw["provider_payloads"])
        reversed_raw["provider_payloads"]["observations"] = [
            self.raw["provider_payloads"]["observations"][0],
            list(reversed(self.raw["provider_payloads"]["observations"][1])),
        ]
        self.assertEqual(
            self.module.normalize_raw_fixture(self.raw)["normalized_fingerprint"],
            self.module.normalize_raw_fixture(reversed_raw)["normalized_fingerprint"],
        )

    def test_duplicate_observations_are_rejected(self):
        bad = self.module.raw_fixture_from_provider_payloads(
            selection_contract=self.contract,
            observation_payload=provider_payload([record(2020, 1), record(2020, 2)]),
            indicator_metadata_payload=metadata_payload(),
            observation_response_bytes=b"observation-bytes",
            indicator_metadata_response_bytes=b"metadata-bytes",
            access_timestamp_utc="2026-07-10T00:00:00Z",
        )
        with self.assertRaisesRegex(ValueError, "duplicate observation"):
            self.module.normalize_raw_fixture(bad)

    def test_selection_scope_is_enforced(self):
        outside = record(2020, 1)
        outside["countryiso3code"] = "SWE"
        outside["country"] = {"id": "SE", "value": "Sweden"}
        bad = self.module.raw_fixture_from_provider_payloads(
            selection_contract=self.contract,
            observation_payload=provider_payload([outside]),
            indicator_metadata_payload=metadata_payload(),
            observation_response_bytes=b"observation-bytes",
            indicator_metadata_response_bytes=b"metadata-bytes",
            access_timestamp_utc="2026-07-10T00:00:00Z",
        )
        with self.assertRaisesRegex(ValueError, "outside entity scope"):
            self.module.normalize_raw_fixture(bad)

    def test_raw_fingerprint_verification_rejects_tampering(self):
        tampered = dict(self.raw)
        tampered["raw_artifacts"] = dict(self.raw["raw_artifacts"])
        tampered["raw_artifacts"]["observation_response_sha256"] = "sha256:bad"
        with self.assertRaisesRegex(ValueError, "raw observation fingerprint mismatch"):
            self.module.validate_raw_fixture(tampered)

    def test_malformed_provider_response_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "provider response must be"):
            self.module.raw_fixture_from_provider_payloads(
                selection_contract=self.contract,
                observation_payload={"not": "a world bank response"},
                indicator_metadata_payload=metadata_payload(),
                observation_response_bytes=b"observation-bytes",
                indicator_metadata_response_bytes=b"metadata-bytes",
                access_timestamp_utc="2026-07-10T00:00:00Z",
            )

    def test_offline_reproduction_from_retained_raw_fixture(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp)
            self.module.write_fixture_artifacts(self.raw, output_dir)
            regenerated = self.module.regenerate_normalized_from_raw(output_dir)
            written = json.loads((output_dir / "normalized_observations.json").read_text())
            self.assertEqual(regenerated["normalized_fingerprint"], written["normalized_fingerprint"])
            self.assertEqual(regenerated["observations"], written["observations"])

    def test_module_has_no_macroforge_runtime_or_database_dependency(self):
        source = MODULE_PATH.read_text()
        forbidden = ["MacroForge", "macroforge", "psql", "psycopg", "postgres", "sqlite", "duckdb"]
        for term in forbidden:
            self.assertNotIn(term, source)

    def test_selection_contract_uses_https_urls(self):
        self.assertTrue(self.contract["request"]["observation_url"].startswith("https://api.worldbank.org/"))
        self.assertTrue(self.contract["request"]["indicator_metadata_url"].startswith("https://api.worldbank.org/"))

    def test_https_downgrade_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "HTTPS downgrade"):
            self.module.validate_final_url(
                requested_url="https://api.worldbank.org/v2/country/DNK/indicator/SP.POP.TOTL",
                final_url="http://api.worldbank.org/v2/country/DNK/indicator/SP.POP.TOTL",
            )

    def test_raw_fixture_records_final_resolved_urls(self):
        self.assertEqual(
            self.raw["access_metadata"]["final_resolved_urls"]["observation_response"],
            self.contract["request"]["observation_url"],
        )
        self.assertEqual(
            self.raw["access_metadata"]["final_resolved_urls"]["indicator_metadata_response"],
            self.contract["request"]["indicator_metadata_url"],
        )


if __name__ == "__main__":
    unittest.main()
