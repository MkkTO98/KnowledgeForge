# Campaign 40 — First End-to-End Specification-Driven Pearson Production Batch

## Outcome

Campaign outcome: A. End-to-end specification-driven production validated.

Pearson family status: Stable with limitations.

Next strategic direction: 4. Define a read-only downstream-consumption contract.

## Recovery

Selected recovery option: B. Bounded Campaign 40 package replacement.

Reason: the provisional six canonical packages contained `time_index_error: mismatched entities` inside canonical statement payload diagnostics. Corrected diagnostics changed generated-statement and package fingerprints, while coefficients and aligned evidence were unchanged.

Pre-existing package immutability: True.

## Accepted packages

- pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1: coefficient -0.841257509606, aligned 34 (0.971428571429), diagnostics A/time -0.828711001501, B/time 0.986386181457, diff -0.017407835395
- pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1: coefficient 0.885026927298, aligned 35 (1), diagnostics A/time -0.962386748464, B/time -0.959509920885, diff -0.289912537517
- pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1: coefficient 0.315942832953, aligned 32 (0.914285714286), diagnostics A/time 0.64921014377, B/time 0.804092533899, diff -0.204185174675
- pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1: coefficient 0.316082156476, aligned 35 (1), diagnostics A/time 0.757137531509, B/time 0.521453951784, diff -0.083567273412
- pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1: coefficient -0.951151571489, aligned 35 (1), diagnostics A/time 0.991026536994, B/time -0.940259226282, diff -0.207863151096
- pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1: coefficient 0.98654957106, aligned 35 (1), diagnostics A/time 0.890139366438, B/time 0.935643810072, diff 0.402109713928

## Rejected frozen candidates

- education_primary_secondary_enrollment_nor: aligned pairs below threshold
- finance_atm_credit_swe: aligned pairs below threshold

## Repository and PostgreSQL

Repository count: 538
Repository fingerprint: sha256:958c88d4be0bce735adcaaf3f236a7643aa80fd79846db23f4b521d05459771b
PostgreSQL rebuild: return code 0

## Governance

- Campaign-specific Python lines: 0
- Bespoke Campaign 40 runner: none
- Support artifacts per accepted object: 1.0 versus Campaign 39 baseline 7.67

## Local AI

Contribution: zero. No local-AI retry was performed.

## Doctrine / architecture classification

Doctrine: no doctrine change required.
Architecture: reusable path validated, still limited by missing registry automation and absent downstream consumption contract.
