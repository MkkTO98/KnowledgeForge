# Scalable Coefficient-Free Candidate-Selection Model

Inputs allowed before freeze: Mature-family membership, metadata, units, definitions, annual frequency, coverage/missingness, variance probe, construction risk, transformation compatibility, expected aligned-pair count, and evidence accessibility.

Model:

1. Candidate registry row = `(family, semantic_template, entity, series_a, series_b, period, unit_a, unit_b, definition_fingerprints, coverage_probe, variance_probe, construction_risk)` .
2. Hard rejects: non-Mature family, coefficient already inspected, <30 aligned observations, coverage <0.85, duplicate keys, zero variance, unresolved units, direct identity/complement/component-total/embedded definition.
3. Priority score, coefficient-free only:
   - +3 mature family with prior successful fixture reproduction
   - +3 distinct semantic template underrepresented in repository
   - +2 underrepresented entity
   - +2 clear unit derivation
   - +2 complete coverage
   - +1 real but manageable missingness
   - -3 shared denominator pressure
   - -4 common modeled-estimation pressure
   - -5 post-freeze rejection history for same template
4. Freeze top batch with diversity constraints before calculation.
5. Never replace frozen candidates based on coefficient value.

Implementation recommendation: add a deterministic candidate registry generator only after Pearson-family maturation approves operational continuation.
