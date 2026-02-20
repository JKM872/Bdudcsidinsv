"""
test_health.py – health check, root, and basic route tests.
"""
import json
import pytest


class TestHealth:
    def test_health_returns_200(self, client):
        resp = client.get('/api/health')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data['status'] == 'ok'
        assert 'timestamp' in data

    def test_health_has_supabase_flag(self, client):
        data = client.get('/api/health').get_json()
        assert 'supabaseAvailable' in data

    def test_root_returns_200(self, client):
        resp = client.get('/')
        assert resp.status_code == 200


class TestStandingsLeagues:
    def test_leagues_list(self, client):
        resp = client.get('/api/standings/leagues')
        assert resp.status_code == 200
        data = resp.get_json()
        codes = [l['code'] for l in data['leagues']]
        assert 'PL' in codes
        assert 'PD' in codes
        assert 'BL1' in codes

    def test_standings_no_api_key_returns_503(self, client):
        """Without FOOTBALL_DATA_API_KEY, standings should return 503."""
        resp = client.get('/api/standings?league=PL')
        assert resp.status_code == 503

    def test_standings_invalid_league_returns_400(self, client):
        import os
        os.environ['FOOTBALL_DATA_API_KEY'] = 'test-key'
        resp = client.get('/api/standings?league=INVALID')
        assert resp.status_code == 400
        os.environ.pop('FOOTBALL_DATA_API_KEY', None)


class TestSports:
    def test_sports_returns_list(self, client):
        resp = client.get('/api/sports')
        assert resp.status_code == 200
        data = resp.get_json()
        # Endpoint returns a JSON array directly
        assert isinstance(data, list)
        ids = [s['id'] for s in data]
        assert 'all' in ids
        assert 'football' in ids


class TestDates:
    def test_dates_returns_list(self, client):
        resp = client.get('/api/dates')
        assert resp.status_code == 200
        data = resp.get_json()
        assert 'dates' in data
        assert isinstance(data['dates'], list)
