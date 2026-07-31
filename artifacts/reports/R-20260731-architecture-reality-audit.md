# Architecture-to-Reality Audit

Date: 2026-07-31T23:59:00Z
Project: /tmp/knowledgeforge-eppilot-boundary-contract-v1-20260731/workspace
Mode: generated
Latest previous audit: artifacts/reports/R-20260730-architecture-reality-audit.md
Completed tasks since latest audit: 2

## Scope

This audit checks documented architecture, governance rules, operating procedures, state artifacts, templates, automation, logging/context systems, and available implementation for drift.

## Candidate attestation

This report attests the frozen audit subject identified below; it does not recursively hash itself or predict a final commit.

- Parent repository HEAD: `3b8eacce73e0b460d940ef9b1fcfea9d719f6a72`
- Subject-manifest fingerprint: `sha256:21abcf09d1e56b368223604d947c630180ed441d58bddb89410ab8f9d10e4497`
- Subject path count: 71
- Canonical repository fingerprint: `sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff`
- Audit tool fingerprint: `sha256:3b704ac07262415f5e2eb21dd953898d151fb8129629d3377f31ad6731326192`
- Audit result: `generated`
- Workspace location (informational): `/tmp/knowledgeforge-eppilot-boundary-contract-v1-20260731/workspace`
- Exact exclusions:
  - `artifacts/reports/R-20260731-architecture-reality-audit.md` — audit output cannot be part of its own frozen subject
  - `artifacts/reports/_SUMMARY.md` — must be regenerated after the audit output exists and is independently included in the final candidate manifest
- Machine-readable attestation: `{"audit_result":"generated","audit_tool_fingerprint":"sha256:3b704ac07262415f5e2eb21dd953898d151fb8129629d3377f31ad6731326192","contract":"knowledgeforge.architecture_reality.candidate_attestation.v1@1.0","exclusions":[{"path":"artifacts/reports/R-20260731-architecture-reality-audit.md","reason":"audit output cannot be part of its own frozen subject"},{"path":"artifacts/reports/_SUMMARY.md","reason":"must be regenerated after the audit output exists and is independently included in the final candidate manifest"}],"parent_repository_head":"3b8eacce73e0b460d940ef9b1fcfea9d719f6a72","repository_fingerprint":"sha256:80a9388a21f07191c2758c8d230512535492b9b30f7ed93bab45c3a9471d64ff","subject_manifest_fingerprint":"sha256:21abcf09d1e56b368223604d947c630180ed441d58bddb89410ab8f9d10e4497","subject_path_count":71,"workspace_location_informational":"/tmp/knowledgeforge-eppilot-boundary-contract-v1-20260731/workspace"}`

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

None.

## Warnings

None.

## Remediation workflow

1. Fix blocks before major architecture/governance work continues.
2. Convert durable policy or architecture changes into decision artifacts.
3. Update implementation, templates, docs, and state together so future projects inherit the correction.
4. Refresh affected folder summaries and latest handoff.
5. Rerun `tools/architecture_reality_audit.py`, `tools/check_coherence.py`, and relevant tests.
