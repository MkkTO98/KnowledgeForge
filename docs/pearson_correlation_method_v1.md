# Pearson Correlation Method v1

Method identity: `wdi_annual_scalar_pearson_correlation_v1@1.0`

Calculation-contract fingerprint:
`sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476`

This method implements contemporaneous Pearson correlation only. It excludes p-values, confidence intervals, hypothesis tests, regression coefficients, Spearman correlation, partial correlation, rolling correlation, lagged correlation, and automatic multiple-testing correction.

The method uses Decimal arithmetic under a pinned local context with precision 50 and ROUND_HALF_EVEN. Inputs must be base-10 decimal strings; scientific notation is forbidden. Canonical outputs use 12 decimal places with negative-zero canonicalized to zero.

Alignment is an inner join on observed annual periods after validating series identity, frequency, transformation state, duplicates, minimum aligned-pair count, coverage threshold, and non-constant/non-zero-variance series.

The method records simple spurious-correlation diagnostics for strong monotonic time ordering and always carries a warning that correlation may be spurious due to common trends, structural breaks, autocorrelation, shared construction, or common external factors.
