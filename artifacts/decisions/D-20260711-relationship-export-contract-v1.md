# D-20260711 — Relationship Export Contract v1 Accepted

Decision: **A. Read-only export contract validated; independent consumption is operationally proven.**

PostgreSQL indexing decision: **A. Current PostgreSQL v1 is adequate; defer correlation-specific indexing.**

Next strategic direction: **Continue operational Pearson production toward 100 objects.**

Rationale: The local CLI/file export provides deterministic relationship snapshots, freshness validation, payload/fingerprint validation, stable ordering, query/result fingerprints, and independent consumer verification without direct consumer PostgreSQL access, shared runtime code, filesystem coupling, schema ownership, writes, or InsightForge implementation.

Constraints preserved: canonical KnowledgeObjectPackages remain authoritative; PostgreSQL remains a KnowledgeForge-owned projection; the export is not a second canonical representation; no schema/index expansion is currently justified.
