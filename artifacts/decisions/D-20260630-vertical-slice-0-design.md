# Decision: KnowledgeForge Vertical Slice 0 Implementation Design

Date: 2026-06-30
Status: Superseded by `D-20260630-vertical-slice-0-refined-design.md`
Implementation status: Design only; no runtime implementation introduced

## Decision

Adopt a one-object, file-backed claim packet as the proposed Vertical Slice 0 design.

The slice should demonstrate the smallest coherent KnowledgeForge implementation pressure test:

- durable knowledge object;
- stable identity;
- claim representation;
- claim facets;
- durable-object kernel;
- provenance;
- evidence reference without duplicated observational data;
- dependency posture;
- revision capability;
- representation neutrality.

## Selected slice

A single definition-style claim object, preferably:

> GDP measures aggregate economic output.

This claim should be represented as a durable claim object with governed facets, provenance, outward evidence reference, dependency posture, and revision history.

## Why this slice

This slice is sufficient because it tests the architectural kernel without inviting premature implementation of:

- empirical/statistical discovery;
- relationship computation;
- graph traversal;
- ontology management;
- API boundaries;
- database selection;
- lifecycle automation;
- governance workflow automation;
- confidence scoring.

It validates the hardest foundational question: can KnowledgeForge represent governed, versioned reusable knowledge without allowing representation technology to define the architecture?

## Contracts required

Vertical Slice 0 requires only:

1. Durable-object kernel contract.
2. Claim facet vocabulary contract.
3. Dependency posture vocabulary contract.
4. Evidence reference contract.
5. Revision history contract.
6. Representation neutrality contract.

## Rejected first-slice alternatives

### Empirical relationship claim

Rejected for the first slice because it would prematurely force statistical method, evidence-window, confidence, and relationship-representation decisions.

### Concept graph

Rejected because it biases implementation toward graph-first thinking.

### API-backed implementation

Rejected because API mechanics are unnecessary to validate the knowledge model.

### Database-backed implementation

Rejected because database choice should follow implementation pressure, not precede it.

### General ontology manager

Rejected because it is broader than the first validation question.

## Implementation boundary

This decision does not authorize implementation by itself. It records the proposed design and plan.

Implementation may begin only after the design is accepted and should remain limited to the planned Vertical Slice 0 files and tests.

## Reference

Detailed design:

- `docs/vertical_slice_0_implementation_design.md`
