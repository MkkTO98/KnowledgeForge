# Decision: Setup - clarification_channel

Date: 2026-06-29
Status: Accepted
Severity: L2
Section: operating_model

## Question
Where should blocking questions go: local queue only, Telegram later, email later, or other?

## Answer
Use ProjectForge local question queue and direct user clarification when blocking.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
