"""
conftest.py – shared fixtures for the professional test suite.
"""

import os
import sys
import json
import pytest

# Ensure project root is on the path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


@pytest.fixture()
def app():
    """Create a Flask test app with Supabase disabled (pure in-memory)."""
    import importlib

    # Prevent real Supabase connections during tests
    os.environ.pop('SUPABASE_URL', None)
    os.environ.pop('SUPABASE_KEY', None)
    os.environ.pop('SUPABASE_JWT_SECRET', None)
    os.environ.pop('FOOTBALL_DATA_API_KEY', None)

    # Reload auth_middleware so it sees empty JWT_SECRET (dev mode = anonymous OK)
    import auth_middleware
    importlib.reload(auth_middleware)

    import api_server as _mod
    importlib.reload(_mod)

    _mod.app.config['TESTING'] = True
    return _mod.app


@pytest.fixture()
def client(app):
    """Flask test client."""
    return app.test_client()


@pytest.fixture()
def sample_bet():
    """A minimal valid bet payload."""
    return {
        'home_team': 'Arsenal',
        'away_team': 'Chelsea',
        'match_date': '2025-06-15',
        'bet_selection': '1',
        'odds_at_bet': 1.85,
    }
