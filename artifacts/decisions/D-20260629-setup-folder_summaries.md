# Decision: Setup - folder_summaries

Date: 2026-06-29
Status: Accepted
Severity: L2
Section: quality

## Question
Should every core folder maintain a _SUMMARY.md for agent navigation?

## Answer
Yes. Maintain core folder _SUMMARY.md files for summary-first agent navigation.

## Consequence
Agents must consult this artifact before asking the same question again. If status is Deferred and the issue becomes blocking, create a question in `question_queue/pending/`.
