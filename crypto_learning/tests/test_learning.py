from learning.governance import PromotionPolicy, evaluate_candidate, promote
from learning.schemas import EvaluationResult
from learning.validation import purge_overlapping_labels, time_split


def result(version, ba=.6, ret=2, dd=20, n=300, approved=True):
    return EvaluationResult(version, n, .7, .6, ba, ret, dd, approved, ())


def test_temporal_split_has_no_reordering():
    rows = [{"observed_at": x} for x in ["2026-01-03", "2026-01-01", "2026-01-02", "2026-01-04"]]
    train, val, test = time_split(rows)
    assert [r["observed_at"] for r in train] == ["2026-01-01", "2026-01-02"]
    assert [r["observed_at"] for r in val] == ["2026-01-03"]
    assert [r["observed_at"] for r in test] == ["2026-01-04"]


def test_embargo():
    rows = [{"observed_at": str(i)} for i in range(5)]
    assert len(purge_overlapping_labels(rows, 1)) == 4


def test_candidate_gate():
    bad = evaluate_candidate(result("c", ba=.4, ret=2, dd=20))
    assert not bad.approved
    assert "balanced_accuracy_below_gate" in bad.reasons


def test_promotion_requires_strict_improvement():
    champion = result("champion", ba=.60, ret=2, dd=20)
    challenger = evaluate_candidate(result("challenger", ba=.65, ret=3, dd=18))
    assert promote(champion, challenger)
    assert not promote(champion, evaluate_candidate(result("same", ba=.60, ret=2, dd=20)))


def test_policy_can_be_stricter():
    candidate = evaluate_candidate(result("c", ba=.8, ret=1, dd=10, n=100), PromotionPolicy(min_samples=200))
    assert not candidate.approved
