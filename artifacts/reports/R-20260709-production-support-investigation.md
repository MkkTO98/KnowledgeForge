# Production Support Investigation Report — PEL-008 and PEL-009

Date: 2026-07-09
Status: completed
Scope: PEL-008 and PEL-009 only

## Question

Should repeated Campaigns 0-3 production pressure be addressed by two independent helpers or by a minimal deterministic Production Support layer?

## Evidence reviewed

- Campaign 0 repository evidence characterization.
- Campaign 1 WDI evidence-quality/coverage production.
- Campaign 2 WDI completeness-bucket production.
- Campaign 3 WDI source freshness/release metadata production.
- `docs/production_evolution_log.md` after Campaign 3.
- Existing campaign implementations in `tools/run_campaign*_*.py`.

## Observed pressures

### PEL-008 — SourceEvidencePackage construction

Observed across Campaigns 0-3.

Repeated mechanics:

- assemble existing `SourceEvidencePackage` dictionary shape;
- preserve campaign-specific source identity;
- preserve campaign-specific payload scope;
- preserve campaign-specific evidence metadata;
- preserve campaign-specific provenance;
- preserve campaign-specific reproducibility handle;
- call the existing fingerprint builder.

The repeated work was deterministic and structural. The campaign-specific content remained explicit and should remain explicit.

### PEL-009 — production-quality metric aggregation

Observed across Campaigns 0-3, with the strongest common shape in Campaigns 1-3.

Repeated mechanics:

- count source packages, candidates, accepted objects, and rejected records;
- compute acceptance/rejection rates;
- count produced and rejected knowledge categories;
- aggregate validator failure categories;
- compute average evidence references per accepted object;
- check accepted-object provenance completeness;
- carry determinism, fingerprint-stability, and duplicate-pressure flags.

The repeated work was deterministic and structural. Campaign-specific report sections and cross-campaign comparison should remain explicit.

## Two helpers versus one minimal support layer

Decision: implement one minimal deterministic Production Support layer.

Reason:

- Both PEL-008 and PEL-009 are production mechanics, not domain logic.
- Both operate around the same production boundary: source packages, accepted objects, rejected records, and production-quality evidence.
- A single small module avoids creating two scattered utility surfaces while still preventing a framework.
- The implemented surface is only two functions and one tiny ratio/report helper; it is transparent enough to audit directly.
- Campaign scripts still show campaign-specific source facts, scope, provenance, reports, and final recommendations inline.

Rejected alternative: two independent helpers.

Reason:

- Independent helpers would not materially improve auditability compared with one small module.
- The helper boundaries are adjacent production-support mechanics and would likely share the same imports/conventions.
- Separate files would add navigation overhead without preserving more explicitness.

Rejected alternative: broader production framework.

Reason:

- No production evidence supports a workflow engine, registry, schema layer, adapter layer, runtime infrastructure, plugin system, or generic utility framework.

## Transparency assessment

The support layer preserves transparency because:

- source package campaign-specific values remain at call sites;
- report prose and campaign-specific report shape remain in campaign scripts;
- validators remain unchanged;
- fingerprint builder remains the existing constructor function;
- no hidden defaults invent campaign metadata;
- no persistence, registry, schema, or runtime lifecycle is introduced.

## Implementation boundary

Implemented only:

- `build_source_evidence_package(...)`;
- `aggregate_common_quality_metrics(...)`;
- small deterministic `ratio(...)` and `report_dict(...)` helpers.

Not implemented:

- framework;
- runtime infrastructure;
- registry;
- schema system;
- adapter/API;
- validator change;
- taxonomy/package/model change;
- report-format change;
- new production artifact type.

## Conclusion

Campaigns 0-3 justify a minimal deterministic Production Support layer, not two separate helpers and not a framework.
