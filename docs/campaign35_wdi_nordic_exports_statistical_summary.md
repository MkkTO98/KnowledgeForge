# Campaign 35 — Bounded WDI Nordic Exports Share Statistical-Summary Replication

Status: complete.
Outcome: A — successful bounded replication.

Accepted packages: 3. Rejected candidates: 0. Campaign 36 was not executed. No MacroForge access, PostgreSQL schema change, Production Doctrine change, KnowledgeObjectPackage redesign, commit, or push occurred.

## Evidence fixture fingerprints

- selection fingerprint: `sha256:ef2227e67f93b1a248c7f93a0b984337043892aa0eb476fb77a4c7b5abed6aba`
- raw fixture fingerprint: `sha256:cc428e4b8f22dbd86b71204dbf5b704a7bc17c0d97241e3e8589dc80ec3fc076`
- combined raw artifact fingerprint: `sha256:1fda94bbab635a13ee82d64ec44fabe5c912335289eb523e93a14d335fab093f`
- combined fixture fingerprint: `sha256:68b8dca9219abe64421471b223ee5d340b1ff73630a6abaeaf6d3e95dfe9b5a6`
- normalized evidence fingerprint: `sha256:7a08f2f505a95a4a901dae2b02baead92b1069171ddccd66d640d17d488f2607`

Retained raw fixture is the exact reproducibility anchor because WDI does not provide a guaranteed immutable historical vintage in the response.

## Per-entity measures

### DNK — Denmark

- expected slots: 35
- observed: 35
- missing: 0
- coverage: 1
- first: 36.43094120982 in 1990
- last: 71.002013204305 in 2024
- minimum: 36.43094120982 in [1990]
- maximum: 71.002013204305 in [2024]
- arithmetic mean: 49.21269358036
- median: 50.590780535634
- population standard deviation: 9.903424891466
### NOR — Norway

- expected slots: 35
- observed: 35
- missing: 0
- coverage: 1
- first: 38.873182876877 in 1990
- last: 46.379495845844 in 2024
- minimum: 31.346350576485 in [2020]
- maximum: 53.57954923602 in [2022]
- arithmetic mean: 40.248198696371
- median: 39.570345744281
- population standard deviation: 4.137044260882
### SWE — Sweden

- expected slots: 35
- observed: 35
- missing: 0
- coverage: 1
- first: 28.099133049227 in 1990
- last: 54.497139681544 in 2024
- minimum: 26.122100009274 in [1992]
- maximum: 55.195877970181 in [2023]
- arithmetic mean: 42.379514821825
- median: 43.458732395716
- population standard deviation: 6.967188570239

## Utility decision

Arithmetic mean, median, and population standard deviation were retained for all three entities because annual exports share is a percent-of-GDP ratio whose finite-window center and dispersion have bounded descriptive meaning. These measures do not authorize claims about stationarity, independence, structural stability, performance, causation, forecast expectation, statistical significance, investment implication, or directional change.

## Repository

- total canonical objects: 525
- repository fingerprint: `sha256:257d003fba6800cecef6f7d4750875ce79811955d892e13c176d79316f94c9fd`

## Governance overhead

- counted campaign governance/report/task artifacts: 16
- accepted substantive packages: 3
- artifacts per substantive package: 5.333333333333333
- Campaign 34 baseline: approximately 24:1

## Next recommendation

Prepare the first correlation-method design and falsification gate. Do not execute correlations in Campaign 35; the recommendation is only the next bounded architectural/method task.
