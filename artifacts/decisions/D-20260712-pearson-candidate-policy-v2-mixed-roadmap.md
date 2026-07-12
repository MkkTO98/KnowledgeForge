# D-20260712 Pearson Candidate Policy v2 Mixed Roadmap

Date: 2026-07-12
Status: corrected by `D-20260712-pearson-candidate-policy-v2-consistency-correction.md`

## Decision
Accept `pearson_candidate_policy_v2_mixed_roadmap@1.0` as the successor coefficient-free candidate-construction policy for future ordinary raw Pearson registry work.

Disposition: A — successor policy is ready for a bounded Campaign 42 registry task.

This decision does not create or freeze Campaign 42. It authorizes only use of the policy in a later bounded registry-freeze task.

## Evidence
- Accepted predecessor decision: `D-20260712-pearson-path-to-100-mixed-roadmap.md`.
- Campaign 41 selected 8/8 semantically remote candidates and all 8 had high time-risk.
- The 21-object Pearson utility review found 14/14 numeric-diagnostic Pearson objects high time-risk and 5 strong-raw/weak-first-difference cases.
- Dry-run over the retained 16-series Campaign 40 evidence pool produced 7 defensible non-frozen candidates: 3 close, 2 moderate, 2 remote.
- Campaign 41 frozen registry fingerprint remained unchanged: `sha256:e5ff891bdcf3d02eaa028f58538e4c9c00968f8ec74e8871e65bd4160ddc34dc`.
- Campaign 41 batch spec fingerprint remained unchanged: `sha256:a94d020dfedeb2f069366756e2b28fc20906fef5609df823eccae11ad59cdfa2`.

## Rationale
The successor policy preserves coefficient-free construction, overlap/evidence filters, prior relationship exclusions, deterministic ordering, and package-ID uniqueness. It changes only the rules demonstrated insufficient by Campaign 41: semantic proximity is promoted above diversity, remote candidates are capped for ordinary production, time-risk is visible metadata, and raw candidates can carry transformation-companion eligibility before calculation.

## Scope
Permitted:
- semantic-proximity metadata;
- candidate-purpose classification;
- time-risk category from permitted pre-existing inputs;
- batch-composition validation;
- deterministic priority and tie-breaking;
- transformation-companion recommendation metadata;
- provenance for policy decisions.

Not permitted:
- candidate-pair coefficient calculation;
- first-difference/covariance/p-value/significance/lag calculation;
- Campaign 42 registry freeze;
- package mutation;
- PostgreSQL write/rebuild/schema change;
- Doctrine or KnowledgeObjectPackage redesign.

## Non-invalidations
Campaign 41 and historical Pearson campaigns remain valid under their original policy and frozen artifacts. The successor policy is prospective only.

## Next task
Run a bounded Campaign 42 coefficient-free registry-freeze task using `pearson_candidate_policy_v2_mixed_roadmap@1.0`, without calculating coefficients or canonical packages.
