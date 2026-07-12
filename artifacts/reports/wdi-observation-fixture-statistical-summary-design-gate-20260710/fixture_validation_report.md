# Neutral WDI Observation Evidence Fixture Validation Report

Date: 2026-07-10
Status: complete

## Decision

Decision A — Evidence fixture validated; statistical-summary pilot is ready for separate execution authorization.

No statistical-summary production campaign was executed or promoted. Campaign 34 was not created.

## Selected family and indicator

- Mature family: `external_wdi_annual_scalar_demographic_structure`
- Indicator: `SP.POP.TOTL` — Population, total
- Unit: persons
- Definition: Total population is based on the de facto definition of population, which counts all residents regardless of legal status or citizenship. The values shown are midyear estimates.

Selection reason: the demographic family is Mature, population total is an active authoritative WDI annual-scalar indicator with clear definition/unit, 35/35 observed annual values in the selected scope, low interpretation risk, and no need for cross-indicator reasoning.

## Scope

- Entity: Denmark (`DNK`)
- Period: 1990-2024 inclusive
- Frequency: annual
- Expected observation slots: 35
- Observed values: 35
- Missing values: 0

## Source and acquisition identity

- Provider: World Bank
- Dataset: World Development Indicators
- Observation URL: `http://api.worldbank.org/v2/country/DNK/indicator/SP.POP.TOTL?format=json&date=1990:2024&per_page=100`
- Indicator metadata URL: `http://api.worldbank.org/v2/indicator/SP.POP.TOTL?format=json&per_page=1`
- WDI source id: 2
- WDI lastupdated: 2026-07-01
- Provider pagination: {'page': 1, 'pages': 1, 'per_page': 100, 'total': 35}

Access timestamp is recorded in the acquisition manifest as non-canonical operational metadata and is excluded from deterministic content fingerprints.

## Fixture files

- Raw observation response: `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024/raw_observations_response.json`
- Raw indicator metadata response: `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024/raw_indicator_metadata_response.json`
- Raw fixture: `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024/raw_fixture.json`
- Normalized fixture: `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024/normalized_observations.json`
- Selection contract: `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024/selection_contract.json`
- Acquisition manifest: `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024/acquisition_manifest.json`

## Fingerprints

- Selection fingerprint: `sha256:e5ec35208a8fcaa7561f19843b401b9751fb9246ef2e78185ea17bd5fef80d04`
- Observation response SHA-256: `sha256:81e034a482eb1c4baac214537f1d87b84c2f3247cbed988024b5636d91d694c1`
- Indicator metadata response SHA-256: `sha256:569cda11cb51e244c1f655398efcd22e393891d899e9c1b649f2aebcff07c661`
- Combined raw artifact fingerprint: `sha256:fd0be51504e4cf811a0e20e2858fdbafd567bbc4c9eaed5252f059282cc7153f`
- Raw fixture fingerprint: `sha256:39fd3decdfe4a78b7678104a5cdd97b2a487819dce587650405e8059f08a4e4e`
- Normalized observation fingerprint: `sha256:01f10c90228540c31f2f873ee5b4930006c99bf430c7cb741f41a0e8157734b6`

## Mutable-source vintage limitation

Exact reproducibility is from the retained local raw response bytes and normalized fixture. Source identity and freshness are represented by the WDI API URLs, request parameters, source id, indicator metadata, and WDI `lastupdated` value. WDI did not expose a true immutable historical vintage identifier in the retained response, so this fixture does not claim that the identical historical API response can be reacquired later.

## Validation result

The fixture proves that KnowledgeForge can independently acquire, preserve, validate, fingerprint, and deterministically normalize enough objective numerical WDI evidence for a later statistical-summary Knowledge Object.

The fixture remains evidence input, not canonical knowledge.
