# Pearson Production-Utility Review

## Review basis

Inventory: `pearson_utility_inventory.json` (`sha256:0eac92349d0d442ed5c4e57f678f880e72a8c0eb09f3324019a630c774c35d1f`).

Review-only thresholds used here are descriptive evidence-screening thresholds, not production acceptance rules and not significance tests:

- strong raw: abs(raw Pearson) >= 0.60
- weak first-difference: abs(first-difference diagnostic) <= 0.20
- high time-risk: max(abs(series-vs-time correlations)) >= 0.85, or both series have at least moderate time association with weak first-difference diagnostic
- semantic proximity: deterministic/manual code-pair rubric over WDI definitions/families; coefficient magnitude was not used

## Repository-level counts

- Total Pearson objects: 21
- Numeric time-index diagnostics available: 14
- Numeric time-index diagnostics lacking: 7
- Any diagnostic/time-ordering warning available: 18
- Time-risk distribution: {'high': 14, 'unclassified_numeric_missing': 3, 'unclassified_numeric_missing_time_warning_present': 4}
- Semantic-proximity distribution: {'semantically_close': 12, 'semantically_moderate': 1, 'semantically_remote': 8}
- Strong raw + weak first-difference, review-only: 5
- Objects with present package warnings insufficient for modern diagnostic use: 7
- Consumer reusable under stated limits: 21

## Complete 21-object inventory

| package_id | entity | pair | n | r | fd | risk | semantic | use |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pkg-object-srcpkg-campaign36-dnk-exports-imports-share-pearson-correlation-v1 | DNK | NE.EXP.GNFS.ZS x NE.IMP.GNFS.ZS | 35 | 0.988873850642 |  | unclassified_numeric_missing | semantically_close | reusable_with_warning_gap_numeric_time_diagnostic_absent |
| pkg-object-srcpkg-campaign37-nor-exports-imports-share-pearson-correlation-v1 | NOR | NE.EXP.GNFS.ZS x NE.IMP.GNFS.ZS | 35 | -0.477418804478 |  | unclassified_numeric_missing | semantically_close | reusable_with_warning_gap_numeric_time_diagnostic_absent |
| pkg-object-srcpkg-campaign37-swe-exports-imports-share-pearson-correlation-v1 | SWE | NE.EXP.GNFS.ZS x NE.IMP.GNFS.ZS | 35 | 0.968490740983 |  | unclassified_numeric_missing | semantically_close | reusable_with_warning_gap_numeric_time_diagnostic_absent |
| pkg-object-srcpkg-campaign38-dnk-life-expectancy-fertility-pearson-correlation-v1 | DNK | SP.DYN.LE00.IN x SP.DYN.TFRT.IN | 35 | -0.40932912178 |  | unclassified_numeric_missing_time_warning_present | semantically_moderate | reusable_with_warning_gap_numeric_time_diagnostic_absent |
| pkg-object-srcpkg-campaign39-demographic-rates-pearson-correlation-v1 | SWE | SP.DYN.CBRT.IN x SP.DYN.CDRT.IN | 35 | 0.406143835452 |  | unclassified_numeric_missing_time_warning_present | semantically_close | reusable_with_warning_gap_numeric_time_diagnostic_absent |
| pkg-object-srcpkg-campaign39-health-system-coverage-pearson-correlation-v1 | DNK | SH.IMM.IDPT x SH.IMM.MEAS | 35 | 0.74990264881 |  | unclassified_numeric_missing_time_warning_present | semantically_close | reusable_with_warning_gap_numeric_time_diagnostic_absent |
| pkg-object-srcpkg-campaign39-infrastructure-digital-access-pearson-correlation-v1 | NOR | IT.NET.USER.ZS x IT.CEL.SETS.P2 | 35 | 0.991171458703 |  | unclassified_numeric_missing_time_warning_present | semantically_close | reusable_with_warning_gap_numeric_time_diagnostic_absent |
| pkg-object-srcpkg-campaign40-agriculture-agricultural-forest-land-dnk-pearson-correlation-v1 | DNK | AG.LND.AGRI.ZS x AG.LND.FRST.ZS | 34 | -0.841257509606 | -0.017407835395 | high | semantically_close | positive_descriptor_but_requires_transformation_aware_companion |
| pkg-object-srcpkg-campaign40-demographic-birth-death-rates-nor-pearson-correlation-v1 | NOR | SP.DYN.CBRT.IN x SP.DYN.CDRT.IN | 35 | 0.885026927298 | -0.289912537517 | high | semantically_close | stable_descriptive_relationship_candidate_with_limitations |
| pkg-object-srcpkg-campaign40-energy-fossil-nonhydro-renewables-nor-pearson-correlation-v1 | NOR | EG.ELC.FOSL.ZS x EG.ELC.RNWX.ZS | 32 | 0.315942832953 | -0.204185174675 | high | semantically_close | stable_descriptive_relationship_candidate_with_limitations |
| pkg-object-srcpkg-campaign40-finance-credit-broad-money-dnk-pearson-correlation-v1 | DNK | FS.AST.PRVT.GD.ZS x FM.LBL.BMNY.GD.ZS | 35 | 0.316082156476 | -0.083567273412 | high | semantically_close | stable_descriptive_relationship_candidate_with_limitations |
| pkg-object-srcpkg-campaign40-health-life-expectancy-under5-mortality-nor-pearson-correlation-v1 | NOR | SP.DYN.LE00.IN x SH.DYN.MORT | 35 | -0.951151571489 | -0.207863151096 | high | semantically_close | stable_descriptive_relationship_candidate_with_limitations |
| pkg-object-srcpkg-campaign40-infrastructure-internet-mobile-swe-pearson-correlation-v1 | SWE | IT.NET.USER.ZS x IT.CEL.SETS.P2 | 35 | 0.98654957106 | 0.402109713928 | high | semantically_close | stable_descriptive_relationship_candidate_with_limitations |
| pkg-object-srcpkg-campaign41-dnk-agricultural-land-broad-money-pearson-correlation-v1 | DNK | AG.LND.AGRI.ZS x FM.LBL.BMNY.GD.ZS | 34 | -0.328261524184 | -0.018892915467 | high | semantically_remote | baseline_input_requiring_transformation_aware_companion |
| pkg-object-srcpkg-campaign41-dnk-agricultural-land-private-credit-pearson-correlation-v1 | DNK | AG.LND.AGRI.ZS x FS.AST.PRVT.GD.ZS | 34 | -0.667417505516 | 0.058190335423 | high | semantically_remote | primarily_cautionary_negative_relationship_knowledge |
| pkg-object-srcpkg-campaign41-dnk-forest-area-broad-money-pearson-correlation-v1 | DNK | AG.LND.FRST.ZS x FM.LBL.BMNY.GD.ZS | 34 | 0.473272303276 | -0.101990610667 | high | semantically_remote | baseline_input_requiring_transformation_aware_companion |
| pkg-object-srcpkg-campaign41-nor-crude-birth-rate-fossil-electricity-pearson-correlation-v1 | NOR | SP.DYN.CBRT.IN x EG.ELC.FOSL.ZS | 34 | -0.416716498351 | 0.03778166456 | high | semantically_remote | baseline_input_requiring_transformation_aware_companion |
| pkg-object-srcpkg-campaign41-nor-fossil-electricity-under5-mortality-pearson-correlation-v1 | NOR | EG.ELC.FOSL.ZS x SH.DYN.MORT | 34 | -0.618717118858 | -0.083376899169 | high | semantically_remote | primarily_cautionary_negative_relationship_knowledge |
| pkg-object-srcpkg-campaign41-nor-nonhydro-renewable-electricity-under5-mortality-pearson-correlation-v1 | NOR | EG.ELC.RNWX.ZS x SH.DYN.MORT | 32 | -0.652623909096 | 0.3855860099 | high | semantically_remote | baseline_input_requiring_transformation_aware_companion |
| pkg-object-srcpkg-campaign41-swe-private-credit-internet-users-pearson-correlation-v1 | SWE | FS.AST.PRVT.GD.ZS x IT.NET.USER.ZS | 35 | 0.933818372664 | 0.141137912446 | high | semantically_remote | primarily_cautionary_negative_relationship_knowledge |
| pkg-object-srcpkg-campaign41-swe-private-credit-mobile-cellular-pearson-correlation-v1 | SWE | FS.AST.PRVT.GD.ZS x IT.CEL.SETS.P2 | 35 | 0.937758474347 | 0.161115218727 | high | semantically_remote | primarily_cautionary_negative_relationship_knowledge |

## Utility finding

The 21-object evidence materially weakens the value of continuing toward 100 raw-level Pearson objects as the primary target. Raw Pearson remains useful as a baseline descriptor, but Campaign 41 shows that strong raw coefficients can be dominated by shared time movement, especially when the selector prioritizes cross-family diversity over semantic proximity. The repository value is highest when raw Pearson objects either:

1. describe semantically close relationships with clear limitations; or
2. serve as cautionary/baseline objects paired with transformation-aware or richer diagnostics.

The evidence does not invalidate accepted Campaign 41 packages. It does show that object-count growth alone is a poor production objective.

## Knowledge/warning distinction

- High-time-risk semantically remote raw Pearson packages are best understood primarily as reusable cautionary or baseline knowledge, not positive explanatory relationship knowledge.
- High-time-risk semantically close packages remain useful descriptors but need transformation-aware companion knowledge before scale-up.
- Packages lacking numeric time-index/first-difference diagnostics remain reusable but have insufficient present-package warning precision compared with Campaign 40/41 packages.
