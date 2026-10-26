# Prospective monthly oil-production forecasts frozen on 26 October 2026

This archive holds 1,044 forecasts of monthly field oil production for Norway (Norwegian Offshore Directorate FactPages) and the UK (NSTA PPRS). They were frozen at 2026-10-26T01:51:38Z, before any of their target months had been released. The forecasting procedure, scoring dates and the primary comparison are fixed in `package/protocol_prospective.md`. No method, threshold or forecast may be changed after this freeze.

| Country | Latest released month at freeze | Production-month targets | Two-month-delay targets |
|---|---|---|---|
| Norway | August 2026 | Sep 2026, Nov 2026, Feb 2027 | Nov 2026, Jan 2027, Apr 2027 |
| UK | July 2026 | Aug 2026, Oct 2026, Jan 2027 | Oct 2026, Dec 2026, Mar 2027 |

## Proof of time

- `SHA256SUMS.txt` lists the SHA-256 of every file in `package/`. Its own SHA-256 is `65e31239f2da0814bfdd13f9be383a4f44f5ec92fd4070d5954803c10e68aa69`.
- At 2026-10-26T06:10:29Z, that digest was submitted to four independent public OpenTimestamps calendars: alice and bob (opentimestamps.org), Eternity Wall and Catallaxy. Their detached proofs are in `timestamps/*.ots`. Only the digest was sent.
- After the calendars anchor the digest in Bitcoin, run `python ots_upgrade.py` and then `python ots_check.py`. Alternatively use the official client: `ots upgrade timestamps/<file>.ots`, then `ots verify -f SHA256SUMS.txt timestamps/<file>.ots`. Once upgraded, the proof shows that this exact file set existed no later than the time of the Bitcoin block containing it.

To verify: recompute `sha256sum package/*` and compare it with `SHA256SUMS.txt`; recompute the SHA-256 of `SHA256SUMS.txt`; then verify any one `.ots` proof against that digest.

## Contents of `package/`

- `forecasts_frozen.csv`: the 1,044 frozen forecasts for all methods (P, H, M, C, mean3, drift3, state policy).
- `freeze_manifest.json`: freeze time, latest released months, and hashes of the inputs, the code and this file set.
- `protocol_prospective.md`: the procedure and the scoring plan, written before the forecasts were generated.
- `calibration_*_L0.csv` and `fit_audit.csv`: calibration coefficients and annual-fit audit.
- `panel_norway_to_202608.csv` and `panel_uk_to_202607.csv`: the public input series as acquired on 26 October 2026.
- `code_equivalence_check_uk2025.json`: the check that the freeze code reproduces all 3,973 earlier UK 2025-origin forecasts exactly.
- `prospective_hash_record.json`: hashes recorded at freeze time.

The forecasting code is identified by hash in `freeze_manifest.json`. It will be released with the associated manuscript.

## Data attribution

Norwegian data: Norwegian Offshore Directorate, FactPages (Norwegian Licence for Open Government Data). Contains information provided by the North Sea Transition Authority and/or other third parties (Open Government Licence).
