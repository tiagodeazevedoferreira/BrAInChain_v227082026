# Phase 9 — Continuous Learning

Phase 9 adds the governance foundation for learning from completed paper-trading outcomes.

## Pipeline

`paper outcomes -> append-only dataset -> chronological train/validation/test split -> candidate evaluation -> champion/challenger -> promotion gate`

## Safety rules

- No random split is used for time-dependent observations.
- Future-labelled observations must not leak into training.
- A challenger is never promoted merely because it exists.
- Promotion requires minimum sample size, balanced accuracy, positive mean return and a drawdown ceiling.
- A challenger must strictly improve balanced accuracy and mean return without increasing drawdown.
- Firebase is not used as an unbounded historical training store.
- This phase does not enable live trading or model auto-promotion into a live executor.

Thresholds are initial governance defaults and must be calibrated with statistically meaningful out-of-sample evidence before production use.
