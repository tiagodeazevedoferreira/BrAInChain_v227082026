# Phase 7 — Exit Intelligence

Deterministic exit-decision foundation for paper trading.

The engine combines trailing-stop protection, liquidity deterioration, dynamic take-profit with reversal confirmation, reversal-risk scoring and time stops. It does not submit real orders and has no wallet/signing capability.

`peak_capture_pct` measures how close the simulated exit price is to the observed peak, enabling later evaluation of how much of a move the strategy captured.

Future work may replace heuristic thresholds with calibrated probabilistic peak/reversal models trained only on information available at decision time.
