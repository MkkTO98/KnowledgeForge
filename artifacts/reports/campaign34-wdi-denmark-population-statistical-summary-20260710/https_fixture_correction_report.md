# HTTPS Evidence Fixture Correction Report

Status: passed

The prior WDI observation fixture used plain HTTP URLs. Stage 1 corrected the selection contract and acquisition tooling to use HTTPS-only World Bank API URLs, record requested and final resolved URLs, and reject HTTPS-to-HTTP downgrade.

## Corrected requested URLs

- Observation response: `https://api.worldbank.org/v2/country/DNK/indicator/SP.POP.TOTL?format=json&date=1990:2024&per_page=100`
- Indicator metadata response: `https://api.worldbank.org/v2/indicator/SP.POP.TOTL?format=json&per_page=1`

## Final resolved URLs

- Observation response: `https://api.worldbank.org/v2/country/DNK/indicator/SP.POP.TOTL?format=json&date=1990:2024&per_page=100`
- Indicator metadata response: `https://api.worldbank.org/v2/indicator/SP.POP.TOTL?format=json&per_page=1`

## Prior fixture retention

The prior HTTP-acquired fixture was retained at `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024/` for traceability. The corrected fixture is stored separately at `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024-https-corrected/`.

## Old-versus-new evidence comparison

- Indicator identity changed: False
- Entity/period/value/missingness changes: 0
- Observation set equivalent for indicator/entity/period/missingness/value: True

## Corrected fingerprints

- Selection: `sha256:16fe627795e31ec9aab2c49a6c8e0f6a3ee2d5271235c06d46dfbd55cfc038ee`
- Combined raw artifact: `sha256:034e8f4da6afdbdddf54a7a553f16483af4339f5348e0427f1706dfd9141a258`
- Raw fixture: `sha256:35c9d2ee63b1f63166f4ed3650402ccc1c0f52d763801e258cb911b9726c4bee`
- Normalized evidence: `sha256:cce0367fc05bf8ad974a14593eec8e2d4f8fdf7fafced1976d9001c9c1eaeb93`
