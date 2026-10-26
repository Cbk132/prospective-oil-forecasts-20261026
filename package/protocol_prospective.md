# Prospective forecast freeze: Norway (Sodir) and UK (NSTA PPRS)

Version 1, 26 October 2026. Written before the forecasts are generated. The forecasts are produced from public snapshots downloaded on 26 October 2026 and contain no target month. Every target lies after the latest month released in that snapshot. They are frozen locally with SHA-256 hashes. They have **not** been deposited publicly: a public deposit (OSF, Zenodo or GitHub) would establish an independent timestamp, but it is a publication step and needs the author's explicit approval.

## Inputs

- Norway: Sodir FactPages, Field > Production > Sum wellbores > Monthly, full CSV export, acquired 26 October 2026; latest released month August 2026. Oil = `prfPrdOilGrossMillSm3`, water = `prfPrdProducedWaterInFieldMillSm3`, converted from million Sm3 to Sm3 before any transformation; identifier = `prfNpdidInformationCarrier`; Volve (3420717) excluded, as in v11.
- UK: NSTA PPRS ArcGIS layer (item dd38204275a04618ab7ddd00f87224e3), report types P/OTL/T, all months, acquired 26 October 2026; latest released month July 2026 (180 units have reported it). Oil = OILPRODM3, water = WATPRODVOL; identifier = `UK::`+UNITNAME; the ten documented UK–Norway shared units are excluded, as in v11.
- Each series runs from its first source month to the latest released month of its country; reported zeros are kept, and null, negative and absent months are unknown.

## Forecasts frozen

The procedure is the frozen v11 procedure, using hash-checked imports of `run_external.py`, `run_delay.py` and `regime_policy.py`. Only the year loop is new, because the frozen drivers stop at December 2025. `prospective/code_check/code_equivalence_check_uk2025.json` shows that this loop reproduces all 3,973 v9 UK forecasts from 2025 origins exactly.

1. Production-month design (primary): origin t* = the country's latest released month. The 2026 annual models are trained on labels through December 2025 under 2025 eligibility, and the 2025 models are used only to build the calibration feedback window. Targets are t*+1, t*+3 and t*+6, for methods P, H, M, C, mean3, drift3 and the frozen state policy G/B. C uses matured forecasts with targets in [t*−12, t*−1], and the 12-month window must be complete.
2. Two-month delay design (secondary): observation month t*, assumed issue month s = t*+2, leads k = 1, 3, 6 (targets t*+3, t*+5, t*+8). The cutoff for issue year 2026 is October 2025. C uses the pool [t*−12, t*), which must be complete.

Candidates are every identifier that satisfies the frozen eligibility and origin rules at t*. No target-dependent selection is possible, because no target exists in the inputs.

## Scoring plan (fixed now)

- Target months: Norway L0 Sep 2026, Nov 2026, Feb 2027; Norway L2 Nov 2026, Jan 2027, Apr 2027; UK L0 Aug 2026, Oct 2026, Jan 2027; UK L2 Oct 2026, Dec 2026, Mar 2027. The manifest verifies these against the latest released months.
- Scoring snapshot A is downloaded at the end of the third calendar month after a design's last target month (Norway L0: end of May 2027; Norway L2: end of July 2027; UK L0: end of April 2027; UK L2: end of June 2027). Snapshot B, six months after snapshot A, is a revision sensitivity check. Missing targets are counted and excluded only from scoring.
- Metrics follow v11: pooled WAPE and identifier-equal WAPE over the common scorable cases of each country and horizon, plus over- and underestimation volumes. Countries are scored separately.
- Primary prospective comparison (descriptive): for each country, at h=3 and h=6 of the production-month design, is the pooled WAPE of M lower than that of P and of C? This gives 8 comparisons, and all of them are reported. With a single origin month, these results are a small prospective check, not an annual repeatability test. They are not a significance test, and identifiers are not treated as independent.
- The two-month delay design, h=1, mean3, drift3, H and G are secondary. No method, threshold or forecast may be changed after this freeze. Any later issue month needs its own new freeze file before its targets are released.

## Integrity

`freeze_manifest.json` records the time of freezing, the SHA-256 of the forecast file, every input, the frozen code and this protocol, and the latest released month for each country. Its hash is also written to the shared session notes. Local hashes alone do not prove a time to third parties. That needs a public deposit or a trusted timestamp, and both require the author's approval.

Attribution: Norwegian data from the Norwegian Offshore Directorate FactPages. Contains information provided by the North Sea Transition Authority and/or other third parties.
