# D-20260712 Campaign 41 Production Sequencing

Decision: Campaign 41 must stop before calculation until a coefficient-free candidate registry and batch specification are accepted.

Classification: accepted roadmap item requiring bounded specification.

Rationale:

- The accepted roadmap direction after Relationship Export Contract v1 is to resume operational Pearson production toward 100 relationship objects.
- Existing artifacts do not define the concrete Campaign 41 candidate set, scope, units, transformations, evidence identities, compatibility rules, or expected package identities.
- Candidate selection must be frozen before coefficient calculation and must not depend on calculated outcomes.
- Therefore execution now would require silent candidate/method selection, which is outside the authorized production boundary.

No Doctrine Review Trigger, architecture pressure, package redesign, PostgreSQL schema change, or new method family is justified by this decision.

Next task: create Campaign 41 coefficient-free Pearson candidate registry and batch specification decision, then execute Campaign 41 only after that registry is frozen and compatible with the existing generic engine.
