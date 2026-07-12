# D-20260712 Pearson Candidate Policy v2 Consistency Correction

Date: 2026-07-12
Status: accepted

## Decision
Select disposition B: first-difference Pearson method validation should precede further raw Pearson production.

The corrected v2 policy machinery is valid for future coefficient-free raw-Pearson candidate eligibility, but the prior reported dry-run was not valid future-production evidence because it mixed historical comparison with post-Campaign-41 production eligibility.

## Corrections accepted
1. Historical comparison output must be labeled as historical/audit output, not a future candidate batch.
2. Future-production eligibility must exclude all currently canonical Pearson relationships from `knowledge_repository/objects/`, including reversed pairs under the same entity/scope/transformation.
3. Remote-share arithmetic is percentage-based on the actual selected batch size: `floor(n * 0.25)`. No upward rounding is allowed when it would exceed the declared cap.
4. The corrected future-production dry-run over the retained 16-series pool leaves only 4 selected candidates, all high time-risk. It is not sufficient evidence for a useful raw Campaign 42 registry.

## Evidence
- The original v2 dry-run included 4 already canonical Campaign 41 relationships because the helper's exclusion inventory was static through Campaign 40.
- The original v2 dry-run had 2 remote candidates among 7 selected candidates, a 28.5714% remote share; validation compared against nominal 8-candidate capacity instead of actual selected size.
- Corrected future-production mode selected 4 candidates: 3 close and 1 remote; all are high time-risk.
- Existing 21-object evidence shows 14/14 numerically diagnosed Pearson objects are high time-risk and 5 strong raw relationships have weak first-difference diagnostics.

## Method sequencing consequence
Do not freeze Campaign 42 now. The next bounded task should validate a first-difference Pearson companion method contract before another raw batch. This is a narrow method-boundary validation, not a broad transformation framework.

## Architecture classification
Roadmap/policy correction inside existing architecture. No Doctrine amendment, KnowledgeObjectPackage redesign, PostgreSQL schema change, canonical mutation, Campaign 42 registry, coefficient calculation, package publication, commit, or push.
