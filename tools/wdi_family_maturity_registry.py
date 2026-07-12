#!/usr/bin/env python3
"""Authoritative WDI production-family maturity registry.

The source of truth is the accepted family closeout artifact for each WDI
production family, not stale generated campaign-local candidate state.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

AUTHORITATIVE_MATURE_CLOSEOUTS: dict[str, str] = {
    "Demographic": "artifacts/production/campaign-7-wdi-demographic-structure-provenance-lineage-completeness/reports/campaign_family_maturity_assessment.md",
    "Environment": "artifacts/production/campaign-12-wdi-environment-provenance-lineage-closeout/reports/environment_family_maturity_assessment.md",
    "Infrastructure": "artifacts/production/campaign-15-wdi-infrastructure-provenance-lineage-closeout/reports/infrastructure_family_maturity_assessment.md",
    "Energy & Mining": "artifacts/production/campaign-18-wdi-energy-mining-provenance-lineage-closeout/reports/energy_mining_family_maturity_assessment.md",
    "Agriculture & Rural Development": "artifacts/production/campaign-21-wdi-agriculture-rural-development-provenance-lineage-closeout/reports/agriculture_rural_development_family_maturity_assessment.md",
    "Health": "artifacts/production/campaign-24-wdi-health-provenance-lineage-closeout/reports/health_family_maturity_assessment.md",
    "Education": "artifacts/production/campaign-27-wdi-education-provenance-lineage-closeout/reports/education_family_maturity_assessment.md",
    "Trade": "artifacts/production/campaign-30-wdi-trade-provenance-lineage-closeout/reports/trade_family_maturity_assessment.md",
    "Financial Sector": "artifacts/production/campaign-33-wdi-financial-sector-provenance-lineage-closeout/reports/financial_sector_family_maturity_assessment.md",
}


def _classify_from_text(text: str) -> str:
    for line in text.splitlines():
        lower = line.lower()
        if "classification:" in lower or "status:" in lower:
            if "mature" in lower:
                return "Mature"
            if "stable" in lower:
                return "Stable"
    if "mature status" in text.lower() or "status: mature" in text.lower():
        return "Mature"
    raise ValueError("unable to resolve maturity classification from authoritative closeout text")


def mature_wdi_family_registry(project_root: Path | str = Path(".")) -> dict[str, dict[str, Any]]:
    root = Path(project_root)
    records: dict[str, dict[str, Any]] = {}
    for family, rel in AUTHORITATIVE_MATURE_CLOSEOUTS.items():
        path = root / rel
        if not path.exists():
            raise FileNotFoundError(f"authoritative maturity closeout missing for {family}: {rel}")
        text = path.read_text(encoding="utf-8")
        classification = _classify_from_text(text)
        if classification != "Mature":
            raise ValueError(f"authoritative closeout for {family} is not Mature: {classification}")
        records[family] = {
            "family": family,
            "classification": classification,
            "authoritative_source": rel,
            "evidence_text": text[:1200],
            "source_policy": "accepted family closeout artifact",
        }
    return records


def is_mature_wdi_family(family: str, project_root: Path | str = Path(".")) -> bool:
    return family in mature_wdi_family_registry(project_root)


def main() -> int:
    import json
    print(json.dumps(mature_wdi_family_registry(Path.cwd()), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
