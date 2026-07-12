# Knowledge Opportunity Catalogue

Date: 2026-07-09
Status: complete
Scope: opportunities only; no production knowledge generated

## Boundary rule

Every opportunity below must remain inside KnowledgeForge:

Allowed:

- factual knowledge;
- statistical characterization;
- deterministic classification;
- derived metrics;
- structural descriptions;
- trend summaries stated as method-scoped computations;
- mathematically demonstrable indicator relationships;
- methodological knowledge;
- negative knowledge;
- evidence quality summaries.

Forbidden:

- hypotheses;
- macro or investment interpretation;
- forecasting;
- recommendations;
- causal claims not directly supported by deterministic evidence;
- InsightForge-style meaning such as "this implies", "key takeaway", "risk", "bullish/bearish", or policy/investment conclusions.

## Opportunity matrix by capability group

| Capability group | Safe KnowledgeForge opportunities | Boundary exclusions |
|---|---|---|
| Country profiles / structural metadata | Source-backed factual identity packages for WDI source, territories, annual periods, indicator families, repository scope, and current coverage. Deterministic lists of which countries/years/indicators exist. Negative knowledge for absent non-WDI provider coverage. | No judgment about country quality, economic strength, risk, or investment relevance. |
| Demographic indicators | Evidence-quality and coverage packages; age-sex cohort indicator-family descriptions; completeness/missingness profiles; deterministic population-pyramid structural summaries; age-band availability matrices; source-freshness records; method-scoped derived shares/checks where formulas are explicit. | No demographic forecasts, social interpretation, policy conclusions, dependency-burden narrative, or causal statements. |
| National accounts / GDP | Factual GDP indicator identity; country-year availability; nominal USD observation reference packages; deterministic coverage summaries; missingness profiles. | No growth interpretation, recession claims, business-cycle narrative, investment meaning, or causal attribution. |
| Labor/human capital | Labor-force-participation coverage/missingness by sex and year; education/health context availability packages; source-backed indicator-family classification. | No labor-market tightness interpretation, human-capital quality narrative, wage/productivity implications, or policy assessment. |
| Inflation | Annual CPI inflation availability and descriptive distribution packages; source and missingness summaries. | No inflation regime labels unless mechanically defined and named as method-scoped; no central-bank policy interpretation. |
| Monetary/banking/credit | Source-backed indicator families for rates, credit, broad money, banking access, NPLs, capitalization; coverage and missingness profiles; deterministic threshold classifications if thresholds are explicit and non-interpretive. | No credit-cycle, financial-stability, monetary-policy stance, or risk conclusions. |
| Fiscal indicators | Factual note that current WDI PostgreSQL fiscal coverage is limited; government education expenditure coverage where present; negative knowledge for absent broad fiscal repository coverage. | No fiscal sustainability, deficit/debt interpretation, or policy recommendation. |
| Trade/tourism/external balances | Source-backed trade indicator family descriptions; import/export availability; deterministic net-trade-balance derivation from WDI package evidence; balance-direction labels if explicitly formulaic; tourism coverage/missingness; merchandise/services subfamily classifications. | No competitiveness, trade-risk, geopolitical, supply-chain vulnerability, or external-balance interpretation. |
| External finance | Remittance and market/banking indicator availability; negative knowledge for absent BOP/IIP/CPIS/CDIS in current PostgreSQL WDI repository. | No external vulnerability or capital-flow interpretation. |
| Productivity/business/innovation | R&D/patent/logistics/business-market indicator availability; deterministic coverage summaries; indicator-family descriptions. | No productivity regime, innovation strength, or business-cycle interpretation. |
| Environment/energy/health/welfare/migration/agriculture/tourism/digital | Factual source-backed indicator-family coverage, missingness, source metadata, temporal coverage, and method-scoped descriptive statistics. | No environmental risk, social welfare, health-system quality, migration pressure, food-security, or development interpretation. |
| Temporal evolution | Deterministic trend-shape descriptors such as first/last observed year, coverage continuity, count of observed years, arithmetic change between explicitly selected endpoints, rolling-window missingness, and mechanically defined monotonicity over a stated window. | No explanation of why changes happened; no forecasts; no regime interpretation. |
| Cross-country comparison | Deterministic ranking/quantiles/percentile bands for explicitly selected year/indicator; coverage comparability checks; same-indicator same-year availability matrices. | No country ranking as attractiveness, quality, performance judgment, or policy success unless quoting an external source claim. |
| Evidence quality | Evidence sufficiency summaries, raw artifact hash presence, source freshness, lineage completeness, validation status, missingness and contradiction placeholders. | No claim that evidence quality means the economy is strong/weak or usable for investment decisions. |
| Methodological knowledge | Reusable statements about WDI annual-scalar source behavior, release/freshness handling, non-aggregate country filter, indicator availability, missingness handling, and MacroForge/KF boundary responsibilities. | No MacroForge schema redesign or KnowledgeForge ownership of observations. |
| Negative knowledge | Explicit records that current PostgreSQL repository lacks non-WDI sources, revision/vintage production support, broad fiscal coverage, BOP/IIP, product-level trade, company identity, matrix facts, forecasts, or causal/investment semantics. | Negative knowledge must state evidence scope; it cannot imply the world lacks the concept, only that the audited repository lacks evidence. |

## Candidate package families

### 1. Evidence inventory packages

Purpose: record what MacroForge WDI evidence exists.

Statements allowed:

- "The audited MacroForge PostgreSQL repository contains WDI observations for 182 indicators, 217 territories, and annual periods 1990-2024."
- "The audited repository contains 1,095,789 observed facts and 281,806 explicit missing facts."
- "The WDI source identity is recorded in `meta.source` with source URL and license note."

Intelligence needed: deterministic computation + templates.

### 2. Evidence quality and missingness packages

Purpose: produce reusable evidence quality summaries.

Statements allowed:

- coverage counts by indicator, country, period, and observation status;
- missingness rates per indicator/country/period;
- raw artifact hash presence summaries;
- validation-output summaries.

Intelligence needed: deterministic computation only for metrics; deterministic templates for package text.

### 3. Demographic structure packages

Purpose: preserve reusable source-backed knowledge about WDI age-sex cohort evidence.

Statements allowed:

- indicator-family membership for five-year female/male age bands;
- complete coverage claims for the audited TASK-180 cohort family if validated by deterministic queries;
- country-year cohort availability matrices;
- source-freshness and artifact-hash evidence.

Intelligence needed: deterministic computation + templates.

### 4. Indicator family classification packages

Purpose: classify indicators into governed, evidence-backed families such as demographics, trade, monetary/credit, education, health, energy/environment.

Statements allowed:

- mapping from WDI source indicator code to family, when the mapping is rule-backed and reviewed;
- family coverage counts and missingness.

Intelligence needed: deterministic + templates. Local AI could later propose draft classifications, but acceptance should be deterministic/reviewed.

### 5. Derived metric packages

Purpose: produce formula-backed facts from WDI observations.

Examples:

- net goods-and-services trade balance = exports - imports;
- observed-year count;
- completeness percentage;
- endpoint arithmetic change;
- share/ratio checks where source indicators and formulas are explicit.

Intelligence needed: deterministic computation only, plus templates for package assembly.

### 6. Statistical characterization packages

Purpose: describe distributions without interpretation.

Examples:

- min/max/median/quantiles for an indicator in a country-year or cross-section;
- standard deviation or interquartile range;
- rank/percentile where method is explicit;
- correlation/covariance where no causal language is used.

Intelligence needed: deterministic computation only. Human governance should review vocabulary before production.

### 7. Methodological/source-behavior packages

Purpose: preserve reusable facts about WDI/MacroForge method behavior.

Examples:

- WDI API raw artifact URLs and source metadata include `lastupdated`;
- MacroForge WDI annual-scalar packages preserve raw SHA-256 hashes;
- MacroForge current PostgreSQL WDI facts preserve `observed` versus `missing` status.

Intelligence needed: deterministic + templates.

### 8. Negative knowledge packages

Purpose: keep limitations explicit.

Examples:

- current PostgreSQL production repository lacks non-WDI sources;
- current repository lacks revision/vintage production coverage;
- current repository lacks company/entity production facts;
- current WDI annual-scalar data does not by itself support causal or investment claims.

Intelligence needed: deterministic + templates, with human review for wording.

## Prioritized opportunity ordering

1. Evidence inventory and evidence-quality packages for WDI annual-scalar repository.
2. Demographic structure coverage/missingness packages.
3. Indicator-family classification packages for WDI annual-scalar indicators.
4. Deterministic derived metric packages with simple formulas and complete input evidence.
5. Statistical characterization packages with strict boundary-language validator coverage.
6. Cross-country/cross-time descriptive packages.
7. Broader non-WDI or multi-provider packages only after separate MacroForge evidence audits.

## Catalogue conclusion

KnowledgeForge can produce many useful packages without frontier LLMs, but the first production target should not be economically interesting relationships. It should be evidence-quality and demographic-structure knowledge because those are reproducible, deterministic, validator-friendly, and preserve the KnowledgeForge/InsightForge boundary.
