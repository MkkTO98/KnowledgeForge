# Campaign 36 Specification — Not Executed

```json
{
  "authoritative_https_requests": {
    "series_a_metadata": "https://api.worldbank.org/v2/indicator/NE.EXP.GNFS.ZS?format=json&per_page=1",
    "series_a_observations": "https://api.worldbank.org/v2/country/DNK/indicator/NE.EXP.GNFS.ZS?format=json&date=1990:2024&per_page=20000",
    "series_b_metadata": "https://api.worldbank.org/v2/indicator/NE.IMP.GNFS.ZS?format=json&per_page=1",
    "series_b_observations": "https://api.worldbank.org/v2/country/DNK/indicator/NE.IMP.GNFS.ZS?format=json&date=1990:2024&per_page=20000"
  },
  "calculation_contract_fingerprint": "sha256:916fd60c347214eda2a7a7b384c70b737a1ff3c62ce1e7971034dc7df473f476",
  "campaign_name": "Campaign 36 — Bounded WDI Denmark Exports-Imports Share Pearson Correlation Pilot",
  "candidate_package_count": 1,
  "coverage_threshold": "0.85",
  "entity": "DNK",
  "expected_aligned_pairs": 35,
  "expected_evidence_slots": 70,
  "falsification_questions": [
    "Is the relationship mechanically manufactured by definition?",
    "Does raw-rate transformation still carry obvious time-ordering/spurious-correlation risk?",
    "Do missing pairs or metadata changes invalidate reproducibility?"
  ],
  "frequency": "annual",
  "future_evidence_family": "external_wdi_annual_scalar_trade_pearson_correlation",
  "method_identity": "wdi_annual_scalar_pearson_correlation_v1@1.0",
  "minimum_aligned_pair_threshold": 30,
  "period": "1990-2024",
  "postgresql_requirements": [
    "no schema changes",
    "package ID lookup",
    "family filter",
    "statement type filter",
    "lifecycle filter",
    "fingerprint filter",
    "provenance lineage retrieval",
    "payload fidelity verification"
  ],
  "prohibited_language": [
    "causation",
    "explanation",
    "forecasting",
    "recommendation",
    "investment implication",
    "statistical significance",
    "trend",
    "stationarity",
    "lead/lag"
  ],
  "series_a": {
    "code": "NE.EXP.GNFS.ZS",
    "definition": "Exports of goods includes changes in the economic ownership of goods from residents of the compiling economy to non-residents, irrespective of physical movement of goods across national borders. Exports of services includes services provided by residents to non-residents. This indicator is expressed as a percentage of Gross Domestic Product (GDP) which is the total income earned through the production of goods and services in an economic territory during an accounting period.",
    "final_url": "https://api.worldbank.org/v2/indicator/NE.EXP.GNFS.ZS?format=json&per_page=1",
    "metadata_response_fingerprint": "sha256:57dae5fa8dbd577b2cff50f9cfe581b3273ecdaa1125c4188164ef9a3cdddff4",
    "metadata_url": "https://api.worldbank.org/v2/indicator/NE.EXP.GNFS.ZS?format=json&per_page=1",
    "name": "Exports of goods and services (% of GDP)",
    "sourceOrganization": "Country official statistics, National Statistical Offices (NSOs);\nNational Accounts data files, Central Banks;\nStaff estimates, World Bank (WB)",
    "unit": null
  },
  "series_b": {
    "code": "NE.IMP.GNFS.ZS",
    "definition": "Imports of goods includes change in the economic ownership of goods from non-residents to\n\n\n\n\nresidents of the compiling economy, irrespective of physical movement of goods across national borders. Imports of services includes services provided by non-residents to residents. This indicator is expressed as a percentage of Gross Domestic Product (GDP) which is the total income earned through the production of goods and services in an economic territory during an accounting period.",
    "final_url": "https://api.worldbank.org/v2/indicator/NE.IMP.GNFS.ZS?format=json&per_page=1",
    "metadata_response_fingerprint": "sha256:a6e803f45b0ecfabb89dfa448350c47e4994f543f62f46d2060362b91853eb75",
    "metadata_url": "https://api.worldbank.org/v2/indicator/NE.IMP.GNFS.ZS?format=json&per_page=1",
    "name": "Imports of goods and services (% of GDP)",
    "sourceOrganization": "Country official statistics, National Statistical Offices (NSOs);\nNational Accounts data files, Central Banks;\nStaff estimates, World Bank (WB)",
    "unit": null
  },
  "status": "specified_not_executed",
  "stop_conditions": [
    "authoritative metadata no longer supports percent-of-GDP units",
    "aligned observed pairs below 30",
    "duplicate period keys",
    "constant/zero-variance series",
    "component-total or mechanical identity evidence emerges",
    "PostgreSQL v1 projection cannot preserve JSON payload losslessly"
  ],
  "transformation_state": "raw percentage-of-GDP observations for both series"
}
```
