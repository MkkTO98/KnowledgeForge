from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "tools" / "evidence_portfolio_conformance.py"
SPEC = importlib.util.spec_from_file_location("evidence_portfolio_conformance", MODULE)
assert SPEC is not None
conformance = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(conformance)

HEALTH = ROOT / "artifacts/production/evidence-portfolio-pilot-health-baseline-20260730"
SWEDEN = ROOT / "artifacts/production/evidence-portfolio-infrastructure-sweden-baseline-20260731"
HEALTH_REPORT = ROOT / "artifacts/reports/R-20260730-first-bounded-evidence-portfolio-production-pilot.md"
SWEDEN_REPORT = ROOT / "artifacts/reports/R-20260731-second-evidence-portfolio-sweden-infrastructure-v1.md"
HEALTH_HEADING = "## 12. Architecture sustainability conclusion"
SWEDEN_HEADING = "## Production conclusion"


def report_inputs(root: Path):
    report = HEALTH_REPORT if root == HEALTH else SWEDEN_REPORT
    heading = HEALTH_HEADING if root == HEALTH else SWEDEN_HEADING
    return report, heading


def load_inputs(root: Path):
    return {
        "manifest": json.loads((root / "portfolio_manifest.json").read_text()),
        "execution_results": json.loads((root / "production_execution_results.json").read_text()),
        "packages": json.loads((root / "production_packages.json").read_text()),
        "views": json.loads((root / "production_views.json").read_text()),
    }


def build(root: Path = HEALTH):
    inputs = load_inputs(root)
    label = "Norway Health" if root == HEALTH else "Sweden Infrastructure"
    report, conclusion_heading = report_inputs(root)
    return conformance.build_historical_conformance_envelope(
        **inputs,
        portfolio_label=label,
        question=f"What deterministic baseline characteristics are present in the retained {label} annual series?",
        intended_use="bounded descriptive baseline characterization",
        prohibited_uses=["causal inference", "forecasting", "independent corroboration claim"],
        source_report_path=report.relative_to(ROOT).as_posix(),
        source_report_text=report.read_text(),
        conclusion_heading=conclusion_heading,
    )


def reseal(value):
    value["conformance_fingerprint"] = conformance.fingerprint(
        {key: item for key, item in value.items() if key != "conformance_fingerprint"}
    )
    return value


class AccountingConformanceTests(unittest.TestCase):
    def test_valid_portfolio_reconciles_exactly(self):
        envelope = build()
        result = conformance.validate_conformance_envelope(envelope)
        self.assertTrue(result["valid"])
        self.assertEqual(envelope["accounting"]["manifest_candidates"], 3)
        self.assertEqual(envelope["accounting"]["excluded_pre_execution"], 1)
        self.assertEqual(envelope["accounting"]["executed_candidates"], 2)
        self.assertEqual(envelope["accounting"]["valid_candidates"], 2)
        self.assertEqual(envelope["accounting"]["rejected_execution"], 0)
        self.assertEqual(envelope["accounting"]["valid_result_records"], 56)

    def test_missing_double_counted_contradictory_and_unknown_dispositions_fail(self):
        probes = []
        missing = build(); missing["candidate_outcomes"].pop(); probes.append(("missing", missing))
        duplicate = build(); duplicate["candidate_outcomes"].append(copy.deepcopy(duplicate["candidate_outcomes"][0])); probes.append(("duplicate", duplicate))
        contradictory = build(); contradictory["candidate_outcomes"][0]["terminal_disposition"] = "excluded_pre_execution"; probes.append(("contradictory", contradictory))
        unknown = build(); unknown["candidate_outcomes"][0]["terminal_disposition"] = "successful-ish"; probes.append(("unknown", unknown))
        for label, envelope in probes:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_outcome_relation_and_evidence_counts_are_semantically_bound(self):
        count_mismatch = build()
        outcome = count_mismatch["candidate_outcomes"][0]
        outcome["valid_result_count"] -= 1
        outcome["redundant_result_count"] += 1
        count_mismatch["accounting"] = conformance.derive_accounting(count_mismatch)
        null_support = build()
        null_support["candidate_outcomes"][0]["terminal_disposition"] = "null"
        null_support["accounting"] = conformance.derive_accounting(null_support)
        for label, envelope in [("count", count_mismatch), ("null_support", null_support)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_runtime_negative_outcomes_require_execution_stage(self):
        entry = {"disposition": "execute"}
        with self.assertRaises(ValueError):
            conformance.classify_terminal_disposition(entry, {"disposition": "rejected"})
        self.assertEqual(
            conformance.classify_terminal_disposition(entry, {"disposition": "rejected", "stage": "execution"}),
            "rejected_execution",
        )
        with self.assertRaises(ValueError):
            conformance.classify_terminal_disposition(entry, {"disposition": "failed", "stage": "pre_execution"})

    def test_transformed_records_do_not_inflate_independent_support(self):
        envelope = build()
        self.assertEqual(envelope["accounting"]["record_diversity"]["valid_result_records"], 56)
        self.assertEqual(envelope["accounting"]["record_diversity"]["transformation_definitions"], 3)
        self.assertEqual(envelope["accounting"]["record_diversity"]["transformed_series_variants"], 6)
        self.assertEqual(envelope["accounting"]["support_diversity"]["source_series_clusters"], 2)
        self.assertEqual(envelope["accounting"]["support_diversity"]["fully_independent_support_claims"], 0)
        self.assertEqual(envelope["accounting"]["support_diversity"]["shared_support_groups"], 1)


class TraceabilityConformanceTests(unittest.TestCase):
    def test_complete_directional_chain_resolves(self):
        envelope = build()
        chain = conformance.resolve_question_evidence_chain(envelope, envelope["questions"][0]["question_id"])
        self.assertEqual(len(chain["candidates"]), 3)
        self.assertEqual(len(chain["evidence_units"]), 56)
        self.assertEqual({row["relation"] for row in chain["candidate_links"]}, {"supports", "excludes"})
        self.assertTrue(all(row["historical_result_id"] for row in chain["evidence_units"]))

    def test_orphan_evidence_and_unsupported_question_link_fail(self):
        orphan = build(); orphan["evidence_units"][0]["candidate_id"] = "missing-candidate"
        unsupported = build(); unsupported["candidate_links"] = [row for row in unsupported["candidate_links"] if row["relation"] != "supports"]
        for label, envelope in [("orphan", orphan), ("unsupported", unsupported)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_direction_and_relation_substitution_fail(self):
        wrong_direction = build(); wrong_direction["candidate_links"][0]["direction"] = "evidence_to_candidate_to_question"
        wrong_relation = build(); wrong_relation["candidate_links"][0]["relation"] = "qualifies"
        for label, envelope in [("direction", wrong_direction), ("relation", wrong_relation)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_exclusion_reason_and_direction_are_manifest_bound(self):
        envelope = build()
        exclusion = next(row for row in envelope["candidate_links"] if row["relation"] == "excludes")
        exclusion["reason"] = "unrestricted all-pairs relationship excluded"
        with self.assertRaisesRegex(ValueError, "exclusion"):
            conformance.validate_conformance_envelope(reseal(envelope))

    def test_generated_ledger_cannot_drift_from_machine_chain(self):
        envelope = build(); envelope["candidate_ledger_markdown"] += "drift\n"
        with self.assertRaisesRegex(ValueError, "ledger"):
            conformance.validate_conformance_envelope(reseal(envelope))


class TransformationIdentityConformanceTests(unittest.TestCase):
    def test_same_base_series_has_distinct_stable_transformation_identities(self):
        envelope = build()
        first_source = envelope["dependence_declarations"][0]["source_series_cluster_id"]
        rows = [row for row in envelope["transformations"] if row["base_series_identity"] == first_source]
        self.assertEqual({row["transformation_id"] for row in rows}, {"level", "adjacent_first_difference", "linear_time_index_slope"})
        self.assertEqual(len({row["transformation_identity"] for row in rows}), 3)
        self.assertEqual(rows, build()["transformations"][:3])

    def test_identity_includes_definition_parameters_and_base_lineage(self):
        level = conformance.transformation_identity("source-a", {"transformation_id": "level", "operation": "identity", "parameters": {}})
        other_source = conformance.transformation_identity("source-b", {"transformation_id": "level", "operation": "identity", "parameters": {}})
        lagged = conformance.transformation_identity("source-a", {"transformation_id": "lag", "operation": "lag", "parameters": {"periods": 1}})
        lagged_two = conformance.transformation_identity("source-a", {"transformation_id": "lag", "operation": "lag", "parameters": {"periods": 2}})
        self.assertEqual(len({level, other_source, lagged, lagged_two}), 4)

    def test_orphan_transformation_and_source_lineage_substitution_fail(self):
        orphan = build(); orphan["transformations"][0]["candidate_id"] = "missing-candidate"
        detached = build(); detached["transformations"][0]["base_series_identity"] = "source-series:sha256:" + "0" * 64
        definition = {key: detached["transformations"][0][key] for key in ["transformation_id", "operation", "parameters"]}
        detached["transformations"][0]["transformation_identity"] = conformance.transformation_identity(detached["transformations"][0]["base_series_identity"], definition)
        for label, envelope in [("orphan", orphan), ("detached", detached)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_collision_incomplete_parameters_alias_and_substitution_fail(self):
        collision = build(); collision["transformations"][1]["transformation_identity"] = collision["transformations"][0]["transformation_identity"]
        incomplete = build(); slope = next(row for row in incomplete["transformations"] if row["transformation_id"] == "linear_time_index_slope"); slope["parameters"].pop("independent_variable")
        alias = build(); next(row for row in alias["transformations"] if row["transformation_id"] == "linear_time_index_slope")["transformation_id"] = "linear_time_index"
        substitution = build()
        first = substitution["evidence_units"][0]
        other = next(row for row in substitution["evidence_units"] if row["transformation_id"] != first["transformation_id"])
        first["transformation_identity"] = other["transformation_identity"]
        for label, envelope in [("collision", collision), ("incomplete", incomplete), ("alias", alias), ("substitution", substitution)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))


class DependenceConformanceTests(unittest.TestCase):
    def test_shared_source_and_method_dimensions_are_explicit(self):
        envelope = build()
        declarations = envelope["dependence_declarations"]
        self.assertEqual(len({row["source_series_cluster_id"] for row in declarations}), 2)
        self.assertEqual(len({row["provider_cluster_id"] for row in declarations}), 1)
        self.assertEqual(len({row["acquisition_cluster_id"] for row in declarations}), 1)
        self.assertEqual(len({tuple(row["method_cluster_ids"]) for row in declarations}), 1)

    def test_unresolved_dependence_is_represented_without_becoming_independence(self):
        envelope = build()
        envelope["dependence_declarations"][0]["dependence_status"] = "unresolved"
        envelope["accounting"] = conformance.derive_accounting(envelope)
        self.assertTrue(conformance.validate_conformance_envelope(reseal(envelope))["valid"])
        self.assertEqual(envelope["accounting"]["support_diversity"]["fully_independent_support_claims"], 0)

    def test_unknown_dependence_and_false_independence_fail_closed(self):
        unresolved = build(); unresolved["dependence_declarations"][0]["dependence_status"] = "unresolved"; unresolved["accounting"]["support_diversity"]["fully_independent_support_claims"] = 1
        false_independence = build(); false_independence["accounting"]["support_diversity"]["fully_independent_support_claims"] = 2
        missing = build(); missing["dependence_declarations"][0].pop("method_cluster_ids")
        for label, envelope in [("unresolved", unresolved), ("false", false_independence), ("missing", missing)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_shared_lineage_cannot_masquerade_under_different_cluster_ids(self):
        provider = build(); provider["dependence_declarations"][0]["provider_cluster_id"] = "provider-cluster-forged"; provider["accounting"] = conformance.derive_accounting(provider)
        acquisition = build(); acquisition["dependence_declarations"][0]["acquisition_cluster_id"] = "acquisition-cluster-forged"; acquisition["accounting"] = conformance.derive_accounting(acquisition)
        method = build(); method["dependence_declarations"][0]["method_cluster_ids"][0] = "method-cluster-forged"; method["accounting"] = conformance.derive_accounting(method)
        for label, envelope in [("provider", provider), ("acquisition", acquisition), ("method", method)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_coherent_dependence_basis_replacement_fails(self):
        provider = build(); provider["dependence_declarations"][0]["provider_basis"] = {"provider": "forged", "dataset": "forged"}; provider["dependence_declarations"][0]["provider_cluster_id"] = conformance.fingerprint(provider["dependence_declarations"][0]["provider_basis"]).replace("sha256:", "provider-cluster-")[:41]; provider["accounting"] = conformance.derive_accounting(provider)
        acquisition = build(); acquisition["dependence_declarations"][0]["acquisition_basis"] = ["forged_fixture"]; acquisition["dependence_declarations"][0]["acquisition_cluster_id"] = conformance.fingerprint(acquisition["dependence_declarations"][0]["acquisition_basis"]).replace("sha256:", "acquisition-cluster-")[:44]; acquisition["accounting"] = conformance.derive_accounting(acquisition)
        method = build(); method["dependence_declarations"][0]["method_basis"] = ["forged-method"]; method["dependence_declarations"][0]["method_cluster_ids"] = [conformance.fingerprint("forged-method").replace("sha256:", "method-cluster-")[:39]]; method["accounting"] = conformance.derive_accounting(method)
        for label, envelope in [("provider", provider), ("acquisition", acquisition), ("method", method)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_shared_attribute_does_not_collapse_legitimate_distinct_series(self):
        envelope = build()
        self.assertEqual(envelope["accounting"]["support_diversity"]["distinct_evidence_candidates"], 2)
        self.assertEqual(envelope["accounting"]["support_diversity"]["source_series_clusters"], 2)


class CompatibilityAndPortfolioProofTests(unittest.TestCase):
    def test_historical_artifact_is_explicitly_rejected_without_adaptation(self):
        historical = load_inputs(HEALTH)["manifest"]
        with self.assertRaisesRegex(ValueError, "conformance schema"):
            conformance.validate_conformance_envelope(historical)

    def test_serialization_round_trip_and_fingerprint_are_stable(self):
        envelope = build()
        round_trip = json.loads(conformance.canonical_json(envelope))
        self.assertEqual(envelope, round_trip)
        self.assertEqual(envelope["conformance_fingerprint"], build()["conformance_fingerprint"])
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "conformance.json"
            path.write_text(conformance.pretty_json(envelope))
            self.assertEqual(json.loads(path.read_text()), envelope)

    def test_norway_health_conforms_without_rewriting_historical_identity(self):
        envelope = build(HEALTH)
        self.assertTrue(conformance.validate_conformance_envelope(envelope)["valid"])
        self.assertEqual(envelope["historical_representation"]["manifest_fingerprint"], "sha256:7c5f85ffe0660d012915db2cbec240e02e2ad4c0ca61efa2ef44298e55dedc15")
        self.assertEqual(envelope["preserved_conclusion"]["text"], conformance.extract_report_section(HEALTH_REPORT.read_text(), HEALTH_HEADING))
        self.assertEqual(envelope["preserved_conclusion"]["source_report_sha256"], conformance.text_sha256(HEALTH_REPORT.read_text()))

    def test_sweden_infrastructure_conforms_without_rewriting_historical_identity(self):
        envelope = build(SWEDEN)
        self.assertTrue(conformance.validate_conformance_envelope(envelope)["valid"])
        self.assertEqual(envelope["historical_representation"]["manifest_fingerprint"], "sha256:d59dfd9944f47aa81adf6b4bd9b5b9ddcde8551956545e21e0ab2ed34744db1f")
        self.assertEqual(envelope["preserved_conclusion"]["text"], conformance.extract_report_section(SWEDEN_REPORT.read_text(), SWEDEN_HEADING))
        self.assertEqual(envelope["preserved_conclusion"]["source_report_sha256"], conformance.text_sha256(SWEDEN_REPORT.read_text()))

    def test_coherent_cross_candidate_historical_evidence_reassignment_fails(self):
        envelope = build()
        first = next(unit for unit in envelope["evidence_units"] if unit["candidate_id"] == envelope["candidates"][0]["candidate_id"])
        second = next(unit for unit in envelope["evidence_units"] if unit["candidate_id"] == envelope["candidates"][1]["candidate_id"] and unit["transformation_id"] == first["transformation_id"])
        fields = [
            "historical_package_id", "historical_package_fingerprint", "historical_result_id",
            "historical_result_fingerprint", "historical_result_semantic_fingerprint",
            "historical_view_id", "historical_view_fingerprint",
        ]
        saved = {key: first[key] for key in fields}
        for key in fields:
            first[key] = second[key]
        for key, value in saved.items():
            second[key] = value
        for unit in [first, second]:
            unit["provenance_fingerprint"] = conformance.fingerprint({
                "input_normalized_fingerprint": unit["source_series_identity"].removeprefix("source-series:"),
                "package_id": unit["historical_package_id"],
                "result_id": unit["historical_result_id"],
                "semantic_fingerprint": unit["historical_result_semantic_fingerprint"],
            })
        with self.assertRaises(ValueError):
            conformance.validate_conformance_envelope(reseal(envelope))

    def test_embedded_source_report_package_and_question_bindings_reject_tampering(self):
        report = build(); report["preserved_conclusion"]["source_report_text"] += "\nforged"
        package = build(); package["historical_representation"]["source_packages"][0]["package_id"] = "forged-package"
        question = build(); question["questions"][0]["source_candidates"][0]["indicator_code"] = "FORGED"; question["questions"][0]["scope_fingerprint"] = conformance.fingerprint({key: value for key, value in question["questions"][0].items() if key != "scope_fingerprint"})
        for label, envelope in [("report", report), ("package", package), ("question", question)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_unknown_historical_transformation_and_extra_populations_fail_adaptation(self):
        report, heading = report_inputs(HEALTH)
        kwargs = {
            "portfolio_label": "Norway Health",
            "question": "What bounded characteristics are present?",
            "intended_use": "bounded description",
            "prohibited_uses": ["causal inference"],
            "source_report_path": report.relative_to(ROOT).as_posix(),
            "source_report_text": report.read_text(),
            "conclusion_heading": heading,
        }
        unknown = load_inputs(HEALTH)
        unknown["packages"] = copy.deepcopy(unknown["packages"])
        unknown["packages"][0]["generated_statements"][0]["structured_payload"]["result_records"][0]["transformation"] = "unknown_transform"
        extra_package = load_inputs(HEALTH); extra_package["packages"] = copy.deepcopy(extra_package["packages"]); extra_package["packages"].append(copy.deepcopy(extra_package["packages"][0])); extra_package["packages"][-1]["package_id"] = "unrelated-package"
        duplicate_view = load_inputs(HEALTH); duplicate_view["views"] = copy.deepcopy(duplicate_view["views"]); duplicate_view["views"].append(copy.deepcopy(duplicate_view["views"][0]))
        for label, inputs in [("unknown", unknown), ("extra_package", extra_package), ("duplicate_view", duplicate_view)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.build_historical_conformance_envelope(**inputs, **kwargs)

    def test_malformed_identifiers_and_hidden_extension_fields_fail(self):
        malformed = build(); malformed["candidates"][0]["candidate_id"] = ""
        extension = build(); extension["candidate_outcomes"][0]["hidden_semantics"] = True
        for label, envelope in [("malformed", malformed), ("extension", extension)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_top_level_extensions_malformed_prohibited_uses_and_report_paths_fail(self):
        extension = build(); extension["hidden_semantics"] = True
        prohibited = build(); prohibited["questions"][0]["prohibited_uses"] = [""]; prohibited["questions"][0]["scope_fingerprint"] = conformance.fingerprint({key: value for key, value in prohibited["questions"][0].items() if key != "scope_fingerprint"})
        report_path = build(); report_path["preserved_conclusion"]["source_report"] = "../escape.md"; report_path["preserved_conclusion_fingerprint"] = conformance.fingerprint(report_path["preserved_conclusion"])
        for label, envelope in [("extension", extension), ("prohibited", prohibited), ("report_path", report_path)]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                conformance.validate_conformance_envelope(reseal(envelope))

    def test_views_and_packages_are_only_referenced_not_rewritten(self):
        inputs = load_inputs(HEALTH); envelope = build(HEALTH)
        self.assertEqual(envelope["historical_representation"]["package_fingerprints"], [conformance.fingerprint(value) for value in inputs["packages"]])
        self.assertEqual(envelope["historical_representation"]["view_fingerprints"], [value["view_fingerprint"] for value in inputs["views"]])
        self.assertNotIn("corrected_packages", envelope)
        self.assertNotIn("corrected_views", envelope)


if __name__ == "__main__":
    unittest.main()
