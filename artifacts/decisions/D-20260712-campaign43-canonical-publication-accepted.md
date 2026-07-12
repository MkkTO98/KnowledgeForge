# D-20260712 Campaign 43 Canonical Publication Accepted

Date: 2026-07-12
Status: accepted and published locally; Git push pending until final publication step

## Decision

Accept the bounded Campaign 43 canonical publication of exactly six first-difference Pearson companion KnowledgeObjectPackages, plus deterministic Knowledge Repository metadata updates, PostgreSQL projection rebuild, and Relationship Export verification.

## Published canonical result

- canonical package count: 560
- repository fingerprint: `sha256:e69a86bc7574383bc2fbbc9380d9de049d82abcaf35a767019ada98b3a299fb7`
- package-set fingerprint: `sha256:9ed161b9dcf7472b7e13979cbd9cd1a24f1ce3009108e677c41dace20277d559`

The six companion packages were added append-only. Existing canonical package bytes, including Campaign 40-42 packages and Campaign 41 raw source packages, were not changed.

## Operational projection and export evidence

The established KnowledgeForge PostgreSQL projection target was identified as database `knowledgeforge`, schema `knowledgeforge_projection`, with no projection tables in non-KnowledgeForge schemas. Rebuild and verification produced 560 projected packages, no missing or extra package IDs, zero payload-fidelity failures, zero package-fingerprint failures, and the 560-package repository fingerprint.

Relationship Export v1 returned 21 raw Pearson relationships and 14 first-difference Pearson relationships. Raw and first-difference result sets do not overlap. Independent consumer simulation succeeded without requiring campaign numbers, filenames, package IDs known in advance, KnowledgeForge runtime imports, PostgreSQL access, or repository reads.

## Semantic decision

Campaign 43 remains a companion expansion, not a correction or supersession of Campaign 41 raw Pearson packages. Raw-level and first-difference Pearson relationships are separate estimands.

Five transformed coefficients are near zero or weak after differencing and are retained as robustness/limiting evidence. The approximately `0.3855860099` Norwegian nonhydro-renewable-electricity / under-5-mortality result remains descriptive finite-window association evidence only. No causal, predictive, structural, statistical-significance, independence, absence-of-relationship, recommendation, or investment-signal claim is accepted.

## Classification

This is a bounded append-only production publication and projection refresh. It does not change KnowledgeForge architecture, doctrine, schemas, method family, PostgreSQL schema, Relationship Export Contract, or KnowledgeObjectPackage representation.
