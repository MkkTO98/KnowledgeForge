# Statistical-Summary Measure-Utility Rules

```json
{
  "conditional_descriptive_measures": {
    "arithmetic_mean": "Include only when the summarized population is explicit; useful for rates/percentages/shares over bounded windows; weak for ordered level series unless purpose is narrowly descriptive.",
    "median": "Include under same conditions as mean; useful as robust bounded-window center only when ordered observations are not presented as independent samples.",
    "population_standard_deviation": "Include only as finite-set dispersion over observed values with denominator N; clearer for rates/percentages/shares than raw population levels."
  },
  "conditional_requirements": [
    "state summarized population",
    "state unit semantics",
    "state window semantics",
    "minimum observed count and coverage satisfied",
    "state prohibited interpretations",
    "omit weak measures when merely cheap"
  ],
  "core_reusable_measures": {
    "coverage": "Always include with denominator and scope.",
    "expected_slot_count": "Always include when expected slot derivation is explicit.",
    "first_and_last_valid_observations": "Include as bounded window anchors; prohibit trend language.",
    "minimum_and_maximum_with_periods": "Include when extrema have periods and unit; prohibit significance/trend inference.",
    "missing_count_and_share": "Always include; missing rows must remain distinct from zero values.",
    "observation_count": "Always include for validated scopes; direct evidence completeness fact."
  },
  "prohibited_language": [
    "causation",
    "forecasting",
    "statistical significance unless separately tested",
    "stationarity",
    "randomness or independence of ordered annual observations",
    "normative judgment",
    "investment implications",
    "trend conclusions unless future trend method"
  ]
}
```
