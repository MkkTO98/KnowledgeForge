from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUPPORT_PATH = PROJECT_ROOT / "tools" / "production_support.py"
CAMPAIGN3_PATH = PROJECT_ROOT / "tools" / "run_campaign3_wdi_freshness_metadata.py"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ProductionSupportTests(unittest.TestCase):
    def test_source_package_builder_matches_existing_campaign3_contract(self):
        support = load_module(SUPPORT_PATH, "production_support")
        campaign3 = load_module(CAMPAIGN3_PATH, "campaign3_for_support_test")
        snapshot = campaign3.immutable_wdi_freshness_snapshot()
        metadata = {"topic": "last-updated metadata availability", "available": True, "coverage": 1.0}

        expected = campaign3.source_package(
            "srcpkg-campaign3-lastupdated-availability",
            "The Campaign 3 WDI freshness snapshot records last-updated metadata availability for every audited pipeline-run record.",
            "provenance",
            snapshot,
            metadata,
        )
        actual = support.build_source_evidence_package(
            package_id="srcpkg-campaign3-lastupdated-availability",
            statement="The Campaign 3 WDI freshness snapshot records last-updated metadata availability for every audited pipeline-run record.",
            category="provenance",
            created_at=campaign3.CAMPAIGN_DATE,
            source_name="World Bank World Development Indicators audited demographic-structure freshness metadata snapshot",
            source_family="external_wdi_annual_scalar_demographic_structure_freshness_metadata",
            source_version=snapshot["snapshot_fingerprint"],
            scope=campaign3.package_scope("last-updated metadata availability"),
            payload_metadata=metadata,
            evidence_class="external_observational_metadata",
            classification={
                "generated_by_llm": False,
                "contains_observational_values": False,
                "direct_evidence": True,
                "evidence_kind": "audited_wdi_demographic_structure_freshness_metadata",
                "campaign_id": campaign3.CAMPAIGN_ID,
            },
            validation_metadata={
                "validator": "construct_knowledge_package_v1",
                "campaign": campaign3.CAMPAIGN_ID,
                "source_snapshot_fingerprint": snapshot["snapshot_fingerprint"],
            },
            provenance={
                "source_snapshot_id": snapshot["snapshot_fingerprint"],
                "source_snapshot_date": campaign3.CAMPAIGN_DATE,
                "evidence_basis": snapshot["evidence_basis"],
                "selection_rule": "approved Campaign 3 WDI annual-scalar demographic-structure source freshness and release metadata scope",
                "source_family": snapshot["evidence_family"],
            },
            reproducibility={
                "state": "reproducible",
                "handle": f"python3 tools/run_campaign3_wdi_freshness_metadata.py --output artifacts/production/{campaign3.CAMPAIGN_ID}",
                "rerun_method": "deterministic embedded immutable WDI freshness metadata snapshot and canonical JSON construction",
                "nondeterminism": "none",
            },
            fingerprint_builder=campaign3.constructor.expected_source_fingerprints,
        )
        self.assertEqual(actual, expected)

    def test_quality_metric_aggregation_matches_campaign3_common_metrics(self):
        support = load_module(SUPPORT_PATH, "production_support")
        campaign3 = load_module(CAMPAIGN3_PATH, "campaign3_for_quality_test")
        snapshot = campaign3.immutable_wdi_freshness_snapshot()
        source_packages = campaign3.build_source_packages(snapshot)
        pipelines = [campaign3.constructor.construct_pipeline(pkg) for pkg in source_packages]
        accepted = [p["knowledge_object_package"] for p in pipelines]
        rejected_records = []
        for pkg in campaign3.build_rejected_source_packages(snapshot):
            pipeline = campaign3.constructor.construct_pipeline(pkg)
            validation = campaign3.validate_pipeline(pipeline) if "knowledge_object_package" in pipeline else {"ok": False, "stage_reports": {"source": pipeline["source_validation"]}}
            rejected_records.append({
                "source_evidence_package": pkg,
                "validation": campaign3.report_dict(validation),
                "reason_categories": campaign3.blocker_categories(validation["stage_reports"]),
            })

        metrics = support.aggregate_common_quality_metrics(
            campaign_id=campaign3.CAMPAIGN_ID,
            source_packages=source_packages,
            knowledge_candidates=[p["knowledge_candidate_package"] for p in pipelines],
            accepted_objects=accepted,
            rejected_records=rejected_records,
            validation_records=[{"validation": campaign3.report_dict(campaign3.validator.validate_knowledge_object(obj))} for obj in accepted],
            determinism_verified=True,
            fingerprint_stability=True,
            duplicate_knowledge_objects_detected=False,
        )

        self.assertEqual(metrics["source_evidence_packages_processed"], 12)
        self.assertEqual(metrics["knowledge_candidate_packages_generated"], 12)
        self.assertEqual(metrics["knowledge_object_packages_accepted"], 12)
        self.assertEqual(metrics["rejected_candidates"], 4)
        self.assertEqual(metrics["acceptance_rate"], 0.75)
        self.assertEqual(metrics["rejection_rate"], 0.25)
        self.assertEqual(metrics["knowledge_categories_produced"], {"classified": 1, "coverage": 1, "evidence_quality": 2, "methodological": 5, "negative": 2, "provenance": 1})
        self.assertEqual(metrics["validator_failures_by_category"], {"constitutional_boundary": 1, "evidence_contract": 2, "lineage_fingerprint": 2, "provenance": 1, "unsupported_inference": 1})
        self.assertTrue(metrics["provenance_completeness"])
        self.assertTrue(metrics["determinism_verification"])


if __name__ == "__main__":
    unittest.main()
