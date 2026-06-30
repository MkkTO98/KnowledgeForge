# Decision: KnowledgeForge Vertical Slice 0 Refined Design

Date: 2026-06-30
Status: Superseded by `D-20260630-vertical-slice-0-final-dependency-refinement.md`
Implementation status: Design only; no runtime implementation introduced
Supersedes: `D-20260630-vertical-slice-0-design.md` one-object proposal

## Decision

Refine Vertical Slice 0 from a single durable claim object to a minimal durable knowledge object ecosystem.

The refined slice should contain exactly five durable objects:

1. `concept-gdp`
2. `concept-aggregate-economic-output`
3. `claim-gdp-measures-aggregate-economic-output`
4. `evidence-ref-gdp-source-documentation`
5. `dependency-claim-gdp-measures-output-to-concepts-and-evidence`

Revision history remains required, but it should be embedded inside durable objects rather than represented as a separate durable object in Slice 0.

## Rationale

The prior one-claim design was too narrow. It validated object serialization and parts of the durable-object kernel, but it did not adequately validate interactions between KnowledgeForge's architectural primitives.

The refined five-object ecosystem validates:

- concepts as durable identities rather than inline text;
- claims as first-class assertions over durable concepts;
- evidence references as distinct from claims and observational data;
- dependency declarations as semantic dependency records rather than graph edges;
- revision history as part of stable durable objects;
- representation neutrality across the object ecosystem.

## Explicitly included

### Two concepts

Two concepts are the minimum needed to validate a claim connecting durable meanings without introducing relationship representations or graph traversal.

### One claim

A claim is required because KnowledgeForge is claim-first. Concepts alone would reduce the slice to a concept catalog.

### One evidence reference

An evidence reference is required to validate provenance and the MacroForge boundary principle: KnowledgeForge references evidence but does not duplicate observational data.

### One dependency declaration

A dependency declaration is required because references alone do not validate dependency type, necessity, direction, scope, strength, or review-propagation meaning.

### Embedded revision history

Revision history validates stable identity across object changes without introducing event sourcing or transaction infrastructure.

## Explicitly excluded

The refined slice excludes:

- relationship representation;
- mapping object;
- evidence evaluation object;
- methodology object;
- context/regime object;
- knowledge change object;
- separate revision object;
- confidence object or engine;
- lifecycle automation;
- ontology/vocabulary manager;
- graph traversal;
- database/API/infrastructure choices.

These are valid later concerns but not necessary for Vertical Slice 0.

## Implementation boundary

This decision does not authorize implementation by itself. It records the refined design.

Implementation may begin only after this refined design is accepted and should remain limited to the five-object ecosystem, minimal deterministic validation, one end-to-end test, and an implementation-evidence report.

## Reference

Detailed refined design:

- `docs/vertical_slice_0_implementation_design.md`
