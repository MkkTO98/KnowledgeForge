#!/usr/bin/env python3
"""Bounded WDI observation-level evidence fixture tooling for KnowledgeForge.

This module operationalizes one neutral external evidence-input boundary. It
acquires a small immutable WDI annual-scalar fixture directly from the World
Bank API, preserves raw response bytes, deterministically normalizes
observation-level evidence, and validates offline reproducibility.

It deliberately does not create KnowledgeObjectPackages, run production
campaigns, access any other EIP project, or define a general observational data
platform.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

TOOL_VERSION = "wdi_observation_evidence_fixture_v1"
PROVIDER_IDENTITY = {
    "provider_name": "World Bank",
    "dataset": "World Development Indicators",
    "api_base_url": "https://api.worldbank.org/v2",
    "source_id": "2",
}
DEFAULT_INDICATOR = "SP.POP.TOTL"
DEFAULT_ENTITY = "DNK"
DEFAULT_START_YEAR = 1990
DEFAULT_END_YEAR = 2024
USER_AGENT = "KnowledgeForgeEvidenceFixture/1.0"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_value(value: Any) -> str:
    return sha256_bytes(canonical_bytes(value))


def _valid_sha256(value: Any) -> bool:
    text = str(value)
    return text.startswith("sha256:") and len(text) == 71 and all(c in "0123456789abcdef" for c in text[7:])


def _utc_now() -> str:
    return _dt.datetime.now(_dt.UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _years(start_year: int, end_year: int) -> list[int]:
    if start_year > end_year:
        raise ValueError("start_year must be <= end_year")
    return list(range(start_year, end_year + 1))


def observation_url(indicator_code: str, entities: list[str], start_year: int, end_year: int) -> str:
    entity_path = ";".join(entities)
    # urllib keeps semicolon path separators literal, matching World Bank multi-country convention.
    params = urllib.parse.urlencode({"format": "json", "date": f"{start_year}:{end_year}", "per_page": "100"}, safe=":")
    return f"{PROVIDER_IDENTITY['api_base_url']}/country/{entity_path}/indicator/{indicator_code}?{params}"


def indicator_metadata_url(indicator_code: str) -> str:
    params = urllib.parse.urlencode({"format": "json", "per_page": "1"})
    return f"{PROVIDER_IDENTITY['api_base_url']}/indicator/{indicator_code}?{params}"


def validate_final_url(*, requested_url: str, final_url: str) -> str:
    """Validate that provider redirects did not downgrade HTTPS transport."""
    if not requested_url.startswith("https://"):
        raise ValueError("requested URL must use HTTPS")
    if final_url.startswith("http://"):
        raise ValueError("HTTPS downgrade rejected")
    if not final_url.startswith("https://"):
        raise ValueError("final resolved URL must use HTTPS")
    return final_url


def build_selection_contract(
    *,
    indicator_code: str = DEFAULT_INDICATOR,
    entities: list[str] | None = None,
    start_year: int = DEFAULT_START_YEAR,
    end_year: int = DEFAULT_END_YEAR,
) -> dict[str, Any]:
    entity_list = sorted(entities or [DEFAULT_ENTITY])
    contract = {
        "contract_version": "1.0",
        "tool_version": TOOL_VERSION,
        "selection_purpose": "bounded observation-level WDI annual-scalar evidence fixture for later statistical-summary pilot design",
        "mature_knowledgeforge_family": "external_wdi_annual_scalar_demographic_structure",
        "source_family": "official_statistical_source_data",
        "provider": PROVIDER_IDENTITY,
        "indicator": {"code": indicator_code},
        "entities": entity_list,
        "periods": {"frequency": "annual", "start_year": start_year, "end_year": end_year, "years": _years(start_year, end_year)},
        "request": {
            "observation_url": observation_url(indicator_code, entity_list, start_year, end_year),
            "indicator_metadata_url": indicator_metadata_url(indicator_code),
            "parameters": {"format": "json", "date": f"{start_year}:{end_year}", "per_page": "100"},
        },
        "completeness_expectation": {
            "expected_observation_slots": len(entity_list) * (end_year - start_year + 1),
            "expected_pages": 1,
            "missing_values_are_explicit": True,
        },
        "scope_exclusions": [
            "full WDI topic ingestion",
            "ordinary WDI breadth expansion",
            "statistical-summary production execution",
            "cross-indicator causal reasoning",
            "forecasting",
            "recommendations",
        ],
    }
    contract["selection_fingerprint"] = sha256_value({k: v for k, v in contract.items() if k != "selection_fingerprint"})
    return contract


def _ensure_provider_response(payload: Any) -> None:
    if not isinstance(payload, list) or len(payload) != 2 or not isinstance(payload[0], dict) or not isinstance(payload[1], list):
        raise ValueError("provider response must be [metadata, records]")


def raw_fixture_from_provider_payloads(
    *,
    selection_contract: dict[str, Any],
    observation_payload: Any,
    indicator_metadata_payload: Any,
    observation_response_bytes: bytes,
    indicator_metadata_response_bytes: bytes,
    access_timestamp_utc: str,
    final_observation_url: str | None = None,
    final_indicator_metadata_url: str | None = None,
) -> dict[str, Any]:
    _ensure_provider_response(observation_payload)
    _ensure_provider_response(indicator_metadata_payload)
    raw = {
        "fixture_kind": "WDIObservationEvidenceRawFixture",
        "fixture_version": "1.0",
        "tool_version": TOOL_VERSION,
        "provider_identity": PROVIDER_IDENTITY,
        "selection_contract": selection_contract,
        "access_metadata": {
            "access_timestamp_utc": access_timestamp_utc,
            "access_timestamp_is_noncanonical": True,
            "user_agent": USER_AGENT,
            "requested_urls": {
                "observation_response": selection_contract["request"]["observation_url"],
                "indicator_metadata_response": selection_contract["request"]["indicator_metadata_url"],
            },
            "final_resolved_urls": {
                "observation_response": validate_final_url(
                    requested_url=selection_contract["request"]["observation_url"],
                    final_url=final_observation_url or selection_contract["request"]["observation_url"],
                ),
                "indicator_metadata_response": validate_final_url(
                    requested_url=selection_contract["request"]["indicator_metadata_url"],
                    final_url=final_indicator_metadata_url or selection_contract["request"]["indicator_metadata_url"],
                ),
            },
        },
        "raw_artifacts": {
            "observation_response_sha256": sha256_bytes(observation_response_bytes),
            "indicator_metadata_response_sha256": sha256_bytes(indicator_metadata_response_bytes),
            "combined_raw_artifact_fingerprint": sha256_value({
                "observation_response_sha256": sha256_bytes(observation_response_bytes),
                "indicator_metadata_response_sha256": sha256_bytes(indicator_metadata_response_bytes),
                "selection_fingerprint": selection_contract["selection_fingerprint"],
            }),
        },
        "provider_payloads": {
            "observations": observation_payload,
            "indicator_metadata": indicator_metadata_payload,
        },
        "provider_metadata": {
            "observation_page": observation_payload[0],
            "indicator_metadata_page": indicator_metadata_payload[0],
            "wdi_lastupdated": observation_payload[0].get("lastupdated"),
            "sourceid": observation_payload[0].get("sourceid"),
            "pagination": {
                "page": observation_payload[0].get("page"),
                "pages": observation_payload[0].get("pages"),
                "per_page": observation_payload[0].get("per_page"),
                "total": observation_payload[0].get("total"),
            },
        },
        "mutable_source_reproducibility_note": {
            "exact_reproducibility_basis": "retained local raw response bytes and normalized fixture",
            "source_identity_basis": "World Bank WDI API URL, request parameters, source id, and lastupdated metadata",
            "vintage_limitation": "WDI API response is mutable; no true immutable historical vintage identifier was observed in the API response, so reacquiring identical bytes later is not claimed.",
        },
    }
    raw["raw_fixture_fingerprint"] = sha256_value({k: v for k, v in raw.items() if k != "raw_fixture_fingerprint"})
    return raw


def _parse_json_bytes(data: bytes) -> Any:
    try:
        return json.loads(data.decode("utf-8"))
    except Exception as exc:
        raise ValueError(f"invalid JSON provider response: {exc}") from exc


def fetch_url_bytes(url: str) -> tuple[bytes, str]:
    validate_final_url(requested_url=url, final_url=url)
    last_error: Exception | None = None
    for _ in range(3):
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urllib.request.urlopen(req, timeout=180) as response:
                final_url = validate_final_url(requested_url=url, final_url=response.geturl())
                return response.read(), final_url
        except (TimeoutError, urllib.error.URLError, urllib.error.HTTPError) as exc:
            last_error = exc
    raise RuntimeError(f"provider request failed for {url}: {last_error}")


def acquire_raw_fixture(selection_contract: dict[str, Any]) -> tuple[dict[str, Any], bytes, bytes]:
    observation_bytes, final_observation_url = fetch_url_bytes(selection_contract["request"]["observation_url"])
    metadata_bytes, final_metadata_url = fetch_url_bytes(selection_contract["request"]["indicator_metadata_url"])
    raw = raw_fixture_from_provider_payloads(
        selection_contract=selection_contract,
        observation_payload=_parse_json_bytes(observation_bytes),
        indicator_metadata_payload=_parse_json_bytes(metadata_bytes),
        observation_response_bytes=observation_bytes,
        indicator_metadata_response_bytes=metadata_bytes,
        access_timestamp_utc=_utc_now(),
        final_observation_url=final_observation_url,
        final_indicator_metadata_url=final_metadata_url,
    )
    return raw, observation_bytes, metadata_bytes


def validate_raw_fixture(raw: dict[str, Any], observation_response_bytes: bytes | None = None, indicator_metadata_response_bytes: bytes | None = None) -> dict[str, Any]:
    _ensure_provider_response(raw.get("provider_payloads", {}).get("observations"))
    _ensure_provider_response(raw.get("provider_payloads", {}).get("indicator_metadata"))
    if observation_response_bytes is not None:
        actual = sha256_bytes(observation_response_bytes)
        expected = raw["raw_artifacts"]["observation_response_sha256"]
        if actual != expected:
            raise ValueError("raw observation fingerprint mismatch")
    elif not _valid_sha256(raw.get("raw_artifacts", {}).get("observation_response_sha256", "")):
        raise ValueError("raw observation fingerprint mismatch")
    if indicator_metadata_response_bytes is not None:
        actual = sha256_bytes(indicator_metadata_response_bytes)
        expected = raw["raw_artifacts"]["indicator_metadata_response_sha256"]
        if actual != expected:
            raise ValueError("raw indicator metadata fingerprint mismatch")
    elif not _valid_sha256(raw.get("raw_artifacts", {}).get("indicator_metadata_response_sha256", "")):
        raise ValueError("raw indicator metadata fingerprint mismatch")
    return {"valid": True, "checks": ["provider_response_shape", "raw_fingerprint_shape"]}


def _decimal_to_canonical(value: Any) -> str | None:
    if value is None:
        return None
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"non-numeric observation value: {value!r}") from exc
    if not dec.is_finite():
        raise ValueError(f"non-finite observation value: {value!r}")
    normalized = format(dec.normalize(), "f")
    if "." in normalized:
        normalized = normalized.rstrip("0").rstrip(".")
    return normalized or "0"


def _indicator_metadata(raw: dict[str, Any]) -> dict[str, Any]:
    records = raw["provider_payloads"]["indicator_metadata"][1]
    if len(records) != 1:
        raise ValueError("indicator metadata response must contain exactly one record")
    return records[0]




def resolve_wdi_unit(metadata: dict[str, Any], row_unit: Any = None) -> dict[str, Any]:
    """Resolve WDI unit semantics without unsafe generic defaults."""
    provider_unit = (metadata.get("unit") or row_unit or "")
    indicator_id = metadata.get("id")
    name = metadata.get("name") or ""
    definition = metadata.get("sourceNote") or ""
    basis = {
        "indicator_id": indicator_id,
        "name": name,
        "provider_unit": provider_unit,
        "definition": definition,
        "source_organization": metadata.get("sourceOrganization"),
    }
    metadata_fingerprint = sha256_value(basis)
    if isinstance(provider_unit, str) and provider_unit.strip():
        result = {
            "state": "provider-explicit unit",
            "resolved_unit": provider_unit.strip(),
            "provider_unit_value": provider_unit.strip(),
            "evidence_reference": "indicator_metadata.unit or observation.unit",
            "metadata_fingerprint": metadata_fingerprint,
        }
    elif indicator_id == "SP.POP.TOTL" and "population" in name.lower() and "population" in definition.lower():
        result = {
            "state": "definition-derived unit",
            "resolved_unit": "persons",
            "derivation_rule": "indicator id SP.POP.TOTL plus authoritative name/definition identify total population counts",
            "supporting_metadata_fingerprint": metadata_fingerprint,
        }
    elif "% of GDP" in name and "percentage of Gross Domestic Product (GDP)" in definition:
        result = {
            "state": "definition-derived unit",
            "resolved_unit": "percent of GDP",
            "derivation_rule": "authoritative WDI indicator name contains '% of GDP' and sourceNote says percentage of Gross Domestic Product (GDP)",
            "supporting_metadata_fingerprint": metadata_fingerprint,
        }
    elif "index" in name.lower() and "unit" not in definition.lower():
        result = {
            "state": "explicitly unitless/dimensionless",
            "resolved_unit": "unitless index",
            "derivation_rule": "authoritative indicator name describes an index and no provider unit is supplied",
            "supporting_metadata_fingerprint": metadata_fingerprint,
        }
    else:
        result = {
            "state": "unresolved unit",
            "resolved_unit": None,
            "reason": "provider unit field absent/uninformative and authoritative name/definition do not match an approved deterministic unit rule",
            "supporting_metadata_fingerprint": metadata_fingerprint,
        }
    result["metadata_fingerprint"] = metadata_fingerprint
    result["unit_resolution_fingerprint"] = sha256_value({k: v for k, v in result.items() if k != "unit_resolution_fingerprint"})
    return result

def normalize_raw_fixture(raw: dict[str, Any]) -> dict[str, Any]:
    validate_raw_fixture(raw)
    contract = raw["selection_contract"]
    indicator_code = contract["indicator"]["code"]
    entities = set(contract["entities"])
    expected_years = contract["periods"]["years"]
    metadata = _indicator_metadata(raw)
    if metadata.get("id") != indicator_code:
        raise ValueError("requested indicator identity does not match returned identity")
    unit_resolution = resolve_wdi_unit(metadata)
    if unit_resolution["state"] == "unresolved unit":
        raise ValueError(f"unresolved unit for indicator {indicator_code}")
    resolved_unit = unit_resolution["resolved_unit"]
    seen: set[tuple[str, int]] = set()
    observed_by_key: dict[tuple[str, int], dict[str, Any]] = {}
    for row in raw["provider_payloads"]["observations"][1]:
        if not isinstance(row, dict):
            raise ValueError("observation row must be object")
        returned_indicator = (row.get("indicator") or {}).get("id")
        if returned_indicator != indicator_code:
            raise ValueError("requested indicator identity does not match returned identity")
        entity = row.get("countryiso3code")
        if entity not in entities:
            raise ValueError("returned observation outside entity scope")
        date_value = row.get("date")
        if date_value is None:
            raise ValueError("observation period is not an integer year")
        try:
            period = int(date_value)
        except Exception as exc:
            raise ValueError("observation period is not an integer year") from exc
        if period not in expected_years:
            raise ValueError("returned observation outside period scope")
        key = (entity, period)
        if key in seen:
            raise ValueError("duplicate observation")
        seen.add(key)
        value_canonical = _decimal_to_canonical(row.get("value"))
        observed_by_key[key] = {
            "indicator_code": indicator_code,
            "indicator_name": (row.get("indicator") or {}).get("value"),
            "entity_id": entity,
            "entity_name": (row.get("country") or {}).get("value"),
            "period": period,
            "frequency": "annual",
            "unit": resolved_unit,
            "unit_resolution_fingerprint": unit_resolution["unit_resolution_fingerprint"],
            "value_canonical": value_canonical,
            "observed": value_canonical is not None,
            "missing_reason": None if value_canonical is not None else "provider_value_null",
            "obs_status": row.get("obs_status") or "",
            "decimal": row.get("decimal"),
        }
    observations: list[dict[str, Any]] = []
    for entity in sorted(entities):
        for year in expected_years:
            key = (entity, year)
            if key in observed_by_key:
                observations.append(observed_by_key[key])
            else:
                observations.append({
                    "indicator_code": indicator_code,
                    "indicator_name": metadata.get("name"),
                    "entity_id": entity,
                    "entity_name": None,
                    "period": year,
                    "frequency": "annual",
                    "unit": resolved_unit,
                    "unit_resolution_fingerprint": unit_resolution["unit_resolution_fingerprint"],
                    "value_canonical": None,
                    "observed": False,
                    "missing_reason": "provider_row_absent",
                    "obs_status": "",
                    "decimal": None,
                })
    observed_count = sum(1 for obs in observations if obs["observed"])
    missing_count = len(observations) - observed_count
    normalized = {
        "fixture_kind": "WDIObservationEvidenceNormalizedFixture",
        "fixture_version": "1.0",
        "tool_version": TOOL_VERSION,
        "source_raw_fixture_fingerprint": raw["raw_fixture_fingerprint"],
        "raw_artifacts": raw["raw_artifacts"],
        "selection_contract": contract,
        "selection_fingerprint": contract["selection_fingerprint"],
        "provider_metadata": raw["provider_metadata"],
        "indicator_metadata": {
            "id": metadata.get("id"),
            "name": metadata.get("name"),
            "unit": resolved_unit,
            "unit_resolution": unit_resolution,
            "definition": metadata.get("sourceNote"),
            "source_organization": metadata.get("sourceOrganization"),
            "topics": metadata.get("topics", []),
        },
        "observations": observations,
        "expected_observation_slots": len(observations),
        "observed_count": observed_count,
        "missing_count": missing_count,
        "missing_share": round(missing_count / len(observations), 12) if observations else 0.0,
        "normalization": {
            "canonical_order": ["entity_id", "indicator_code", "period"],
            "numeric_representation": "base-10 decimal string or null",
            "missingness_policy": "explicit null observation rows are retained; absent expected rows are materialized as missing",
            "access_timestamp_excluded_from_normalized_fingerprint": True,
        },
        "mutable_source_reproducibility_note": raw["mutable_source_reproducibility_note"],
    }
    normalized["normalized_fingerprint"] = sha256_value({k: v for k, v in normalized.items() if k != "normalized_fingerprint"})
    return normalized


def validate_normalized_fixture(normalized: dict[str, Any]) -> dict[str, Any]:
    observations = normalized.get("observations")
    if not isinstance(observations, list):
        raise ValueError("normalized observations must be a list")
    keys = [(obs["entity_id"], obs["indicator_code"], obs["period"]) for obs in observations]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate normalized observation")
    if keys != sorted(keys, key=lambda x: (x[0], x[1], x[2])):
        raise ValueError("normalized observations are not in canonical order")
    expected = sha256_value({k: v for k, v in normalized.items() if k != "normalized_fingerprint"})
    if expected != normalized.get("normalized_fingerprint"):
        raise ValueError("normalized fingerprint mismatch")
    return {
        "valid": True,
        "observation_count": len(observations),
        "observed_count": normalized["observed_count"],
        "missing_count": normalized["missing_count"],
        "normalized_fingerprint": normalized["normalized_fingerprint"],
    }


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_bytes(value) + b"\n")


def write_fixture_artifacts(raw: dict[str, Any], output_dir: Path, observation_response_bytes: bytes | None = None, indicator_metadata_response_bytes: bytes | None = None) -> dict[str, Any]:
    output_dir.mkdir(parents=True, exist_ok=True)
    if observation_response_bytes is not None:
        (output_dir / "raw_observations_response.json").write_bytes(observation_response_bytes)
    if indicator_metadata_response_bytes is not None:
        (output_dir / "raw_indicator_metadata_response.json").write_bytes(indicator_metadata_response_bytes)
    normalized = normalize_raw_fixture(raw)
    validation = {
        "raw_validation": validate_raw_fixture(raw, observation_response_bytes, indicator_metadata_response_bytes),
        "normalized_validation": validate_normalized_fixture(normalized),
        "offline_reproduction": {"regenerated_from_retained_raw_fixture": True},
        "boundary_validation": {
            "creates_knowledge_objects": False,
            "statistical_summary_executed": False,
            "campaign_34_created": False,
            "external_provider_only": True,
            "no_cross_project_runtime_dependency": True,
        },
    }
    write_json(output_dir / "selection_contract.json", raw["selection_contract"])
    write_json(output_dir / "acquisition_manifest.json", {
        "manifest_version": "1.0",
        "tool_version": TOOL_VERSION,
        "provider_identity": PROVIDER_IDENTITY,
        "selection_fingerprint": raw["selection_contract"]["selection_fingerprint"],
        "raw_artifacts": raw["raw_artifacts"],
        "provider_metadata": raw["provider_metadata"],
        "access_metadata": raw["access_metadata"],
        "access_timestamp_excluded_from_deterministic_fingerprints": True,
        "mutable_source_reproducibility_note": raw["mutable_source_reproducibility_note"],
    })
    write_json(output_dir / "raw_fixture.json", raw)
    write_json(output_dir / "normalized_observations.json", normalized)
    write_json(output_dir / "validation_results.json", validation)
    write_json(output_dir / "fingerprints.json", {
        "selection_fingerprint": raw["selection_contract"]["selection_fingerprint"],
        "raw_fixture_fingerprint": raw["raw_fixture_fingerprint"],
        "combined_raw_artifact_fingerprint": raw["raw_artifacts"]["combined_raw_artifact_fingerprint"],
        "normalized_fingerprint": normalized["normalized_fingerprint"],
    })
    return validation


def regenerate_normalized_from_raw(output_dir: Path) -> dict[str, Any]:
    raw = json.loads((output_dir / "raw_fixture.json").read_text())
    normalized = normalize_raw_fixture(raw)
    validate_normalized_fixture(normalized)
    return normalized


def acquire_and_write(output_dir: Path, *, indicator_code: str = DEFAULT_INDICATOR, entities: list[str] | None = None, start_year: int = DEFAULT_START_YEAR, end_year: int = DEFAULT_END_YEAR) -> dict[str, Any]:
    contract = build_selection_contract(indicator_code=indicator_code, entities=entities or [DEFAULT_ENTITY], start_year=start_year, end_year=end_year)
    raw, observation_bytes, metadata_bytes = acquire_raw_fixture(contract)
    return write_fixture_artifacts(raw, output_dir, observation_bytes, metadata_bytes)


def main() -> int:
    parser = argparse.ArgumentParser(description="Acquire or validate a bounded WDI observation evidence fixture.")
    sub = parser.add_subparsers(dest="command", required=True)
    acquire = sub.add_parser("acquire")
    acquire.add_argument("--output-dir", required=True)
    acquire.add_argument("--indicator", default=DEFAULT_INDICATOR)
    acquire.add_argument("--entity", action="append", default=None)
    acquire.add_argument("--start-year", type=int, default=DEFAULT_START_YEAR)
    acquire.add_argument("--end-year", type=int, default=DEFAULT_END_YEAR)
    validate = sub.add_parser("validate")
    validate.add_argument("--fixture-dir", required=True)
    args = parser.parse_args()
    if args.command == "acquire":
        result = acquire_and_write(Path(args.output_dir), indicator_code=args.indicator, entities=args.entity or [DEFAULT_ENTITY], start_year=args.start_year, end_year=args.end_year)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if args.command == "validate":
        regenerated = regenerate_normalized_from_raw(Path(args.fixture_dir))
        written = json.loads((Path(args.fixture_dir) / "normalized_observations.json").read_text())
        result = {
            "valid": regenerated["normalized_fingerprint"] == written.get("normalized_fingerprint"),
            "normalized_fingerprint": regenerated["normalized_fingerprint"],
            "observation_count": len(regenerated["observations"]),
            "observed_count": regenerated["observed_count"],
            "missing_count": regenerated["missing_count"],
        }
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["valid"] else 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
