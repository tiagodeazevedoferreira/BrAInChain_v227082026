from __future__ import annotations


def time_split(records: list[dict], train_ratio: float = 0.7, validation_ratio: float = 0.15) -> tuple[list[dict], list[dict], list[dict]]:
    """Chronological split. Future observations never enter train data.

    Boundary rounding is remainder-aware so small datasets do not silently
    produce an empty validation set when a non-zero validation ratio is given.
    """
    if not 0 < train_ratio < 1 or not 0 <= validation_ratio < 1 or train_ratio + validation_ratio >= 1:
        raise ValueError("invalid split ratios")
    ordered = sorted(records, key=lambda r: str(r["observed_at"]))
    n = len(ordered)
    train_end = int(n * train_ratio)
    test_size = int(n * (1.0 - train_ratio - validation_ratio))
    validation_end = n - test_size
    if validation_ratio > 0 and n >= 3 and validation_end <= train_end:
        validation_end = min(n - 1, train_end + 1)
    return ordered[:train_end], ordered[train_end:validation_end], ordered[validation_end:]


def purge_overlapping_labels(records: list[dict], embargo_count: int = 0) -> list[dict]:
    """Optional embargo helper for forward-labelled samples."""
    if embargo_count < 0:
        raise ValueError("embargo_count must be non-negative")
    return list(records[:-embargo_count] if embargo_count else records)
