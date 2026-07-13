# Terms-First Two-Source Evidence Candidate Screening

Date: 2026-07-13
Accessed: 2026-07-13T06:53:22Z; adversarial correction evidence gathered 2026-07-13
Status: adversarially corrected; no candidate selected
Outcome: B — no screened pair cleared all hard eligibility requirements

## Scope and boundary

This remains a documentation and eligibility screen only. The original screen covered three bounded source pairs. The correction reassessed only Candidate 3, U.S. Census International Database versus UN World Population Prospects, as requested.

No observation values, source data payloads, cross-source differences, agreement/disagreement classifications, registries, KnowledgeObjectPackages, PostgreSQL mutations, or Relationship Export mutations were produced.

Bulky fetched documentation diagnostics were kept under `/tmp/kf_terms_screen/` and `/tmp/kf_terms_screen_correction/` and are not repository recovery dependencies. Official URLs, document titles, release identifiers, access dates and compact findings are retained here and in `candidate_matrix.json`.

## Gate vocabulary used in the corrected matrix

- Passed: compact official evidence supports the gate for screening purposes.
- Failed: official evidence contradicts the gate or establishes non-eligibility.
- Unresolved: official evidence found so far is insufficient; do not infer eligibility.
- Not applicable: gate does not apply to that candidate dimension.

## Candidates screened

### 1. World Bank WDI vs Eurostat population, Denmark, annual 2024

Candidate boundary considered: total/resident population for Denmark, annual/historical 2024, World Development Indicators vs Eurostat national-level population.

Official terms/licensing evidence:

- World Bank WDI Data Catalog, title `World Development Indicators - World Bank Data Catalog`, URL `https://datacatalog.worldbank.org/search/dataset/0037712/World-Development-Indicators`, states dataset version/date modified `2026-07-01` and licence `Creative Commons Attribution 4.0` in embedded metadata.
- World Bank legal terms page, title `Terms & Conditions | World Bank Group`, URL `https://www.worldbank.org/en/about/legal/terms-of-use-for-datasets` redirected to `https://www.worldbank.org/ext/en/legal/terms-conditions`, requires attribution and includes general reuse conditions.
- European Commission legal notice, title `Legal notice - European Commission`, URL `https://commission.europa.eu/legal-notice_en`, states EU-owned content is licensed under CC BY 4.0 unless otherwise indicated and reuse is allowed with credit and change indication.

Release/vintage evidence:

- WDI catalog exposes a concrete current version/date modified: `2026-07-01`.
- Eurostat population metadata page, title `Population (national level) (demo_pop)`, URL `https://ec.europa.eu/eurostat/cache/metadata/en/demo_pop_esms.htm`, documents metadata and revision policy, but the screen did not establish an immutable archived release/vintage for the intended future dataset extraction. A mutable Eurostat database/current metadata page alone is insufficient.

Underlying-producer and independence assessment:

- World Bank WDI states it aggregates statistics from reputable national and international agencies.
- Eurostat national population statistics are transmitted by Member States/EFTA and validated/disseminated by Eurostat.
- For population, shared upstream national statistical offices and/or international demographic processing remain plausible. The screen did not establish that WDI and Eurostat are independently compiled estimation authorities for the exact concept rather than sharing underlying national evidence. Distinct publishers are insufficient.

Observation-status assessment:

- Eurostat metadata explicitly documents flags including provisional, estimated, break, and forecast, and data revision/correction practice.
- The screen did not establish that the exact 2024 Denmark observation would be finalized/observed rather than provisional or estimated.

Metadata-readiness assessment:

- Some metadata exists for definition, unit, reference period, source data, revision policy, and flags on the Eurostat side, and WDI has dataset-level metadata/version/licence.
- Comparability readiness failed because reference-period equivalence, observation-status equivalence, release/vintage identity, source independence, and missing-value semantics were not all established from official compact documentation.

Gate status: retention/reuse partly passed; immutable identity unresolved; source independence unresolved; observation status unresolved; comparability readiness unresolved.

### 2. World Bank WDI vs United Nations World Population Prospects, total population, bounded historical year

Candidate boundary considered: total population for one country, annual bounded historical year, World Development Indicators vs UN World Population Prospects.

Official terms/licensing evidence:

- World Bank WDI evidence as above: WDI catalog licence `Creative Commons Attribution 4.0` and version/date modified `2026-07-01`.
- United Nations Terms of Use, title `Terms of Use | United Nations`, URL `https://www.un.org/en/about-us/terms-of-use`, grants permission to download/copy site materials for personal, non-commercial use, without any right to resell/redistribute or compile/create derivative works, subject to further restrictions.
- UN World Population Prospects page, title `World Population Prospects`, URL `https://population.un.org/wpp/`, identifies the official WPP site, but the original screen did not establish separate WPP-specific reuse permission allowing repository retention/redistribution of the intended narrow evidence.

Release/vintage evidence:

- WDI current catalog version/date modified `2026-07-01` was observed.
- WPP is a named release family, but the original screen did not establish a specific archived WPP release/vintage plus stable retrieval identity for the exact intended observation without entering data-download territory.

Underlying-producer and independence assessment:

- WDI population indicators commonly draw on national/international demographic sources; WPP is a UN demographic estimation/revision product.
- The original screen did not establish independence for the exact concept. WDI may use UN/WPP-derived population evidence for population indicators, which would make the pair a mirror/shared-upstream pair rather than a genuine two-source disagreement candidate.

Observation-status assessment:

- WPP/IDB-style population products include estimates and projections; the original screen did not establish that the bounded historical year would be finalized historical source-estimate evidence under KnowledgeForge boundaries.

Metadata-readiness assessment:

- Basic concept/frequency/entity metadata appears plausible, but release/vintage, observation status, exact definition/reference period, revision policy, and missing-value semantics were not sufficiently established for both sources without retrieving data payloads.

Gate status: retention/reuse unresolved for UN/WPP dataset; immutable identity unresolved; source independence unresolved; observation status unresolved; comparability readiness unresolved.

### 3. U.S. Census International Database vs United Nations World Population Prospects, total population, bounded historical year — adversarial correction

Candidate boundary considered after correction: `published historical mid-year population estimate`, one country, annual, July 1/mid-year reference, historical-estimate period only; not observed population, not forecast, not future projection.

#### Source-specific licensing findings

Census IDB:

- U.S. Census citation page, title `Citing our Data, Tools, Technical Documents and Research`, URL `https://www.census.gov/about/policies/citation.html`, states Census statistical products and research can be discovered, reused, replicated for verification, and credited by citation. It gives citation patterns for data files and API datasets using author, dataset title, vintage, URL and access date.
- U.S. Census IDB page, title `International Database (IDB)`, URL `https://www.census.gov/programs-surveys/international-programs/about/idb.html`, links to the IDB web tool, API, full-dataset download, release notes, countries/areas page, errata page and methodology statement. No IDB-specific restriction overriding the general Census public-use/citation guidance was found in the compact official pages inspected.
- Screening classification: retention/reuse appears passed for a narrow attributed Census evidence fixture, subject to normal attribution and citation. This is not permission to retain bulky payloads; it is enough to avoid rejecting the Census side at the terms gate.

UN WPP:

- UN general Terms of Use, title `Terms of Use | United Nations`, URL `https://www.un.org/en/about-us/terms-of-use`, permits personal non-commercial download/copy and states no right to resell/redistribute or compile/create derivative works, subject to more specific restrictions.
- WPP 2024 methodology report, title/citation `World Population Prospects 2024: Methodology of the United Nations population estimates and projections`, URL `https://population.un.org/wpp/assets/Files/WPP2024_Methodology.pdf`, states copyright © United Nations 2024 and made available under Creative Commons `CC BY 3.0 IGO`.
- WPP 2024 data sources report, title/citation `World Population Prospects 2024: Data Sources`, URL `https://population.un.org/wpp/assets/Files/WPP2024_Data_Sources.pdf`, states figures and tables in that publication can be reproduced without prior permission under `CC BY 3.0 IGO`.
- The WPP web application/publications page provides citations for WPP 2024 release note, release note revision 1, methodology and data sources. However, I did not find a dataset-download-specific licence or terms page for the actual WPP CSV/Excel data files. The publication licences cover the reports/figures/tables; they do not by themselves prove that a future retained source-data payload from the WPP bulk files may be redistributed as a repository fixture.
- Screening classification: WPP retention/reuse for methodology/report excerpts is passed; WPP retention/reuse for a future narrow retained data-value fixture remains unresolved. Do not infer permission from file accessibility.

#### Release-identity findings

Census IDB:

- IDB official page states: `The IDB was last updated in December 2025. The next update is planned for November 2026.`
- IDB release-notes page, title `International Database Release Notes`, URL `https://www.census.gov/programs-surveys/international-programs/data/tools/international-data-base/idb-release-notes.html`, lists `Data Tool Release Notes: December 2025` and prior releases.
- IDB methodology statement, URL `https://www2.census.gov/programs-surveys/international-programs/technical-documentation/methodology/idb-methodology.pdf`, is a stable official methodology PDF, but it is not the data release itself.
- The full-dataset download link exposed by the IDB page is `https://www.census.gov/data-tools/demo/data/idb/dataset/idbzip.zip`; based on the link name it appears to be the current complete dataset, not a release-specific immutable archive path. I did not download it.
- Screening classification: named Census release `December 2025` is identified, but version-specific stable retrieval identity for the future data payload remains unresolved. A release note plus mutable current download is not enough.

UN WPP:

- WPP official site identifies `World Population Prospects 2024` as the 28th edition of official UN population estimates and projections.
- WPP 2024 release note, URL `https://population.un.org/wpp/assets/Files/WPP2024_Release-Note.pdf`, has release date `11 July 2024`.
- WPP 2024 revision 1/interim update, URL `https://population.un.org/wpp/assets/Files/WPP2024_Release-Note-rev1.pdf`, has release date `19 January 2026`; it states the next WPP revision was postponed to 11 July 2027 and lists updated files for Togo only, including version-specific update filenames.
- WPP 2024 methodology/data-source documents have stable version-specific filenames and document symbols. The WPP application also exposes version-specific file paths such as `WPP2024_Methodology.pdf`, `WPP2024_Data_Sources.pdf`, and update file names in the rev.1 note.
- Screening classification: WPP has a named edition/revision and stable version-specific document identities; future source-data retrieval could probably be tied to WPP 2024 or WPP 2024 rev.1 only if the exact version-specific data-file path is used and the Togo rev.1 exception is excluded or explicitly handled. For this candidate, WPP release identity is passed conditionally for non-Togo WPP 2024 / rev.1, but final future retrieval would still need the exact version-specific data file path.

#### Estimation-authority and independence evidence

Census IDB:

- IDB official page says the Census Bureau regularly estimates and projects the world's population and, along with the UN Population Division, is one of the few organizations that regularly does so. It says IDB data include total population, population by age/sex, fertility, mortality and migration, and that the Census Bureau provides metadata describing source data.
- IDB official page states IDB estimates/projections are informed by hundreds of sources including censuses, surveys, administrative records and vital statistics; national statistical offices are primary resources.
- IDB methodology statement says the process involves data collection, data evaluation, parameter estimation, developing assumptions about future change, and final projection; available data are evaluated with attention to internal and temporal consistency; after adjustments, data are used to estimate population by single years of age and estimate fertility, mortality and migration parameters needed for projections; DAPPS/RUP processes inputs and generates cohort-component projections.

UN WPP:

- WPP 2024 official site says the 2024 Revision is the 28th edition of official UN population estimates and projections prepared by the Population Division of UN DESA; it presents population estimates from 1950 to the present for 237 countries/areas, underpinned by analyses of historical demographic trends, and projections to 2100.
- WPP 2024 methodology report says the revision uses systematic compilation and evaluation of censuses and other empirical data, probabilistic models for estimating fertility/mortality indicators, and methods for accounting for crises including COVID-19; it identifies CCMPP population inputs/outputs and published estimates with 1 July reference date as arithmetic means of 1 January values.
- WPP 2024 data-sources report lists country-specific source evidence and notes, including official estimates, censuses, vital registration, surveys and international estimates.

Corrected independence classification:

- `shared-upstream but independently estimated`.
- Reason: both products use overlapping upstream demographic evidence such as national censuses, surveys, vital registration, administrative records and migration evidence. That shared upstream base does not by itself prove mirroring or dependence. Official methodology supports that Census and UN DESA separately evaluate source evidence, apply their own demographic methods/models, and publish their own estimates/projections. I found no official evidence that either simply republishes the other's resulting estimate for the exact candidate. This corrects the original overstatement that shared upstream alone made independence fail.

#### Corrected observation-status classification

- Not direct observation or census count.
- Not forecast if restricted to historical estimate years.
- Not future projection if the boundary excludes projection years.
- Correct classification: `published historical mid-year population estimate`, with possible adjustment/model content.

Existing-doctrine compatibility:

- KnowledgeForge doctrine forbids owning observations, ingestion outputs, forecasts and recommendations, but permits objective, reproducible, evidence-backed knowledge and evidence-level knowledge when provenance, evidence state, scope and boundaries are explicit.
- SourceEvidencePackage fixtures may classify whether they contain observational values; existing fixture contracts show `contains_observational_values` is explicit rather than automatically disqualifying all source evidence.
- Therefore, existing doctrine does not categorically forbid admitting a historical estimate as objective evidence of a source's published estimate, provided the future package is explicitly scoped as `published historical mid-year population estimate`, not `observed population`, and provided provenance, retention permission, stable identity and scope are satisfied. Do not change doctrine.

#### Potential historical boundary

Potential future boundary if unresolved gates are later cleared:

- Candidate: U.S. Census IDB December 2025 versus UN World Population Prospects 2024 Revision / revision 1.
- Concept: published historical mid-year total population estimate.
- Entity: Denmark, unless future official metadata shows a better single-country boundary.
- Reference date: July 1 / mid-year.
- Frequency: annual.
- Reference year: 2023, because WPP 2024 release-note evidence explicitly describes estimates through 2023 and projections thereafter; avoid 2024+ projection years.
- Population boundary: WPP `de facto population in a country, area or region as of 1 January or 1 July of the year indicated`, figures in thousands; Census IDB methodology says it strives for a modified de facto population universe where possible and traditionally uses July 1 as midyear for population estimates/projections.

Status boundary caveat: this boundary is not selected yet. It remains unresolved on the Census side until official IDB documentation establishes that Denmark 2023 in the December 2025 release is a historical estimate, not a projection or other status category, without retrieving values.

#### Candidate 3 corrected gate status

Passed:

- Census retention/reuse for narrow attributed evidence appears passed under official Census citation/public-use guidance.
- WPP methodology/report retention/reuse appears passed under CC BY 3.0 IGO for the official publications inspected.
- Estimation-authority independence classification is corrected to `shared-upstream but independently estimated`.
- Historical-estimate doctrine compatibility is passed in principle when the concept is source-published historical estimate, not observed population.
- Metadata comparability is plausible in part: both sources expose total population/mid-year or July 1 framing, annual frequency, country/area scope, and demographic methodology documentation.

Unresolved:

- WPP data-file-specific retention/reuse permission for a future retained value fixture.
- Census IDB version-specific immutable retrieval identity for the December 2025 data payload; release notes are named, but the observed full-dataset URL appears mutable/current.
- Exact Census historical/projection cutoff and status for Denmark 2023 in the December 2025 release.
- Exact version-specific WPP future data file path to use, and whether WPP 2024 or WPP 2024 rev.1 should be authoritative for the selected country; avoid Togo unless the rev.1 update is intentionally selected.
- Full comparability readiness across all required fields, especially exact population universe, status flags, revision policy and missing-value semantics.

Failed:

- No hard gate is now classified as substantively failed for Candidate 3 except by unresolved evidence. The candidate is not selected because unresolved hard gates remain.

Not applicable:

- Forecast/projection admission is not applicable because the corrected boundary excludes forecast/projection years.

## Final outcome

Outcome B — no candidate selected.

The corrected Candidate 3 assessment is materially stronger than the original screen: independence should not be rejected merely because of shared upstream demographic inputs, and a historical estimate may be compatible with KnowledgeForge doctrine if framed as a published source estimate. However, hard eligibility still requires retention permission for the future retained data fixture, exact immutable/version-specific release identity, exact historical-estimate status, and full metadata readiness. Those remain unresolved, so Candidate 3 cannot be selected yet.

## Architecture and production-state classification

No architecture, doctrine, schema, package-model, PostgreSQL, Relationship Export, or producer-project change is required or justified. The correction changes the screening analysis only; it does not admit evidence or alter production state.
