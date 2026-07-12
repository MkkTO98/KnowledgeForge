# D-20260712 Campaign 43 Companion Package Publication Preflight Accepted

Date: 2026-07-12
Status: accepted for local publication readiness; not published

## Decision

Accept the six Campaign 43 first-difference Pearson companion package candidates as locally validated publication-preflight artifacts.

This decision does not authorize or perform canonical publication, PostgreSQL projection, Relationship Export publication, Git staging, commit, or push.

## Evidence

Inputs matched accepted identities:

- Registry: `sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1`
- Freeze specification: `sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf`
- Calculation result: `sha256:140eb37de9ef29a5363e0c60a6d87591b5ecd1c7538b1818abca75da306e2462`

Constructed candidate package-set fingerprint:

`sha256:9ed161b9dcf7472b7e13979cbd9cd1a24f1ce3009108e677c41dace20277d559`

Safe temporary-repository publication dry run computed:

- expected package count: 560
- expected repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- expected PostgreSQL projected package count: 560
- expected Relationship Export counts: raw Pearson 21; first-difference Pearson 14

## Interpretation boundary

The candidates preserve first-difference coefficients as descriptive finite-window association evidence for annual changes. They explicitly distinguish raw-level and first-difference estimands, state that first differencing discards one observation before missing-value alignment, preserve raw-package non-supersession, and prohibit causal, predictive, structural, significance, independence, investment-signal, or absence-of-relationship claims.

Near-zero and weakened coefficients remain valid robustness/limiting evidence and were not excluded or downgraded. The approximately `0.3855860099` Norwegian coefficient remains descriptive association evidence only.

## Classification

Bounded non-canonical publication preflight. No architecture, doctrine, schema, KnowledgeObjectPackage representation, PostgreSQL schema, or Relationship Export Contract change.

## Remaining condition before publication

Canonical publication remains a separate authorization gate. Publication must add the six candidate package files append-only and mutate only the expected manifest/index/evolution files, then rebuild/verify PostgreSQL and Relationship Export outputs under the existing contracts.
