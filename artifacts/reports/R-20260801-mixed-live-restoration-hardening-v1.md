# R-20260801 — Mixed-Live Restoration Hardening v1

Date: 2026-08-01
Status: Validated unstaged correction; publication prohibited
Task: `artifacts/tasks/T-20260801-mixed-live-restoration-hardening-v1.md`
Decision: `artifacts/decisions/D-20260801-mixed-live-restoration-hardening-v1.md`

## Outcome and classification

This is a bounded governance/tooling correction to the existing publication-authority mechanism. It does not alter Evidence Portfolio production, Knowledge Object semantics, Evidence Bundles, Calculation Campaigns, lifecycle, promotion, PostgreSQL projection or any cross-project contract.

## Defect and correction

The earlier mixed-path snapshot could be taken after candidate bytes had already replaced live originals. Because it authenticated only the then-current live bytes, a late snapshot could misclassify candidate state as preserved original state.

The corrected path requires separately retained independently authenticated original evidence, verifies current live identities against it before capture, copies snapshot bytes from the retained evidence source, verifies live identities again, and revalidates original evidence, protected snapshot, live files and candidate files separately at gate construction and verification. The staging gate now binds the original-evidence fingerprint.

## Preservation evidence

Eight protected originals were restored and verified byte-for-byte, size-for-size and mode-for-mode against `/home/mkkto/srv/EIP/recovery/KnowledgeForge/mixed-originals-4de0fcc-v1/manifest.json`. Aggregate recovery identity: `sha256:65b021ab0474f48d9d897bdfc2b1b4d904055c3a1ae71702bba953d1178a03ab`.

## Independent review

An independent rereview found that the stated late-capture defect is addressed under the documented trust model and reported no correctness defect. It identified one low test-adequacy gap: no synchronized test proved the copy source and post-copy live check. That finding was corrected by a test which observes the retained-evidence descriptor, mutates live state during capture, requires controlled failure and verifies cleanup.

The review also confirmed two explicit trust boundaries: external original evidence must be genuinely retained and authenticated, and path-based checks are not a single atomic filesystem transaction. Those are preserved as operational limitations rather than silently claimed away.

## Verification

- Focused authority suite in isolated workspace and live repository: 54/54 passed.
- Full repository discovery: 488/488 passed in 40.812 seconds.
- Compileall of all changed Python modules: passed.
- Coherence/context health: 0 blocks; two unrelated warnings for the existing `state/architecture.md` size and stale generated `context/active_context.md`.
- Architecture-to-Reality Audit: 0 blocks, 0 warnings. Its existing report was restored byte-for-byte and mode-for-mode after the run; verification output is retained externally at `/tmp/knowledgeforge-mixed-restoration-hardening-4de0fcc-v1/live-architecture-audit-final.log`.
- Preservation: 496 frozen unrelated identities checked with zero mismatches; eight authenticated protected originals matched exact hashes, sizes and filesystem modes.
- Exact allowlisted delta relative to the frozen pre-restoration baseline: 19 paths — eight exact protected-original restorations and eleven hardened complete/closeout files.
- Final Git state: HEAD and `origin/main` both `4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3`, ahead/behind 0/0, staged paths zero.

## Publication disposition

Publication is not authorized by this task. Existing authority, registry and gate identities predate this correction and cannot authorize a changed candidate. Any later publication requires a newly frozen candidate, new source manifests, independent original evidence, a new protected snapshot, rebuilt authority/registry/gate, explicit ownership, immediate pre/post-staging verification and human approval.

No Git index, commit, remote, tag, release, PostgreSQL instance or sibling EIP project was intentionally mutated. No follow-on task was activated.
