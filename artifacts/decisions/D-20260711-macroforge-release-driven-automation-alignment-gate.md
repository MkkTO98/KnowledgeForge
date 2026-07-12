# D-20260711 — MacroForge-Release-Driven Automation Alignment Gate

Decision: KnowledgeForge should adopt a provider-neutral evidence-release contract and file-backed release automation prototype as the next boundary pattern, while rejecting dependence on MacroForge private schemas, MacroForge runtime code, shared database ownership, InsightForge implementation, PostgreSQL schema expansion, or canonical package mutation.

Next slice: implement a file-backed seen-release registry plus release-diff CLI over one real provider-neutral fixture. Continue to avoid MacroForge private access.

Rationale: release-driven automation can improve reproducibility, provenance, incremental recomputation, supersession, and downstream delta export, but only if the boundary object is neutral and KnowledgeForge-owned.
