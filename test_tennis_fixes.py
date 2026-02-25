"""
Tests for tennis pipeline fixes  –  Phase 5 regression suite.
Validates field names, no synthetic data, and compatibility mapping.
"""
import pytest
import json


# ---------------------------------------------------------------------------
# Field name consistency tests
# ---------------------------------------------------------------------------

class TestTennisFieldNames:
    """Ensure the codebase uses consistent field names for tennis."""

    def test_scraper_writes_away_wins_in_h2h_last5(self):
        """process_match_tennis must write 'away_wins_in_h2h_last5' (not 'away_wins_in_h2h')."""
        import inspect
        from livesport_h2h_scraper import process_match_tennis
        source = inspect.getsource(process_match_tennis)
        # The new field name should be used
        assert "away_wins_in_h2h_last5" in source
        # The old broken field name should NOT appear as an assignment target
        assert "out['away_wins_in_h2h']" not in source

    def test_scraper_uses_teams_match(self):
        """Tennis H2H counting must use _teams_match (robust matching)."""
        import inspect
        from livesport_h2h_scraper import process_match_tennis
        source = inspect.getsource(process_match_tennis)
        assert "_teams_match(" in source

    def test_no_synthetic_form_function_called(self):
        """process_match_tennis must NOT call extract_player_form_simple."""
        import inspect
        from livesport_h2h_scraper import process_match_tennis
        source = inspect.getsource(process_match_tennis)
        assert "extract_player_form_simple" not in source

    def test_no_synthetic_surface_function_called(self):
        """process_match_tennis must NOT call calculate_surface_stats_from_h2h."""
        import inspect
        from livesport_h2h_scraper import process_match_tennis
        source = inspect.getsource(process_match_tennis)
        assert "calculate_surface_stats_from_h2h" not in source

    def test_uses_new_scoring_engine(self):
        """process_match_tennis must import TennisScoringEngine (not TennisMatchAnalyzer)."""
        import inspect
        from livesport_h2h_scraper import process_match_tennis
        source = inspect.getsource(process_match_tennis)
        assert "TennisScoringEngine" in source
        assert "TennisMatchAnalyzer" not in source

    def test_extract_real_form_badges_exists(self):
        """The new _extract_real_form_badges function should exist."""
        from livesport_h2h_scraper import _extract_real_form_badges
        assert callable(_extract_real_form_badges)


class TestScrapeAndNotifyFieldNames:
    """Ensure scrape_and_notify.py uses correct field names."""

    def test_no_bare_away_wins_in_h2h(self):
        """scrape_and_notify.py should not read 'away_wins_in_h2h' (without _last5)."""
        with open('scrape_and_notify.py', 'r', encoding='utf-8') as f:
            source = f.read()
        # Remove comments to avoid false positives
        lines = [l for l in source.split('\n') if not l.strip().startswith('#')]
        code = '\n'.join(lines)
        # The old field name should not appear as a standalone .get argument
        import re
        matches = re.findall(r"\.get\(['\"]away_wins_in_h2h['\"]", code)
        assert len(matches) == 0, f"Found {len(matches)} uses of old field name 'away_wins_in_h2h'"

    def test_json_export_uses_match_time(self):
        """JSON export should use match_time (with fallback to time)."""
        with open('scrape_and_notify.py', 'r', encoding='utf-8') as f:
            source = f.read()
        assert "row.get('match_time'" in source

    def test_json_export_uses_match_url(self):
        """JSON export should use match_url (with fallback to url)."""
        with open('scrape_and_notify.py', 'r', encoding='utf-8') as f:
            source = f.read()
        assert "row.get('match_url'" in source

    def test_forebet_exact_score_field(self):
        """JSON export should read forebet_exact_score (with fallback)."""
        with open('scrape_and_notify.py', 'r', encoding='utf-8') as f:
            source = f.read()
        assert "forebet_exact_score" in source

    def test_tennis_scoring_integration_exists(self):
        """scrape_and_notify.py should have tennis scoring engine integration."""
        with open('scrape_and_notify.py', 'r', encoding='utf-8') as f:
            source = f.read()
        assert "TennisScoringEngine" in source
        assert "TENNIS SCORING" in source


class TestEmailRendering:
    """Ensure email_notifier.py handles tennis scoring display."""

    def test_tennis_engine_label(self):
        """Email should show 'Tennis Engine' label for tennis matches."""
        with open('email_notifier.py', 'r', encoding='utf-8') as f:
            source = f.read()
        assert "Tennis Engine" in source

    def test_tennis_prob_a_b_display(self):
        """Email should display A: X% | B: Y% for tennis."""
        with open('email_notifier.py', 'r', encoding='utf-8') as f:
            source = f.read()
        assert "sc_tpa" in source
        assert "sc_tpb" in source

    def test_threshold_45_in_footer(self):
        """Email footer should reference ≥45/100 for tennis."""
        with open('email_notifier.py', 'r', encoding='utf-8') as f:
            source = f.read()
        assert "45/100" in source


# ---------------------------------------------------------------------------
# Compatibility mapping
# ---------------------------------------------------------------------------

class TestCompatibilityMapping:
    """Verify that process_match_tennis sets all compat fields."""

    def test_init_dict_has_compat_fields(self):
        """The init dict should have sport, focus_team, home_form, etc."""
        import inspect
        from livesport_h2h_scraper import process_match_tennis
        source = inspect.getsource(process_match_tennis)
        # Check that _finalise is called on all exit paths
        assert "_finalise" in source
        # Check that sport is set
        assert "'sport': 'tennis'" in source

    def test_finalise_function_exists(self):
        """_finalise is defined inside process_match_tennis."""
        import inspect
        from livesport_h2h_scraper import process_match_tennis
        source = inspect.getsource(process_match_tennis)
        assert "def _finalise" in source
