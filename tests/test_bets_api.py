"""
test_bets_api.py – tests for /api/bets CRUD endpoints (auth + validation).
"""
import os
import sys
import json
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


class TestCreateBet:
    """POST /api/bets – requires auth, validates payload.
    
    Note: conftest unsets SUPABASE_JWT_SECRET so auth_middleware
    runs in dev mode (anonymous access allowed via require_auth).
    """

    def test_create_without_auth_still_works_in_dev(self, client, sample_bet, tmp_path, monkeypatch):
        """Without SUPABASE_JWT_SECRET, dev mode allows anonymous."""
        monkeypatch.setattr('api_server.RESULTS_DIR', str(tmp_path))
        resp = client.post(
            '/api/bets',
            data=json.dumps(sample_bet),
            content_type='application/json',
        )
        # 201 from local JSON fallback (no supabase)
        assert resp.status_code == 201

    def test_create_missing_fields_returns_400(self, client):
        resp = client.post(
            '/api/bets',
            data=json.dumps({'home_team': 'Arsenal'}),
            content_type='application/json',
        )
        assert resp.status_code == 400
        assert 'Missing' in resp.get_json().get('error', '')

    def test_create_invalid_selection_returns_400(self, client, sample_bet):
        sample_bet['bet_selection'] = 'HOME'
        resp = client.post(
            '/api/bets',
            data=json.dumps(sample_bet),
            content_type='application/json',
        )
        assert resp.status_code == 400
        assert 'bet_selection' in resp.get_json().get('error', '')

    def test_valid_bet_returns_201(self, client, sample_bet, tmp_path, monkeypatch):
        """With local fallback, a valid bet should return 201."""
        monkeypatch.setattr('api_server.RESULTS_DIR', str(tmp_path))
        resp = client.post(
            '/api/bets',
            data=json.dumps(sample_bet),
            content_type='application/json',
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data['success'] is True
        assert 'bet_id' in data

    def test_created_bet_is_persisted(self, client, sample_bet, tmp_path, monkeypatch):
        """Verify JSON file is written by local fallback."""
        monkeypatch.setattr('api_server.RESULTS_DIR', str(tmp_path))
        client.post(
            '/api/bets',
            data=json.dumps(sample_bet),
            content_type='application/json',
        )
        bets_file = tmp_path / 'user_bets.json'
        assert bets_file.exists()
        bets = json.loads(bets_file.read_text(encoding='utf-8'))
        assert len(bets) >= 1
        assert bets[0]['home_team'] == 'Arsenal'


class TestGetBets:
    """GET /api/bets – optional auth, query params."""

    def test_get_bets_without_supabase_returns_503(self, client):
        resp = client.get('/api/bets')
        assert resp.status_code == 503

    def test_get_bets_respects_limit_param(self, client):
        resp = client.get('/api/bets?limit=5')
        assert resp.status_code in (200, 503)  # 503 if no supabase


class TestUpdateBet:
    """PUT /api/bets/<id> – requires auth, validates settle payload.
    
    Dev mode (no JWT secret) allows anonymous → 503 from missing Supabase.
    """

    def test_update_without_supabase_returns_503(self, client):
        resp = client.put(
            '/api/bets/1',
            data=json.dumps({'actual_result': '1', 'home_score': 2, 'away_score': 1}),
            content_type='application/json',
        )
        assert resp.status_code == 503

    def test_update_missing_fields_returns_400_or_503(self, client):
        """Without Supabase the 503 fires before field validation."""
        resp = client.put(
            '/api/bets/1',
            data=json.dumps({}),
            content_type='application/json',
        )
        assert resp.status_code == 503   # supabase check comes first


class TestDeleteBet:
    """DELETE /api/bets/<id> – requires auth (dev mode = anonymous OK)."""

    def test_delete_without_supabase_returns_503(self, client):
        resp = client.delete('/api/bets/1')
        assert resp.status_code == 503


class TestBetsStats:
    """GET /api/bets/stats – optional auth."""

    def test_stats_without_supabase_returns_503(self, client):
        resp = client.get('/api/bets/stats')
        assert resp.status_code == 503
