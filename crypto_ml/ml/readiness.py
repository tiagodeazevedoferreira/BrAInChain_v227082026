"""Dataset readiness gates."""


def check_readiness(samples: list[dict], min_samples: int = 100, min_tokens: int = 10) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    if len(samples) < min_samples:
        reasons.append(f"samples<{min_samples}")
    tokens = {str(s.get("token_id")) for s in samples if s.get("token_id")}
    if len(tokens) < min_tokens:
        reasons.append(f"unique_tokens<{min_tokens}")
    labeled = [s for s in samples if s.get("label") not in (None, "UNKNOWN")]
    if not labeled:
        reasons.append("no_labeled_samples")
    return not reasons, reasons
