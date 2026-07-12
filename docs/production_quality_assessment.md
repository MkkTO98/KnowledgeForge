# Production Quality Assessment Standard

Status: authoritative campaign-reporting standard
Date: 2026-07-09
Scope: all KnowledgeForge production campaigns

## Purpose

Every KnowledgeForge production campaign must produce a production-quality assessment before its outputs are treated as accepted production knowledge.

The assessment is not a presentation report. It is an audit artifact proving whether the campaign preserved determinism, provenance, reproducibility, validator compliance, constitutional boundaries, and package maturity discipline.

## Required campaign counts

Each campaign assessment must record:

- Source Evidence Packages processed;
- KnowledgeCandidatePackages created;
- KnowledgeObjectPackages accepted;
- packages rejected;
- rejected candidates preserved for analysis;
- duplicate knowledge detected;
- ambiguous classifications;
- objects requiring human review.

## Required validation evidence

Each campaign assessment must record validator outcomes by stage:

- Source Evidence Package validation;
- Evidence validation;
- Evidence Evaluation validation;
- KnowledgeCandidatePackage validation;
- KnowledgeObjectPackage validation;
- final constitutional boundary validation.

The assessment must classify validator failures by category, including at minimum:

- constitutional boundary violation;
- evidence contract failure;
- provenance failure;
- reproducibility failure;
- unsupported inference;
- schema/package failure;
- lineage/fingerprint failure;
- maturity/lifecycle failure;
- duplicate knowledge;
- ambiguous classification.

## Required provenance and fingerprint evidence

Each campaign assessment must record:

- source snapshot/package fingerprints;
- input-set fingerprints;
- evidence-reference fingerprints;
- query/selection fingerprints where applicable;
- computation-recipe fingerprints;
- generated-statement fingerprints;
- package-manifest fingerprints;
- replay fingerprint stability;
- determinism verification result.

If any required fingerprint is missing, the affected package must be rejected.

## Required constitutional boundary evidence

Each campaign assessment must state whether any candidate contained:

- interpretation;
- explanation of significance;
- policy implication;
- investment implication;
- causal language;
- predictive language;
- recommendation;
- presentation narrative;
- unsupported domain conclusion.

Any such candidate must be rejected and preserved in the rejected-object catalogue.

## Required architectural observations

Each campaign assessment must record production evidence about:

- whether every architectural contract behaved as intended;
- whether validator rules were unexpectedly restrictive;
- whether validator rules were too permissive;
- whether additional metadata fields were required;
- whether provenance remained sufficient;
- whether fingerprints remained stable;
- whether new knowledge categories appeared;
- whether production revealed architectural weaknesses;
- which improvements are evidence-backed rather than speculative.

Architectural changes may be recommended only when supported by observed production evidence.

## Required final recommendation

Each campaign assessment must conclude with one of:

1. Continue to the next narrow production campaign.
2. Repeat the current campaign after fixing concrete blockers.
3. Pause production and resolve a specific architecture/validator/provenance/reproducibility blocker.

The recommendation must not speculate beyond campaign evidence.
