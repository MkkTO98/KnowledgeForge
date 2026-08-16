#!/usr/bin/env python3
"""Coefficient-free Pearson candidate registry helper.

This helper constructs and validates frozen Pearson candidate registries from retained
KnowledgeForge WDI evidence fixtures. It is deliberately pre-calculation only: it may
inspect metadata, fingerprints, missingness/overlap, units, transformations, duplicate
identity, and existing package identities, but it must not compute Pearson coefficients,
covariance, p-values, significance measures, or any other association outcome.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass, replace
from decimal import Decimal, ROUND_FLOOR
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
METHOD_IDENTITY = "wdi_annual_scalar_pearson_correlation_v1@1.0"
METHOD_CONTRACT_FINGERPRINT = "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476"
ENGINE_CONTRACT = "correlation_batch_engine_v1"
DEFAULT_FIXTURE_ROOT = Path("artifacts/evidence-fixtures/campaign40-spec-driven-pearson-production-1990-2024-https")
DEFAULT_REPORT_ROOT = Path("artifacts/reports/campaign41-coefficient-free-pearson-candidate-registry-20260712")
DEFAULT_SPEC_PATH = Path("specs/correlation_batches/campaign41_coefficient_free_pearson_batch_spec.json")
FORBIDDEN_KEYS = {
    "pearson_coefficient",
    "coefficient",
    "coefficient_magnitude",
    "coefficient_sign",
    "correlation",
    "covariance",
    "p_value",
    "significance",
    "r_squared",
    "regression",
}
FUNNEL_RESULT_DERIVED_KEYS = FORBIDDEN_KEYS | {
    "acceptance_prediction",
    "association_outcome",
    "coefficient_estimate",
    "correlation_coefficient",
    "effect_size",
    "generated_statement",
    "generated_statements",
    "lag",
    "lag_result",
    "pearson_r",
    "preliminary_result",
    "preliminary_result_cache",
    "result_rank",
}

FAMILY_BY_INDICATOR = {
    "AG.LND.AGRI.ZS": "Agriculture & Rural Development",
    "AG.LND.FRST.ZS": "Agriculture & Rural Development",
    "EG.ELC.FOSL.ZS": "Energy & Mining",
    "EG.ELC.RNWX.ZS": "Energy & Mining",
    "FB.ATM.TOTL.P5": "Financial Sector",
    "FM.LBL.BMNY.GD.ZS": "Financial Sector",
    "FS.AST.PRVT.GD.ZS": "Financial Sector",
    "IT.CEL.SETS.P2": "Infrastructure",
    "IT.NET.USER.ZS": "Infrastructure",
    "SE.PRM.ENRR": "Education",
    "SE.SEC.ENRR": "Education",
    "SH.DYN.MORT": "Health",
    "SP.DYN.CBRT.IN": "Demographic",
    "SP.DYN.CDRT.IN": "Demographic",
    "SP.DYN.LE00.IN": "Demographic",
}

# Existing canonical or frozen prior relationship pairs to exclude for same entity/scope/transformation.
EXCLUDED_PRIOR_PAIRS = {
    ("DNK", "AG.LND.AGRI.ZS", "AG.LND.FRST.ZS"): "campaign40 canonicalized agriculture/agricultural-forest land relationship",
    ("DNK", "FM.LBL.BMNY.GD.ZS", "FS.AST.PRVT.GD.ZS"): "campaign40 canonicalized finance credit/broad money relationship",
    ("DNK", "NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"): "campaign36 canonicalized exports/imports share relationship",
    ("NOR", "EG.ELC.FOSL.ZS", "EG.ELC.RNWX.ZS"): "campaign40 canonicalized fossil/nonhydro renewables relationship",
    ("NOR", "SE.PRM.ENRR", "SE.SEC.ENRR"): "campaign40 frozen/rejected primary/secondary enrollment relationship",
    ("NOR", "SH.DYN.MORT", "SP.DYN.LE00.IN"): "campaign40 canonicalized health life-expectancy/under-5 mortality relationship",
    ("NOR", "SP.DYN.CBRT.IN", "SP.DYN.CDRT.IN"): "campaign40 canonicalized birth/death rates relationship",
    ("NOR", "NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"): "campaign37 canonicalized exports/imports share relationship",
    ("SWE", "FB.ATM.TOTL.P5", "FS.AST.PRVT.GD.ZS"): "campaign40 frozen/rejected ATM/private credit relationship",
    ("SWE", "IT.CEL.SETS.P2", "IT.NET.USER.ZS"): "campaign40 canonicalized internet/mobile relationship",
    ("SWE", "NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"): "campaign37 canonicalized exports/imports share relationship",
}

MECHANICAL_EXCLUSIONS = {
    tuple(sorted(("AG.LND.AGRI.ZS", "AG.LND.FRST.ZS"))): "same land-area denominator and direct land-share family already canonicalized; avoid component/near-component pressure",
    tuple(sorted(("EG.ELC.FOSL.ZS", "EG.ELC.RNWX.ZS"))): "electricity-source shares of total electricity already canonicalized; avoid component-share pressure",
    tuple(sorted(("NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"))): "trade exports/imports share pair already canonicalized for available entities",
    tuple(sorted(("SE.PRM.ENRR", "SE.SEC.ENRR"))): "near-duplicate school-enrollment construction and insufficient retained overlap in prior freeze",
}

SLUGS = {
    "AG.LND.AGRI.ZS": "agricultural-land",
    "AG.LND.FRST.ZS": "forest-area",
    "EG.ELC.FOSL.ZS": "fossil-electricity",
    "EG.ELC.RNWX.ZS": "nonhydro-renewable-electricity",
    "FB.ATM.TOTL.P5": "atms",
    "FM.LBL.BMNY.GD.ZS": "broad-money",
    "FS.AST.PRVT.GD.ZS": "private-credit",
    "IT.CEL.SETS.P2": "mobile-cellular",
    "IT.NET.USER.ZS": "internet-users",
    "SE.PRM.ENRR": "primary-enrollment",
    "SE.SEC.ENRR": "secondary-enrollment",
    "SH.DYN.MORT": "under5-mortality",
    "SP.DYN.CBRT.IN": "crude-birth-rate",
    "SP.DYN.CDRT.IN": "crude-death-rate",
    "SP.DYN.LE00.IN": "life-expectancy",
}

ENTITY_ORDER = {"DNK": 0, "NOR": 1, "SWE": 2}


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_value(value: Any) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_file(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text())


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n")


def has_forbidden_key(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in FORBIDDEN_KEYS or has_forbidden_key(item):
                return True
    elif isinstance(value, list):
        return any(has_forbidden_key(item) for item in value)
    return False


def has_funnel_result_derived_key(value: Any) -> bool:
    result_markers = (
        "acceptanceprediction", "associationscore", "associationoutcome", "candidatepaircoefficient",
        "coefficient", "correlationresult", "covariance", "effectsize", "generatedrelationship",
        "generatedstatement", "lagestimate", "lagresult", "lags", "pearsonr", "preliminaryresult", "pvalue",
        "regression", "resultcache", "resultderived", "resultrank", "significance",
    )
    if isinstance(value, dict):
        for key, item in value.items():
            normalized = re.sub(r"[^a-z0-9]+", "", str(key).lower())
            allowed_boundary_markers = {"coefficientfree", "candidatepairresultsused", "resultderivedinputsused"}
            if normalized not in allowed_boundary_markers and (
                str(key).lower() in FUNNEL_RESULT_DERIVED_KEYS
                or any(marker in normalized for marker in result_markers)
            ):
                return True
            if has_funnel_result_derived_key(item):
                return True
    elif isinstance(value, list):
        return any(has_funnel_result_derived_key(item) for item in value)
    return False


@dataclass(frozen=True)
class Series:
    code: str
    entity: str
    name: str
    definition: str
    unit: str
    frequency: str
    transformation: str
    family: str
    normalized_path: str
    normalized_fingerprint: str
    validation_path: str
    validation_fingerprint: str
    raw_fixture_path: str
    raw_fixture_fingerprint: str
    selection_contract_path: str
    selection_contract_fingerprint: str
    acquisition_manifest_path: str
    acquisition_manifest_fingerprint: str
    observed_periods: tuple[int, ...]
    missing_periods: tuple[int, ...]

    @property
    def observed_count(self) -> int:
        return len(self.observed_periods)


def _rel(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT)) if path.is_absolute() and path.is_relative_to(PROJECT_ROOT) else str(path)


def load_series_pool(fixture_root: Path = DEFAULT_FIXTURE_ROOT) -> list[Series]:
    root = PROJECT_ROOT / fixture_root if not fixture_root.is_absolute() else fixture_root
    series: list[Series] = []
    for normalized_path in sorted(root.glob("*/normalized_observations.json")):
        data = read_json(normalized_path)
        validation_path = normalized_path.parent / "validation_results.json"
        validation = read_json(validation_path)
        if validation.get("valid") is False:
            continue
        observations = data["observations"]
        first = observations[0]
        md = data.get("indicator_metadata", {})
        code = md.get("id") or first["indicator_code"]
        entity_values = sorted({row["entity_id"] for row in observations})
        if len(entity_values) != 1:
            continue
        observed = tuple(sorted(int(row["period"]) for row in observations if row.get("value_canonical") is not None))
        all_periods = tuple(range(1990, 2025))
        missing = tuple(y for y in all_periods if y not in observed)
        series.append(
            Series(
                code=code,
                entity=entity_values[0],
                name=md.get("name") or first.get("indicator_name") or code,
                definition=md.get("definition") or "",
                unit=md.get("unit") or first.get("unit") or "",
                frequency=first.get("frequency", "annual"),
                transformation=first.get("transformation", "raw"),
                family=FAMILY_BY_INDICATOR.get(code, "Unknown"),
                normalized_path=_rel(normalized_path),
                normalized_fingerprint=data.get("normalized_fingerprint") or sha256_file(normalized_path),
                validation_path=_rel(validation_path),
                validation_fingerprint=sha256_file(validation_path),
                raw_fixture_path=_rel(normalized_path.parent / "raw_fixture.json"),
                raw_fixture_fingerprint=sha256_file(normalized_path.parent / "raw_fixture.json"),
                selection_contract_path=_rel(normalized_path.parent / "selection_contract.json"),
                selection_contract_fingerprint=sha256_file(normalized_path.parent / "selection_contract.json"),
                acquisition_manifest_path=_rel(normalized_path.parent / "acquisition_manifest.json"),
                acquisition_manifest_fingerprint=sha256_file(normalized_path.parent / "acquisition_manifest.json"),
                observed_periods=observed,
                missing_periods=missing,
            )
        )
    return series


def canonical_pair_key(entity: str, a: str, b: str) -> tuple[str, str, str]:
    x, y = sorted((a, b))
    return (entity, x, y)

def remote_cap_count(batch_size: int, share: str = "0.25") -> int:
    if batch_size < 0:
        raise ValueError("batch_size must be non-negative")
    cap = (Decimal(batch_size) * Decimal(share)).to_integral_value(rounding=ROUND_FLOOR)
    return int(cap)


def extract_pearson_relationship_key(package: dict[str, Any]) -> tuple[str, str, str] | None:
    for statement in package.get("generated_statements", []):
        payload = statement.get("structured_payload", {})
        if statement.get("statement_type") != "derived_relationship":
            continue
        if payload.get("method_contract_fingerprint") != METHOD_CONTRACT_FINGERPRINT:
            continue
        entity = payload.get("entity_id")
        series_a = payload.get("series_a", {})
        series_b = payload.get("series_b", {})
        if not entity or not series_a.get("code") or not series_b.get("code"):
            continue
        if series_a.get("transformation", "raw") != "raw" or series_b.get("transformation", "raw") != "raw":
            continue
        if statement.get("applicability", {}).get("frequency") != "annual":
            continue
        return canonical_pair_key(entity, series_a["code"], series_b["code"])
    return None


def load_current_canonical_pearson_relationship_keys(repository_root: Path | None = None) -> set[tuple[str, str, str]]:
    root = repository_root or (PROJECT_ROOT / "knowledge_repository" / "objects")
    keys: set[tuple[str, str, str]] = set()
    for path in sorted(root.glob("*.json")):
        try:
            package = read_json(path)
        except Exception:
            continue
        if package.get("status") != "accepted":
            continue
        key = extract_pearson_relationship_key(package)
        if key:
            keys.add(key)
    return keys


def candidate_id(entity: str, a: Series, b: Series) -> str:
    return f"{entity.lower()}_{SLUGS[a.code].replace('-', '_')}_{SLUGS[b.code].replace('-', '_')}"


def package_id(entity: str, a: Series, b: Series) -> str:
    return f"pkg-object-srcpkg-campaign41-{entity.lower()}-{SLUGS[a.code]}-{SLUGS[b.code]}-pearson-correlation-v1"


def construction_risk(a: Series, b: Series) -> dict[str, str]:
    shared_denominator = "not present"
    if a.unit == b.unit and a.unit in {"% of land area", "% of total", "percent of GDP"}:
        shared_denominator = "material limitation"
    elif "%" in a.unit and "%" in b.unit:
        shared_denominator = "ordinary limitation"
    definitional_overlap = "not present"
    if a.family == b.family:
        definitional_overlap = "ordinary limitation"
    return {
        "algebraic_identity": "not present",
        "common_administrative_reporting": "ordinary limitation",
        "common_modeled_estimation_process": "ordinary limitation",
        "definitional_overlap": definitional_overlap,
        "direct_component_total_construction": "not present",
        "embedded_series_construction": "not present",
        "frequency_mismatch": "not present",
        "shared_denominator": shared_denominator,
        "transformation_mismatch": "not present",
        "unit_incompatibility": "not present",
    }


def semantic_limitations(a: Series, b: Series) -> list[str]:
    limits = [
        "Pearson relationship is contemporaneous and descriptive only.",
        "No causation, explanation, mechanism, forecast, prediction, recommendation, statistical-significance, stationarity, trend, or investment claim is authorized.",
        "Different units are acceptable for Pearson calculation but make the coefficient dimensionless and limited to the retained finite window.",
        "WDI source data are mutable; retained raw fixture bytes and normalized fingerprints are the reproducibility anchor.",
    ]
    if a.unit == b.unit:
        limits.append(f"Both indicators use unit '{a.unit}'; shared-denominator or common-construction risk is recorded as a limitation where applicable.")
    if a.family == b.family:
        limits.append("Both indicators are in the same broad WDI family; definitional or reporting-system overlap is a limitation, not an interpretation basis.")
    return limits


def evidence_identity(s: Series) -> dict[str, Any]:
    return {
        "indicator_code": s.code,
        "indicator_name": s.name,
        "definition": s.definition,
        "entity": s.entity,
        "frequency": s.frequency,
        "period_scope": {"start": 1990, "end": 2024},
        "source_identity": "World Bank WDI retained KnowledgeForge fixture",
        "unit": s.unit,
        "transformation": s.transformation,
        "normalized_path": s.normalized_path,
        "normalized_fingerprint": s.normalized_fingerprint,
        "validation_path": s.validation_path,
        "validation_fingerprint": s.validation_fingerprint,
        "raw_fixture_path": s.raw_fixture_path,
        "raw_fixture_fingerprint": s.raw_fixture_fingerprint,
        "selection_contract_path": s.selection_contract_path,
        "selection_contract_fingerprint": s.selection_contract_fingerprint,
        "acquisition_manifest_path": s.acquisition_manifest_path,
        "acquisition_manifest_fingerprint": s.acquisition_manifest_fingerprint,
        "observed_count": s.observed_count,
        "missing_periods": list(s.missing_periods),
    }


def build_candidate(a: Series, b: Series) -> dict[str, Any]:
    # Canonicalize pair ordering by broad family, indicator code, then name. This is result-independent.
    ordered = sorted([a, b], key=lambda s: (s.family, s.code, s.name))
    a, b = ordered[0], ordered[1]
    periods = list(range(1990, 2025))
    aligned = [y for y in periods if y in a.observed_periods and y in b.observed_periods]
    coverage = str(len(aligned) / len(periods)).rstrip("0").rstrip(".") if aligned else "0"
    cid = candidate_id(a.entity, a, b)
    return {
        "candidate_id": cid,
        "entity": a.entity,
        "family": f"{a.family} x {b.family}" if a.family != b.family else a.family,
        "period": {"start": 1990, "end": 2024},
        "expected_package_id": package_id(a.entity, a, b),
        "method_contract": {
            "identity": METHOD_IDENTITY,
            "contract_fingerprint": METHOD_CONTRACT_FINGERPRINT,
        },
        "alignment_keys": ["entity_id", "indicator_code", "annual_period"],
        "transformation_state": {"series_a": a.transformation, "series_b": b.transformation},
        "thresholds": {"min_aligned_pairs": 30, "min_aligned_coverage": "0.85"},
        "selection_evidence": {
            "coefficient_free": True,
            "coverage_probe": {
                "expected_slots": 35,
                "expected_aligned_pairs": len(aligned),
                "aligned_coverage": coverage,
                "series_a_observed": a.observed_count,
                "series_b_observed": b.observed_count,
                "missing_series_a": list(a.missing_periods),
                "missing_series_b": list(b.missing_periods),
            },
            "variance_probe": {
                "series_a_nonconstant": "not evaluated in registry task; deferred to Pearson engine before calculation",
                "series_b_nonconstant": "not evaluated in registry task; deferred to Pearson engine before calculation",
            },
        },
        "construction_risk": construction_risk(a, b),
        "semantic_limitations": semantic_limitations(a, b),
        "series_a": {
            "identity": {
                "code": a.code,
                "name": a.name,
                "definition": a.definition,
                "source_identity": "World Bank WDI",
                "frequency": a.frequency,
                "unit": a.unit,
                "transformation": a.transformation,
            },
            "evidence_identity": evidence_identity(a),
            "acquisition": {
                "provider": "World Bank",
                "dataset": "World Development Indicators",
                "indicator": a.code,
                "entity": a.entity,
                "entities": [a.entity],
                "period": {"start": 1990, "end": 2024},
                "frequency": "annual",
                "expected_slots": 35,
                "https_required": True,
                "pagination_expectation": {"expected_pages": 1},
                "raw_output_identity": f"WDI {a.code} {a.entity} 1990-2024",
                "unit_resolution_expectation": a.unit,
                "retained_fixture_path": str(Path(a.normalized_path).parent),
            },
        },
        "series_b": {
            "identity": {
                "code": b.code,
                "name": b.name,
                "definition": b.definition,
                "source_identity": "World Bank WDI",
                "frequency": b.frequency,
                "unit": b.unit,
                "transformation": b.transformation,
            },
            "evidence_identity": evidence_identity(b),
            "acquisition": {
                "provider": "World Bank",
                "dataset": "World Development Indicators",
                "indicator": b.code,
                "entity": b.entity,
                "entities": [b.entity],
                "period": {"start": 1990, "end": 2024},
                "frequency": "annual",
                "expected_slots": 35,
                "https_required": True,
                "pagination_expectation": {"expected_pages": 1},
                "raw_output_identity": f"WDI {b.code} {b.entity} 1990-2024",
                "unit_resolution_expectation": b.unit,
                "retained_fixture_path": str(Path(b.normalized_path).parent),
            },
        },
    }


def enumerate_proposals(pool: list[Series], prior_pairs: set[tuple[str, str, str]] | None = None) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    proposals: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    excluded_prior_pairs = set(EXCLUDED_PRIOR_PAIRS)
    if prior_pairs:
        excluded_prior_pairs.update(prior_pairs)
    by_entity: dict[str, list[Series]] = {}
    for s in pool:
        by_entity.setdefault(s.entity, []).append(s)
    for entity, rows in sorted(by_entity.items(), key=lambda kv: ENTITY_ORDER.get(kv[0], 99)):
        rows = sorted(rows, key=lambda s: (s.family, s.code, s.name))
        for i, a in enumerate(rows):
            for b in rows[i + 1 :]:
                key = canonical_pair_key(entity, a.code, b.code)
                pair_code_key = tuple(sorted((a.code, b.code)))
                aligned = sorted(set(a.observed_periods).intersection(b.observed_periods))
                base = {"entity": entity, "series_a": a.code, "series_b": b.code, "aligned_pair_count": len(aligned)}
                if a.code == b.code:
                    excluded.append({**base, "reason": "self-correlation"}); continue
                if key in excluded_prior_pairs:
                    reason = EXCLUDED_PRIOR_PAIRS.get(key, "current canonical Pearson relationship already exists for same entity/scope/transformation")
                    record = {**base, "reason": reason}
                    if prior_pairs and key in prior_pairs and key not in EXCLUDED_PRIOR_PAIRS:
                        record["exclusion_class"] = "current_canonical_pearson_relationship"
                    excluded.append(record); continue
                if pair_code_key in MECHANICAL_EXCLUSIONS:
                    excluded.append({**base, "reason": MECHANICAL_EXCLUSIONS[pair_code_key]}); continue
                if a.frequency != "annual" or b.frequency != "annual":
                    excluded.append({**base, "reason": "frequency mismatch"}); continue
                if a.transformation != "raw" or b.transformation != "raw":
                    excluded.append({**base, "reason": "transformation mismatch"}); continue
                if not a.unit or not b.unit:
                    excluded.append({**base, "reason": "unresolved unit"}); continue
                if len(aligned) < 30:
                    excluded.append({**base, "reason": "insufficient aligned overlap under Pearson v1 threshold"}); continue
                if len(aligned) / 35 < 0.85:
                    excluded.append({**base, "reason": "insufficient aligned coverage under Pearson v1 threshold"}); continue
                proposals.append(build_candidate(a, b))
    return proposals, excluded


def select_candidates(proposals: list[dict[str, Any]], max_count: int = 8) -> list[dict[str, Any]]:
    # Result-independent ordering and diversity: entity round-robin, max 3 per entity, max 2 uses per indicator per entity.
    proposals = sorted(
        proposals,
        key=lambda c: (
            ENTITY_ORDER.get(c["entity"], 99),
            c["series_a"]["identity"]["code"],
            c["series_b"]["identity"]["code"],
            c["candidate_id"],
        ),
    )
    by_entity: dict[str, list[dict[str, Any]]] = {}
    for proposal in proposals:
        by_entity.setdefault(proposal["entity"], []).append(proposal)
    selected: list[dict[str, Any]] = []
    per_entity_count = {entity: 0 for entity in by_entity}
    indicator_use: dict[tuple[str, str], int] = {}
    entities = sorted(by_entity, key=lambda e: ENTITY_ORDER.get(e, 99))
    while len(selected) < max_count:
        progressed = False
        for entity in entities:
            if len(selected) >= max_count:
                break
            if per_entity_count.get(entity, 0) >= 3:
                continue
            for proposal in by_entity[entity]:
                if proposal in selected:
                    continue
                codes = [proposal["series_a"]["identity"]["code"], proposal["series_b"]["identity"]["code"]]
                if any(indicator_use.get((entity, code), 0) >= 2 for code in codes):
                    continue
                selected.append(proposal)
                per_entity_count[entity] = per_entity_count.get(entity, 0) + 1
                for code in codes:
                    indicator_use[(entity, code)] = indicator_use.get((entity, code), 0) + 1
                progressed = True
                break
        if not progressed:
            # Relax indicator-use cap if necessary, but keep max 3/entity. This is deterministic and recorded.
            for entity in entities:
                if len(selected) >= max_count:
                    break
                if per_entity_count.get(entity, 0) >= 3:
                    continue
                for proposal in by_entity[entity]:
                    if proposal not in selected:
                        selected.append(proposal)
                        per_entity_count[entity] = per_entity_count.get(entity, 0) + 1
                        progressed = True
                        break
        if not progressed:
            break
    return selected



SUCCESSOR_POLICY_VERSION = "pearson_candidate_policy_v2_mixed_roadmap@1.0"
SUCCESSOR_ORDINARY_MAX_REMOTE_SHARE = "0.25"

SEMANTIC_CLOSE_PAIRS = {
    tuple(sorted(("SP.DYN.CBRT.IN", "SP.DYN.CDRT.IN"))): "same demographic vital-rates subject domain",
    tuple(sorted(("SP.DYN.CBRT.IN", "SP.DYN.LE00.IN"))): "demographic fertility/survival structure",
    tuple(sorted(("SP.DYN.CDRT.IN", "SP.DYN.LE00.IN"))): "demographic mortality/survival structure",
    tuple(sorted(("SP.DYN.CBRT.IN", "SH.DYN.MORT"))): "population-health vital-outcome subject domain",
    tuple(sorted(("SP.DYN.CDRT.IN", "SH.DYN.MORT"))): "mortality/vital-rates subject domain",
    tuple(sorted(("SP.DYN.LE00.IN", "SH.DYN.MORT"))): "life expectancy and mortality measure survival outcomes",
    tuple(sorted(("IT.CEL.SETS.P2", "IT.NET.USER.ZS"))): "digital access/adoption subject domain",
    tuple(sorted(("FS.AST.PRVT.GD.ZS", "FM.LBL.BMNY.GD.ZS"))): "monetary/credit financial-sector subject domain",
    tuple(sorted(("AG.LND.AGRI.ZS", "AG.LND.FRST.ZS"))): "land-use share subject domain",
    tuple(sorted(("EG.ELC.FOSL.ZS", "EG.ELC.RNWX.ZS"))): "electricity-source share subject domain",
    tuple(sorted(("NE.EXP.GNFS.ZS", "NE.IMP.GNFS.ZS"))): "trade-flow share subject domain",
}
SEMANTIC_MODERATE_PAIRS = {
    tuple(sorted(("FS.AST.PRVT.GD.ZS", "IT.CEL.SETS.P2"))): "financial depth and communications infrastructure are macro-development infrastructure proxies, but not same measurement concept",
    tuple(sorted(("FS.AST.PRVT.GD.ZS", "IT.NET.USER.ZS"))): "financial depth and digital access are macro-development proxies, but not same measurement concept",
}

# Permitted successor-policy time-risk inputs: prior accepted per-series time-index diagnostics only.
# These values come from accepted Campaign 40/41 diagnostic artifacts and contain no candidate-pair result.
PREVIOUS_SERIES_TIME_RISK = {
    ("DNK", "AG.LND.AGRI.ZS"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("DNK", "AG.LND.FRST.ZS"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("DNK", "FS.AST.PRVT.GD.ZS"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("NOR", "EG.ELC.RNWX.ZS"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("NOR", "SH.DYN.MORT"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("NOR", "SP.DYN.CBRT.IN"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("NOR", "SP.DYN.CDRT.IN"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("NOR", "SP.DYN.LE00.IN"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("SWE", "FS.AST.PRVT.GD.ZS"): {"risk": "high", "basis": "accepted Campaign 41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("SWE", "IT.CEL.SETS.P2"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("SWE", "IT.NET.USER.ZS"): {"risk": "high", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) >= 0.75"},
    ("DNK", "FM.LBL.BMNY.GD.ZS"): {"risk": "moderate", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) between 0.40 and 0.75"},
    ("NOR", "EG.ELC.FOSL.ZS"): {"risk": "moderate", "basis": "accepted Campaign 40/41 per-series time-index diagnostic abs(value) between 0.40 and 0.75"},
}


def semantic_proximity(a: Series, b: Series) -> dict[str, Any]:
    pair_key = tuple(sorted((a.code, b.code)))
    allowed_fields = [
        "indicator code", "indicator name", "indicator definition", "unit", "frequency",
        "transformation", "entity", "production family", "period scope", "retained evidence fingerprints",
    ]
    if pair_key in SEMANTIC_CLOSE_PAIRS:
        value, rule = "close", SEMANTIC_CLOSE_PAIRS[pair_key]
    elif pair_key in SEMANTIC_MODERATE_PAIRS:
        value, rule = "moderate", SEMANTIC_MODERATE_PAIRS[pair_key]
    elif a.family == b.family:
        value, rule = "close", "same production family and compatible annual raw series"
    elif {a.family, b.family} <= {"Demographic", "Health"}:
        value, rule = "close", "demographic/health population-outcome subject domain"
    elif not a.definition or not b.definition:
        value, rule = "unresolved", "missing indicator definition prevents deterministic semantic classification"
    else:
        value, rule = "remote", "different production families without accepted structural or shared-subject rule"
    return {
        "classification": value,
        "rule": rule,
        "allowed_evidence_fields": allowed_fields,
        "tie_breaking": "explicit pair rule > same family > demographic/health bridge > unresolved missing definition > remote",
        "manual_review_boundary": "unresolved classifications require human review before ordinary production freeze",
        "local_ai_advisory_boundary": "optional local AI may advise using metadata only, but deterministic/manual classification remains authoritative",
        "provenance": {
            "policy_version": SUCCESSOR_POLICY_VERSION,
            "series_a_metadata_fingerprint": a.normalized_fingerprint,
            "series_b_metadata_fingerprint": b.normalized_fingerprint,
        },
    }


def series_time_risk(s: Series) -> dict[str, str]:
    item = PREVIOUS_SERIES_TIME_RISK.get((s.entity, s.code))
    if item:
        return {"category": item["risk"], "basis": item["basis"], "input_boundary": "prior accepted per-series diagnostic artifact; no candidate-pair association inspected"}
    bounded = "%" in s.unit or "per 100" in s.unit or "per 1,000" in s.unit
    if bounded:
        return {"category": "unknown", "basis": "bounded/ratio metadata flag present but no accepted per-series time diagnostic available", "input_boundary": "metadata flag only; unknown remains visible"}
    return {"category": "unknown", "basis": "no permitted pre-existing per-series time-risk input", "input_boundary": "unknown remains visible and is not low risk"}


def pair_time_risk(a: Series, b: Series) -> dict[str, Any]:
    ra, rb = series_time_risk(a), series_time_risk(b)
    order = {"low": 0, "moderate": 1, "unknown": 2, "high": 3}
    category = max([ra["category"], rb["category"]], key=lambda x: order[x])
    return {"category": category, "series_a": ra, "series_b": rb, "permitted_inputs_only": True}


def transformation_companion_eligibility(a: Series, b: Series, proximity: str, risk: str) -> dict[str, Any]:
    checks = [
        "unit semantics", "zero/negative-value behavior", "bounded-ratio behavior",
        "missingness after transformation", "minimum transformed overlap", "interpretability of transformed values",
    ]
    recommend = risk in {"high", "unknown"} or proximity == "remote"
    candidates = []
    if recommend:
        candidates = ["first_difference", "growth_rate_or_percentage_change_only_if_unit_semantics_and_zero_behavior_pass"]
    return {
        "raw_level_candidate_should_prioritize_companion": recommend,
        "permitted_companion_recommendations": candidates,
        "required_checks_before_method_use": checks,
        "non_implementation_boundary": "metadata and sequencing only; no companion relationship calculated here",
    }


def candidate_utility_statement(a: Series, b: Series, proximity: str, risk: str) -> dict[str, str]:
    if proximity == "close" and risk != "high":
        purpose = "positive_descriptive_knowledge"
        worth = "same or structurally adjacent measurement domain with usable evidence quality"
    elif proximity == "close":
        purpose = "transformation_companion_candidate"
        worth = "semantically meaningful baseline, but high time risk requires companion sequencing"
    elif proximity == "moderate":
        purpose = "baseline_relationship_knowledge"
        worth = "moderately related macro-development concepts with explicit limitation needs"
    else:
        purpose = "methodological_pressure_test_candidate" if risk != "high" else "cautionary_relationship_knowledge"
        worth = "bounded cautionary or pressure-test value; not ordinary positive relationship discovery"
    return {
        "why_worth_canonizing_before_calculation": worth,
        "expected_descriptive_use": "finite-window raw-level baseline descriptor only",
        "expected_limitation": "no causation, mechanism, forecast, recommendation, significance, or stationarity claim",
        "likely_consumer_use": "retrieve as baseline/cautionary context with provenance and diagnostics",
        "purpose_classification": purpose,
        "coefficient_prediction": "none; result-independent statement",
    }


def enrich_candidate_for_successor_policy(c: dict[str, Any]) -> dict[str, Any]:
    a_id = c["series_a"]["identity"]
    b_id = c["series_b"]["identity"]
    # Reconstruct the two Series-like inputs from original evidence pool by matching code/entity.
    pool = { (s.entity, s.code): s for s in load_series_pool() }
    a, b = pool[(c["entity"], a_id["code"])], pool[(c["entity"], b_id["code"])]
    sem = semantic_proximity(a, b)
    risk = pair_time_risk(a, b)
    companion = transformation_companion_eligibility(a, b, sem["classification"], risk["category"])
    utility = candidate_utility_statement(a, b, sem["classification"], risk["category"])
    enriched = dict(c)
    enriched["successor_policy_metadata"] = {
        "policy_version": SUCCESSOR_POLICY_VERSION,
        "semantic_proximity": sem,
        "time_risk": risk,
        "transformation_companion_eligibility": companion,
        "candidate_utility_statement": utility,
    }
    return enriched


def select_candidates_successor_policy(proposals: list[dict[str, Any]], max_count: int = 8) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    enriched = [enrich_candidate_for_successor_policy(c) for c in proposals]
    rank = {"close": 0, "moderate": 1, "remote": 2, "unresolved": 3}
    risk_rank = {"low": 0, "moderate": 1, "unknown": 2, "high": 3}
    enriched.sort(key=lambda c: (
        rank[c["successor_policy_metadata"]["semantic_proximity"]["classification"]],
        risk_rank[c["successor_policy_metadata"]["time_risk"]["category"]],
        ENTITY_ORDER.get(c["entity"], 99),
        c["series_a"]["identity"]["code"], c["series_b"]["identity"]["code"], c["candidate_id"],
    ))
    selected, deprioritized = [], []
    per_entity: dict[str, int] = {}
    per_family: dict[str, int] = {}
    per_indicator: dict[tuple[str, str], int] = {}
    remote_cap = remote_cap_count(max_count, SUCCESSOR_ORDINARY_MAX_REMOTE_SHARE)
    remote_count = 0
    for c in enriched:
        sem = c["successor_policy_metadata"]["semantic_proximity"]["classification"]
        entity = c["entity"]
        fam = c["family"]
        codes = [c["series_a"]["identity"]["code"], c["series_b"]["identity"]["code"]]
        reason = None
        if len(selected) >= max_count:
            reason = "outside maximum ordinary batch size"
        elif sem == "remote" and remote_count >= remote_cap:
            reason = "remote-candidate ordinary-production share cap reached"
        elif per_entity.get(entity, 0) >= 3:
            reason = "entity repetition cap reached"
        elif per_family.get(fam, 0) >= 3:
            reason = "production-family-pair repetition cap reached"
        elif any(per_indicator.get((entity, code), 0) >= 2 for code in codes):
            reason = "indicator reuse cap reached"
        if reason:
            d = dict(c); d["successor_deprioritization_reason"] = reason; deprioritized.append(d); continue
        selected.append(c)
        per_entity[entity] = per_entity.get(entity, 0) + 1
        per_family[fam] = per_family.get(fam, 0) + 1
        for code in codes:
            per_indicator[(entity, code)] = per_indicator.get((entity, code), 0) + 1
        if sem == "remote":
            remote_count += 1
    return selected, deprioritized


def _dist(items: list[dict[str, Any]], path) -> dict[str, int]:
    out: dict[str, int] = {}
    for c in items:
        v = path(c)
        out[v] = out.get(v, 0) + 1
    return dict(sorted(out.items()))


def _successor_policy_result(
    *,
    mode: str,
    fixture_root: Path,
    proposals: list[dict[str, Any]],
    excluded: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    deprioritized: list[dict[str, Any]],
    valid_future_production_evidence: bool,
    enforce_actual_remote_share: bool,
) -> dict[str, Any]:
    semantic_distribution = _dist(selected, lambda c: c["successor_policy_metadata"]["semantic_proximity"]["classification"])
    remote = semantic_distribution.get("remote", 0)
    selected_count = len(selected)
    remote_share = 0 if selected_count == 0 else remote / selected_count
    actual_remote_cap = remote_cap_count(selected_count, SUCCESSOR_ORDINARY_MAX_REMOTE_SHARE)
    validation_errors = []
    if valid_future_production_evidence and selected_count < 6:
        validation_errors.append("fewer than 6 defensible future-production candidates remain")
    if enforce_actual_remote_share and remote > actual_remote_cap:
        validation_errors.append("remote candidate count exceeds declared percentage cap for actual selected batch size")
    if has_forbidden_key({"selected": selected, "deprioritized": deprioritized}):
        validation_errors.append("forbidden outcome-derived field present")
    result = {
        "policy_version": SUCCESSOR_POLICY_VERSION,
        "mode": mode,
        "mode_boundary": "historical/audit ranking only; not future-production evidence" if mode == "historical_comparison" else "future-production eligibility dry-run; canonical relationships excluded",
        "valid_future_production_evidence": valid_future_production_evidence,
        "dry_run_only": True,
        "not_campaign42_registry": True,
        "fixture_root": str(fixture_root),
        "eligible_candidate_count": len(proposals),
        "selected_candidate_count": selected_count,
        "selected_candidates": selected,
        "deprioritized_candidates": deprioritized,
        "excluded_candidates": excluded,
        "semantic_proximity_distribution": semantic_distribution,
        "time_risk_distribution": _dist(selected, lambda c: c["successor_policy_metadata"]["time_risk"]["category"]),
        "candidate_purpose_distribution": _dist(selected, lambda c: c["successor_policy_metadata"]["candidate_utility_statement"]["purpose_classification"]),
        "remote_count": remote,
        "remote_share": remote_share,
        "remote_cap_arithmetic": {
            "declared_share_cap": SUCCESSOR_ORDINARY_MAX_REMOTE_SHARE,
            "actual_selected_count": selected_count,
            "max_remote_count_for_actual_selected_count": actual_remote_cap,
            "integer_rule": "floor(actual_selected_count * declared_share_cap); no upward rounding",
            "nominal_8_candidate_remote_cap": remote_cap_count(8, SUCCESSOR_ORDINARY_MAX_REMOTE_SHARE),
        },
        "batch_composition_policy": {
            "ordinary_default_close_share": "prefer majority close when available",
            "ordinary_default_moderate_share": "use after close candidates with explicit justification",
            "ordinary_default_remote_share_cap": SUCCESSOR_ORDINARY_MAX_REMOTE_SHARE,
            "max_candidates_per_entity": 3,
            "max_candidates_per_family_pair": 3,
            "max_uses_of_indicator_per_entity": 2,
            "roadmap_policy_not_doctrine": True,
        },
        "coefficient_free_proof": {
            "candidate_pair_pearson_used": False,
            "candidate_pair_first_difference_used": False,
            "covariance_used": False,
            "p_values_or_significance_used": False,
            "preliminary_result_cache_used": False,
            "allowed_inputs": ["metadata", "fingerprints", "overlap/missingness", "units", "transformation state", "prior accepted per-series time diagnostics"],
        },
    }
    result["dry_run_fingerprint"] = sha256_value({k: v for k, v in result.items() if k != "dry_run_fingerprint"})
    result["validation"] = {"valid": not validation_errors, "errors": validation_errors}
    return result


def build_successor_policy_historical_comparison(fixture_root: Path = DEFAULT_FIXTURE_ROOT) -> dict[str, Any]:
    pool = load_series_pool(fixture_root)
    proposals, excluded = enumerate_proposals(pool)
    selected, deprioritized = select_candidates_successor_policy(proposals, 8)
    return _successor_policy_result(
        mode="historical_comparison",
        fixture_root=fixture_root,
        proposals=proposals,
        excluded=excluded,
        selected=selected,
        deprioritized=deprioritized,
        valid_future_production_evidence=False,
        enforce_actual_remote_share=False,
    )


def build_successor_policy_future_production_dry_run(fixture_root: Path = DEFAULT_FIXTURE_ROOT) -> dict[str, Any]:
    pool = load_series_pool(fixture_root)
    canonical_keys = load_current_canonical_pearson_relationship_keys()
    proposals, excluded = enumerate_proposals(pool, prior_pairs=canonical_keys)
    selected, deprioritized = select_candidates_successor_policy(proposals, 8)
    return _successor_policy_result(
        mode="future_production",
        fixture_root=fixture_root,
        proposals=proposals,
        excluded=excluded,
        selected=selected,
        deprioritized=deprioritized,
        valid_future_production_evidence=True,
        enforce_actual_remote_share=True,
    )


def build_successor_policy_dry_run(fixture_root: Path = DEFAULT_FIXTURE_ROOT) -> dict[str, Any]:
    return build_successor_policy_historical_comparison(fixture_root)


CANDIDATE_FUNNEL_PROFILE = "knowledgeforge.deterministic_candidate_funnel.v1@1.0"
CANDIDATE_FUNNEL_POLICY_VERSION = "pearson_candidate_funnel_pilot_v1@1.0"
UNRESOLVED_ESCALATION_PROFILE = "knowledgeforge.candidate_funnel_unresolved.v1@1.0"
CANDIDATE_FUNNEL_REPORT_ROOT = Path("artifacts/reports/deterministic-candidate-funnel-compact-escalation-pilot-20260808")


def scalar_leaf_count(value: Any) -> int:
    if isinstance(value, dict):
        return sum(scalar_leaf_count(item) for item in value.values())
    if isinstance(value, list):
        return sum(scalar_leaf_count(item) for item in value)
    return 1


def load_current_canonical_pearson_relationship_index(
    repository_root: Path | None = None,
) -> dict[tuple[str, str, str], list[str]]:
    root = repository_root or (PROJECT_ROOT / "knowledge_repository" / "objects")
    index: dict[tuple[str, str, str], list[str]] = {}
    for path in sorted(root.glob("*.json")):
        try:
            package = read_json(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            raise ValueError(f"unreadable canonical repository object: {path}") from exc
        if not isinstance(package, dict):
            raise ValueError(f"malformed canonical repository object: {path}")
        if package.get("status") != "accepted":
            continue
        target_statements: list[tuple[dict[str, Any], dict[str, Any]]] = []
        for collection_name, payload_name in (
            ("generated_statements", "structured_payload"),
            ("statements", "payload"),
        ):
            collection = package.get(collection_name, [])
            if not isinstance(collection, list):
                raise ValueError(f"malformed accepted statement collection: {path}")
            for statement in collection:
                if not isinstance(statement, dict):
                    raise ValueError(f"malformed accepted statement entry: {path}")
                payload = statement.get(payload_name)
                is_derived = statement.get("statement_type") == "derived_relationship"
                if is_derived and not isinstance(payload, dict):
                    raise ValueError(f"malformed accepted relationship statement: {path}")
                targets_pearson = (
                    isinstance(payload, dict)
                    and payload.get("method_contract_fingerprint") == METHOD_CONTRACT_FINGERPRINT
                )
                if targets_pearson:
                    if not is_derived:
                        raise ValueError(f"malformed accepted Pearson relationship statement: {path}")
                    assert isinstance(payload, dict)
                    target_statements.append((statement, payload))
        target_keys: list[tuple[str, str, str]] = []
        for statement, payload in target_statements:
            entity = payload.get("entity_id")
            series_a = payload.get("series_a", {})
            series_b = payload.get("series_b", {})
            structurally_valid = (
                bool(entity)
                and isinstance(series_a, dict) and bool(series_a.get("code"))
                and isinstance(series_b, dict) and bool(series_b.get("code"))
                and series_a.get("transformation", "raw") == "raw"
                and series_b.get("transformation", "raw") == "raw"
                and statement.get("applicability", {}).get("frequency") == "annual"
            )
            if not structurally_valid:
                raise ValueError(f"malformed accepted Pearson relationship identity: {path}")
            target_keys.append(canonical_pair_key(str(entity), series_a["code"], series_b["code"]))
        if len(set(target_keys)) > 1:
            raise ValueError(f"inconsistent accepted Pearson relationship identities: {path}")
        key = target_keys[0] if target_keys else None
        if key:
            package_identity = package.get("package_id") or package.get("id") or path.stem
            index.setdefault(key, []).append(str(package_identity))
    return {key: sorted(set(package_ids)) for key, package_ids in sorted(index.items())}


def _candidate_series(candidate: dict[str, Any], side: str) -> Series:
    item = candidate[side]
    identity = item["identity"]
    evidence = item["evidence_identity"]
    missing = tuple(int(year) for year in evidence.get("missing_periods", []))
    all_periods = tuple(range(int(candidate["period"]["start"]), int(candidate["period"]["end"]) + 1))
    observed = tuple(year for year in all_periods if year not in missing)
    return Series(
        code=identity["code"],
        entity=candidate["entity"],
        name=identity.get("name", ""),
        definition=identity.get("definition", ""),
        unit=identity.get("unit", ""),
        frequency=identity.get("frequency", ""),
        transformation=identity.get("transformation", ""),
        family=FAMILY_BY_INDICATOR.get(identity["code"], "Unknown"),
        normalized_path=evidence.get("normalized_path", ""),
        normalized_fingerprint=evidence.get("normalized_fingerprint", ""),
        validation_path=evidence.get("validation_path", ""),
        validation_fingerprint=evidence.get("validation_fingerprint", ""),
        raw_fixture_path=evidence.get("raw_fixture_path", ""),
        raw_fixture_fingerprint=evidence.get("raw_fixture_fingerprint", ""),
        selection_contract_path=evidence.get("selection_contract_path", ""),
        selection_contract_fingerprint=evidence.get("selection_contract_fingerprint", ""),
        acquisition_manifest_path=evidence.get("acquisition_manifest_path", ""),
        acquisition_manifest_fingerprint=evidence.get("acquisition_manifest_fingerprint", ""),
        observed_periods=observed,
        missing_periods=missing,
    )


def _evidence_reference_errors(candidate: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for side in ("series_a", "series_b"):
        evidence = candidate.get(side, {}).get("evidence_identity", {})
        references = (
            ("raw_fixture", evidence.get("raw_fixture_path"), evidence.get("raw_fixture_fingerprint"), False),
            ("validation", evidence.get("validation_path"), evidence.get("validation_fingerprint"), False),
            ("selection_contract", evidence.get("selection_contract_path"), evidence.get("selection_contract_fingerprint"), False),
            ("acquisition_manifest", evidence.get("acquisition_manifest_path"), evidence.get("acquisition_manifest_fingerprint"), False),
            ("normalized", evidence.get("normalized_path"), evidence.get("normalized_fingerprint"), True),
        )
        for label, rel, expected, normalized_identity in references:
            if not rel or not expected:
                errors.append(f"missing_evidence_reference:{side}:{label}")
                continue
            path = PROJECT_ROOT / str(rel)
            try:
                resolved = path.resolve(strict=True)
                resolved.relative_to(PROJECT_ROOT.resolve())
            except (FileNotFoundError, ValueError, OSError):
                errors.append(f"missing_evidence_reference:{side}:{label}")
                continue
            if not resolved.is_file():
                errors.append(f"missing_evidence_reference:{side}:{label}")
                continue
            if normalized_identity:
                try:
                    normalized = read_json(resolved)
                    embedded = normalized.get("normalized_fingerprint")
                    payload = {key: value for key, value in normalized.items() if key != "normalized_fingerprint"}
                    recomputed = sha256_value(payload)
                    current = recomputed if embedded == recomputed else ""
                except Exception:
                    current = ""
            else:
                current = sha256_file(resolved)
            if current != expected:
                errors.append(f"stale_evidence_reference:{side}:{label}")
    return sorted(errors)


def _candidate_projection(candidate: dict[str, Any]) -> dict[str, Any]:
    a = _candidate_series(candidate, "series_a")
    b = _candidate_series(candidate, "series_b")
    a, b = sorted((a, b), key=lambda item: item.code)
    coverage = candidate["selection_evidence"]["coverage_probe"]
    return {
        "policy_version": CANDIDATE_FUNNEL_POLICY_VERSION,
        "candidate_id": candidate["candidate_id"],
        "candidate_key": list(canonical_pair_key(candidate["entity"], a.code, b.code)),
        "method_contract": candidate["method_contract"],
        "period": candidate["period"],
        "thresholds": candidate["thresholds"],
        "qualification_observations": {
            "expected_slots": coverage["expected_slots"],
            "aligned_pairs": coverage["expected_aligned_pairs"],
            "aligned_coverage": coverage["aligned_coverage"],
        },
        "series": [
            {
                "code": series.code,
                "name": series.name,
                "definition": series.definition,
                "entity": series.entity,
                "family": series.family,
                "frequency": series.frequency,
                "unit": series.unit,
                "transformation": series.transformation,
                "normalized_fingerprint": series.normalized_fingerprint,
                "raw_fixture_fingerprint": series.raw_fixture_fingerprint,
            }
            for series in (a, b)
        ],
        "construction_risk": candidate["construction_risk"],
    }


def _invalid_funnel_classification(candidate: dict[str, Any], reason_codes: list[str]) -> dict[str, Any]:
    candidate_id = str(candidate.get("candidate_id", "invalid-candidate"))
    entity = str(candidate.get("entity", ""))
    codes = []
    for side in ("series_a", "series_b"):
        code = candidate.get(side, {}).get("identity", {}).get("code")
        if code:
            codes.append(str(code))
    candidate_key = [entity, *sorted(codes)] if len(codes) == 2 else [entity]
    return {
        "candidate_id": candidate_id,
        "candidate_key": candidate_key,
        "input_fingerprint": sha256_value({"candidate_id": candidate_id, "candidate_key": candidate_key}),
        "policy_version": CANDIDATE_FUNNEL_POLICY_VERSION,
        "qualification": {"passed": False, "checks": {}, "observed": {}, "thresholds": {}, "blocker_codes": sorted(reason_codes)},
        "contradiction_context": {"canonical_package_ids": [], "mechanical_rule": None, "prior_relationship": None, "construction_limitations": [], "hard_blocker_codes": sorted(reason_codes)},
        "statistical_context": {"result_derived_inputs_used": "result_derived_input" in reason_codes},
        "semantic_classification": {"classification": "not_evaluated", "rule": "invalid input fails before semantic classification"},
        "disposition": "invalid",
        "reason_codes": sorted(reason_codes),
        "recovery_context": {"funnel_stage": "input_validation", "unresolved_fields": [], "required_action": "correct and re-authenticate candidate input", "reentry_condition": "all result-derived fields absent and all evidence references current"},
        "provenance": {},
    }


def _classify_verified_candidate_for_funnel(
    candidate: dict[str, Any],
    a: Series,
    b: Series,
    canonical_relationship_index: dict[tuple[str, str, str], list[str]] | None = None,
) -> dict[str, Any]:
    try:
        projection = _candidate_projection(candidate)
    except (KeyError, TypeError, ValueError):
        return _invalid_funnel_classification(candidate, ["malformed_candidate_identity"])

    key = canonical_pair_key(candidate["entity"], a.code, b.code)
    canonical_index = canonical_relationship_index if canonical_relationship_index is not None else load_current_canonical_pearson_relationship_index()
    aligned = int(projection["qualification_observations"]["aligned_pairs"])
    coverage = Decimal(str(projection["qualification_observations"]["aligned_coverage"]))
    min_aligned = int(projection["thresholds"]["min_aligned_pairs"])
    min_coverage = Decimal(str(projection["thresholds"]["min_aligned_coverage"]))
    checks = {
        "identity_complete": bool(candidate.get("candidate_id") and a.code and b.code and candidate.get("entity")),
        "same_entity": a.entity == b.entity == candidate["entity"],
        "annual_frequency": a.frequency == b.frequency == "annual",
        "raw_transformation": a.transformation == b.transformation == "raw",
        "units_resolved": bool(a.unit and b.unit),
        "minimum_aligned_pairs": aligned >= min_aligned,
        "minimum_aligned_coverage": coverage >= min_coverage,
        "not_self_pair": a.code != b.code,
    }
    blocker_codes = [name for name, passed in checks.items() if not passed]
    pair_code_key = tuple(sorted((a.code, b.code)))
    canonical_package_ids = canonical_index.get(key, [])
    mechanical_rule = MECHANICAL_EXCLUSIONS.get(pair_code_key)
    prior_relationship = EXCLUDED_PRIOR_PAIRS.get(key)
    reason_codes = list(blocker_codes)
    if canonical_package_ids:
        reason_codes.append("current_canonical_relationship")
    elif prior_relationship:
        reason_codes.append("prior_relationship")
    if mechanical_rule:
        reason_codes.append("mechanical_exclusion")
    construction_limitations = sorted(
        f"{name}:{value}" for name, value in candidate["construction_risk"].items() if value != "not present"
    )
    qualification = {
        "passed": not blocker_codes,
        "checks": checks,
        "observed": projection["qualification_observations"],
        "thresholds": projection["thresholds"],
        "blocker_codes": sorted(blocker_codes),
    }
    contradiction = {
        "canonical_package_ids": canonical_package_ids,
        "mechanical_rule": mechanical_rule,
        "prior_relationship": prior_relationship,
        "construction_limitations": construction_limitations,
        "hard_blocker_codes": sorted(set(reason_codes)),
    }
    evidence_provenance = {
        "policy_version": CANDIDATE_FUNNEL_POLICY_VERSION,
        "method_identity": candidate["method_contract"]["identity"],
        "method_contract_fingerprint": candidate["method_contract"]["contract_fingerprint"],
        "expected_package_id": candidate["expected_package_id"],
        "series": [
            {
                "code": series.code,
                "normalized_path": series.normalized_path,
                "normalized_fingerprint": series.normalized_fingerprint,
                "raw_fixture_path": series.raw_fixture_path,
                "raw_fixture_fingerprint": series.raw_fixture_fingerprint,
                "validation_path": series.validation_path,
                "validation_fingerprint": series.validation_fingerprint,
                "selection_contract_path": series.selection_contract_path,
                "selection_contract_fingerprint": series.selection_contract_fingerprint,
                "acquisition_manifest_path": series.acquisition_manifest_path,
                "acquisition_manifest_fingerprint": series.acquisition_manifest_fingerprint,
            }
            for series in sorted((a, b), key=lambda item: item.code)
        ],
    }
    if reason_codes:
        return {
            "candidate_id": candidate["candidate_id"],
            "candidate_key": list(key),
            "input_fingerprint": sha256_value(projection),
            "policy_version": CANDIDATE_FUNNEL_POLICY_VERSION,
            "qualification": qualification,
            "contradiction_context": contradiction,
            "statistical_context": {"result_derived_inputs_used": False},
            "semantic_classification": {"classification": "not_evaluated", "rule": "deterministic exclusion precedes semantic classification"},
            "disposition": "excluded",
            "reason_codes": sorted(set(reason_codes)),
            "recovery_context": {"funnel_stage": "deterministic_qualification", "unresolved_fields": [], "required_action": "none; excluded", "reentry_condition": None},
            "provenance": evidence_provenance,
        }

    semantic = semantic_proximity(a, b)
    risk = pair_time_risk(a, b)
    companion = transformation_companion_eligibility(a, b, semantic["classification"], risk["category"])
    statistical = {
        "series_a_time_risk": risk["series_a"],
        "series_b_time_risk": risk["series_b"],
        "pair_time_risk": risk["category"],
        "companion_priority": companion["raw_level_candidate_should_prioritize_companion"],
        "result_derived_inputs_used": False,
    }
    unresolved_fields = []
    if not a.definition:
        unresolved_fields.append("series_a.definition")
    if not b.definition:
        unresolved_fields.append("series_b.definition")
    unresolved = semantic["classification"] == "unresolved"
    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_key": list(key),
        "input_fingerprint": sha256_value(projection),
        "policy_version": CANDIDATE_FUNNEL_POLICY_VERSION,
        "qualification": qualification,
        "contradiction_context": contradiction,
        "statistical_context": statistical,
        "semantic_classification": {"classification": semantic["classification"], "rule": semantic["rule"]},
        "disposition": "unresolved" if unresolved else "eligible",
        "reason_codes": ["semantic_metadata_unresolved"] if unresolved else ["qualified", f"semantic_{semantic['classification']}"],
        "recovery_context": {
            "funnel_stage": "semantic_classification" if unresolved else "classification_complete",
            "unresolved_fields": sorted(unresolved_fields),
            "required_action": "human metadata review" if unresolved else "apply deterministic batch composition",
            "reentry_condition": "supply authenticated missing metadata or an accepted explicit pair rule" if unresolved else None,
        },
        "provenance": evidence_provenance,
    }


def load_authenticated_series_pool(fixture_root: Path = DEFAULT_FIXTURE_ROOT) -> list[Series]:
    resolved_root = fixture_root if fixture_root.is_absolute() else PROJECT_ROOT / fixture_root
    normalized_paths = sorted(resolved_root.rglob("normalized_observations.json"))
    if not normalized_paths:
        raise ValueError(f"fixture root has no normalized observations: {resolved_root}")
    for normalized_path in normalized_paths:
        normalized = read_json(normalized_path)
        if not isinstance(normalized, dict):
            raise ValueError(f"normalized evidence is malformed: {normalized_path}")
        embedded_fingerprint = normalized.get("normalized_fingerprint")
        fingerprint_payload = {key: value for key, value in normalized.items() if key != "normalized_fingerprint"}
        recomputed_fingerprint = sha256_value(fingerprint_payload)
        if embedded_fingerprint != recomputed_fingerprint:
            raise ValueError(f"normalized evidence fingerprint mismatch: {normalized_path}")
        validation_path = normalized_path.parent / "validation_results.json"
        validation = read_json(validation_path)
        normalized_validation = validation.get("normalized_validation", {}) if isinstance(validation, dict) else {}
        if (
            not isinstance(validation, dict)
            or validation.get("raw_validation", {}).get("valid") is not True
            or normalized_validation.get("valid") is not True
            or normalized_validation.get("normalized_fingerprint") != recomputed_fingerprint
        ):
            raise ValueError(f"fixture validation is not explicitly true and fingerprint-bound: {validation_path}")
    return load_series_pool(fixture_root)


def _authenticated_series_index(fixture_root: Path = DEFAULT_FIXTURE_ROOT) -> dict[str, Series]:
    index: dict[str, Series] = {}
    for series in load_authenticated_series_pool(fixture_root):
        if series.normalized_path in index:
            raise ValueError(f"duplicate authenticated normalized evidence path: {series.normalized_path}")
        index[series.normalized_path] = series
    return index


def classify_candidate_for_funnel(
    candidate: dict[str, Any],
    canonical_relationship_index: dict[tuple[str, str, str], list[str]] | None = None,
    authenticated_series_index: dict[str, Series] | None = None,
) -> dict[str, Any]:
    if not isinstance(candidate, dict):
        return _invalid_funnel_classification({}, ["malformed_candidate_identity"])
    if has_funnel_result_derived_key(candidate):
        return _invalid_funnel_classification(candidate, ["result_derived_input"])
    try:
        reference_errors = _evidence_reference_errors(candidate)
    except (AttributeError, KeyError, TypeError, ValueError):
        return _invalid_funnel_classification(candidate, ["malformed_candidate_identity"])
    if reference_errors:
        classes = sorted({error.split(":", 1)[0] for error in reference_errors})
        return _invalid_funnel_classification(candidate, classes)
    try:
        series_index = authenticated_series_index or _authenticated_series_index()
        a_path = candidate["series_a"]["evidence_identity"]["normalized_path"]
        b_path = candidate["series_b"]["evidence_identity"]["normalized_path"]
        a = series_index[a_path]
        b = series_index[b_path]
        authenticated_candidate = build_candidate(a, b)
    except (KeyError, TypeError, ValueError):
        return _invalid_funnel_classification(candidate, ["unauthenticated_candidate_identity"])
    if canonical_json(candidate) != canonical_json(authenticated_candidate):
        return _invalid_funnel_classification(candidate, ["candidate_contract_mismatch"])
    return _classify_verified_candidate_for_funnel(authenticated_candidate, a, b, canonical_relationship_index)


def build_unresolved_escalation_package(classification: dict[str, Any]) -> dict[str, Any] | None:
    if classification.get("disposition") != "unresolved":
        return None
    fingerprint = classification["input_fingerprint"]
    return {
        "profile": UNRESOLVED_ESCALATION_PROFILE,
        "escalation_id": f"esc-{classification['candidate_id']}-{fingerprint.split(':', 1)[-1][:12]}",
        "candidate_id": classification["candidate_id"],
        "candidate_key": classification["candidate_key"],
        "input_fingerprint": fingerprint,
        "provenance": classification["provenance"],
        "qualification": classification["qualification"],
        "contradiction_context": classification["contradiction_context"],
        "statistical_context": classification["statistical_context"],
        "unresolved": {
            "field_codes": classification["recovery_context"]["unresolved_fields"],
            "question_codes": ["resolve_semantic_proximity"],
            "allowed_evidence_fields": [
                "entity", "frequency", "indicator_code", "indicator_definition", "indicator_name",
                "period_scope", "production_family", "retained_evidence_fingerprint", "transformation", "unit",
            ],
        },
        "recovery": {
            "resume_stage": "semantic_classification",
            "required_action": classification["recovery_context"]["required_action"],
            "reentry_condition": classification["recovery_context"]["reentry_condition"],
            "prohibited_action": "do not inspect or calculate candidate-pair results",
        },
    }


def _all_pair_candidates(pool: list[Series]) -> list[dict[str, Any]]:
    by_entity: dict[str, list[Series]] = {}
    for series in pool:
        by_entity.setdefault(series.entity, []).append(series)
    candidates: list[dict[str, Any]] = []
    for entity in sorted(by_entity, key=lambda item: ENTITY_ORDER.get(item, 99)):
        rows = sorted(by_entity[entity], key=lambda item: (item.family, item.code, item.name))
        for index, first in enumerate(rows):
            for second in rows[index + 1:]:
                candidates.append(build_candidate(first, second))
    return candidates


def _compact_funnel_classification(classification: dict[str, Any]) -> dict[str, Any]:
    contradiction = classification["contradiction_context"]
    return {
        "candidate_id": classification["candidate_id"],
        "candidate_key": classification["candidate_key"],
        "input_fingerprint": classification["input_fingerprint"],
        "disposition": classification["disposition"],
        "reason_codes": classification["reason_codes"],
        "qualification": {
            "passed": classification["qualification"]["passed"],
            "blocker_codes": classification["qualification"]["blocker_codes"],
            "observed": classification["qualification"]["observed"],
        },
        "semantic_classification": classification["semantic_classification"]["classification"],
        "contradiction_context": {
            "canonical_package_ids": contradiction["canonical_package_ids"],
            "mechanical_rule_present": contradiction["mechanical_rule"] is not None,
            "prior_relationship_present": contradiction["prior_relationship"] is not None,
            "construction_limitation_codes": [item.split(":", 1)[0] for item in contradiction["construction_limitations"]],
        },
        "recovery_stage": classification["recovery_context"]["funnel_stage"],
    }


def _candidate_population_records(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = [
        {
            "candidate_id": candidate["candidate_id"],
            "candidate_key": list(canonical_pair_key(
                candidate["entity"],
                candidate["series_a"]["identity"]["code"],
                candidate["series_b"]["identity"]["code"],
            )),
            "input_fingerprint": sha256_value(_candidate_projection(candidate)),
        }
        for candidate in candidates
    ]
    return sorted(records, key=lambda item: item["candidate_id"])


def _rebuild_authenticated_candidate_funnel(
    fixture_root: Path = DEFAULT_FIXTURE_ROOT,
) -> tuple[list[Series], list[dict[str, Any]], list[dict[str, Any]]]:
    pool = load_authenticated_series_pool(fixture_root)
    authenticated_series = {series.normalized_path: series for series in pool}
    if len(authenticated_series) != len(pool):
        raise ValueError("duplicate authenticated normalized evidence path")
    candidates = _all_pair_candidates(pool)
    canonical_index = load_current_canonical_pearson_relationship_index()
    full_classifications = [
        classify_candidate_for_funnel(candidate, canonical_index, authenticated_series)
        for candidate in candidates
    ]
    if any(item["disposition"] == "invalid" for item in full_classifications):
        raise ValueError("authenticated candidate population produced an invalid classification")
    by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    eligible = [by_id[item["candidate_id"]] for item in full_classifications if item["disposition"] == "eligible"]
    selected, deprioritized = select_candidates_successor_policy(eligible, 8)
    selected_ids = {candidate["candidate_id"] for candidate in selected}
    deprioritized_reason = {
        candidate["candidate_id"]: candidate["successor_deprioritization_reason"]
        for candidate in deprioritized
    }
    for classification in full_classifications:
        if classification["candidate_id"] in selected_ids:
            classification["disposition"] = "selected"
            classification["reason_codes"] = sorted(set(
                classification["reason_codes"] + ["selected_by_batch_composition"]
            ))
            classification["recovery_context"]["required_action"] = "freeze only under separate production authority"
        elif classification["candidate_id"] in deprioritized_reason:
            classification["disposition"] = "deprioritized"
            classification["reason_codes"] = sorted(set(
                classification["reason_codes"] + [deprioritized_reason[classification["candidate_id"]]]
            ))
            classification["recovery_context"]["required_action"] = "observe until a later expansion boundary"
    full_classifications.sort(key=lambda item: item["candidate_id"])
    return pool, candidates, full_classifications


def validate_candidate_funnel_report(report: dict[str, Any]) -> dict[str, Any]:
    """Validate a funnel report without leaking incidental container exceptions."""
    malformed = {"valid": False, "errors": ["malformed candidate funnel report"]}
    if not isinstance(report, dict):
        return malformed
    if not isinstance(report.get("source_candidate_ids"), list):
        return malformed
    classifications = report.get("candidate_classifications")
    if not isinstance(classifications, list):
        return malformed
    if not isinstance(report.get("disposition_counts"), dict):
        return malformed
    if not isinstance(report.get("funnel_stage_counts"), dict):
        return malformed
    for item in classifications:
        if not isinstance(item, dict):
            return malformed
        candidate_key = item.get("candidate_key")
        if not isinstance(candidate_key, list) or any(not isinstance(value, str) for value in candidate_key):
            return malformed
        if not isinstance(item.get("reason_codes"), list):
            return malformed
    try:
        return _validate_candidate_funnel_report(report)
    except (AttributeError, KeyError, TypeError, ValueError, OSError):
        return malformed


def _validate_candidate_funnel_report(report: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    expected_report_keys = {
        "profile", "policy_version", "mode", "dry_run_only", "fixture_root",
        "source_candidate_count", "source_candidate_ids", "source_population_fingerprint",
        "candidate_classifications", "disposition_counts", "funnel_stage_counts",
        "frontier_calls", "local_model_calls", "candidate_pair_results_used", "report_fingerprint",
    }
    if set(report) not in {frozenset(expected_report_keys), frozenset(expected_report_keys | {"validation"})}:
        errors.append("unexpected candidate funnel report schema")
    expected_boundaries = {
        "profile": CANDIDATE_FUNNEL_PROFILE,
        "policy_version": CANDIDATE_FUNNEL_POLICY_VERSION,
        "mode": "representative_future_production_dry_run",
        "dry_run_only": True,
        "frontier_calls": 0,
        "local_model_calls": 0,
        "candidate_pair_results_used": False,
    }
    if any(report.get(key) != value for key, value in expected_boundaries.items()):
        errors.append("candidate funnel execution boundary mismatch")
    try:
        fixture_root = Path(report["fixture_root"])
        resolved_fixture = (fixture_root if fixture_root.is_absolute() else PROJECT_ROOT / fixture_root).resolve(strict=True)
        resolved_fixture.relative_to(PROJECT_ROOT.resolve())
        _, expected_candidates, expected_full_classifications = _rebuild_authenticated_candidate_funnel(resolved_fixture)
        expected_records = _candidate_population_records(expected_candidates)
        expected_compact_classifications = [
            _compact_funnel_classification(item) for item in expected_full_classifications
        ]
    except (KeyError, TypeError, ValueError, OSError):
        expected_records = []
        expected_compact_classifications = []
        errors.append("fixture root or authenticated source population is invalid")

    declared_ids = report.get("source_candidate_ids", [])
    classifications = report.get("candidate_classifications", [])
    classified_ids = [item.get("candidate_id") for item in classifications if isinstance(item, dict)]
    classified_records = sorted(
        [
            {
                "candidate_id": item.get("candidate_id"),
                "candidate_key": item.get("candidate_key"),
                "input_fingerprint": item.get("input_fingerprint"),
            }
            for item in classifications if isinstance(item, dict)
        ],
        key=lambda item: str(item["candidate_id"]),
    )
    candidate_keys = [tuple(item.get("candidate_key", [])) for item in classifications if isinstance(item, dict)]
    if len(declared_ids) != report.get("source_candidate_count") or len(declared_ids) != len(set(declared_ids)):
        errors.append("declared source identities are not unique and cardinality-consistent")
    if sorted(classified_ids, key=str) != sorted(declared_ids, key=str) or len(classified_ids) != len(declared_ids):
        errors.append("candidate population does not exactly match declared source identities")
    if len(candidate_keys) != len(set(candidate_keys)):
        errors.append("duplicate canonical candidate relationship identity")
    if classified_records != expected_records:
        errors.append("classified candidate identities do not match authenticated source population")
    if classifications != expected_compact_classifications:
        errors.append("candidate classifications do not match deterministic authenticated reconstruction")
    expected_population_fingerprint = sha256_value(expected_records)
    if report.get("source_population_fingerprint") != expected_population_fingerprint:
        errors.append("source population fingerprint mismatch")

    allowed = {"selected", "deprioritized", "excluded", "unresolved", "invalid"}
    if any(not isinstance(item, dict) or item.get("disposition") not in allowed for item in classifications):
        errors.append("unknown candidate disposition")
    counts: dict[str, int] = {key: 0 for key in report.get("disposition_counts", {})}
    for item in classifications:
        if isinstance(item, dict):
            disposition = item.get("disposition")
            counts[disposition] = counts.get(disposition, 0) + 1
    if dict(sorted(counts.items())) != report.get("disposition_counts"):
        errors.append("disposition counts do not match candidate classifications")

    exclusion_counts: dict[str, int] = {}
    semantic_counts: dict[str, int] = {}
    mechanically_eligible = 0
    for item in classifications:
        if not isinstance(item, dict):
            continue
        if item.get("disposition") == "excluded":
            for reason in item.get("reason_codes", []):
                exclusion_counts[reason] = exclusion_counts.get(reason, 0) + 1
        elif item.get("disposition") != "invalid":
            mechanically_eligible += 1
            semantic_class = item.get("semantic_classification")
            semantic_counts[semantic_class] = semantic_counts.get(semantic_class, 0) + 1
    expected_stages = {
        "total_inventory": len(classifications),
        "mechanical_exclusions_by_reason": dict(sorted(exclusion_counts.items())),
        "mechanically_excluded_count": counts.get("excluded", 0),
        "mechanically_eligible_count": mechanically_eligible,
        "deterministic_semantic_classifications_by_class": dict(sorted(semantic_counts.items())),
        "unresolved_manual_review_count": counts.get("unresolved", 0),
        "escalation_inclusion_count": counts.get("unresolved", 0),
    }
    if report.get("funnel_stage_counts") != expected_stages:
        errors.append("funnel stage accounting mismatch")
    if expected_stages["mechanically_excluded_count"] + expected_stages["mechanically_eligible_count"] != expected_stages["total_inventory"]:
        errors.append("funnel stage conservation failure")
    if has_forbidden_key(report):
        errors.append("forbidden outcome-derived field present")
    fingerprint_payload = {key: value for key, value in report.items() if key not in {"report_fingerprint", "validation"}}
    if not report.get("report_fingerprint") or sha256_value(fingerprint_payload) != report.get("report_fingerprint"):
        errors.append("report fingerprint mismatch")
    return {"valid": not errors, "errors": sorted(set(errors))}


def _build_synthetic_unresolved_verification(
    pool: list[Series],
    candidates: list[dict[str, Any]],
    full_classifications: list[dict[str, Any]],
) -> dict[str, Any]:
    authenticated_series = {series.normalized_path: series for series in pool}
    by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    synthetic_candidate_id = next(
        item["candidate_id"]
        for item in full_classifications
        if item["semantic_classification"]["classification"] == "remote"
        and item["disposition"] in {"selected", "deprioritized"}
    )
    synthetic_original = by_id[synthetic_candidate_id]
    synthetic_a = authenticated_series[synthetic_original["series_a"]["evidence_identity"]["normalized_path"]]
    synthetic_b = authenticated_series[synthetic_original["series_b"]["evidence_identity"]["normalized_path"]]
    synthetic_a = replace(synthetic_a, definition="")
    synthetic_source = build_candidate(synthetic_a, synthetic_b)
    synthetic_classification = _classify_verified_candidate_for_funnel(
        synthetic_source, synthetic_a, synthetic_b, canonical_relationship_index={}
    )
    synthetic_package = build_unresolved_escalation_package(synthetic_classification)
    if synthetic_package is None:
        raise ValueError("adversarial unresolved fixture did not emit an escalation package")
    restored_classification = classify_candidate_for_funnel(
        synthetic_original, canonical_relationship_index={}, authenticated_series_index=authenticated_series
    )
    return {
        "test_only": True,
        "mutation": "withhold one indicator definition from a real authenticated candidate shape",
        "candidate_id": synthetic_classification["candidate_id"],
        "unresolved_disposition": synthetic_classification["disposition"],
        "restored_disposition": restored_classification["disposition"],
        "restored_semantic_classification": restored_classification["semantic_classification"]["classification"],
        "required_context_sections": sorted(
            key for key in ("provenance", "qualification", "contradiction_context", "statistical_context", "recovery")
            if key in synthetic_package
        ),
        "full_candidate_canonical_json_bytes": len(canonical_json(synthetic_original).encode()),
        "full_candidate_scalar_leaf_count": scalar_leaf_count(synthetic_original),
        "compact_escalation_canonical_json_bytes": len(canonical_json(synthetic_package).encode()),
        "compact_escalation_scalar_leaf_count": scalar_leaf_count(synthetic_package),
        "escalation_package_fingerprint": sha256_value(synthetic_package),
        "result_derived_inputs_used": synthetic_package["statistical_context"]["result_derived_inputs_used"],
    }


def build_candidate_funnel_pilot(
    fixture_root: Path = DEFAULT_FIXTURE_ROOT,
    elapsed_time_seconds: str | None = None,
) -> dict[str, Any]:
    # Retained as a caller-compatibility input only. Runtime observations are
    # deliberately excluded from governed deterministic artifacts.
    _ = elapsed_time_seconds
    pool, candidates, full_classifications = _rebuild_authenticated_candidate_funnel(fixture_root)
    canonical_index = load_current_canonical_pearson_relationship_index()
    by_id = {candidate["candidate_id"]: candidate for candidate in candidates}
    source_ids = sorted(by_id)
    counts: dict[str, int] = {"deprioritized": 0, "excluded": 0, "selected": 0, "unresolved": 0}
    for item in full_classifications:
        counts[item["disposition"]] = counts.get(item["disposition"], 0) + 1
    compact_classifications = [_compact_funnel_classification(item) for item in full_classifications]
    population_records = _candidate_population_records(candidates)
    exclusion_counts: dict[str, int] = {}
    semantic_counts: dict[str, int] = {}
    for item in compact_classifications:
        if item["disposition"] == "excluded":
            for reason in item["reason_codes"]:
                exclusion_counts[reason] = exclusion_counts.get(reason, 0) + 1
        else:
            semantic_class = item["semantic_classification"]
            semantic_counts[semantic_class] = semantic_counts.get(semantic_class, 0) + 1
    funnel_stage_counts = {
        "total_inventory": len(source_ids),
        "mechanical_exclusions_by_reason": dict(sorted(exclusion_counts.items())),
        "mechanically_excluded_count": counts["excluded"],
        "mechanically_eligible_count": len(source_ids) - counts["excluded"],
        "deterministic_semantic_classifications_by_class": dict(sorted(semantic_counts.items())),
        "unresolved_manual_review_count": counts["unresolved"],
        "escalation_inclusion_count": counts["unresolved"],
    }
    report: dict[str, Any] = {
        "profile": CANDIDATE_FUNNEL_PROFILE,
        "policy_version": CANDIDATE_FUNNEL_POLICY_VERSION,
        "mode": "representative_future_production_dry_run",
        "dry_run_only": True,
        "fixture_root": str(fixture_root),
        "source_candidate_count": len(source_ids),
        "source_candidate_ids": source_ids,
        "source_population_fingerprint": sha256_value(population_records),
        "candidate_classifications": compact_classifications,
        "disposition_counts": dict(sorted(counts.items())),
        "funnel_stage_counts": funnel_stage_counts,
        "frontier_calls": 0,
        "local_model_calls": 0,
        "candidate_pair_results_used": False,
    }
    report["report_fingerprint"] = sha256_value(report)
    report["validation"] = validate_candidate_funnel_report(report)
    if not report["validation"]["valid"]:
        raise ValueError(f"candidate funnel report validation failed: {report['validation']['errors']}")
    packages = [package for item in full_classifications if (package := build_unresolved_escalation_package(item)) is not None]
    escalation_collection: dict[str, Any] = {
        "profile": "knowledgeforge.candidate_funnel_unresolved_collection.v1@1.0",
        "policy_version": CANDIDATE_FUNNEL_POLICY_VERSION,
        "report_fingerprint": report["report_fingerprint"],
        "package_count": len(packages),
        "packages": packages,
    }
    escalation_collection["collection_fingerprint"] = sha256_value(escalation_collection)

    synthetic_verification = _build_synthetic_unresolved_verification(
        pool, candidates, full_classifications
    )
    legacy = build_successor_policy_future_production_dry_run(fixture_root)
    legacy_full_candidates = legacy["selected_candidates"] + legacy["deprioritized_candidates"]
    run_evidence: dict[str, Any] = {
        "profile": "knowledgeforge.candidate_funnel_run_evidence.v1@1.0",
        "workflow_identity": "knowledgeforge.deterministic_candidate_funnel.pilot@1.0",
        "placement": "deterministic",
        "deterministic_route": [
            "authenticated_fixture_inventory",
            "mechanical_qualification_and_exclusion",
            "deterministic_semantic_proximity",
            "deterministic_batch_composition",
            "unresolved_only_escalation_packaging",
            "fail_closed_validation",
        ],
        "input_artifact_identities": {
            "fixture_root": str(fixture_root),
            "source_population_fingerprint": report["source_population_fingerprint"],
            "canonical_relationship_index_fingerprint": sha256_value({str(key): value for key, value in canonical_index.items()}),
        },
        "output_artifact_identities": {
            "funnel_report": {"path": "funnel_report.json", "fingerprint": report["report_fingerprint"]},
            "unresolved_escalation_package": {"path": "unresolved_escalation_package.json", "fingerprint": escalation_collection["collection_fingerprint"]},
        },
        "reused_artifacts": [
            {"identity": METHOD_IDENTITY, "fingerprint": METHOD_CONTRACT_FINGERPRINT},
            {"path": "docs/model_routing_policy.md", "fingerprint": sha256_file(PROJECT_ROOT / "docs/model_routing_policy.md")},
            {"path": str(fixture_root), "fingerprint": report["source_population_fingerprint"]},
        ],
        "funnel_counts": funnel_stage_counts,
        "validator_result": report["validation"],
        "hermes_implementation_review_usage": {
            "boundary": "outside deterministic candidate-funnel execution",
            "normalized_project_workflow_usage_available": False,
            "reason": "Hermes usage is not normalized to KnowledgeForge workflow identities",
        },
        "report_fingerprint": report["report_fingerprint"],
        "escalation_collection_fingerprint": escalation_collection["collection_fingerprint"],
        "source_population_fingerprint": report["source_population_fingerprint"],
        "source_candidate_count": len(source_ids),
        "deterministically_resolved_candidate_count": sum(counts.get(key, 0) for key in ("selected", "deprioritized", "excluded")),
        "human_review_candidate_count": counts.get("unresolved", 0),
        "invalid_candidate_count": counts.get("invalid", 0),
        "pre_change_full_candidate_records_materialized": len(legacy_full_candidates),
        "pre_change_full_candidate_context_canonical_json_bytes": len(canonical_json(legacy_full_candidates).encode()),
        "pre_change_full_candidate_context_scalar_leaf_count": scalar_leaf_count(legacy_full_candidates),
        "post_change_funnel_report_canonical_json_bytes": len(canonical_json(report).encode()),
        "post_change_funnel_report_scalar_leaf_count": scalar_leaf_count(report),
        "post_change_escalation_context_canonical_json_bytes": len(canonical_json(escalation_collection).encode()),
        "post_change_escalation_context_scalar_leaf_count": scalar_leaf_count(escalation_collection),
        "post_change_combined_context_canonical_json_bytes": len(canonical_json(report).encode()) + len(canonical_json(escalation_collection).encode()),
        "post_change_combined_context_scalar_leaf_count": scalar_leaf_count(report) + scalar_leaf_count(escalation_collection),
        "comparison_basis": {
            "pre_change": "10 full mechanically eligible selected/deprioritized candidate records materialized by the prior future-production workflow",
            "post_change": "40 compact funnel classifications plus the unresolved-only escalation collection",
            "limitation": "different schemas and cardinalities; valid as representative workflow context-burden evidence, not as an intrinsic per-candidate efficiency estimate",
        },
        "adversarial_unresolved_verification": synthetic_verification,
        "measurement_boundary": "serialized JSON bytes and scalar leaves measure candidate/context burden; they are not token, cost, latency or capability-savings claims",
        "coefficient_free": not has_funnel_result_derived_key({"report": report, "escalation": escalation_collection}),
        "replay_command": "python3 -m unittest tests.test_coefficient_free_pearson_candidate_registry",
    }
    run_evidence["run_fingerprint"] = sha256_value(run_evidence)
    return {
        "funnel_report": report,
        "unresolved_escalation_package": escalation_collection,
        "run_evidence": run_evidence,
    }


def validate_candidate_funnel_outputs(outputs: dict[str, Any], require_elapsed: bool = True) -> dict[str, Any]:
    # Compatibility parameter retained for existing callers. Elapsed time is
    # not governed evidence and therefore is neither expected nor required.
    _ = require_elapsed
    errors: list[str] = []
    try:
        report = outputs["funnel_report"]
        escalation = outputs["unresolved_escalation_package"]
        run = outputs["run_evidence"]
        report_validation = validate_candidate_funnel_report(report)
        if not report_validation["valid"]:
            errors.extend(f"report:{error}" for error in report_validation["errors"])
        escalation_payload = {key: value for key, value in escalation.items() if key != "collection_fingerprint"}
        if escalation.get("profile") != "knowledgeforge.candidate_funnel_unresolved_collection.v1@1.0":
            errors.append("unexpected escalation collection profile")
        if escalation.get("policy_version") != CANDIDATE_FUNNEL_POLICY_VERSION:
            errors.append("escalation collection policy version mismatch")
        if sha256_value(escalation_payload) != escalation.get("collection_fingerprint"):
            errors.append("escalation collection fingerprint mismatch")
        if escalation.get("report_fingerprint") != report.get("report_fingerprint"):
            errors.append("escalation/report cross-fingerprint mismatch")
        packages = escalation.get("packages", [])
        if escalation.get("package_count") != len(packages):
            errors.append("escalation package count mismatch")
        if len(packages) != report.get("funnel_stage_counts", {}).get("escalation_inclusion_count"):
            errors.append("escalation membership does not match funnel accounting")
        if any(not isinstance(package, dict) or package.get("profile") != UNRESOLVED_ESCALATION_PROFILE for package in packages):
            errors.append("non-unresolved package entered escalation collection")
        fixture_root = Path(report["fixture_root"])
        resolved_fixture = (fixture_root if fixture_root.is_absolute() else PROJECT_ROOT / fixture_root).resolve(strict=True)
        resolved_fixture.relative_to(PROJECT_ROOT.resolve())
        expected_pool, expected_candidates, expected_full_classifications = _rebuild_authenticated_candidate_funnel(resolved_fixture)
        expected_packages = [
            package
            for item in expected_full_classifications
            if (package := build_unresolved_escalation_package(item)) is not None
        ]
        if packages != expected_packages:
            errors.append("escalation packages do not match deterministic unresolved reconstruction")

        if report.get("validation") != report_validation:
            errors.append("stored report validation result mismatch")
        expected_counts: dict[str, int] = {}
        for item in expected_full_classifications:
            expected_counts[item["disposition"]] = expected_counts.get(item["disposition"], 0) + 1
        expected_legacy = build_successor_policy_future_production_dry_run(resolved_fixture)
        expected_legacy_full = expected_legacy["selected_candidates"] + expected_legacy["deprioritized_candidates"]
        expected_canonical_index = load_current_canonical_pearson_relationship_index()
        expected_synthetic = _build_synthetic_unresolved_verification(
            expected_pool, expected_candidates, expected_full_classifications
        )
        expected_run: dict[str, Any] = {
            "profile": "knowledgeforge.candidate_funnel_run_evidence.v1@1.0",
            "workflow_identity": "knowledgeforge.deterministic_candidate_funnel.pilot@1.0",
            "placement": "deterministic",
            "deterministic_route": [
                "authenticated_fixture_inventory",
                "mechanical_qualification_and_exclusion",
                "deterministic_semantic_proximity",
                "deterministic_batch_composition",
                "unresolved_only_escalation_packaging",
                "fail_closed_validation",
            ],
            "input_artifact_identities": {
                "fixture_root": report["fixture_root"],
                "source_population_fingerprint": report["source_population_fingerprint"],
                "canonical_relationship_index_fingerprint": sha256_value({
                    str(key): value for key, value in expected_canonical_index.items()
                }),
            },
            "output_artifact_identities": {
                "funnel_report": {
                    "path": "funnel_report.json",
                    "fingerprint": report["report_fingerprint"],
                },
                "unresolved_escalation_package": {
                    "path": "unresolved_escalation_package.json",
                    "fingerprint": escalation["collection_fingerprint"],
                },
            },
            "reused_artifacts": [
                {"identity": METHOD_IDENTITY, "fingerprint": METHOD_CONTRACT_FINGERPRINT},
                {"path": "docs/model_routing_policy.md", "fingerprint": sha256_file(PROJECT_ROOT / "docs/model_routing_policy.md")},
                {"path": report["fixture_root"], "fingerprint": report["source_population_fingerprint"]},
            ],
            "funnel_counts": report["funnel_stage_counts"],
            "validator_result": report_validation,
            "hermes_implementation_review_usage": {
                "boundary": "outside deterministic candidate-funnel execution",
                "normalized_project_workflow_usage_available": False,
                "reason": "Hermes usage is not normalized to KnowledgeForge workflow identities",
            },
            "report_fingerprint": report["report_fingerprint"],
            "escalation_collection_fingerprint": escalation["collection_fingerprint"],
            "source_population_fingerprint": report["source_population_fingerprint"],
            "source_candidate_count": len(expected_candidates),
            "deterministically_resolved_candidate_count": sum(
                expected_counts.get(key, 0) for key in ("selected", "deprioritized", "excluded")
            ),
            "human_review_candidate_count": expected_counts.get("unresolved", 0),
            "invalid_candidate_count": expected_counts.get("invalid", 0),
            "pre_change_full_candidate_records_materialized": len(expected_legacy_full),
            "pre_change_full_candidate_context_canonical_json_bytes": len(canonical_json(expected_legacy_full).encode()),
            "pre_change_full_candidate_context_scalar_leaf_count": scalar_leaf_count(expected_legacy_full),
            "post_change_funnel_report_canonical_json_bytes": len(canonical_json(report).encode()),
            "post_change_funnel_report_scalar_leaf_count": scalar_leaf_count(report),
            "post_change_escalation_context_canonical_json_bytes": len(canonical_json(escalation).encode()),
            "post_change_escalation_context_scalar_leaf_count": scalar_leaf_count(escalation),
            "post_change_combined_context_canonical_json_bytes": len(canonical_json(report).encode()) + len(canonical_json(escalation).encode()),
            "post_change_combined_context_scalar_leaf_count": scalar_leaf_count(report) + scalar_leaf_count(escalation),
            "comparison_basis": {
                "pre_change": "10 full mechanically eligible selected/deprioritized candidate records materialized by the prior future-production workflow",
                "post_change": "40 compact funnel classifications plus the unresolved-only escalation collection",
                "limitation": "different schemas and cardinalities; valid as representative workflow context-burden evidence, not as an intrinsic per-candidate efficiency estimate",
            },
            "adversarial_unresolved_verification": expected_synthetic,
            "measurement_boundary": "serialized JSON bytes and scalar leaves measure candidate/context burden; they are not token, cost, latency or capability-savings claims",
            "coefficient_free": not has_funnel_result_derived_key({"report": report, "escalation": escalation}),
            "replay_command": "python3 -m unittest tests.test_coefficient_free_pearson_candidate_registry",
        }
        expected_run["run_fingerprint"] = sha256_value(expected_run)
        if run != expected_run:
            errors.append("run evidence does not match deterministic reconstruction")

        run_payload = {key: value for key, value in run.items() if key != "run_fingerprint"}
        if sha256_value(run_payload) != run.get("run_fingerprint"):
            errors.append("run evidence fingerprint mismatch")
        if run.get("report_fingerprint") != report.get("report_fingerprint"):
            errors.append("run/report cross-fingerprint mismatch")
        if run.get("escalation_collection_fingerprint") != escalation.get("collection_fingerprint"):
            errors.append("run/escalation cross-fingerprint mismatch")
        if run.get("source_population_fingerprint") != report.get("source_population_fingerprint"):
            errors.append("run/source-population cross-fingerprint mismatch")
        if run.get("funnel_counts") != report.get("funnel_stage_counts"):
            errors.append("run funnel counts mismatch")
        if run.get("validator_result") != report.get("validation"):
            errors.append("run validator result mismatch")
        if run.get("placement") != "deterministic":
            errors.append("run placement is not deterministic")
        if has_funnel_result_derived_key(outputs):
            errors.append("result-derived field entered deterministic outputs")
    except (AttributeError, KeyError, TypeError, ValueError):
        errors.append("malformed candidate funnel output set")
    return {"valid": not errors, "errors": sorted(set(errors))}


def write_candidate_funnel_outputs(
    outputs: dict[str, Any],
    report_root: Path = CANDIDATE_FUNNEL_REPORT_ROOT,
    authorized_root: Path | None = None,
) -> dict[str, str]:
    validation = validate_candidate_funnel_outputs(outputs, require_elapsed=True)
    if not validation["valid"]:
        raise ValueError(f"candidate funnel outputs invalid: {validation['errors']}")
    root = report_root if report_root.is_absolute() else PROJECT_ROOT / report_root
    authority = authorized_root or (PROJECT_ROOT / "artifacts/reports")
    authority = authority.resolve(strict=True)
    resolved_root = root.resolve(strict=False)
    try:
        resolved_root.relative_to(authority)
    except ValueError as exc:
        raise ValueError("output root escapes authorized report boundary") from exc
    cursor = root.absolute()
    while cursor != authority and cursor != cursor.parent:
        if cursor.exists() and cursor.is_symlink():
            raise ValueError(f"symlinked output path component rejected: {cursor}")
        cursor = cursor.parent
    root.mkdir(parents=True, exist_ok=True)
    paths = {
        "funnel_report": root / "funnel_report.json",
        "unresolved_escalation_package": root / "unresolved_escalation_package.json",
        "run_evidence": root / "run_evidence.json",
    }
    for key, path in paths.items():
        if path.is_symlink():
            raise ValueError(f"symlinked output destination rejected: {path}")
        temporary = path.with_name(f".{path.name}.tmp")
        if temporary.exists() or temporary.is_symlink():
            raise ValueError(f"unsafe temporary output destination: {temporary}")
        temporary.write_text(json.dumps(outputs[key], indent=2, sort_keys=True, ensure_ascii=False) + "\n")
        temporary.replace(path)
    return {key: str(path) for key, path in paths.items()}


def registry_records_from_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for c in candidates:
        records.append({
            "candidate_id": c["candidate_id"],
            "entity": c["entity"],
            "family": c["family"],
            "period": c["period"],
            "expected_package_id": c["expected_package_id"],
            "series_a": c["series_a"]["identity"],
            "series_b": c["series_b"]["identity"],
            "evidence_fingerprints": {
                "series_a_normalized": c["series_a"]["evidence_identity"]["normalized_fingerprint"],
                "series_b_normalized": c["series_b"]["evidence_identity"]["normalized_fingerprint"],
                "series_a_raw_fixture": c["series_a"]["evidence_identity"]["raw_fixture_fingerprint"],
                "series_b_raw_fixture": c["series_b"]["evidence_identity"]["raw_fixture_fingerprint"],
            },
            "alignment_keys": c["alignment_keys"],
            "thresholds": c["thresholds"],
            "selection_evidence": c["selection_evidence"],
            "construction_risk_tags": c["construction_risk"],
            "semantic_limitations": c["semantic_limitations"],
            "contains_pearson_coefficient": False,
        })
    return records


def validate_registry_and_spec(registry: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    if has_forbidden_key(registry) or has_forbidden_key(spec.get("selection_evidence", {})):
        errors.append("forbidden outcome-derived field present")
    candidates = spec.get("candidates", [])
    if not (6 <= len(candidates) <= 8):
        errors.append("candidate count outside 6-8")
    ids = [c["candidate_id"] for c in candidates]
    pkgs = [c["expected_package_id"] for c in candidates]
    if len(ids) != len(set(ids)):
        errors.append("duplicate candidate ids")
    if len(pkgs) != len(set(pkgs)):
        errors.append("duplicate expected package ids")
    existing_pkg_paths = [PROJECT_ROOT / "knowledge_repository" / "objects" / f"{pkg}.json" for pkg in pkgs]
    collisions = []
    frozen_selection = spec.get("selection", {}).get("frozen_selection_fingerprint")
    for path in existing_pkg_paths:
        if not path.exists():
            continue
        try:
            existing = json.loads(path.read_text())
        except Exception:
            collisions.append(str(path))
            continue
        refs = existing.get("input_references", [])
        # Before publication, expected package IDs must not collide. After successful
        # publication, rerunning coefficient-free validation should still be able to
        # verify the frozen registry against its own already-published packages.
        if frozen_selection not in refs:
            collisions.append(str(path))
    if collisions:
        errors.append(f"expected package IDs collide with unrelated existing packages: {collisions}")
    seen_pairs = set()
    for c in candidates:
        a = c["series_a"]["identity"]["code"]
        b = c["series_b"]["identity"]["code"]
        key = canonical_pair_key(c["entity"], a, b)
        if key in seen_pairs:
            errors.append(f"duplicate/reversed pair: {key}")
        seen_pairs.add(key)
        if key in EXCLUDED_PRIOR_PAIRS:
            errors.append(f"prior relationship not excluded: {key}")
        if a == b:
            errors.append(f"self-pair: {key}")
        if c["series_a"]["identity"].get("frequency") != "annual" or c["series_b"]["identity"].get("frequency") != "annual":
            errors.append(f"non-annual frequency: {key}")
        if c["selection_evidence"]["coverage_probe"]["expected_aligned_pairs"] < 30:
            errors.append(f"insufficient overlap: {key}")
    return {"valid": not errors, "errors": errors, "candidate_count": len(candidates), "expected_package_ids": pkgs}


def build_outputs(fixture_root: Path = DEFAULT_FIXTURE_ROOT, report_root: Path = DEFAULT_REPORT_ROOT, spec_path: Path = DEFAULT_SPEC_PATH) -> dict[str, Any]:
    pool = load_series_pool(fixture_root)
    proposals, excluded = enumerate_proposals(pool)
    selected = select_candidates(proposals, 8)
    records = registry_records_from_candidates(selected)
    selection_policy = {
        "eligible_evidence_pool": str(fixture_root),
        "pool_rule": "retained validated Campaign 40 WDI annual-scalar individual-series fixtures only",
        "canonical_ordering_rules": [
            "group by entity order DNK, NOR, SWE",
            "within entity sort by canonical series order: family, indicator code, indicator name",
            "canonicalize pair side ordering by family, indicator code, indicator name",
        ],
        "duplicate_removal": "remove self-pairs and duplicate/reversed entity-indicator pairs before selection",
        "prior_relationship_exclusion": "exclude relationships already canonicalized or frozen/rejected in Campaigns 36-40 with same entity/scope/transformation",
        "compatibility_filters": ["same entity", "annual frequency", "raw transformation", "resolved units", "at least 30 aligned observed annual pairs", "at least 0.85 aligned coverage"],
        "semantic_risk_filters": ["exclude direct arithmetic identities", "exclude direct component-total relationships", "exclude near-duplicate indicator definitions", "exclude candidates requiring interpretive/causal/forecast/investment justification"],
        "diversity_rules": ["round-robin across DNK/NOR/SWE", "maximum three candidates per entity", "maximum two uses of the same indicator per entity before deterministic relaxation", "prefer cross-family retained pairs when available"],
        "tie_breaking_rules": ["entity order", "series_a indicator code", "series_b indicator code", "candidate_id lexical order"],
        "maximum_candidate_count": 8,
        "outcome_values_used": False,
    }
    registry_base = {
        "registry_id": "campaign41_coefficient_free_pearson_candidate_registry_v1",
        "campaign_id": "campaign41_coefficient_free_pearson_batch",
        "created_for_task": "Campaign 41 — Coefficient-Free Pearson Candidate Registry and Batch Specification",
        "method_identity": METHOD_IDENTITY,
        "method_contract_fingerprint": METHOD_CONTRACT_FINGERPRINT,
        "forbidden_fields": sorted(FORBIDDEN_KEYS),
        "selection_policy": selection_policy,
        "eligible_pool_summary": {
            "series_count": len(pool),
            "proposal_count_after_filters": len(proposals),
            "selected_candidate_count": len(selected),
            "retained_fixture_root": str(fixture_root),
            "series": [evidence_identity(s) for s in sorted(pool, key=lambda s: (ENTITY_ORDER.get(s.entity, 99), s.family, s.code))],
        },
        "records": records,
        "excluded_proposals": sorted(excluded, key=lambda e: (ENTITY_ORDER.get(e["entity"], 99), e["entity"], e["series_a"], e["series_b"])),
        "coefficient_free_proof": {
            "no_campaign41_coefficient_calculated": True,
            "no_covariance_calculated": True,
            "no_p_value_or_significance_calculated": True,
            "no_outcome_cache_consulted": True,
            "no_candidate_ranked_by_numerical_association": True,
            "registry_contains_result_field": False,
            "proof_basis": "helper uses retained metadata, fingerprints, observed/missing period overlap, units, transformation, duplicate/existing-pair exclusion, and deterministic ordering only",
        },
    }
    registry_base["registry_fingerprint"] = sha256_value({k: v for k, v in registry_base.items() if k != "registry_fingerprint"})
    spec_base = {
        "campaign_id": "campaign41_coefficient_free_pearson_batch",
        "engine_contract": ENGINE_CONTRACT,
        "mode": "production",
        "publication_date": "2026-07-12",
        "method": {"identity": METHOD_IDENTITY, "contract_fingerprint": METHOD_CONTRACT_FINGERPRINT},
        "registry_path": str(report_root / "selection" / "candidate_registry.json"),
        "registry_fingerprint": registry_base["registry_fingerprint"],
        "thresholds": {"min_aligned_pairs": 30, "min_aligned_coverage": "0.85"},
        "selection": {
            "campaign_id": "campaign41_coefficient_free_pearson_batch",
            "coefficient_freeze_verified": True,
            "frozen_candidate_ids": [c["candidate_id"] for c in selected],
            "registry_fingerprint": registry_base["registry_fingerprint"],
            "selection_rules": selection_policy,
        },
        "selection_evidence": {
            "contains_coefficients": False,
            "registry_records": records,
            "selection_policy_fingerprint": sha256_value(selection_policy),
        },
        "scope_exclusions": [
            "Campaign 41 calculation",
            "Pearson coefficient computation",
            "covariance/p-value/significance computation",
            "canonical package creation",
            "repository publication",
            "PostgreSQL rebuild or write",
            "relationship export execution",
            "Campaign 42",
            "MacroForge or InsightForge modification",
            "Doctrine amendment",
        ],
        "candidates": selected,
    }
    spec_base["selection"]["frozen_selection_fingerprint"] = sha256_value({"records": records, "policy": selection_policy})
    spec_base["batch_spec_fingerprint"] = sha256_value({k: v for k, v in spec_base.items() if k != "batch_spec_fingerprint"})
    validation = validate_registry_and_spec(registry_base, spec_base)
    return {
        "pool": pool,
        "proposals": proposals,
        "excluded": excluded,
        "registry": registry_base,
        "spec": spec_base,
        "validation": validation,
        "paths": {
            "registry": str(report_root / "selection" / "candidate_registry.json"),
            "spec": str(spec_path),
        },
    }


def write_outputs(outputs: dict[str, Any], report_root: Path = DEFAULT_REPORT_ROOT, spec_path: Path = DEFAULT_SPEC_PATH) -> dict[str, Any]:
    registry_path = PROJECT_ROOT / report_root / "selection" / "candidate_registry.json"
    compatibility_path = PROJECT_ROOT / report_root / "selection" / "candidate_compatibility_report.json"
    validation_path = PROJECT_ROOT / report_root / "selection" / "coefficient_free_validation_result.json"
    manifest_path = PROJECT_ROOT / report_root / "selection" / "expected_package_id_manifest.json"
    spec_abs = PROJECT_ROOT / spec_path
    registry = outputs["registry"]
    spec = outputs["spec"]
    validation = outputs["validation"]
    compatibility = {
        "campaign_id": spec["campaign_id"],
        "registry_fingerprint": registry["registry_fingerprint"],
        "batch_spec_fingerprint": spec["batch_spec_fingerprint"],
        "candidate_count": len(spec["candidates"]),
        "candidates": [
            {
                "candidate_id": c["candidate_id"],
                "expected_package_id": c["expected_package_id"],
                "entity": c["entity"],
                "series_a": c["series_a"]["identity"],
                "series_b": c["series_b"]["identity"],
                "aligned_pair_count": c["selection_evidence"]["coverage_probe"]["expected_aligned_pairs"],
                "aligned_coverage": c["selection_evidence"]["coverage_probe"]["aligned_coverage"],
                "units": {"series_a": c["series_a"]["identity"]["unit"], "series_b": c["series_b"]["identity"]["unit"]},
                "transformation_state": c["transformation_state"],
                "method_contract": c["method_contract"],
                "construction_risk": c["construction_risk"],
                "semantic_limitations": c["semantic_limitations"],
                "compatible": True,
            }
            for c in spec["candidates"]
        ],
    }
    expected_manifest = {
        "campaign_id": spec["campaign_id"],
        "package_ids_unique": len({c["expected_package_id"] for c in spec["candidates"]}) == len(spec["candidates"]),
        "expected_package_ids": [c["expected_package_id"] for c in spec["candidates"]],
        "existing_package_collision": [],
    }
    write_json(registry_path, registry)
    write_json(spec_abs, spec)
    write_json(compatibility_path, compatibility)
    write_json(validation_path, validation)
    write_json(manifest_path, expected_manifest)
    return {
        "registry_path": _rel(registry_path),
        "spec_path": _rel(spec_abs),
        "compatibility_path": _rel(compatibility_path),
        "validation_path": _rel(validation_path),
        "expected_package_manifest_path": _rel(manifest_path),
        "registry_fingerprint": registry["registry_fingerprint"],
        "batch_spec_fingerprint": spec["batch_spec_fingerprint"],
        "valid": validation["valid"],
    }


def detect_campaign40_engine_hardcoding() -> dict[str, Any]:
    engine_path = PROJECT_ROOT / "tools" / "correlation_batch_engine.py"
    text = engine_path.read_text()
    snippets = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        if "campaign40" in line:
            snippets.append({"line": line_no, "text": line.strip()})
    return {
        "engine_path": "tools/correlation_batch_engine.py",
        "campaign40_hardcoded_package_internals_found": bool(snippets),
        "snippets": snippets,
        "calculation_gate_decision": "bounded reusable engine extension required before Campaign 41 calculation" if snippets else "existing engine sufficient for calculation",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build/validate Campaign 41 coefficient-free Pearson candidate registry")
    parser.add_argument("--fixture-root", default=str(DEFAULT_FIXTURE_ROOT))
    parser.add_argument("--report-root", default=str(DEFAULT_REPORT_ROOT))
    parser.add_argument("--spec-path", default=str(DEFAULT_SPEC_PATH))
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    outputs = build_outputs(Path(args.fixture_root), Path(args.report_root), Path(args.spec_path))
    written = write_outputs(outputs, Path(args.report_root), Path(args.spec_path)) if args.write else {}
    result = {
        "valid": outputs["validation"]["valid"],
        "validation": outputs["validation"],
        "candidate_count": len(outputs["spec"]["candidates"]),
        "registry_fingerprint": outputs["registry"]["registry_fingerprint"],
        "batch_spec_fingerprint": outputs["spec"]["batch_spec_fingerprint"],
        "expected_package_ids": [c["expected_package_id"] for c in outputs["spec"]["candidates"]],
        "written": written,
        "engine_reuse_assessment": detect_campaign40_engine_hardcoding(),
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if outputs["validation"]["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
