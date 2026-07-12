# D-20260710 — Statistical-Summary Pilot Evaluation and Bounded Replication Gate

Status: accepted
Date: 2026-07-10

## Decision

Sequencing decision **D** — Both numerical-method remediation and knowledge-design refinement are required before replication.

## Campaign 34 disposition

Historical-package disposition **B** — Campaign 34 remains valid under its historical toolchain, but should be superseded by a corrected method version before replication.

The promoted Campaign 34 package remains accepted and was not modified. Package byte hash during this gate: `ee124afc43b6db03c9ceacb9905864caa8abe15057d1bac507ba1a9db6e913eb`.

## Justification

Adversarial Decimal-context tests showed that Campaign 34 v1 depends on ambient global Decimal context for division and square root. Lower precision, higher precision, and different rounding mode changed canonical numerical output and package fingerprints. This is bounded computational-method pressure, not a doctrine defect.

Measure-utility review also found that counts and coverage are strongly reusable, endpoints/extrema are conditionally reusable, and mean/median/population standard deviation over ordered annual population levels are mathematically valid but substantively weak without stronger method context.

## Next bounded task

Bounded Numerical-Method v2 and Statistical-Summary Knowledge-Design Refinement Gate.

No Campaign 35 or replication is authorized by this decision.
