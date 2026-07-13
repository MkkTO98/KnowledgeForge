import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "operational_state_checkpoint.py"


def load_tool():
    spec = importlib.util.spec_from_file_location("operational_state_checkpoint", TOOL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["operational_state_checkpoint"] = module
    spec.loader.exec_module(module)
    return module


osc = load_tool()


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def base_config(tmp_path: Path, protected_path: str = "state") -> Path:
    config = {
        "contract_version": "knowledgeforge.protected_state.v1",
        "protected_paths": [{"path": protected_path, "class": "test_state", "required": True}],
        "sensitive_exclusions": {
            "path_globs": [".env", "**/.env", "**/*secret*"],
            "content_regexes": ["-----BEGIN [A-Z ]*PRIVATE KEY-----", "postgres(?:ql)?://[^\\s'\\\"]+"],
        },
        "postgresql_operational_recovery": {
            "mode": "reconstruction_evidence",
            "projection_tool": "tools/postgresql_operational_projection.py",
            "projection_config_example": "docs/postgresql_projection_config.example",
            "canonical_source": "knowledge_repository",
            "production_database_write_allowed": False,
            "backup_dump_destination_configured": False,
            "machine_loss_durable": False,
        },
        "durability_destination": {
            "type": "same_host_local_checkpoint",
            "tested_local_only": True,
            "machine_loss_durable": False,
            "external_destination_configured": False,
        },
    }
    path = tmp_path / "protected_state_test.json"
    write_json(path, config)
    return path


class OperationalStateCheckpointTests(unittest.TestCase):
    def test_create_validate_restore_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = base_config(tmp_path)
            result = osc.create_checkpoint(config, tmp_path / "checkpoints", "unit-test")
            checkpoint = tmp_path / result["checkpoint_path"] if not Path(result["checkpoint_path"]).is_absolute() else Path(result["checkpoint_path"])
            # create_checkpoint reports repo-relative when destination is inside repo; for tmp paths use direct destination.
            checkpoint = tmp_path / "checkpoints" / "unit-test"

            validation = osc.validate_checkpoint(checkpoint)
            self.assertIs(validation["valid"], True)
            self.assertIs(validation["tested_local_only"], True)
            self.assertIs(validation["machine_loss_durable"], False)
            self.assertIs(validation["postgresql_reconstruction_evidence_present"], True)

            restore_root = tmp_path / "isolated_restore"
            report = osc.restore_checkpoint(checkpoint, restore_root)
            self.assertIs(report["valid"], True)
            self.assertGreater(report["restored_file_count"], 0)
            self.assertTrue((restore_root / "restore_validation.json").exists())
            self.assertTrue((restore_root / "state" / "active_goal.md").exists())

    def test_sensitive_paths_are_excluded(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "repo" / "protected"
            source.mkdir(parents=True)
            (source / "safe.json").write_text('{"ok": true}\n')
            (source / "contains_secret.txt").write_text("do not copy\n")
            (source / "db.txt").write_text("postgres" + "ql://user:***@example/db\n")

            config_data = json.loads(base_config(tmp_path, "protected").read_text())
            config = tmp_path / "repo" / "config.json"
            write_json(config, config_data)
            with mock.patch.object(osc, "ROOT", tmp_path / "repo"):
                result = osc.create_checkpoint(config, tmp_path / "checkpoints", "sensitive-test")

            skipped = result["manifest"]["skipped"]
            copied = [f["path"] for f in result["manifest"]["files"]]
            self.assertIn("protected/safe.json", copied)
            self.assertTrue(any(item["path"] == "protected/contains_secret.txt" and item["reason"] == "sensitive_path_exclusion" for item in skipped))
            self.assertTrue(any(item["path"] == "protected/db.txt" and item["reason"] == "sensitive_content_exclusion" for item in skipped))

    def test_validate_fails_on_missing_checkpoint_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = base_config(tmp_path)
            osc.create_checkpoint(config, tmp_path / "checkpoints", "missing-file-test")
            checkpoint = tmp_path / "checkpoints" / "missing-file-test"
            target = next((checkpoint / "files").rglob("*"))
            while target.is_dir():
                target = next(target.rglob("*"))
            target.unlink()
            validation = osc.validate_checkpoint(checkpoint)
            self.assertIs(validation["valid"], False)
            self.assertTrue(any(isinstance(e, dict) and e["error"] == "checkpoint_file_missing" for e in validation["errors"]))

    def test_validate_fails_on_hash_tamper(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = base_config(tmp_path)
            osc.create_checkpoint(config, tmp_path / "checkpoints", "tamper-test")
            checkpoint = tmp_path / "checkpoints" / "tamper-test"
            target = next(p for p in (checkpoint / "files").rglob("*") if p.is_file())
            target.write_text("tampered\n")
            validation = osc.validate_checkpoint(checkpoint)
            self.assertIs(validation["valid"], False)
            self.assertTrue(any(isinstance(e, dict) and e["error"] == "sha256_mismatch" for e in validation["errors"]))

    def test_restore_refuses_invalid_checkpoint(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = base_config(tmp_path)
            osc.create_checkpoint(config, tmp_path / "checkpoints", "invalid-restore-test")
            checkpoint = tmp_path / "checkpoints" / "invalid-restore-test"
            target = next(p for p in (checkpoint / "files").rglob("*") if p.is_file())
            target.write_text("tampered\n")
            with self.assertRaises(osc.CheckpointError):
                osc.restore_checkpoint(checkpoint, tmp_path / "restore")

    def test_required_protected_path_missing_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = base_config(tmp_path, "does-not-exist")
            with self.assertRaises(osc.CheckpointError):
                osc.create_checkpoint(config, tmp_path / "checkpoints", "missing-required")


if __name__ == "__main__":
    unittest.main()
