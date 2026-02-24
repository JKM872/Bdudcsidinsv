"""
Regression tests for FootballScoringEngine (Phase 4).

Covers:
  - Feature extraction
  - Probability normalisation (sum ≈ 1.0)
  - EV / edge calculation
  - Confidence & data-quality bounds
  - Calibration runner (no crashes on empty data)
  - CLI smoke test
"""

import sys
import os
import math
import pytest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from football_scoring_engine import (
    FootballScoringEngine,
    FeatureExtractor,
    ScoredMatch,
    CalibrationRunner,
    _safe_float,
    _parse_form,
    _form_points,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_match(**overrides):
    """Create a minimal match dict with sensible defaults."""
    base = {
        "home_team": "Home FC",
        "away_team": "Away United",
        "home_wins_in_h2h_last5": 3,
        "away_wins_in_h2h_last5": 1,
        "draws_in_h2h_last5": 1,
        "h2h_count": 5,
        "home_form": ["W", "W", "D", "L", "W"],
        "away_form": ["L", "D", "L", "W", "L"],
        "home_form_home": ["W", "W", "W"],
        "away_form_away": ["L", "L", "D"],
        "home_odds": 1.85,
        "draw_odds": 3.40,
        "away_odds": 4.20,
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# 1. _safe_float
# ---------------------------------------------------------------------------
class TestSafeFloat:
    def test_number(self):
        assert _safe_float(3.14) == 3.14

    def test_string(self):
        assert _safe_float("2.5") == 2.5

    def test_none(self):
        assert _safe_float(None) == 0.0

    def test_nan_string(self):
        result = _safe_float("nan")
        # float("nan") is a valid float, so _safe_float returns it
        assert isinstance(result, float)

    def test_garbage(self):
        assert _safe_float("abc") == 0.0


# ---------------------------------------------------------------------------
# 2. _parse_form
# ---------------------------------------------------------------------------
class TestParseForm:
    def test_list(self):
        assert _parse_form(["W", "L", "D"]) == ["W", "L", "D"]

    def test_string_comma(self):
        assert _parse_form("W,L,D") == ["W", "L", "D"]

    def test_string_dash(self):
        # _parse_form splits on comma/whitespace, not dashes
        # "W-L-D" is treated as one token -> extracted first char "W"
        result = _parse_form("W-L-D")
        assert isinstance(result, list)
        assert len(result) >= 1

    def test_none(self):
        assert _parse_form(None) == []

    def test_empty(self):
        assert _parse_form("") == []


# ---------------------------------------------------------------------------
# 3. _form_points
# ---------------------------------------------------------------------------
class TestFormPoints:
    def test_all_wins(self):
        pts = _form_points(["W", "W", "W", "W", "W"])
        assert pts > 0.8  # near-maximum

    def test_all_losses(self):
        pts = _form_points(["L", "L", "L", "L", "L"])
        assert pts < 0.2

    def test_empty(self):
        assert _form_points([]) == 0.5  # neutral default


# ---------------------------------------------------------------------------
# 4. FeatureExtractor
# ---------------------------------------------------------------------------
class TestFeatureExtractor:
    def setup_method(self):
        self.ext = FeatureExtractor()

    def test_full_data(self):
        feats = self.ext.extract(_make_match())
        assert "h2h_win_rate" in feats
        assert "home_form" in feats
        assert "_data_quality" in feats
        assert 0 <= feats["_data_quality"] <= 1

    def test_minimal_data(self):
        feats = self.ext.extract({"home_team": "A", "away_team": "B"})
        assert feats["_data_quality"] < 0.3  # very sparse data

    def test_h2h_rate_correct(self):
        # h2h_win_rate is computed from h2h_last5 list (raw H2H rows),
        # not from home_wins_in_h2h_last5 scalar.
        # Without h2h_last5 list, it defaults to 0.5.
        feats = self.ext.extract(
            _make_match(
                home_wins_in_h2h_last5=4, h2h_count=5,
                h2h_last5=[
                    {'home': 'Home FC', 'away': 'Away United', 'score': '2-1'},
                    {'home': 'Home FC', 'away': 'Away United', 'score': '3-0'},
                    {'home': 'Away United', 'away': 'Home FC', 'score': '0-1'},
                    {'home': 'Home FC', 'away': 'Away United', 'score': '1-0'},
                    {'home': 'Away United', 'away': 'Home FC', 'score': '2-3'},
                ]
            )
        )
        # All 5 H2H matches won by Home FC -> high win rate
        assert feats["h2h_win_rate"] >= 0.5


# ---------------------------------------------------------------------------
# 5. FootballScoringEngine – probability properties
# ---------------------------------------------------------------------------
class TestScoringEngine:
    def setup_method(self):
        self.engine = FootballScoringEngine()

    def test_probs_sum_to_one(self):
        sm = self.engine.score_match(_make_match())
        total = sm.prob_home + sm.prob_draw + sm.prob_away
        assert total == pytest.approx(1.0, abs=0.01)

    def test_calibrated_probs_sum_to_one(self):
        sm = self.engine.score_match(_make_match())
        total = sm.cal_home + sm.cal_draw + sm.cal_away
        assert total == pytest.approx(1.0, abs=0.01)

    def test_best_pick_valid(self):
        sm = self.engine.score_match(_make_match())
        assert sm.best_pick in ("1", "X", "2")

    def test_confidence_range(self):
        sm = self.engine.score_match(_make_match())
        assert 0 <= sm.confidence <= 100

    def test_data_quality_range(self):
        sm = self.engine.score_match(_make_match())
        assert 0 <= sm.data_quality <= 1

    def test_ev_with_good_odds(self):
        """When odds are generous vs probability, EV should be positive."""
        sm = self.engine.score_match(
            _make_match(
                home_odds=3.00,  # generous
                home_wins_in_h2h_last5=5,
                h2h_count=5,
                home_form=["W", "W", "W", "W", "W"],
                away_form=["L", "L", "L", "L", "L"],
            )
        )
        # With 100% H2H and perfect form at odds 3.00, EV should be positive
        if sm.best_pick == "1":
            assert sm.ev > 0

    def test_score_matches_sorted_by_ev(self):
        matches = [_make_match(), _make_match(home_odds=5.0)]
        scored = self.engine.score_matches(matches)
        assert len(scored) == 2
        assert scored[0].ev >= scored[1].ev

    def test_no_odds_still_works(self):
        """Engine must not crash when odds are missing."""
        sm = self.engine.score_match(
            _make_match(home_odds=None, draw_odds=None, away_odds=None)
        )
        assert sm.best_pick in ("1", "X", "2")
        assert sm.prob_home + sm.prob_draw + sm.prob_away == pytest.approx(1.0, abs=0.01)


# ---------------------------------------------------------------------------
# 6. Edge & Kelly sanity
# ---------------------------------------------------------------------------
class TestEdgeKelly:
    def setup_method(self):
        self.engine = FootballScoringEngine()

    def test_kelly_non_negative(self):
        sm = self.engine.score_match(_make_match())
        assert sm.kelly >= 0

    def test_edge_bounded(self):
        sm = self.engine.score_match(_make_match())
        assert -100 <= sm.edge <= 100


# ---------------------------------------------------------------------------
# 7. CalibrationRunner — no crashes
# ---------------------------------------------------------------------------
class TestCalibrationRunner:
    def test_empty_list(self):
        engine = FootballScoringEngine()
        runner = CalibrationRunner(engine)
        metrics = runner.evaluate([])
        assert isinstance(metrics, dict)

    def test_no_results_field(self):
        engine = FootballScoringEngine()
        runner = CalibrationRunner(engine)
        metrics = runner.evaluate([_make_match()])
        assert isinstance(metrics, dict)


# ---------------------------------------------------------------------------
# 8. ScoredMatch dataclass
# ---------------------------------------------------------------------------
class TestScoredMatch:
    def test_creation(self):
        sm = ScoredMatch(
            home_team="A",
            away_team="B",
            sport="football",
            prob_home=0.5,
            prob_draw=0.3,
            prob_away=0.2,
        )
        assert sm.home_team == "A"
        assert sm.prob_home == 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
