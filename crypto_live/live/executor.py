class LiveExecutor:
    """Safety boundary. No real order transport is implemented in Phase 8."""

    def __init__(self, preflight_ok: bool = False):
        self.preflight_ok = preflight_ok

    def submit(self, order: dict) -> dict:
        if not self.preflight_ok:
            return {"status": "BLOCKED", "reason": "LIVE_PREFLIGHT_NOT_PASSED"}
        # Deliberately fail closed until a separately reviewed venue adapter exists.
        return {"status": "BLOCKED", "reason": "NO_APPROVED_VENUE_ADAPTER"}
