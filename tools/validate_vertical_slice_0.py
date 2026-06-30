#!/usr/bin/env python3
"""Minimal deterministic validation for KnowledgeForge Vertical Slice 0.

This is intentionally not a framework, API, graph engine, ontology manager, or
persistence layer. It validates only the approved four-object fixture ecosystem.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


EXPECTED_OBJECT_IDS = [
    "claim-gdp-measures-aggregate-economic-output",
    "concept-aggregate-economic-output",
    "concept-gdp",
    "evidence-ref-gdp-source-documentation",
]

EXPECTED_OBJECT_FILES = {
    "claim-gdp-measures-aggregate-economic-output.json",
    "concept-aggregate-economic-output.json",
    "concept-gdp.json",
    "evidence-ref-gdp-source-documentation.json",
}

KERNEL_FIELDS = {
    "stable_id",
    "object_kind",
    "content_summary",
    "provenance",
    "applicability",
    "evidence_state",
    "lifecycle_state",
    "governance_state",
    "revision_history",
    "dependency_posture",
    "representation_neutrality",
}

ALLOWED_CLAIM_FACETS = {
    "assertion_function": {"definitional", "measurement/comparability"},
    "epistemic_nature": {"definition", "convention"},
    "polarity": {"positive assertion"},
    "domain_role": {"concept", "canonical concept"},
    "representation_form": {"textual assertion"},
}

REQUIRED_CLAIM_DEPENDENCIES = [
    "concept-gdp",
    "concept-aggregate-economic-output",
    "evidence-ref-gdp-source-documentation",
]

EXCLUDED_PREFIXES = ("dependency-", "relationship-", "mapping-")
FORBIDDEN_AUTHORITATIVE_REPRESENTATIONS = {"graph node", "graph edge", "database row", "api resource"}
FORBIDDEN_REPRESENTATION_SPECIFIC_FIELDS = {
    "api_endpoint",
    "api_resource",
    "api_url",
    "database_column",
    "database_row_id",
    "database_table",
    "db_column",
    "db_table",
    "graph_edge_id",
    "graph_id",
    "graph_node_id",
}
FORBIDDEN_OBSERVATIONAL_DATASET_VALUE_FIELDS = {
    "dataset_values",
    "observations",
    "observational_data",
    "observational_dataset",
    "observational_values",
    "rows",
    "series_values",
    "time_series",
    "values",
}


class ValidationError(Exception):
    """Raised when the Vertical Slice 0 fixture ecosystem violates scope."""


def _load_objects(project_root: Path) -> dict[str, dict[str, Any]]:
    objects_dir = project_root / "knowledge" / "objects"
    if not objects_dir.exists():
        raise ValidationError("knowledge/objects does not exist")

    object_files = sorted(path.name for path in objects_dir.glob("*.json"))
    if set(object_files) != EXPECTED_OBJECT_FILES:
        raise ValidationError(f"expected exactly {sorted(EXPECTED_OBJECT_FILES)}, found {object_files}")
    if any(name.startswith(EXCLUDED_PREFIXES) for name in object_files):
        raise ValidationError("excluded dependency/relationship/mapping object fixture present")

    objects: dict[str, dict[str, Any]] = {}
    for path in sorted(objects_dir.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        stable_id = data.get("stable_id")
        if not isinstance(stable_id, str):
            raise ValidationError(f"{path.name} has no string stable_id")
        if stable_id in objects:
            raise ValidationError(f"duplicate stable_id: {stable_id}")
        objects[stable_id] = data
    return objects


def _walk_fields(value: Any, path: tuple[str, ...] = ()):
    if isinstance(value, dict):
        for key, child in value.items():
            child_path = (*path, str(key))
            yield child_path, child
            yield from _walk_fields(child, child_path)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_fields(child, (*path, str(index)))


def _validate_no_observational_values(obj: dict[str, Any]) -> None:
    for field_path, value in _walk_fields(obj):
        field_name = field_path[-1]
        if field_name in FORBIDDEN_OBSERVATIONAL_DATASET_VALUE_FIELDS and value not in (None, [], {}, ""):
            raise ValidationError(
                f"{obj.get('stable_id', '<unknown>')} duplicates observational dataset values at {'.'.join(field_path)}"
            )


def _validate_representation_neutrality(obj: dict[str, Any]) -> None:
    for field_path, _value in _walk_fields(obj):
        field_name = field_path[-1]
        if field_name in FORBIDDEN_REPRESENTATION_SPECIFIC_FIELDS:
            raise ValidationError(
                f"{obj.get('stable_id', '<unknown>')} has representation-specific field {'.'.join(field_path)}"
            )

    neutrality = obj["representation_neutrality"]
    authoritative = str(neutrality.get("authoritative_representation", "")).lower()
    if authoritative in FORBIDDEN_AUTHORITATIVE_REPRESENTATIONS:
        raise ValidationError(f"{obj['stable_id']} makes {authoritative} authoritative")


def _validate_kernel(obj: dict[str, Any]) -> None:
    missing = sorted(KERNEL_FIELDS - set(obj))
    if missing:
        raise ValidationError(f"{obj.get('stable_id', '<unknown>')} missing kernel fields: {missing}")

    stable_id = obj["stable_id"]
    if not isinstance(stable_id, str) or not stable_id:
        raise ValidationError("durable object has missing stable identity")
    if not isinstance(obj["object_kind"], str) or not obj["object_kind"]:
        raise ValidationError(f"{stable_id} has missing object kind")
    if not isinstance(obj["provenance"], dict) or not obj["provenance"]:
        raise ValidationError(f"{stable_id} has missing provenance")

    revisions = obj["revision_history"]
    if not isinstance(revisions, list) or not revisions:
        raise ValidationError(f"{obj['stable_id']} must have revision_history")
    revision_ids = set()
    for revision in revisions:
        if revision.get("stable_id") != obj["stable_id"]:
            raise ValidationError(f"{obj['stable_id']} revision changes stable identity")
        revision_id = revision.get("revision_id")
        if not revision_id or revision_id in revision_ids:
            raise ValidationError(f"{obj['stable_id']} has missing/duplicate revision_id")
        revision_ids.add(revision_id)

    posture = obj["dependency_posture"]
    if not isinstance(posture, dict) or "state" not in posture or "dependencies" not in posture:
        raise ValidationError(f"{obj['stable_id']} has invalid dependency_posture")

    _validate_no_observational_values(obj)
    _validate_representation_neutrality(obj)


def _validate_claim(objects: dict[str, dict[str, Any]]) -> list[str]:
    claim = objects["claim-gdp-measures-aggregate-economic-output"]
    if claim["object_kind"] != "claim":
        raise ValidationError("claim object has wrong object_kind")

    claim_body = claim.get("claim", {})
    facets = claim_body.get("facets", {})
    for facet_name, allowed_values in ALLOWED_CLAIM_FACETS.items():
        value = facets.get(facet_name)
        if value not in allowed_values:
            raise ValidationError(f"claim facet {facet_name} has invalid value {value!r}")

    referenced_concepts = claim_body.get("referenced_concepts")
    if referenced_concepts != ["concept-gdp", "concept-aggregate-economic-output"]:
        raise ValidationError("claim must reference exactly the two approved concept objects")
    for concept_id in referenced_concepts:
        if objects[concept_id]["object_kind"] != "concept":
            raise ValidationError(f"{concept_id} is not a concept")

    supported_by = claim_body.get("supported_by")
    if supported_by != ["evidence-ref-gdp-source-documentation"]:
        raise ValidationError("claim must be supported by the approved evidence reference")
    if objects["evidence-ref-gdp-source-documentation"]["object_kind"] != "evidence_reference":
        raise ValidationError("evidence reference has wrong object_kind")

    posture = claim["dependency_posture"]
    if posture.get("state") != "dependencies listed":
        raise ValidationError("claim must declare dependency_posture.state as 'dependencies listed'")
    dependencies = posture.get("dependencies")
    if not isinstance(dependencies, list):
        raise ValidationError("claim dependency_posture.dependencies must be a list")
    dependency_ids = [item.get("object_id") for item in dependencies]
    for item in dependencies:
        if not isinstance(item, dict):
            raise ValidationError("claim dependency entry must be an object")
        for field in [
            "object_id",
            "object_kind",
            "dependency_type",
            "necessity",
            "strength",
            "direction",
            "scope",
            "review_propagation_meaning",
        ]:
            if field not in item:
                raise ValidationError(f"claim dependency {item.get('object_id')} missing {field}")
        if item["object_id"] not in objects:
            raise ValidationError(f"claim dependency points to unknown object {item['object_id']}")
        if item["direction"] != "dependent object -> dependency object":
            raise ValidationError(f"claim dependency {item['object_id']} has wrong direction")
    if dependency_ids != REQUIRED_CLAIM_DEPENDENCIES:
        raise ValidationError(f"claim dependencies mismatch: {dependency_ids}")

    if len(claim["revision_history"]) < 2:
        raise ValidationError("claim must contain at least two revisions")

    return dependency_ids


def _validate_evidence_reference(objects: dict[str, dict[str, Any]]) -> None:
    evidence = objects["evidence-ref-gdp-source-documentation"]
    reference = evidence.get("evidence_reference", {})
    if reference.get("owns_observational_data") is not False:
        raise ValidationError("evidence reference must not own observational data")
    if reference.get("observational_data_copied") is not False:
        raise ValidationError("evidence reference must not copy observational data")


def validate_vertical_slice_0(project_root: Path | str | None = None) -> dict[str, Any]:
    root = Path(project_root) if project_root is not None else Path.cwd()
    objects = _load_objects(root)
    object_ids = sorted(objects)
    if object_ids != EXPECTED_OBJECT_IDS:
        raise ValidationError(f"unexpected object ids: {object_ids}")

    for obj in objects.values():
        _validate_kernel(obj)
    claim_dependencies = _validate_claim(objects)
    _validate_evidence_reference(objects)

    return {
        "ok": True,
        "object_count": len(objects),
        "object_ids": object_ids,
        "claim_dependencies": claim_dependencies,
        "representation_neutral": True,
    }


def main() -> int:
    project_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    try:
        result = validate_vertical_slice_0(project_root)
    except ValidationError as exc:
        print(f"vertical_slice_0: FAIL: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
