# T-20260712 Durability-Destination Decision and Pre-Staging Remediation

Status: completed
Date: 2026-07-12

## Objective

Make a bounded durability-destination decision for KnowledgeForge recovery-critical artifacts and prepare a safe pre-staging remediation plan without staging, committing, pushing, deleting, resetting, cleaning, checking out, restoring, reverting, mutating canonical packages, writing production PostgreSQL, or modifying MacroForge/InsightForge.

## Scope executed

- Verified prior durability report, closeout addendum, inventory, commit plan, sensitive findings, and current git state.
- Revalidated current inventory using the repository-wide durability validator.
- Corrected validator staged-state parsing so `??` untracked files are not counted as staged.
- Classified every required recovery-critical artifact class by primary durability treatment.
- Produced a reviewed sensitive/local-path findings ledger without reproducing secret values.
- Parameterized/remediated active host-specific absolute path dependencies in source/test/config/manifest metadata.
- Produced staged-state inventory, dependency-aware durability plan, updated validator output, and final decision report.

## Deliverables

Directory: `artifacts/reports/durability-destination-decision-pre-staging-remediation-20260712/`

Key files:
- `durability_destination_decision.md`
- `artifact_class_policy.json`
- `sensitive_local_path_findings_ledger.json`
- `staged_state_inventory.json`
- `updated_dependency_aware_durability_plan.json`
- `repository_wide_validator.json`
- `consolidated_machine_readable_summary.json`

Decision artifact:
- `artifacts/decisions/D-20260712-durability-destination-policy-and-pre-staging-remediation.md`

## Result

Decision: B — durability policy is complete and sensitive/local-path review is clean, but operational backup/checkpointing destination still requires approval and implementation. The validator remains failing because canonical/recovery-critical implementation files are untracked/local-only and mutable operational state lacks a backup destination.

## Boundaries maintained

No staging, unstaging, commit, push, deletion, reset, clean, checkout, restore, revert, production PostgreSQL write, canonical package mutation, isolated database deletion, Campaign 41, MacroForge modification, or InsightForge modification was performed.

## Verification

- `uvx --from pytest pytest tests/test_knowledge_repository.py tests/test_external_outbox_polling_supersession_v1.py -q` -> 11 passed.
- `python3 -m py_compile tools/repository_wide_durability_validator.py tools/knowledge_repository.py tools/external_outbox_poller_v1.py tools/macroforge_neutral_release_adapter_v1.py tests/test_external_outbox_polling_supersession_v1.py` -> passed.
- `python3 tools/repository_wide_durability_validator.py --report artifacts/reports/durability-destination-decision-pre-staging-remediation-20260712` -> valid false with expected blocks.

## Remaining blocker

Authorize the smallest next step: implement/approve operational backup/checkpoint destination for mutable registries and PostgreSQL operational backup policy, then rerun validator before any staging request.
