# D-20260712 Campaign 42 Coefficient-Free First-Difference Pearson Companion Registry

Date: 2026-07-12
Status: accepted

## Decision

A. Registry frozen and ready for separately authorized Campaign 42 companion production.

## Context

The previously validated method contract `wdi_annual_scalar_first_difference_pearson_v1@1.0` required a coefficient-free companion-production registry before any Campaign 42 calculation or publication.

## Accepted contracts

- Transformation: `wdi_annual_scalar_first_difference_v1@1.0`
- Transformation fingerprint: `sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f`
- Method: `wdi_annual_scalar_first_difference_pearson_v1@1.0`
- Method fingerprint: `sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade`
- Validation registry fingerprint: `sha256:5954ecc7b6322efe42a0246d3023b5ab28caa05ee76d8258773391f846188657`

## Frozen outputs

- Registry fingerprint: `sha256:be7a085b5a74860c9a6c95fb2c9e6f45a066679d317fc743694959d502e3dc15`
- Specification fingerprint: `sha256:ec3eaf0f735a888bc01f9cf394f015dd87eab3096be2690e75de0c4ec6f86d00`
- Candidate count: 8
- Eligible canonical raw Pearson packages: 14 of 21
- Ineligible canonical raw Pearson packages: 7; reason: retained raw evidence fixture missing.

## Justification

The registry is deterministic, coefficient-independent, provenance-complete, evidence-fixture-backed, and compatible with the accepted method. It improves future consumer retrieval of annual-change co-movement knowledge without mutating or superseding raw Pearson packages.

## Boundaries

No coefficients, production transformations, canonical companion packages, repository mutation, PostgreSQL write/rebuild, relationship export execution, Doctrine amendment, schema expansion, local AI, commit, or push occurred.

## Next task

Separately authorize Campaign 42 companion production from the frozen registry/specification.
