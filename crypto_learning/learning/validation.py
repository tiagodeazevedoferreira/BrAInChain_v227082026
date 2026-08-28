from __future__ import annotations
from math import ceil


def time_split(records: list[dict], train_ratio: float = 0.7, validation_ratio: float = 0.15) -> tuple[list[dict], list[dict], list[dict]]:
    """Chronological split with deterministic remainder allocation.

    The train boundary uses floor while validation/test boundaries allocate
    fractional remainders so small datasets retain non-empty validation and
    test partitions whenever their requested ratios are non-zero.
    """
    if not 0 < train_ratio < 1 or not 0 <= validation_ratio < 1 or train_ratio + validation_ratio >= 1:
        raise ValueError("invalid split ratios")
    ordered = sorted(records, key=lambda r: str(r["observed_at"]))
    n = len(ordered)
    train_end = int(n * train_ratio)
    if validation_ratio == 0:
        validation_end = train_end
    else:
        test_size = ceil(n * (1.0 - train_ratio - validation_ratio))
        test_size = min(test_size, max(0, n - train_end - 1)) if n > train_end else 0
        validation_end = n - test_size
        if validation_end <= train_end and n - train_end >= 2:
            validation_end = train_end + 1
    return ordered[:train_end], ordered[train_end:validation_end], ordered[validation_end:]


def purge_overlapping_labels(records: list[dict], embargo_count: int = 0) -> list[dict]:
    """Optional embargo helper for forward-labelled samples."""
    if embargo_count < 0:
        raise ValueError("embargo_count must be non-negative")
    return list(records[:-embargo_count] if embargo_count else records)
