# Project State

## Current canonical repository state

- Canonical package count: 560
- Repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- PostgreSQL projection: valid at 560 projected packages
- Relationship Export: 35 relationships, 21 raw Pearson, 14 first-difference Pearson, no raw/first-difference overlap
- Campaign 43: fully closed and pushed before this task

## Current operational/test state

- Repository-wide standard-library unittest discovery is restored.
- `tests/test_operational_state_checkpoint.py` no longer imports or uses pytest.
- `python3 -m unittest tests.test_operational_state_checkpoint -v` passed with 6 tests.
- `python3 -m unittest discover -s tests -v` passed with 336 tests.

## Current selected next step

Open a new post-repair production-readiness decision gate and select exactly one bounded next production or production-enabling task from the documented roadmap/backlog.

## Guardrails

- Do not infer authorization for package production from restored test discovery.
- Do not calculate coefficients, construct or publish packages, mutate PostgreSQL, modify Relationship Export outputs, change doctrine/schema/architecture, clean unrelated residue, stage, commit, push, tag, or release without explicit instruction.
- Preserve local residue including six tracked `architecture/architectureharvest/` deletions, operational/checkpoint/report residue, stale generated context bundles, and Campaign 43 export artifacts modified by prior verification.
