# D-20260712 First-Difference Pearson Method Contract Validation

Date: 2026-07-12
Status: accepted

## Decision

A. `wdi_annual_scalar_first_difference_pearson_v1@1.0` is validated as a deterministic companion relationship method for bounded WDI annual-scalar first-difference Pearson production preparation.

This decision does not authorize canonical production, Campaign 42 execution, package publication, PostgreSQL mutation, export publication, or raw package supersession.

## Method boundary

The method applies the transformation `delta_x_t = x_t - x_(t-1)` to raw annual scalar WDI series before pairwise alignment, labels transformed observations by ending period `t`, refuses to bridge annual gaps, and then calculates Pearson correlation over aligned transformed observations.

## Accepted threshold

For the retained WDI annual-scalar 1990-2024 evidence shape, production-preparation validation accepts:

- minimum aligned transformed observations: 30;
- minimum transformed coverage: 0.85.

This threshold is validated only for the current retained evidence class. Broader evidence classes require revalidation.

## Architectural justification

First-difference Pearson is a distinct deterministic companion method, not a replacement for raw Pearson. It strengthens auditability and provenance by making transformation semantics explicit and independently reproducible while preserving the existing KnowledgeObjectPackage, provenance, PostgreSQL projection, Relationship Export Contract, and repository architecture.

Existing representation is sufficient. No Production Doctrine amendment, package redesign, PostgreSQL schema change, universal transformation framework, local AI, or frontier LLM use is justified.

## Evidence

- Method contract fingerprint: `sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade`
- Transformation contract fingerprint: `sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f`
- Validation registry fingerprint: `sha256:5954ecc7b6322efe42a0246d3023b5ab28caa05ee76d8258773391f846188657`
- Diagnostic reconciliation: 14 compared, 0 mismatches.
- Representation simulation: package, PostgreSQL projection, and Relationship Export Contract compatible without schema expansion.

## Next task

Create a coefficient-free bounded first-difference Pearson companion-production registry for selected existing raw Pearson packages, preserving raw package immutability and stopping before coefficient calculation or canonical package publication.
