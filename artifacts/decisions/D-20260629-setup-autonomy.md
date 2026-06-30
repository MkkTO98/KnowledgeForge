# Decision: Setup - autonomy

Date: 2026-06-29
Status: Accepted
Severity: L3
Section: operating_model

## Question
Agent autonomy: conservative, balanced, aggressive, or project-specific?

## Answer
conservative: agents may update specifications, governance artifacts, and state within approved task scope; implementation/runtime changes require explicit approval and task artifact.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
