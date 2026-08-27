from dataclasses import dataclass
from .config import LiveConfig


@dataclass(frozen=True)
class Evidence:
    backtest_passed: bool = False
    out_of_sample_passed: bool = False
    paper_passed: bool = False
    security_tests_passed: bool = False
    failure_tests_passed: bool = False
    secrets_configured: bool = False


def preflight(config: LiveConfig, evidence: Evidence) -> tuple[bool, list[str]]:
    failures = config.validate()
    checks = {
        "BACKTEST_EVIDENCE_REQUIRED": evidence.backtest_passed,
        "OUT_OF_SAMPLE_EVIDENCE_REQUIRED": evidence.out_of_sample_passed,
        "PAPER_EVIDENCE_REQUIRED": evidence.paper_passed,
        "SECURITY_TESTS_REQUIRED": evidence.security_tests_passed,
        "FAILURE_TESTS_REQUIRED": evidence.failure_tests_passed,
        "SIGNING_SECRETS_REQUIRED": evidence.secrets_configured,
    }
    failures.extend(name for name, ok in checks.items() if not ok)
    return not failures, failures
