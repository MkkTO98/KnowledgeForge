# Decision: Setup - command_policy

Date: 2026-06-29
Status: Accepted
Severity: L3
Section: governance

## Question
Command permission model: layered default, restrictive allowlist, or project-specific?

## Answer
layered default with specification-only constraint: documentation/governance writes allowed; runtime implementation, infrastructure, external service setup, data/database creation, and cross-project mutation require explicit approval.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
