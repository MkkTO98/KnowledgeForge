# Decision: Setup - external_services

Date: 2026-06-29
Status: Accepted
Severity: L3
Section: architecture

## Question
Will the project depend on external APIs, cloud services, databases, or paid services?

## Answer
None in V1. Future services must be introduced only through KnowledgeForge decision artifacts and must not duplicate MacroForge observational storage.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
