# Intelligence-Routing Assessment

Date: 2026-07-09
Status: complete
Scope: generation-method assessment only; no production generation

## Routing principle

KnowledgeForge should route work to the lowest intelligence level that can produce a reproducible, auditable, validator-passable package.

Allowed routing levels:

1. deterministic computation only;
2. deterministic + templates;
3. deterministic + local AI;
4. local AI only;
5. frontier LLM required.

Audit conclusion: no audited first-production category requires frontier LLMs. Most categories require deterministic computation only or deterministic computation plus governed templates.

## Routing matrix

| Knowledge category | Lowest sufficient routing | Justification | Frontier LLM justified? |
|---|---|---|---|
| Evidence inventory | Deterministic + templates | Counts, source identities, table/query outputs, and artifact handles are deterministic. Templates can render package statements. | No. |
| Source identity packages | Deterministic + templates | `meta.source`, dataset releases, URLs, and license notes are structured. | No. |
| Canonical observation reference packages | Deterministic + templates | Fact/dimension IDs and source/release/run references can be assembled mechanically. | No. |
| Raw artifact provenance summaries | Deterministic computation only | Artifact manifest hashes, URLs, bytes, row counts, and source metadata are structured. | No. |
| Query fingerprinting | Deterministic computation only | Normalize SQL/structured query specs and hash them. | No. |
| Missingness summaries | Deterministic computation only | `observation_status` and expected/observed row counts are computable from PostgreSQL and manifests. | No. |
| Evidence quality summaries | Deterministic + templates | Quality checks, hash presence, lineage completeness, and freshness fields are structured. Templates suffice for text. | No. |
| Demographic age-sex cohort structural packages | Deterministic + templates | Indicator-code patterns and audited campaign scope define cohort family. Human-reviewed template avoids interpretation. | No. |
| Indicator-family classification | Deterministic + templates initially; deterministic + local AI later for draft suggestions only | Existing WDI source codes and indicator names support rule/table classification. Local AI may propose draft mappings in future, but accepted mappings should be deterministic/reviewed. | No. |
| Derived metrics with explicit formulas | Deterministic computation only | Formulas such as exports - imports, observed-year count, missingness rate, endpoint arithmetic change are deterministic. | No. |
| Statistical characterization | Deterministic computation only | Quantiles, ranks, descriptive statistics, correlations, and coverage metrics are mechanical if method-scoped and non-interpretive. | No. |
| Methodological/source-behavior knowledge | Deterministic + templates | Source behavior can be recorded from manifests, runbooks, and audited architecture. Human review may be needed for precise wording. | No. |
| Negative knowledge | Deterministic + templates with human review | Absence claims must be scoped to audited repository/evidence. They can be produced from table/source/provider inventory plus templates. | No. |
| Cross-country descriptive comparisons | Deterministic computation only | Same-indicator same-period comparisons are mechanical. Boundary validator must reject evaluative language. | No. |
| Cross-time descriptive summaries | Deterministic computation only | Window, endpoint, monotonicity, and missingness summaries are algorithmic. | No. |
| Contradiction detection within current WDI PostgreSQL | Deterministic + templates, limited scope | Current WDI-only repository has limited contradiction surface. Contradictions are mostly missingness/scope conflicts unless multiple sources or vintages are added. | No. |
| Cross-provider contradiction/evidence evaluation | Defer; likely deterministic + templates after source audits | Current audited PostgreSQL is WDI-only. Broader artifacts are not enough for production contradiction packages. | No current frontier need; defer. |
| Natural-language explanatory synthesis | Disallowed or defer | Explanation drifts into InsightForge unless preserving external source claims. | Frontier LLM not justified because output is outside first campaign scope. |

## Local AI opportunities

Local AI may later be useful for:

- proposing indicator-family labels from WDI indicator names;
- drafting candidate statement text from deterministic package fields;
- spotting possible duplicate/overlapping wording in generated templates;
- summarizing source documentation into GeneratedIntermediatePackage candidates.

Local AI must not be acceptance authority. Every local-model output would need:

- prompt/template fingerprint;
- model identifier/checksum;
- decoding parameters;
- retained output artifact hash;
- deterministic validator pass;
- human/governance review where used for accepted knowledge.

## Frontier LLM assessment

No frontier LLM use is justified for the first production campaign because:

- all required evidence exists in structured PostgreSQL rows, manifests, or project artifacts;
- package statements should be constrained and template-generated;
- knowledge opportunities are descriptive, structural, and method-scoped;
- economic interpretation is explicitly forbidden;
- frontier LLM output would increase audit burden without improving correctness.

Possible future frontier use cases are limited to high-ambiguity architecture review or source-document interpretation after deterministic/local methods fail. Even then, frontier output would remain candidate material only.

## Routing conclusion

First campaign routing should be:

```text
PostgreSQL/read-only artifact queries
-> deterministic metrics/fingerprints
-> governed text templates
-> v1 validation
-> human/governance review
```

No local AI or frontier LLM should be in the first production path.
