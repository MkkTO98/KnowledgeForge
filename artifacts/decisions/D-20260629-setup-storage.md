# Decision: Setup - storage

Date: 2026-06-29
Status: Accepted
Severity: L3
Section: architecture

## Question
Does the project need persistent storage? If yes, which kind?

## Answer
Future persistent knowledge store expected, separate from MacroForge observational databases; exact database/storage technology deferred. V1 stores only Markdown/YAML/JSON architectural specifications and governance artifacts.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
