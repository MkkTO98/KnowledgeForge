# Folder Summary: .

## Purpose
Root of KnowledgeForge, the EIP canonical reusable knowledge substrate project. Current phase: Vertical Slice 0 implemented, verified, and validator-hardened as a minimal four-object file-backed ecosystem with deterministic invariant checks and standard-library unittest coverage.

## Contains
<!-- PROJECTFORGE:BEGIN-CONTAINS -->
- `.gitignore`
- `.gitkeep`
- `AGENTS.md`
- `CONSTITUTION.md`
- `README.md`
- `agents/`
- `architecture/`
- `artifacts/`
- `automation/`
- `confidence/`
- `config/`
- `context/`
- `docs/`
- `hardware/`
- `instructions/`
- `knowledge/`
- `logs/`
- `memory/`
- `metrics/`
- `models/`
- `permissions/`
- `policies/`
- `project.yaml`
- `question_queue/`
- `recovery/`
- `simulation/`
- `skills/`
- `state/`
- `tests/`
- `tools/`
- `workspace_config.yaml`
<!-- PROJECTFORGE:END-CONTAINS -->

## Active Work
- Vertical Slice 0 validator hardening completed: `validate_vertical_slice_0.py` checks core architectural invariants and `test_vertical_slice_0.py` includes negative invariant tests.

## Needs Attention
- Do not add runtime code beyond the accepted Vertical Slice 0 scope; no APIs, databases, graph engines, statistical pipelines, visualization, external services, or deployment.
