# Statistical-Summary Pilot Design

Status: design only; not executed

## Future candidate

A future production pilot may create a strictly descriptive, method-scoped statistical-characterization KnowledgeObjectPackage for WDI `SP.POP.TOTL` Denmark annual observations, 1990-2024, using normalized evidence fingerprint `sha256:01f10c90228540c31f2f873ee5b4930006c99bf430c7cb741f41a0e8157734b6`.

## Allowed descriptive measures

- observation count;
- missing count and missing share;
- period coverage;
- minimum and maximum observed value;
- arithmetic mean;
- median;
- population standard deviation if explicitly labeled;
- first and last valid observation.

Selected quantiles are deferred unless the pilot explicitly defines a quantile algorithm and value.

## Boundaries

The later candidate may state only deterministic descriptive facts. It may not state causes, explanations, good/bad assessments, forecasts, recommendations, investment implications, narrative conclusions, or trend claims.

## Acceptance criteria

- retained fixture fingerprint matches;
- observed count >= 30;
- coverage share >= 0.85;
- missing observations are explicitly represented;
- calculation method/version is declared;
- unit is preserved as persons;
- deterministic output fingerprint is reproducible;
- package validates under existing KnowledgeObjectPackage and Production Doctrine boundaries;
- PostgreSQL v1 can project the canonical JSON without schema expansion.
