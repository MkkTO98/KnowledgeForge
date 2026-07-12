# T-20260711 Repository-Wide Durability Inventory and Production Supersession-Code Correction

Status: complete
Decision: D — canonical/recovery-critical state remains locally vulnerable; staging not authorized/requested.

## Outcome

Corrected reusable supersession-related code paths that could mutate existing canonical package bytes, completed repository-wide durability inventory, machine-loss recovery analysis, artifact policy, size/storage assessment, sensitive scan, repository-wide validator, commit plan, and isolated database cleanup assessment.

## Main artifacts

- `tools/external_outbox_poller_v1.py`
- `tools/knowledge_repository.py`
- `tools/repository_wide_durability_validator.py`
- `tests/test_external_outbox_polling_supersession_v1.py`
- `tests/test_knowledge_repository.py`
- `artifacts/reports/repository-wide-durability-inventory-supersession-correction-20260711/`

## Boundary

No production canonical packages changed. No production PostgreSQL writes. No staging, commit, push, deletion, reset, clean, checkout, revert, Campaign 41, scheduler installation, MacroForge modification, or InsightForge modification.

## Verification

- Supersession regression tests: 14 passed.
- Full test suite: 266 passed.
- Canonical repository validation: 538/538 objects; no missing/extra packages.
- Repository-wide durability validator: failed as expected due untracked canonical/recovery-critical files and sensitive/local-path review blockers.
- Coherence/context health/architecture audit: no blocks.

## Next action

Authorize a durability-destination decision for recovery-critical untracked material before staging is reconsidered.
