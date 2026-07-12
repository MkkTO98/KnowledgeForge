# wdi_annual_scalar_first_difference_pearson_v1 Method Contract

Status: validated for bounded WDI annual-scalar companion-production preparation
Version: 1.0
Date: 2026-07-12

Transformation: `wdi_annual_scalar_first_difference_v1@1.0`
Method: `wdi_annual_scalar_first_difference_pearson_v1@1.0`
Transformation fingerprint: `sha256:71573c15a70a0694b6bca3b3fc1c712ef7720ef7f1c30f4c50186cc7c44bbc5f`
Method fingerprint: `sha256:e7de3a78473ca97e0cdb427118a5d5e48b6777b51592f55e2ed50ed5d78a3ade`

Formula: `delta_x_t = x_t - x_(t-1)`.

Period label: ending period `t`.

Missingness: do not bridge gaps; require consecutive annual periods; invalid/non-finite endpoints fail closed; duplicate entity-indicator-period keys fail closed.

Units: absolute first difference in the original unit. Percent-like levels become percentage-point changes. Rates become absolute rate changes. Currency/count levels become absolute changes. Do not call first differences growth rates, percent changes, percentages, or elasticities.

Pearson: transform before alignment; align transformed series by entity and ending period; require at least 30 aligned transformed observations and 0.85 transformed coverage for this retained evidence class; use deterministic Decimal local context precision 50, ROUND_HALF_EVEN, canonical 12 decimal places, zero-variance fail-closed.

Limitations: no causation, stationarity, significance, forecast, investment signal, or lead-lag claim.
