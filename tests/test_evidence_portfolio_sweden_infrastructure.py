from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


epp = load("epp_shared", ROOT / "tools/evidence_portfolio_production.py")
swe = load("epp_sweden", ROOT / "tools/evidence_portfolio_sweden_infrastructure.py")


class SwedenInfrastructurePreregistrationTests(unittest.TestCase):
    def setUp(self):
        self.rubric, self.manifest = swe.build_preregistration()
        self.execute = [e for e in self.manifest["entries"] if e["disposition"] == "execute"]

    def test_exact_frozen_population_and_limits(self):
        self.assertEqual(self.manifest["campaign_id"], "evidence-portfolio-infrastructure-sweden-baseline-20260731")
        self.assertEqual([e["indicator"]["code"] for e in self.execute], ["IT.NET.USER.ZS", "IT.CEL.SETS.P2"])
        self.assertEqual([e["canary"] for e in self.execute], [True, False])
        self.assertEqual(self.manifest["computational_budget"], {"maximum_executed_candidates": 2, "maximum_promoted_objects": 2, "maximum_raw_result_records": 56, "stop_on_canary_failure": True})
        self.assertTrue(all(e["computational_budget"] == {"maximum_result_records": 28, "maximum_wall_seconds": 5} for e in self.manifest["entries"]))
        excluded = [e for e in self.manifest["entries"] if e["disposition"] == "excluded_pre_execution"]
        self.assertEqual(len(excluded), 1)
        self.assertTrue(excluded[0]["canary"])
        self.assertIn("CAGR", excluded[0]["exclusion_reason"])

    def test_fixture_hashes_and_registry_admission_are_frozen(self):
        self.assertEqual([e["input"]["sha256"] for e in self.execute], [
            "sha256:45a1e0f2b69b6dd2a0011e084df3497e2c9687f776189e82cf70812b7630982d",
            "sha256:a6bc1362e18fc768478de9e2b3dfcd5cdb4222b392df5605bdb4e87819028eef",
        ])
        self.assertEqual([e["input"]["normalized_fingerprint"] for e in self.execute], [
            "sha256:ebc7b93fac69eccce658a46d2807a059636a43784f42b2e9ff9589b6e9389de2",
            "sha256:7689361a24f2545a177de984e566594b9cf1284c7bebf19ea1100c37548bf2bd",
        ])
        self.assertEqual(self.rubric["selected_candidate_id"], "infrastructure_internet_mobile_swe")
        self.assertTrue(self.rubric["recorded_before_new_outcome_calculation"])

    def test_sweden_packages_are_family_correct_deterministic_and_distinct(self):
        packages = []
        for entry in self.execute:
            result = epp.execute_entry(entry, ROOT)
            self.assertEqual(result["disposition"], "valid")
            package = epp.build_knowledge_object(entry, result, self.manifest["manifest_fingerprint"])
            self.assertEqual(package, epp.build_knowledge_object(entry, result, self.manifest["manifest_fingerprint"]))
            packages.append(package)
        rendered = epp.canonical_json(packages).lower()
        self.assertNotIn("norway", rendered)
        self.assertNotIn("health", rendered)
        for package in packages:
            source = package["scope"]["source_scope"]
            self.assertEqual((source["entity_id"], source["entity_name"]), ("SWE", "Sweden"))
            self.assertEqual(package["scope"]["evidence_family"], "external_wdi_annual_scalar_infrastructure_baseline_characterization")

    def test_semantic_review_amendment_and_measure_aware_units(self):
        self.assertEqual(self.manifest["manifest_version"], "1.1")
        self.assertEqual(
            self.manifest["amendment"]["predecessor_manifest_fingerprint"],
            "sha256:8e82a5859402f3ded40e739a0ee82525118a224d6031c4a7dbde6ae1b533a5c1",
        )
        self.assertFalse(self.manifest["amendment"]["candidate_universe_changed"])
        self.assertFalse(self.manifest["amendment"]["calculation_methods_changed"])
        across_years = "Level-distribution statistics are unweighted summaries across retained annual observations; they are not population-weighted pooled-period estimates and do not describe a cross-sectional distribution among people, users or subscriptions."
        internet_result = epp.execute_entry(self.execute[0], ROOT)
        mobile_result = epp.execute_entry(self.execute[1], ROOT)
        internet = {record["metric"]: record for record in internet_result["result_records"]}
        mobile = {record["metric"]: record for record in mobile_result["result_records"]}
        self.assertEqual(internet["arithmetic_mean"]["value"]["unit"], "% of population")
        for metric in ("population_standard_deviation", "interquartile_range", "net_level_difference"):
            self.assertEqual(internet[metric]["value"]["unit"], "percentage points")
        for metric in ("first_difference_mean", "first_difference_population_standard_deviation", "mean_absolute_first_difference", "linear_time_index_slope_per_year"):
            self.assertEqual(internet[metric]["value"]["unit"], "percentage points per year")
        self.assertEqual(mobile["arithmetic_mean"]["value"]["unit"], "mobile cellular subscriptions per 100 people")
        self.assertEqual(mobile["interquartile_range"]["value"]["unit"], "mobile cellular subscriptions per 100 people")
        self.assertEqual(mobile["first_difference_mean"]["value"]["unit"], "mobile cellular subscriptions per 100 people per year")
        self.assertTrue(all(across_years in record["limitations"] for record in internet_result["result_records"] + mobile_result["result_records"]))

    def test_limitations_are_complete_propagated_and_distinguish_measure_kind(self):
        internet, mobile = self.execute
        substantive_limit = "Shared population scaling or denominator conventions do not make Internet users and mobile cellular subscriptions substantively equivalent."
        self.assertIn(substantive_limit, self.rubric["known_limitations"])
        for entry in self.execute:
            self.assertIn(substantive_limit, entry["family_configuration"]["applicability_limitations"])
            self.assertIn(substantive_limit, entry["family_configuration"]["package_limitations"])
            limitations = " ".join(entry["family_configuration"]["applicability_limitations"]).lower()
            for concept in ("technology", "adoption", "saturation", "structural break"):
                self.assertIn(concept, limitations)
        self.assertIn("people", " ".join(internet["family_configuration"]["applicability_limitations"]).lower())
        self.assertIn("subscriptions", " ".join(mobile["family_configuration"]["applicability_limitations"]).lower())
        result = epp.execute_entry(mobile, ROOT)
        expected = mobile["family_configuration"]["result_limitations"] + mobile["family_configuration"]["applicability_limitations"]
        self.assertTrue(all(record["limitations"] == expected for record in result["result_records"]))
        package = epp.build_knowledge_object(mobile, result, self.manifest["manifest_fingerprint"])
        self.assertEqual(package["generated_statements"][0]["structured_payload"]["limitations"], mobile["family_configuration"]["package_limitations"])
        self.assertIn(substantive_limit, package["generated_statements"][0]["structured_payload"]["limitations"])
        self.assertEqual(package["confidence_quality"]["uncertainty_dimensions"], mobile["family_configuration"]["uncertainty_dimensions"])

    def test_missing_or_inconsistent_family_configuration_fails_closed(self):
        for mutation in ("missing", "wrong_family", "incomplete"):
            manifest = copy.deepcopy(self.manifest)
            entry = manifest["entries"][0]
            if mutation == "missing":
                entry.pop("family_configuration")
            elif mutation == "wrong_family":
                entry["family_configuration"]["family"] = "Health"
            else:
                entry["family_configuration"].pop("package_limitations")
            manifest["manifest_fingerprint"] = epp.fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
            with self.subTest(mutation=mutation), self.assertRaisesRegex(ValueError, "family configuration"):
                epp.validate_manifest(manifest)

    def test_complete_configuration_cannot_borrow_other_family_semantics(self):
        mutations = {
            "slug": lambda c: c.update(family_slug="health"),
            "domain": lambda c: c.update(domain="WDI Health baseline characterization"),
            "evidence_family": lambda c: c.update(evidence_family="external_wdi_annual_scalar_health_baseline_characterization"),
            "governance": lambda c: c.update(governance_review_state="bounded Health portfolio promotion contract passed"),
            "maturity": lambda c: c.update(promotion_maturity_state="bounded Health portfolio pilot accepted"),
            "date": lambda c: c.update(generation_date="2026-02-30"),
        }
        for label, mutate in mutations.items():
            manifest = copy.deepcopy(self.manifest)
            mutate(manifest["entries"][0]["family_configuration"])
            manifest["manifest_fingerprint"] = epp.fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
            with self.subTest(label=label), self.assertRaisesRegex(ValueError, "family configuration"):
                epp.validate_manifest(manifest)

    def test_relabelled_sweden_health_cannot_use_legacy_configuration_fallback(self):
        manifest = copy.deepcopy(self.manifest)
        entry = manifest["entries"][0]
        entry["indicator"]["family"] = "Health"
        entry.pop("family_configuration")
        manifest["manifest_fingerprint"] = epp.fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
        with mock.patch.object(epp, "calculate_candidate", side_effect=AssertionError("calculation reached")):
            with self.assertRaisesRegex(ValueError, "family configuration"):
                epp.validate_manifest(manifest)

    def test_entry_campaign_must_match_manifest_campaign(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["entries"][0]["campaign_id"] = "other-campaign"
        manifest["manifest_fingerprint"] = epp.fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
        with self.assertRaisesRegex(ValueError, "campaign"):
            epp.validate_manifest(manifest)

    def test_indicator_name_and_definition_bind_fixture_before_calculation(self):
        for field in ("name", "definition"):
            entry = copy.deepcopy(self.execute[0])
            entry["indicator"][field] = f"tampered {field}"
            with self.subTest(field=field), mock.patch.object(epp, "calculate_candidate", side_effect=AssertionError("calculation reached")):
                outcome = epp.execute_entry(entry, ROOT)
                self.assertEqual(outcome["disposition"], "failed")
                self.assertEqual(outcome["stage"], "input_validation")
                self.assertIn("indicator metadata", outcome["reason"])


    def test_valid_but_unauthorized_family_generation_date_fails_with_recomputed_fingerprint(self):
        manifest = copy.deepcopy(self.manifest)
        for entry in manifest["entries"]:
            entry["family_configuration"]["generation_date"] = "1999-01-01"
        manifest["manifest_fingerprint"] = epp.fingerprint({k: v for k, v in manifest.items() if k != "manifest_fingerprint"})
        with self.assertRaisesRegex(ValueError, "generation_date"):
            epp.validate_manifest(manifest)


if __name__ == "__main__":
    unittest.main()
