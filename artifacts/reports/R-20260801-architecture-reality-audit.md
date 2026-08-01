# Architecture-to-Reality Audit

Date: 2026-08-01T03:19:12+00:00
Project: /tmp/knowledgeforge-publication-authority-hardening-4de0fcc/workspace
Mode: generated
Latest previous audit: artifacts/reports/R-20260731-architecture-reality-audit.md
Completed tasks since latest audit: 59

## Scope

This audit checks documented architecture, governance rules, operating procedures, state artifacts, templates, automation, logging/context systems, and available implementation for drift.

## Candidate attestation

This report attests the frozen audit subject identified below; it does not recursively hash itself or predict a final commit.

- Parent repository HEAD: `4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3`
- Subject-manifest fingerprint: `sha256:93fbad3908b02ae451effebf1d8bca9f13e6959825182a18c932c9e9027383a0`
- Subject path count: 20
- Canonical repository fingerprint: `sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff`
- Audit tool fingerprint: `sha256:3b704ac07262415f5e2eb21dd953898d151fb8129629d3377f31ad6731326192`
- Audit result: `generated`
- Workspace location (informational): `/tmp/knowledgeforge-publication-authority-hardening-4de0fcc/workspace`
- Exact exclusions:
  - `artifacts/reports/R-20260801-architecture-reality-audit.md` — audit output depends on the frozen subject and cannot hash itself
  - `artifacts/reports/_SUMMARY.md` — generated reports inventory must list the resulting audit
- Machine-readable attestation: `{"audit_result":"generated","audit_tool_fingerprint":"sha256:3b704ac07262415f5e2eb21dd953898d151fb8129629d3377f31ad6731326192","contract":"knowledgeforge.architecture_reality.candidate_attestation.v1@1.0","exclusions":[{"path":"artifacts/reports/R-20260801-architecture-reality-audit.md","reason":"audit output depends on the frozen subject and cannot hash itself"},{"path":"artifacts/reports/_SUMMARY.md","reason":"generated reports inventory must list the resulting audit"}],"parent_repository_head":"4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3","repository_fingerprint":"sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff","subject_manifest_fingerprint":"sha256:93fbad3908b02ae451effebf1d8bca9f13e6959825182a18c932c9e9027383a0","subject_path_count":20,"workspace_location_informational":"/tmp/knowledgeforge-publication-authority-hardening-4de0fcc/workspace"}`

## Categories

- architecture_vs_implementation
- state_files_vs_reality
- agent_instructions_vs_behavior
- logging_systems
- context_management_systems
- governance_processes
- automation_workflows
- templates_vs_generated_projects

## Drift types

- drift
- obsolete_documentation
- duplicated_systems
- unused_systems
- missing_implementation
- implementation_without_documentation
- documentation_without_implementation

## Blocks

- Category: governance_processes
  Drift type: drift
  Finding: 59 completed task(s) since last Architecture-to-Reality Audit
  Remediation: Run and record an Architecture-to-Reality Audit before continuing major work.

## Warnings

None.

## Remediation workflow

1. Fix blocks before major architecture/governance work continues.
2. Convert durable policy or architecture changes into decision artifacts.
3. Update implementation, templates, docs, and state together so future projects inherit the correction.
4. Refresh affected folder summaries and latest handoff.
5. Rerun `tools/architecture_reality_audit.py`, `tools/check_coherence.py`, and relevant tests.

## Publication authority continuity

Publication-Authority-Schema: knowledgeforge.publication_authority.v1@1.0
Publication-Authority-Parent: 4de0fcc9825dcbeb04a5c52a92bc259b8bd416c3
Publication-Authority-Audit-Subject: sha256:20cacac1d1e222ec8b26221a086ae69ddca35dba19af710c2cdbc88cdd72a3e7
Publication-Authority-Mixed-Manifest: sha256:17c78b4bd618f1e2d480dcb40ccd6f5afbe45168c6af90c16192e335c2f25020
Publication-Authority-Complete-Path-Count: 17
Publication-Authority-Only-Path-Count: 1
Publication-Authority-External-Evidence: /tmp/knowledgeforge-publication-authority-hardening-4de0fcc/final/
