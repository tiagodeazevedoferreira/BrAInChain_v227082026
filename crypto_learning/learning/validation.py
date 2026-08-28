from __future__ import annotations


def time_split(records: list[dict], train_ratio: float = 0.7, validation_ratio: float = 0.15) -> tuple[list[dict], list[dict], list[dict]]:
    """Chronological split. Future observations never enter train data."""
    if not 0 < train_ratio < 1 or not 0 <= validation_ratio < 1 or train_ratio + validation_ratio >= 1:
        raise ValueError("invalid split ratios")
    ordered = sorted(records, key=lambda r: str(r["observed_at"]))
    n = len(ordered)
    a = int(n * train_ratio)
    b = a + int(n * validation_ratio)
    return ordered[:a], ordered[a:b], ordered[b:]


def purge_overlapping_labels(records: list[dict], embargo_count: int = 0) -> list[dict]:
    """Optional embargo helper for forward-labelled samples."""
    if embargo_count < 0:
        raise ValueError("embargo_count must be non-negative")
    return list(records[:-embargo_count] if embargo_count else records)
