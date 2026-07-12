# Knowledge Capability Inventory from MacroForge

Date: 2026-07-09
Status: complete
Scope: inventory only; no economic evaluation and no production knowledge generation

## Inventory basis

This catalogue distinguishes two evidence layers:

1. Current PostgreSQL repository: audited directly from database `macroforge`. This is WDI-only and is the safest basis for first KnowledgeForge production.
2. Broader MacroForge project artifacts: capability atlas/domain coverage/task reports show many bounded evidence-only and operational slices across other providers. These are useful for future planning but should not be treated as current PostgreSQL production repository contents unless separately audited.

## PostgreSQL repository inventory

Current PostgreSQL facts:

- Source: World Bank World Development Indicators (`WDI`).
- Indicators: 182.
- Territories: 217 non-aggregate/country-like territories in current WDI campaigns.
- Periods: annual, 1990-2024.
- Curated facts: 1,377,595.
- Observed facts: 1,095,789.
- Explicit missing facts: 281,806.
- Dataset releases: 3 WDI release keys.
- Pipeline runs: 8.
- Raw artifact hashes and URLs: available through dataset release/pipeline manifests.

## Capability groups available in current PostgreSQL

### Country profiles and structural metadata

Available evidence:

- 217 territories.
- ISO3/canonical territory codes.
- Territory names.
- WDI region and income-group metadata where loaded.
- Annual period dimension 1990-2024.
- WDI indicator identity and indicator names.
- Source identity, source URL, and license note.

Potential KnowledgeForge use:

- factual source/territory/indicator identity knowledge;
- structural descriptions of the WDI repository slice;
- evidence availability and scope boundaries;
- negative knowledge about absent non-WDI/cross-source identity coverage in the current PostgreSQL repository.

### Demographic indicators

Available evidence:

- Total population, population growth, sex-specific population, female/male population shares.
- Broad age shares: 0-14, 15-64, 65+.
- Detailed five-year female/male age-band count/share indicators from 00-04 through 80+.
- Dependency ratios: total, old-age, young-age.
- Fertility rate, adolescent fertility, life expectancy, crude birth/death rates.
- Infant, under-5, adult male/female, and maternal mortality.
- Urban/rural population, rural share, urban share, density, land-area denominator context.
- Net migration and remittance context.

Scale notes:

- TASK-180 WDI demographic structure added 68 five-year age-sex cohort indicators and 516,460 observed rows.
- Demographic Structure is operationally complete within WDI annual-scalar scope for national annual historical five-year age-sex cohort analysis.

### National accounts and macro output

Available evidence:

- GDP current US dollars.
- Agriculture/forestry/fishing value added as percent of GDP.
- Trade shares and goods/services exports/imports as macro aggregates.
- Some macro context via WDI foundational/expansion indicators.

Limitations:

- Current PostgreSQL repository is not a full national-accounts ontology.
- No complete GDP component framework.
- No multi-source canonical national accounts comparison in the current audited repository.

### Labor and human capital

Available evidence:

- Labor-force participation rate: total, female, male.
- Education enrollment: primary, secondary, tertiary gross enrollment.
- Primary completion.
- Adult literacy.
- Government education expenditure as percent of GDP/government expenditure.

Limitations:

- Current WDI PostgreSQL slice does not include the broader MacroForge BLS/ILOSTAT/FRED operational labor artifacts as loaded current PostgreSQL sources.
- No occupation, industry, wage, hours, unemployment, payroll, vacancy, or subnational labor ontology in the current audited repository.

### Inflation

Available evidence:

- Consumer price inflation, annual percent (`FP.CPI.TOTL.ZG`).

Limitations:

- No broad price-index ontology.
- No monthly CPI in current PostgreSQL WDI repository.
- Broader BLS/FRED inflation-related evidence exists in MacroForge artifacts but is not current PostgreSQL production repository content under this audit.

### Monetary policy, banking, credit, and financial intermediation

Available evidence:

- Deposit interest rate.
- Lending interest rate.
- Interest-rate spread.
- Real interest rate.
- Lending risk premium.
- Domestic credit to private sector by banks / financial sector.
- Broad money current LCU, broad money percent of GDP, broad money growth.
- Bank nonperforming loans, bank capital to assets, ATMs, commercial-bank branches, borrowers/depositors.
- GFDD banking/depth indicators for 1990-2021.
- Market capitalization, listed companies, stocks traded.

Limitations:

- No central-bank policy-rate time-series in current PostgreSQL WDI repository.
- No market curve/FX ontology.
- No cross-provider financial-account reconciliation.

### Fiscal indicators

Available evidence:

- Direct fiscal/government finance coverage in current PostgreSQL WDI repository is limited.
- Government expenditure on education is present as a fiscal/human-capital context indicator.

Limitations:

- No broad government receipts/outlays/debt/deficit coverage in current PostgreSQL WDI repository.
- MacroForge artifacts contain Treasury/FRED fiscal slices, but those are outside the current PostgreSQL WDI production audit unless separately promoted/audited.

### Trade, tourism, and external balances

Available evidence:

- Exports/imports of goods and services, current US dollars.
- Exports/imports of goods and services, percent of GDP.
- Trade as percent of GDP.
- Merchandise exports/imports, current US dollars.
- Commercial service exports/imports.
- Services trade percent of GDP.
- Insurance/financial services and transport-service shares.
- ICT goods import/export shares.
- High-technology exports current US dollars and percent of manufactured exports.
- International tourism arrivals, receipts, expenditures, and shares.
- Personal remittances received as percent of GDP.
- Deterministic WDI trade-balance capability package exists as a MacroForge operational artifact, not canonical facts.

Limitations:

- No bilateral partner coverage in current PostgreSQL WDI repository.
- No product-level HS coverage in current PostgreSQL WDI repository.
- No mirror reconciliation or services-component framework.

### External balances and international finance

Available evidence:

- Remittances percent of GDP.
- Trade and services balance inputs.
- Broad financial-market and banking depth indicators.

Limitations:

- No current-account, BOP, IIP, reserve, CPIS/CDIS, or cross-border banking PostgreSQL production coverage in current WDI repository.
- MacroForge artifacts contain bounded IMF/BIS/ECB/FRED slices that require separate readiness audits before KnowledgeForge production use.

### Productivity and business indicators

Available evidence:

- R&D expenditure percent of GDP.
- Patent applications by residents.
- Logistics Performance Index dimensions.
- Food production index.
- Agriculture value added.
- Fixed broadband subscriptions.
- Listed companies and market capitalization.

Limitations:

- No business-cycle model, company fundamentals, productivity/time-use ontology, or firm-level canonical identity in current PostgreSQL WDI repository.

### Environment, energy, health, education, welfare, migration, and structural development

Available evidence:

- PM2.5 exposure.
- Forest area.
- Energy use per capita.
- Electricity production from coal.
- Health expenditure, hospital beds, physicians, immunization, skilled birth attendance.
- Poverty headcount and Gini.
- Migration/remittances.
- Agriculture and food production.
- Digital infrastructure and logistics.

Potential KnowledgeForge use:

- factual coverage and source-identity packages;
- missingness/completeness summaries;
- deterministic descriptive metadata;
- negative knowledge about absent frameworks/cross-source validation.

### Temporal evolution

Available evidence:

- Annual country-indicator observations from 1990-2024 for many indicators.
- Explicit missingness allows method-scoped coverage/missingness time summaries.

Limitations:

- Temporal trend summaries are safe only when described as deterministic descriptive computations, not economic interpretation.
- Revision/vintage time-series behavior is not yet production-ready in current PostgreSQL repository.

### Cross-country comparisons

Available evidence:

- Same WDI indicators across 217 territories and annual periods.
- Country-year panels support deterministic ranking, coverage counts, distributions, quantiles, and cross-sectional summaries.

Limitations:

- Cross-country comparison must remain descriptive/mathematical.
- No causal explanation, performance interpretation, or investment meaning belongs in KnowledgeForge.

## Broader MacroForge artifact inventory beyond current PostgreSQL

MacroForge's `docs/capability-atlas.md` records implemented evidence or operational capability across many categories, including:

- canonical GDP and macro-indicator ingestion;
- observed ingestion packages and deterministic replay;
- price observations;
- national accounts/output/consumption/income/saving;
- fiscal flows and public debt;
- labor-market observations;
- trade, bilateral/product trade, financial accounts/IIP;
- matrix observations;
- energy balances and commodity prices;
- rates, curves, monetary policy, FX;
- housing, subnational, revision-aware vintage, company/issuer, survey/confidence, business indicators, reserves, payment cards, education, health, climate, welfare, migration, agriculture, tourism, high-tech exports, and others.

These are important future KnowledgeForge evidence candidates. They should not be first production targets because current PostgreSQL production state and repository-scale validation are strongest for WDI annual-scalar evidence.

## Inventory conclusion

The safest production-ready capability family is WDI annual-scalar country-year evidence, especially demographic structure and evidence-quality/coverage knowledge. It has broad coverage, high determinism, strong provenance handles, explicit missingness, and minimal need for semantic interpretation.
