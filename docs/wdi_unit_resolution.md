# Bounded WDI Unit-Semantics Remediation Report

Status: implemented and tested.

The unsafe generic WDI unit fallback has been removed from `tools/wdi_observation_evidence_fixture.py`.

Allowed unit-resolution states:

1. Provider-explicit unit — provider supplies an unambiguous unit field; the provider value and evidence reference are preserved.
2. Definition-derived unit — authoritative indicator name/definition deterministically encode the unit; the derivation rule and metadata fingerprint are recorded.
3. Explicitly unitless/dimensionless — only when authoritative metadata supports that classification.
4. Unresolved unit — normalization fails closed before promotion.

`NE.EXP.GNFS.ZS` resolves to `percent of GDP` because the authoritative WDI indicator name contains `% of GDP` and the source note states that the indicator is expressed as a percentage of Gross Domestic Product (GDP).

`SP.POP.TOTL` resolves to `persons` only through the approved definition-derived population rule, not through a generic default.

Historical Campaign 34 and Campaign 35 canonical package files were hash-checked unchanged.

Classification: bounded implementation correction; no Production Doctrine or architecture change.
