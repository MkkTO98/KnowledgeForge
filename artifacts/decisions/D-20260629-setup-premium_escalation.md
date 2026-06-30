# Decision: Setup - premium_escalation

Date: 2026-06-29
Status: Accepted
Severity: L3
Section: model_routing

## Question
When should Codex/OpenAI be used instead of local models?

## Answer
Use Codex/OpenAI only for high-ambiguity architecture review, consistency audit, or repeated local failure; not for routine file edits.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
