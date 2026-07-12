# D-20260712 Campaign 43 First-Difference Coefficients Calculated Without Publication

Date: 2026-07-12
Status: accepted

## Decision

Accept the Campaign 43 first-difference companion coefficient calculation output as locally verified calculation evidence, not as canonical publication.

The calculated output may be used as input to a separately authorized append-only package construction and publication-preflight task.

## Evidence

The calculation used the frozen Campaign 43 registry and specification:

- Registry fingerprint: `sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1`
- Specification fingerprint: `sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf`
- Calculation result fingerprint: `sha256:140eb37de9ef29a5363e0c60a6d87591b5ecd1c7538b1818abca75da306e2462`

All six candidates were calculated and independently recomputed from retained fixtures.

## Boundary

This decision does not authorize or record canonical package publication.

The task did not:

- construct KnowledgeObjectPackages;
- create package files under `knowledge_repository/objects/`;
- rebuild canonical repository metadata;
- project or mutate PostgreSQL;
- supersede Campaign 41 raw Pearson packages;
- alter Campaign 40-42 packages;
- change Doctrine, package schema, PostgreSQL schema, or Relationship Export Contract.

## Canonical state

Canonical repository state remains unchanged:

- packages: 554
- repository fingerprint: `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`

## Next task

Campaign 43 append-only companion package construction and publication preflight from the verified calculation results, stopping before publication unless publication is explicitly authorized.