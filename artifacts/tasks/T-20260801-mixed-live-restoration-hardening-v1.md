# T-20260801 — Mixed-Live Restoration Hardening v1

Status: Completed as an unstaged working-tree correction; publication prohibited
Owner: exclusive Hermes session
Classification: bounded governance/tooling correction; no production, schema or architecture redesign
Decision: `artifacts/decisions/D-20260801-mixed-live-restoration-hardening-v1.md`
Report: `artifacts/reports/R-20260801-mixed-live-restoration-hardening-v1.md`

## Objective

Correct the late-snapshot defect in Publication Authority Hardening v1 without absorbing unrelated repository residue, staging files or publishing.

## Protected baseline

- Parent HEAD: `4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3`.
- Index: empty before mutation.
- Eight mixed live originals recovered and retained under `/home/mkkto/srv/EIP/recovery/KnowledgeForge/mixed-originals-4de0fcc-v1/`.
- Protected-original aggregate fingerprint: `sha256:65b021ab0474f48d9d897bdfc2b1b4d904055c3a1ae71702bba953d1178a03ab`.
- Exact unrelated Git-visible and ignored populations were frozen before restoration/application.
- Task path authority: `/tmp/knowledgeforge-mixed-restoration-hardening-4de0fcc-v1/task_allowlist.json`.

## Implemented correction

1. Restored all eight mixed live paths to authenticated original bytes and exact filesystem modes before applying task-owned complete files.
2. Required independent original-evidence manifest/root inputs for snapshot, gate and gate verification APIs and CLI commands.
3. Bound independent original evidence, protected snapshot, current live identities and candidate identities separately.
4. Copied protected snapshot bytes from retained original evidence rather than mutable live pathnames.
5. Added late-capture, M=1 overwrite, mid-copy mutation, population/mode/hash tampering and missing-evidence regression coverage.
6. Updated the accepted production-boundary contract rather than adding a parallel authority mechanism.

## Verification

- Isolated and live focused authority suites: 54/54 passed.
- Full repository discovery (`python3 -B -m unittest discover -s tests -v`): 488/488 passed in 40.812 seconds.
- Python compileall: passed.
- Independent correctness rereview: stated late-snapshot defect addressed; no correctness finding under the documented original-evidence trust model; one low test-adequacy finding corrected with synchronized mid-copy mutation coverage.
- Architecture-to-Reality Audit: 0 blocks, 0 warnings; generated report was restored to its exact pre-task identity after retaining the task run log externally.
- Coherence/context health: 0 blocks and two pre-existing/non-task warnings (architecture state approaching its limit; stale generated `active_context.md`).
- Exact preservation: 496 frozen unrelated identities matched; 0 mismatches. All eight authenticated protected originals match recovery hashes, sizes and filesystem modes. Final HEAD and `origin/main` both remain `4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3`, ahead/behind is 0/0 and the Git index is empty.

## Completion conditions

- Apply only allowlisted complete hardening and closeout paths.
- Preserve all restored mixed originals and unrelated residue exactly.
- Keep the Git index empty.
- Run focused and full verification plus ProjectForge coherence/audit checks.
- Report publication blockers without staging or activating follow-on work.
