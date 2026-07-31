from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ara", ROOT / "tools" / "architecture_reality_audit.py")
ara = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(ara)

AUDIT_REL = "artifacts/reports/R-20260731-architecture-reality-audit.md"
SUMMARY_REL = "artifacts/reports/_SUMMARY.md"


def fixture(root: Path) -> list[str]:
    for rel, text in [("docs/contract.md", "contract\n"), ("tools/architecture_reality_audit.py", "print('ok')\n"), (SUMMARY_REL, "# Reports\n")]:
        path = root / rel; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text)
    return ["docs/contract.md", "tools/architecture_reality_audit.py"]


def subject(root: Path):
    return ara.build_audit_subject_manifest(root, fixture(root), parent_head="a" * 40, repository_fingerprint="sha256:" + "b" * 64, exclusions=[
        {"path": AUDIT_REL, "reason": "audit output depends on audit generation"},
        {"path": SUMMARY_REL, "reason": "generated reports summary must list audit output"},
    ])


def write_attested_audit(root: Path, value: dict) -> Path:
    path = root / AUDIT_REL; path.parent.mkdir(parents=True, exist_ok=True)
    tool_fingerprint = next(row["blob_sha256"] for row in value["subject_paths"] if row["path"] == "tools/architecture_reality_audit.py")
    report = {"project": str(root), "mode": "generated", "timestamp": "2026-07-31T00:00:00+00:00", "audit_categories": [], "drift_types": [], "latest_architecture_reality_audit": None, "completed_tasks_since_latest_audit": 0, "blocks": [], "warnings": [], "attestation": ara.audit_attestation(value, tool_fingerprint, str(root))}
    path.write_text(ara.render_markdown(report))
    return path


class AuditAttestationTests(unittest.TestCase):
    def test_subject_binds_exact_paths_modes_hashes_and_exclusions(self):
        with tempfile.TemporaryDirectory() as td:
            value = subject(Path(td))
            self.assertEqual(value["subject_path_count"], 2)
            self.assertEqual([row["path"] for row in value["subject_paths"]], ["docs/contract.md", "tools/architecture_reality_audit.py"])
            self.assertTrue(ara.verify_audit_subject_manifest(Path(td), value)["valid"])

    def test_audit_and_summary_are_excluded_and_no_other_path_is_allowed(self):
        with tempfile.TemporaryDirectory() as td:
            value = subject(Path(td))
            self.assertEqual([row["path"] for row in value["exclusions"]], [AUDIT_REL, SUMMARY_REL])
            bad = copy.deepcopy(value); bad["exclusions"].append({"path": "docs/contract.md", "reason": "silent"}); bad["subject_manifest_fingerprint"] = ara.audit_subject_fingerprint(bad)
            with self.assertRaises(ValueError): ara.verify_audit_subject_manifest(Path(td), bad)

    def test_temporary_location_does_not_change_subject_identity(self):
        with tempfile.TemporaryDirectory() as a, tempfile.TemporaryDirectory() as b:
            self.assertEqual(subject(Path(a))["subject_manifest_fingerprint"], subject(Path(b))["subject_manifest_fingerprint"])

    def test_changed_blob_changes_identity_and_old_subject_fails(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); value = subject(root); old = value["subject_manifest_fingerprint"]
            (root / "docs/contract.md").write_text("changed\n")
            with self.assertRaises(ValueError): ara.verify_audit_subject_manifest(root, value)
            rebuilt = ara.build_audit_subject_manifest(root, ["docs/contract.md", "tools/architecture_reality_audit.py"], parent_head="a" * 40, repository_fingerprint="sha256:" + "b" * 64, exclusions=value["exclusions"])
            self.assertNotEqual(old, rebuilt["subject_manifest_fingerprint"])

    def test_current_output_cannot_select_itself_as_predecessor(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); reports = root / "artifacts/reports"; reports.mkdir(parents=True)
            old = reports / "R-20260730-architecture-reality-audit.md"; old.write_text("old")
            current = reports / "R-20260731-architecture-reality-audit.md"; current.write_text("current")
            self.assertEqual(ara.latest_architecture_audit(root, exclude=current), old)

    def test_genuine_predecessor_selection_is_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); reports = root / "artifacts/reports"; reports.mkdir(parents=True)
            for date in ["20260701", "20260730", "20260715"]: (reports / f"R-{date}-architecture-reality-audit.md").write_text(date)
            self.assertEqual(ara.latest_architecture_audit(root).name, "R-20260730-architecture-reality-audit.md")

    def test_report_records_stable_attestation_not_only_workspace(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); value = subject(root)
            report = {"project": str(root), "mode": "generated", "timestamp": "2026-07-31T00:00:00+00:00", "audit_categories": [], "drift_types": [], "latest_architecture_reality_audit": None, "completed_tasks_since_latest_audit": 0, "blocks": [], "warnings": [], "attestation": ara.audit_attestation(value, "sha256:" + "c" * 64)}
            rendered = ara.render_markdown(report)
            self.assertIn(value["subject_manifest_fingerprint"], rendered)
            self.assertIn("Parent repository HEAD", rendered)
            self.assertIn("attests the frozen audit subject", rendered)

    def test_final_manifest_contains_exact_subject_audit_and_summary(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); value = subject(root)
            audit = write_attested_audit(root, value)
            summary = root / SUMMARY_REL; summary.write_text(f"# Reports\n- `{Path(AUDIT_REL).name}`\n")
            final = ara.build_final_candidate_manifest(root, [row["path"] for row in value["subject_paths"]] + [AUDIT_REL, SUMMARY_REL], value, AUDIT_REL, SUMMARY_REL)
            self.assertTrue(ara.verify_final_candidate_manifest(root, final, value, AUDIT_REL, SUMMARY_REL)["valid"])

    def test_final_manifest_rejects_duplicate_or_extra_rows(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); value = subject(root); write_attested_audit(root, value)
            (root / SUMMARY_REL).write_text(Path(AUDIT_REL).name)
            paths = [row["path"] for row in value["subject_paths"]] + [AUDIT_REL, SUMMARY_REL]
            final = ara.build_final_candidate_manifest(root, paths, value, AUDIT_REL, SUMMARY_REL)
            duplicate = copy.deepcopy(final); duplicate["paths"].append(copy.deepcopy(duplicate["paths"][0])); duplicate["path_count"] += 1; duplicate["final_manifest_fingerprint"] = ara.final_manifest_fingerprint(duplicate)
            with self.assertRaisesRegex(ValueError, "exact|duplicate|canonical"):
                ara.verify_final_candidate_manifest(root, duplicate, value, AUDIT_REL, SUMMARY_REL)
            extra_path = root / "extra.txt"; extra_path.write_text("extra")
            extra = copy.deepcopy(final); extra["paths"].append({"path": "extra.txt", "mode": "100644", "sha256": ara.byte_fingerprint(extra_path)}); extra["paths"] = sorted(extra["paths"], key=lambda row: row["path"]); extra["path_count"] += 1; extra["final_manifest_fingerprint"] = ara.final_manifest_fingerprint(extra)
            with self.assertRaisesRegex(ValueError, "exact"):
                ara.verify_final_candidate_manifest(root, extra, value, AUDIT_REL, SUMMARY_REL)

    def test_audit_report_tool_identity_must_match_frozen_subject(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); value = subject(root); audit = write_attested_audit(root, value)
            text = audit.read_text(); tool = next(row["blob_sha256"] for row in value["subject_paths"] if row["path"] == "tools/architecture_reality_audit.py")
            audit.write_text(text.replace(tool, "sha256:" + "0" * 64))
            with self.assertRaisesRegex(ValueError, "tool|attestation"):
                ara.verify_audit_report_binding(root, AUDIT_REL, value)

    def test_final_manifest_rejects_missing_or_changed_subject(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); value = subject(root)
            audit = write_attested_audit(root, value)
            summary = root / SUMMARY_REL; summary.write_text(Path(AUDIT_REL).name)
            paths = [row["path"] for row in value["subject_paths"]] + [AUDIT_REL, SUMMARY_REL]
            final = ara.build_final_candidate_manifest(root, paths, value, AUDIT_REL, SUMMARY_REL)
            (root / "tools/architecture_reality_audit.py").write_text("changed")
            with self.assertRaises(ValueError): ara.verify_final_candidate_manifest(root, final, value, AUDIT_REL, SUMMARY_REL)

    def test_subject_and_final_manifest_generation_is_deterministic(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); a = subject(root); b = subject(root); self.assertEqual(a, b)
            audit = write_attested_audit(root, a)
            summary = root / SUMMARY_REL; summary.write_text(Path(AUDIT_REL).name)
            paths = [row["path"] for row in a["subject_paths"]] + [AUDIT_REL, SUMMARY_REL]
            self.assertEqual(ara.build_final_candidate_manifest(root, paths, a, AUDIT_REL, SUMMARY_REL), ara.build_final_candidate_manifest(root, paths, a, AUDIT_REL, SUMMARY_REL))


if __name__ == "__main__":
    unittest.main()
