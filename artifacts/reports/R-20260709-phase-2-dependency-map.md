# Phase 2 Dependency Map

Date: 2026-07-09
Status: completed planning artifact

## Dependency types

- Prerequisite: should happen first because it reduces ambiguity or provides evidence required by the later work.
- Complementary: increases value when paired with another family but does not strictly depend on it.
- Comparison opportunity: creates multi-reference/cross-family evidence.
- Falsification gate: deliberately tests an assumption not naturally covered by ordinary family maturation.

## Family dependency map

| Family/workstream | Natural prerequisites | Complementary families | Cross-family comparison opportunity | Falsification contribution | Recommended position |
| --- | --- | --- | --- | --- | --- |
| WDI Infrastructure | Demographic + Environment mature; methodology closeout | Energy, Agriculture | Compare infrastructure coverage/provenance against demographic/environment | Third-family transfer; controlled structural family | 1 |
| WDI Energy & Mining | Infrastructure transfer or equivalent third-family transfer | Environment, Infrastructure | Technical-domain coverage vs environment/infrastructure | Boundary-language pressure without high financial/policy load | 2 |
| WDI Agriculture & Rural Development | At least one additional Phase 2 family | Environment, Energy | Small-family coverage/provenance contrast | Tests method efficiency on narrower family | 3 |
| WDI multi-family comparison | At least three mature/near-mature families | All WDI families | Multi-reference, overlap, duplicate, provenance-difference evidence | Exercises PEL-012 and PEL-017 inside WDI | 4 |
| WDI Trade | Stable boundary behaviour across additional families | Financial Sector, Infrastructure | Higher interpretation-risk comparison | Tests trade/economic wording boundary | 5 |
| WDI Financial Sector | Stable boundary behaviour across additional families | Trade, Infrastructure | Higher interpretation-risk comparison | Tests finance-wording boundary without investment meaning | 6 |
| WDI Education/Health | Scaling baseline from smaller/mid-sized families | Demographic | Large-family scale and adjacency comparisons | Tests object-volume/scaling pressure | 7 |
| Non-WDI multi-source disagreement | Multiple WDI families mature; broader WDI comparison complete | WDI families as internal baseline | Disagreement between source systems | Major remaining falsification gap | 8 |

## Recommended maturation order

1. Infrastructure.
2. Energy & Mining.
3. Agriculture & Rural Development.
4. WDI multi-family comparison across Mature or near-Mature families.
5. Trade.
6. Financial Sector.
7. Education or Health scale-family maturation.
8. Non-WDI multi-source disagreement planning and execution.

## Dependency conclusions

Infrastructure does not require a new architecture because it shares the WDI annual-scalar shape. Energy and Agriculture add useful heterogeneity after Infrastructure. Cross-family comparison should wait until more than two families exist because Campaign 9 already validated the two-family comparison pattern; the next useful comparison pressure comes from broader family count.

Trade and Financial Sector should not be first because their domain vocabulary increases risk of unsupported interpretation. That risk is validator/boundary-management risk, not evidence that validators are insufficient.

Education/Health scale pressure should not be first because high indicator counts can obscure whether failures come from scale or immature family-transfer assumptions.

Non-WDI multi-source disagreement is the major remaining falsification gap. It should be explicitly planned later rather than smuggled into an ordinary family campaign.

## Architectural continuity conclusion

The dependency map preserves the agreed architecture and accepted production doctrine. It introduces no new concept, contract, validator, runtime, or governance mechanism.
