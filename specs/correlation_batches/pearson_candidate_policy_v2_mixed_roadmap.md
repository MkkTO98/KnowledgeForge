# Pearson Candidate Policy v2 — Mixed Roadmap Coefficient-Free Successor

Status: corrected after consistency review; valid as policy machinery, but not sufficient to justify a raw Campaign 42 registry freeze as the next task
Version: `pearson_candidate_policy_v2_mixed_roadmap@1.0-corrected-20260712`
Date: 2026-07-12
Supersedes for future ordinary raw-Pearson candidate construction: Campaign 41 coefficient-free selection policy v1
Does not invalidate: Campaign 41 frozen registry or any canonical package

## Purpose
Define a bounded successor policy for coefficient-free raw Pearson candidate construction after the Campaign 41 assimilation review. The policy preserves the sufficient Campaign 41 rules while correcting the observed weakness that cross-family diversity dominated semantic value and produced 8/8 semantically remote high-time-risk candidates.

This policy is roadmap-level operational policy, not Production Doctrine.

## Preserved rules
The following v1 rules remain sufficient and unchanged:

1. Coefficient-free construction: no candidate-pair Pearson coefficient, first-difference coefficient, covariance, p-value, significance, lag result, or preliminary result cache may be used.
2. Evidence pool boundary: retained validated WDI annual scalar fixtures only unless a later task authorizes a different retained evidence pool.
3. Compatibility filters: same entity, annual frequency, raw transformation for raw Pearson, resolved units, minimum 30 aligned observed annual pairs, and at least 0.85 aligned coverage.
4. Duplicate/self-pair removal.
5. Existing canonical/frozen prior relationship exclusion for same entity/scope/transformation. Future-production mode must derive current canonical Pearson relationship identities from `knowledge_repository/objects/`, not only from a static Campaign 36-40 list. Historical comparison mode may intentionally use the original historical exclusion set, but it must be labeled as audit/comparison output and must not be called future-production evidence.
6. Mechanical exclusion for self-correlations, direct arithmetic identities, direct component-total pressure, near-duplicate indicator definitions, and incompatible transformations.
7. Deterministic canonical pair ordering by family, indicator code, and indicator name.
8. Deterministic tie-breaking by metadata only.
9. Expected package ID uniqueness and collision checks.
10. Frozen historical registry fingerprints remain authoritative for Campaign 41.

## Changed rules and evidence basis

### 1. Semantic proximity becomes primary
Evidence: 21-object review found semantic distribution 12 close, 1 moderate, 8 remote; Campaign 41 selected 8/8 remote candidates and all 8 were high time-risk.

Rule: ordinary production prioritizes:
1. close candidates;
2. moderate candidates with explicit justification;
3. remote candidates only for bounded pressure testing or explicitly designated cautionary knowledge.

Remote candidates are not banned; they must not dominate ordinary raw-Pearson batches.

### 2. Diversity becomes secondary
Evidence: Campaign 41 cross-family diversity validated infrastructure but selected remote high-risk pairs more useful as cautionary/baseline knowledge than positive descriptive knowledge.

Rule: diversity may balance entity, family, and indicator repetition only after semantic proximity, evidence quality, transformation suitability, overlap requirements, and duplicate/mechanical exclusions are satisfied.

### 3. Time-risk stratification becomes visible metadata
Evidence: 14/14 Pearson objects with numeric time diagnostics had high review-only time-risk; 5 objects showed strong raw and weak first-difference behavior.

Rule: each candidate receives a time-risk category: low, moderate, high, or unknown. Unknown remains visible and must not silently become low.

### 4. Transformation-companion eligibility is recorded
Evidence: high-time-risk raw relationships may be reusable mainly as baseline/cautionary knowledge until transformation-aware companions exist.

Rule: a candidate may be tagged as requiring or prioritizing a later transformation-aware companion, but no companion relationship is calculated inside candidate selection.

## Semantic-proximity classification

Allowed evidence fields:
- indicator code;
- indicator name;
- indicator definition;
- measurement concept;
- unit;
- frequency;
- transformation state;
- entity;
- production family;
- numerator/denominator relationship where visible in metadata;
- retained evidence fingerprints;
- period scope.

Forbidden evidence fields:
- candidate-pair Pearson coefficient;
- first-difference coefficient;
- covariance;
- p-values/significance;
- lag results;
- result caches;
- post-calculation acceptance outcomes.

Classes:

### close
Use when indicators share a subject domain, measurement concept, structural relation, production family, or known non-causal descriptive association that makes a raw finite-window descriptor likely reusable. Examples: trade exports/imports shares; birth/death rates; life expectancy/mortality; internet/mobile access; private credit/broad money; land-use shares.

### moderate
Use when indicators are not the same measurement concept but have a plausible shared macro-development, institutional, or infrastructure context that can support a baseline descriptor with explicit limitations.

### remote
Use when indicators are from different production families and no deterministic shared-subject or structural rule applies. Remote does not mean invalid; it means ordinary production should treat the candidate as cautionary or pressure-test evidence.

### unresolved
Use when required metadata is missing, contradictory, or insufficient for deterministic/manual classification. Unresolved candidates require manual review before freeze.

Tie-breaking:
1. explicit accepted pair rule;
2. same production family;
3. accepted bridge rule such as demographic/health population outcomes;
4. unresolved if definitions/units are missing;
5. remote by default.

Manual-review boundary: unresolved classifications, moderate classifications without written justification, and ordinary-batch remote candidates above the share cap require manual review.

Optional local-AI boundary: local AI may advise using metadata only, with coefficients and outcomes excluded. Prompt/output fingerprints must be preserved. Deterministic/manual classification remains authoritative.

Provenance required for every classification:
- policy version;
- evidence field list used;
- rule fired;
- series metadata/fingerprint references;
- classifier mode: deterministic/manual/local-AI-advisory.

## Time-risk input boundary

Permitted coefficient-free inputs:
- already canonical or previously recorded per-series time diagnostics;
- deterministic metadata-based risk flags;
- already retained trend descriptors;
- monotonic/bounded-series metadata where objectively available;
- prior accepted diagnostic artifacts.

Forbidden inputs:
- candidate-pair Pearson coefficient;
- candidate-pair first-difference coefficient;
- covariance;
- p-values/significance;
- lag results;
- preliminary result caches.

If a new per-series time-index diagnostic must be calculated, it is a separate deterministic preprocessing method requiring authorization. It must not be hidden inside candidate selection.

Categories:
- low: permitted pre-existing inputs indicate weak per-series time movement and no objective metadata flag raises risk;
- moderate: permitted inputs indicate material but not dominant time movement or bounded/ratio metadata requires caution;
- high: permitted inputs indicate strong per-series time movement, monotonicity, or prior accepted high-time-risk diagnostics;
- unknown: no permitted input resolves time risk. Unknown remains visible and does not count as low.

## Transformation-companion eligibility

A raw-level candidate should prioritize or require a later transformation-aware companion when:
- time-risk is high or unknown;
- semantic proximity is remote;
- both series are levels, ratios, bounded adoption series, mortality/life-expectancy trend series, or percent-of-GDP/land-area shares likely to embed common time movement;
- the expected consumer use is cautionary or baseline rather than positive descriptive knowledge.

Permitted companion recommendations:
- first differences;
- growth rates;
- percentage changes;
- other already evidenced deterministic transformations.

Required checks before any companion method is validated:
- unit semantics;
- zero/negative-value behavior;
- bounded-ratio behavior;
- missingness after transformation;
- minimum transformed overlap;
- interpretability of transformed values.

This is sequencing metadata only. It does not calculate companion relationships.

## Batch-composition defaults

Roadmap defaults for ordinary raw-Pearson batches:
- prefer a majority of close candidates when available;
- allow moderate candidates after close candidates when each has explicit justification;
- cap remote candidates at no more than 25% of the actual ordinary batch size by default, with integer maximum `floor(n * 0.25)` for actual selected size `n`; do not round upward when that would exceed the declared percentage;
- maximum 3 candidates per entity;
- maximum 3 candidates per family-pair bucket;
- maximum 2 uses of one indicator per entity;
- unknown time-risk candidates remain visible and should not dominate a batch;
- raw baseline candidates are acceptable when paired with explicit limitation and companion eligibility metadata;
- cautionary candidates are acceptable as a bounded minority;
- companion-method candidates should be routed to sequencing evidence rather than treated as proof that raw expansion is enough.

These are evidence-revisable roadmap defaults, not permanent Doctrine quotas.

## Candidate utility statement contract
Every future candidate must include a pre-calculation candidate utility statement with:
- why the relationship is worth canonizing;
- expected descriptive use;
- expected limitation;
- likely consumer use;
- one purpose classification: positive descriptive knowledge, baseline relationship knowledge, cautionary relationship knowledge, transformation-companion candidate, or methodological pressure-test candidate;
- explicit statement that no coefficient or acceptance result is predicted.

## Backward compatibility
Campaign 41 remains governed by `campaign41_coefficient_free_pearson_candidate_registry_v1`. Its frozen registry and batch-spec fingerprints remain unchanged. Historical campaigns are not retroactively judged invalid, and no canonical package is mutated.
