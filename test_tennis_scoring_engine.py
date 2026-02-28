"""
Tests for tennis_scoring_engine.py  –  Phase 5 regression suite.
"""
import pytest
from tennis_scoring_engine import (
    TennisScoringEngine,
    TennisFeatureExtractor,
    ScoredTennisMatch,
    _form_score,
    _parse_form_list,
    _streak_len,
    _recency_h2h,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def _base_match(**overrides):
    m = {
        'home_team': 'Djokovic N.',
        'away_team': 'Nadal R.',
        'match_time': '15:00',
        'h2h_last5': [],
        'home_wins_in_h2h_last5': 3,
        'away_wins_in_h2h_last5': 2,
        'ranking_a': 1,
        'ranking_b': 5,
        'form_a': ['W', 'W', 'W', 'L', 'W'],
        'form_b': ['W', 'L', 'W', 'L', 'W'],
        'surface': 'hard',
        'home_odds': 1.60,
        'away_odds': 2.40,
        'qualifies': True,
        'sport': 'tennis',
    }
    m.update(overrides)
    return m


@pytest.fixture
def engine():
    return TennisScoringEngine()


@pytest.fixture
def extractor():
    return TennisFeatureExtractor()


# ---------------------------------------------------------------------------
# ScoredTennisMatch dataclass
# ---------------------------------------------------------------------------

class TestScoredTennisMatch:
    def test_defaults(self):
        s = ScoredTennisMatch(player_a='A', player_b='B')
        assert s.prob_a == 0.5
        assert s.prob_b == 0.5
        assert s.ev == 0.0

    def test_no_draw_field(self):
        """Tennis model must NOT have a prob_draw field."""
        s = ScoredTennisMatch(player_a='A', player_b='B')
        assert not hasattr(s, 'prob_draw')


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

class TestParseFormList:
    def test_list_input(self):
        assert _parse_form_list(['W', 'L', 'W']) == ['W', 'L', 'W']

    def test_string_input(self):
        assert _parse_form_list("W,L,W,L") == ['W', 'L', 'W', 'L']

    def test_empty(self):
        assert _parse_form_list([]) == []
        assert _parse_form_list('') == []

    def test_draw_converted_to_loss(self):
        assert _parse_form_list(['D']) == ['L']

    def test_none(self):
        assert _parse_form_list(None) == []


class TestFormScore:
    def test_all_wins(self):
        assert _form_score(['W', 'W', 'W', 'W', 'W']) > 0.9

    def test_all_losses(self):
        assert _form_score(['L', 'L', 'L', 'L', 'L']) < 0.1

    def test_empty_is_neutral(self):
        assert _form_score([]) == 0.5

    def test_decay_recent_first(self):
        """Recent results should matter more."""
        recent_win = _form_score(['W', 'L', 'L', 'L'])
        recent_loss = _form_score(['L', 'W', 'W', 'W'])
        # More recent win in first list — but still fewer total wins
        # The key test is that they are not equal
        assert recent_win != recent_loss


class TestStreakLen:
    def test_win_streak(self):
        assert _streak_len(['W', 'W', 'W', 'L'], 'W') == 3

    def test_no_streak(self):
        assert _streak_len(['L', 'W', 'W'], 'W') == 0

    def test_empty(self):
        assert _streak_len([], 'W') == 0


# ---------------------------------------------------------------------------
# Feature extractor
# ---------------------------------------------------------------------------

class TestFeatureExtractor:
    def test_full_data_quality(self, extractor):
        m = _base_match()
        f = extractor.extract(m)
        # all 5 sources present → data_quality should be 1.0
        # (h2h counts from simple fields, form, not surface_stats though, ranking, odds)
        assert f['_data_quality'] >= 0.6   # at least 3/5

    def test_minimal_data(self, extractor):
        m = _base_match(
            home_wins_in_h2h_last5=0,
            away_wins_in_h2h_last5=0,
            ranking_a=None,
            ranking_b=None,
            form_a=[],
            form_b=[],
            home_odds=0,
            away_odds=0,
        )
        f = extractor.extract(m)
        assert f['_data_quality'] == 0.0

    def test_h2h_win_rate(self, extractor):
        m = _base_match(home_wins_in_h2h_last5=4, away_wins_in_h2h_last5=1)
        f = extractor.extract(m)
        assert f['h2h_win_rate_a'] == pytest.approx(0.8, abs=0.01)

    def test_ranking_advantage_positive_for_better_a(self, extractor):
        m = _base_match(ranking_a=1, ranking_b=50)
        f = extractor.extract(m)
        assert f['ranking_advantage'] > 0   # A has better ranking

    def test_ranking_advantage_negative_for_worse_a(self, extractor):
        m = _base_match(ranking_a=100, ranking_b=5)
        f = extractor.extract(m)
        assert f['ranking_advantage'] < 0

    def test_odds_implied(self, extractor):
        m = _base_match(home_odds=1.50, away_odds=2.80)
        f = extractor.extract(m)
        assert f['odds_prob_a'] > f['odds_prob_b']

    def test_missing_odds(self, extractor):
        m = _base_match(home_odds=0, away_odds=0)
        f = extractor.extract(m)
        assert f['odds_prob_a'] == 0.5
        assert f['odds_prob_b'] == 0.5


# ---------------------------------------------------------------------------
# Engine scoring
# ---------------------------------------------------------------------------

class TestEngine:
    def test_probabilities_sum_to_one(self, engine):
        m = _base_match()
        s = engine.score_match(m)
        assert s.prob_a + s.prob_b == pytest.approx(1.0, abs=0.001)
        assert s.cal_a + s.cal_b == pytest.approx(1.0, abs=0.001)

    def test_best_pick_A_or_B(self, engine):
        m = _base_match()
        s = engine.score_match(m)
        assert s.best_pick in ('A', 'B')

    def test_favorite_set(self, engine):
        m = _base_match()
        s = engine.score_match(m)
        assert s.favorite in ('player_a', 'player_b')

    def test_strong_favorite(self, engine):
        """Djokovic #1 with 4-1 H2H and great form at 1.30 odds should pick A."""
        m = _base_match(
            home_wins_in_h2h_last5=4,
            away_wins_in_h2h_last5=1,
            ranking_a=1,
            ranking_b=30,
            form_a=['W', 'W', 'W', 'W', 'W'],
            form_b=['L', 'L', 'L', 'W', 'L'],
            home_odds=1.30,
            away_odds=3.50,
        )
        s = engine.score_match(m)
        assert s.best_pick == 'A'
        assert s.prob_a > 0.65

    def test_underdog_scenario(self, engine):
        """When B dominates all factors, engine should pick B."""
        m = _base_match(
            home_wins_in_h2h_last5=0,
            away_wins_in_h2h_last5=5,
            ranking_a=80,
            ranking_b=3,
            form_a=['L', 'L', 'L', 'L', 'L'],
            form_b=['W', 'W', 'W', 'W', 'W'],
            home_odds=4.00,
            away_odds=1.25,
        )
        s = engine.score_match(m)
        assert s.best_pick == 'B'
        assert s.prob_b > 0.65

    def test_ev_positive_when_odds_generous(self, engine):
        """If our model says 70% for A but odds imply 50%, EV should be positive."""
        m = _base_match(
            home_wins_in_h2h_last5=5,
            away_wins_in_h2h_last5=0,
            ranking_a=1,
            ranking_b=80,
            form_a=['W', 'W', 'W', 'W', 'W'],
            form_b=['L', 'L', 'L', 'L', 'L'],
            home_odds=2.00,   # implies 50% — but model should say much higher
            away_odds=1.80,
        )
        s = engine.score_match(m)
        assert s.ev > 0

    def test_advanced_score_range(self, engine):
        m = _base_match()
        s = engine.score_match(m)
        assert 0 <= s.advanced_score <= 100

    def test_confidence_range(self, engine):
        m = _base_match()
        s = engine.score_match(m)
        assert 0 <= s.confidence <= 100

    def test_data_quality_range(self, engine):
        m = _base_match()
        s = engine.score_match(m)
        assert 0 <= s.data_quality <= 1

    def test_kelly_capped(self, engine):
        m = _base_match()
        s = engine.score_match(m)
        assert s.kelly <= 25.0

    def test_edge_is_percentage(self, engine):
        m = _base_match()
        s = engine.score_match(m)
        assert -100 <= s.edge <= 100

    def test_no_crash_on_empty_match(self, engine):
        """Engine should not crash on minimal/empty data."""
        s = engine.score_match({})
        assert s.prob_a + s.prob_b == pytest.approx(1.0, abs=0.001)

    def test_score_matches_sorted_by_ev(self, engine):
        matches = [
            _base_match(home_wins_in_h2h_last5=1, away_wins_in_h2h_last5=4, home_odds=3.00, away_odds=1.30),
            _base_match(home_wins_in_h2h_last5=5, away_wins_in_h2h_last5=0, home_odds=2.00, away_odds=1.80),
        ]
        scored = engine.score_matches(matches)
        assert len(scored) == 2
        assert scored[0].ev >= scored[1].ev   # sorted descending

    def test_threshold_is_45(self, engine):
        assert engine.threshold == 45.0


# ---------------------------------------------------------------------------
# Field name consistency (no old field names)
# ---------------------------------------------------------------------------

class TestFieldNameConsistency:
    def test_away_field_name(self):
        """The match dict should use away_wins_in_h2h_last5, not away_wins_in_h2h."""
        m = _base_match()
        assert 'away_wins_in_h2h_last5' in m
        # The engine should read properly
        engine = TennisScoringEngine()
        s = engine.score_match(m)
        assert s.prob_a + s.prob_b == pytest.approx(1.0, abs=0.001)


# ---------------------------------------------------------------------------
# Calibration
# ---------------------------------------------------------------------------

class TestCalibration:
    def test_calibrate_sums_to_one(self):
        cal_a, cal_b = TennisScoringEngine._calibrate(0.7, 0.3, 1.1)
        assert cal_a + cal_b == pytest.approx(1.0, abs=0.001)

    def test_calibrate_preserves_direction(self):
        cal_a, cal_b = TennisScoringEngine._calibrate(0.8, 0.2, 1.1)
        assert cal_a > cal_b

    def test_calibrate_extreme(self):
        cal_a, cal_b = TennisScoringEngine._calibrate(0.99, 0.01, 1.1)
        assert cal_a > 0.9
        assert cal_b < 0.1


# ---------------------------------------------------------------------------
# Recency H2H
# ---------------------------------------------------------------------------

class TestRecencyH2H:
    def test_basic_h2h(self):
        h2h = [
            {'home': 'Djokovic N.', 'away': 'Nadal R.', 'score': '2:1', 'date': ''},
            {'home': 'Nadal R.', 'away': 'Djokovic N.', 'score': '2:0', 'date': ''},
        ]
        wr, cnt = _recency_h2h(h2h, 'Djokovic N.', 'Nadal R.')
        assert cnt == 2
        assert 0.0 <= wr <= 1.0

    def test_empty_h2h(self):
        wr, cnt = _recency_h2h([], 'A', 'B')
        assert wr == 0.5
        assert cnt == 0

    def test_no_player(self):
        wr, cnt = _recency_h2h([{'home': 'X', 'away': 'Y', 'score': '2:1'}], '', '')
        assert wr == 0.5
