# PostgreSQL Acceptance and Production-Sequencing Report

Date: 2026-07-10
Status: decision gate complete

## Executive conclusion

PostgreSQL v1 is accepted as complete.

The next production direction is not Campaign 34 and not ordinary WDI breadth expansion. The repository should move toward deeper reusable deterministic knowledge only after the existing evidence-input boundary is operationalized for one bounded objective numerical evidence extract.

Decision outcome: **PostgreSQL accepted; an existing evidence-input boundary must first be operationalized.**

## Part 1 — PostgreSQL v1 acceptance

The acceptance gate re-ran targeted verification rather than repeating the full implementation exercise.

### Verified state

- Database exists: `knowledgeforge`.
- Database owner: `mkkto`.
- Projection schema: `knowledgeforge_projection`.
- Canonical packages: `521`.
- Projected packages: `521`.
- Missing projected package IDs: `0`.
- Extra projected package IDs: `0`.
- Package fingerprint failures: `0`.
- Payload fidelity failures: `0`.
- Repository fingerprint: `sha256:9c7ebb9cc47f3dc58a06828fa334e53473b59f563845b1c64343840ee7a9479c`.
- Logical projection fingerprint: `sha256:b0e7f2f80c1dc22ab04d556eed834b05e94fb9bdc1b3b96e249ecd51e474e2c7`.
- Stale-projection probe: failed closed with `stale_or_invalid_projection`.
- Canonical package byte hashes: unchanged.
- MacroForge schema probe: no `knowledgeforge_projection` schema in `macroforge`.
- Campaign 34 file probe: absent.

### Acceptance result

**A. Accept the PostgreSQL operational projection as v1-complete.**

No bounded remediation is required for v1 acceptance.

### Security classification

Current database-level isolation is sufficient for local single-user operation. Both `knowledgeforge` and `macroforge` databases are owned by PostgreSQL role `mkkto`; this is not strong role-level isolation. Stronger role separation should be treated as a future deployment/security concern, not a blocker, because no actual unauthorized cross-database behaviour was discovered.

## Part 2 — Evidence availability audit

### What objective evidence is physically available now?

KnowledgeForge physically has:

- canonical `KnowledgeObjectPackage` JSON files;
- repository manifest, indexes, and evolution records;
- production campaign source snapshots;
- generated production reports;
- source URLs, raw artifact URL/hash metadata, release keys, WDI last-updated metadata where campaigns captured them;
- aggregate observed/missing counts and shares;
- indicator/family/scope classifications;
- provenance and lineage metadata;
- deterministic campaign scripts that can regenerate current aggregate artifacts.

### Does KnowledgeForge retain observation-level numerical evidence?

No material observation-level numerical evidence store was found.

The retained snapshots are primarily source-evidence snapshots, aggregate counts/shares, metadata, provenance handles, family inventories, and evidence-quality measurements. They are objective and useful, but they are not enough to compute genuine statistical summaries, correlations, covariance structures, lag relationships, or trend descriptors over source observations.

### Can existing campaigns be deterministically rerun?

Yes, existing campaign scripts can be rerun deterministically to regenerate their current retained artifacts. The scripts are not evidence that KnowledgeForge can currently reacquire full observation-level numerical data independently.

### Are source snapshots immutable or reproducibly identifiable?

Yes for retained JSON snapshots and package references: snapshots have file hashes/fingerprints, and many source snapshots retain raw artifact URL/hash/release metadata. This supports provenance and auditability but does not equal local observation-level evidence availability.

### Is historical evidence locally preserved?

Yes, but mainly as campaign artifacts, aggregate source snapshots, metadata, and package references. Historical full observation values are not locally preserved as KnowledgeForge-owned source evidence.

### Which mature family has enough actual evidence for a deeper pilot?

None currently has enough locally accessible observation-level numerical evidence for a genuine deeper numerical pilot.

Mature WDI annual-scalar families have enough metadata/provenance/coverage evidence to support evidence-quality, coverage, classification, and provenance knowledge. They do not currently provide the local numerical observation values required for statistical summaries/trends/correlations.

### Would statistical knowledge require reading MacroForge today?

If KnowledgeForge used the only known local observation store, it would likely need MacroForge's private database or implementation. That would violate current KnowledgeForge independence if done directly.

KnowledgeForge may consume independently acquired objective evidence or an explicitly accepted neutral evidence transfer. It must not share MacroForge schemas, import MacroForge runtime code, depend on MacroForge internal tables, or treat MacroForge's database as its own evidence store.

### Existing evidence-input boundary

The accepted architecture already provides the correct boundary. External evidence systems or sources may provide immutable exports/snapshots, reproducibility handles, source metadata, dataset/series references, release/vintage references, and source documentation references. KnowledgeForge may store references and small immutable snapshots where justified by reproducibility; it must not copy full external observational datasets as owned KnowledgeForge data.

Therefore no new architecture is needed. The boundary needs operationalization for one bounded numerical evidence fixture.

## Candidate pilot comparison

| Candidate | Evidence currently accessible? | Assessment |
| --- | --- | --- |
| Statistical summary | No | Best first future pilot after evidence-input fixture; shallow, deterministic, reusable, low interpretation risk. |
| Trend descriptor | No | Useful later, but needs stronger time-series missingness/window rules and carries more interpretation risk. |
| Correlation | No | Premature; requires aligned paired observations and stronger safeguards against explanation/causality misuse. |
| Covariance structure | No | Premature; requires multi-variable aligned matrix and has low first-pilot value. |
| Lag relationship | No | Defer; high forecast/causality confusion risk and requires deeper temporal evidence. |
| Deterministic mathematical relationship | Partially for source documentation, not numerical validation | Compatible but not the cleanest test of numerical evidence access. |

Machine-readable candidate detail: `candidate_pilot_comparison.json`.

## Selected sequencing outcome

**PostgreSQL accepted; an existing evidence-input boundary must first be operationalized.**

The next bounded task should be a design/validation gate for one neutral WDI annual-scalar observation evidence input fixture and a later statistical-summary pilot. It should not be a production campaign implementation.

## Taxonomy and semantic-recurrence follow-up

### Why `other_reusable_deterministic_deductions` primary count is 42 while overlap flag count is 0

The non-overlapping primary classifier and overlapping flag classifier answer different questions. The primary classifier assigns one residual primary type after precedence rules. The overlap classifier emits `other_reusable_deterministic_deductions` only when no other flag is found.

Thus the 42 primary residual objects are mostly method-scoped negative/residual deductions that also trigger other positive category flags such as coverage, structural descriptor, provenance, or deterministic-derived. Because they trigger another overlap flag, the residual overlap flag remains zero.

This is a taxonomy measurement ambiguity, not a repository-quality blocker.

### Semantic recurrence groups

The five normalized semantic recurrence groups are legitimate family-scoped templating/recurrence patterns:

- architectural continuity review;
- required lineage fields;
- territory scope;
- replication contract;
- maturation methodology comparison.

Current follow-up found no duplicate package IDs, duplicate statement IDs, duplicate package fingerprints, or exact duplicate statement texts. The recurrence groups indicate low-variety production templating and composition concentration, but they do not materially undermine repository composition measurements or package meaning.

They do not block the next evidence-input boundary task.

## Final decision

Proceed next to the bounded evidence-input boundary operationalization task.

Do not begin Campaign 34 until that gate determines whether objective numerical evidence is available in a compliant, reproducible, KnowledgeForge-independent form.
