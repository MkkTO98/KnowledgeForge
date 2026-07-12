# Campaign 43 Coefficient-Free First-Difference Companion Registry Freeze

Date: 2026-07-12
Status: locally verified registry frozen; superseded for next-step readiness by the Campaign 43 calculation gate

## Scope

Campaign 43 is limited to a coefficient-free registry-selection and production-contract freeze for exactly six remaining Campaign 41 raw Pearson relationships classified as high shared-time-trend risk after Campaign 42 produced first-difference companions for the two SWE Campaign 41 relationships.

This task did not calculate coefficients, execute first differencing, construct KnowledgeObjectPackages, publish to the canonical repository, project to PostgreSQL, mutate production PostgreSQL, redesign contracts, or amend doctrine.

## Frozen artifacts

- Registry: `specs/correlation_batches/campaign43_coefficient_free_first_difference_companion_registry.json`
- Registry identifier: `campaign43_coefficient_free_first_difference_companion_registry`
- Registry fingerprint: `sha256:f03db436c06350a755f181a4cf0e9852ac30064fea84d77cd79332e774efc5a1`
- Freeze specification: `specs/correlation_batches/campaign43_first_difference_companion_registry_freeze_specification.json`
- Specification fingerprint: `sha256:823ba8d4d144a9d312b41acc4c7fdcf12a2f928b39d2b7a6c615015506ce95cf`
- Validator/generator: `tools/campaign43_first_difference_companion_registry.py`
- Focused tests: `tests/test_campaign43_first_difference_companion_registry.py`

## Candidate boundary

The registry evaluates exactly the six authorized relationships:

1. DNK agricultural land / broad money
2. DNK agricultural land / private credit
3. DNK forest area / broad money
4. NOR crude birth rate / fossil electricity
5. NOR fossil electricity / under-5 mortality
6. NOR nonhydro renewable electricity / under-5 mortality

No Campaign 40 candidates, corrected raw-candidate-pool candidates, or other campaign candidates were added.

## Registry outcome

All six candidates are included. No candidate was excluded.

| Candidate | Source package | Source package manifest fingerprint | Resolvable aligned periods for future differencing | Status |
|---|---|---|---:|---|
| DNK agricultural land / broad money | `pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1` | `sha256:b74efa65ccfd9ee609916d21872c1692fac0a6bdc818f7a89a9f3393215a140a` | 33 | included |
| DNK agricultural land / private credit | `pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1` | `sha256:1d6577ec481d8c118fb18b7188a5c7748b8d025d63ca7dfe3f216547e42fbd52` | 33 | included |
| DNK forest area / broad money | `pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1` | `sha256:d8719416ec59b40ab84df2e8c6019a86070c05eadb33df16a9da15ad7410df3e` | 33 | included |
| NOR crude birth rate / fossil electricity | `pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1` | `sha256:34a47624a077e33e447c0efb62583da04204cccbe19e933ea38ad158b0ab3162` | 33 | included |
| NOR fossil electricity / under-5 mortality | `pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1` | `sha256:a575cdd3c88a276f7d2dd5fef543a7db905b1f47e98aff0629c07aeb2fa9f88e` | 33 | included |
| NOR nonhydro renewable electricity / under-5 mortality | `pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1` | `sha256:79461212ae1829adc1e3cab9a0e52f51a253e476fbd40b02126cfc390caea8a5` | 31 | included |

## Inclusion basis

Each included candidate passed the same deterministic checks:

- source raw package exists in the canonical repository;
- source package is a Campaign 41 raw Pearson v1 package;
- source package manifest fingerprint matches canonical repository content;
- entity, ordered series identities, frequency, raw period scope, and raw method contract resolve;
- source package lifecycle is accepted and not superseded;
- retained input fixtures resolve deterministically;
- period availability is sufficient for future first-difference evaluation without calculating first-differenced values;
- no equivalent canonical first-difference companion package exists;
- future method and transformation identifiers point to the accepted first-difference contracts;
- inclusion rationale and high shared-time-trend evidence are recorded;
- deterministic ordering follows the authorized readiness-decision order.

## Coefficient-free enforcement

The registry records only source identities, fingerprints, fixture identities, raw metadata, future method/transformation contract references, eligibility status, rationale, deterministic ordering, and registry fingerprints.

It does not contain or derive Pearson coefficients, p-values, covariance, first-differenced observation vectors, calculated sample statistics, or acceptance decisions based on unperformed calculations.

The validator rejects forbidden coefficient/result fields and the tests mutate raw coefficient/diagnostic values in an isolated copy to prove registry selection and fingerprint stability do not depend on them.

## Architecture and doctrine classification

This is bounded production preparation inside the existing architecture.

No Production Doctrine amendment, KnowledgeObjectPackage redesign, Relationship Export Contract redesign, PostgreSQL schema change, broad transformation framework, generalized API, new method family, or cross-project dependency is required or authorized.

## Verification summary

Final verification is recorded in this report's closeout and in `registry_validation.json`.

Canonical repository state remained unchanged:

- package count: 554
- repository fingerprint: `sha256:82fbbfecf1b9d33bc164d3380ab5d350435e7d5e0ab8a0cdcebfc8fd9f9a0c8b`
- no new KnowledgeObjectPackages
- no Campaign 40-42 package mutations
- no PostgreSQL projection or production mutation

## Next task

If separately authorized, the smallest next task is Campaign 43 production preflight and coefficient calculation from the frozen registry, stopping before canonical publication unless publication is separately authorized.
