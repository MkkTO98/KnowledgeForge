# WDI Observation Evidence Fixture

Status: v1 bounded fixture complete

This document records the first neutral observation-level WDI evidence fixture used to operationalize KnowledgeForge's external evidence-input boundary.

## Boundary

The fixture is evidence input, not canonical knowledge. It does not make KnowledgeForge a general observational-data platform. It does not query MacroForge or depend on MacroForge runtime/database/schema.

## Fixture

- Family: `external_wdi_annual_scalar_demographic_structure`
- Indicator: `SP.POP.TOTL` — Population, total
- Entity: Denmark (`DNK`)
- Period: 1990-2024 annual
- Source: World Bank World Development Indicators API
- WDI lastupdated: `2026-07-01`
- Fixture directory: `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024/`
- Normalized fingerprint: `sha256:01f10c90228540c31f2f873ee5b4930006c99bf430c7cb741f41a0e8157734b6`

## Reproducibility

Exact reproduction uses the retained raw response bytes and normalized fixture. WDI did not expose a true immutable vintage identifier in the response, so the fixture does not claim future reacquisition of identical provider bytes from the mutable API.

## Validation

Run:

```bash
python3 tools/wdi_observation_evidence_fixture.py validate --fixture-dir artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024
python3 -m unittest tests/test_wdi_observation_evidence_fixture.py -v
```

## Future pilot

A later separately authorized pilot may create a descriptive statistical-characterization KnowledgeObjectPackage using this fixture. It must not include explanation, trend meaning, forecast, recommendation, or investment implication.


## HTTPS correction — Campaign 34 prerequisite

The original fixture directory remains retained for traceability. The corrected HTTPS fixture is `artifacts/evidence-fixtures/wdi-demographic-population-total-denmark-1990-2024-https-corrected/` with normalized fingerprint `sha256:cce0367fc05bf8ad974a14593eec8e2d4f8fdf7fafced1976d9001c9c1eaeb93`. The acquisition manifest records requested HTTPS URLs and final resolved HTTPS URLs and tooling rejects HTTPS-to-HTTP downgrade.
