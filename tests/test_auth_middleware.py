"""
test_auth_middleware.py – unit tests for JWT auth decorators.
"""
import os
import sys
import json
import time
import pytest
import jwt as pyjwt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)


JWT_SECRET = 'test-jwt-secret-for-tests-only'
TEST_USER_ID = 'aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee'


def _make_token(sub: str = TEST_USER_ID, exp_offset: int = 3600) -> str:
    """Build a valid Supabase-like JWT."""
    payload = {
        'sub': sub,
        'aud': 'authenticated',
        'role': 'authenticated',
        'iat': int(time.time()),
        'exp': int(time.time()) + exp_offset,
    }
    return pyjwt.encode(payload, JWT_SECRET, algorithm='HS256')


@pytest.fixture(autouse=True)
def _set_jwt_secret(monkeypatch):
    """Set the JWT secret for every test in this module."""
    monkeypatch.setenv('SUPABASE_JWT_SECRET', JWT_SECRET)

    # Reload auth_middleware so it picks up the new env var
    import importlib
    import auth_middleware
    importlib.reload(auth_middleware)


@pytest.fixture()
def auth_app():
    """Minimal Flask app with auth-protected routes for testing."""
    import importlib
    os.environ['SUPABASE_JWT_SECRET'] = JWT_SECRET
    import auth_middleware
    importlib.reload(auth_middleware)

    from flask import Flask, request, jsonify
    from auth_middleware import require_auth, optional_auth

    app = Flask(__name__)

    @app.route('/protected', methods=['GET'])
    @require_auth
    def protected():
        return jsonify({'user_id': request.user_id})

    @app.route('/optional', methods=['GET'])
    @optional_auth
    def optional():
        return jsonify({'user_id': request.user_id})

    app.config['TESTING'] = True
    return app.test_client()


class TestRequireAuth:
    def test_missing_header_returns_401(self, auth_app):
        resp = auth_app.get('/protected')
        assert resp.status_code == 401
        assert 'error' in resp.get_json()

    def test_invalid_token_returns_401(self, auth_app):
        resp = auth_app.get('/protected', headers={
            'Authorization': 'Bearer total-garbage-token',
        })
        assert resp.status_code == 401

    def test_expired_token_returns_401(self, auth_app):
        token = _make_token(exp_offset=-3600)  # already expired
        resp = auth_app.get('/protected', headers={
            'Authorization': f'Bearer {token}',
        })
        assert resp.status_code == 401

    def test_valid_token_passes(self, auth_app):
        token = _make_token()
        resp = auth_app.get('/protected', headers={
            'Authorization': f'Bearer {token}',
        })
        assert resp.status_code == 200
        assert resp.get_json()['user_id'] == TEST_USER_ID

    def test_wrong_secret_returns_401(self, auth_app):
        token = pyjwt.encode(
            {'sub': TEST_USER_ID, 'aud': 'authenticated',
             'exp': int(time.time()) + 3600},
            'wrong-secret', algorithm='HS256',
        )
        resp = auth_app.get('/protected', headers={
            'Authorization': f'Bearer {token}',
        })
        assert resp.status_code == 401


class TestOptionalAuth:
    def test_no_header_returns_anonymous(self, auth_app):
        resp = auth_app.get('/optional')
        assert resp.status_code == 200
        assert resp.get_json()['user_id'] == 'anonymous'

    def test_valid_token_returns_user_id(self, auth_app):
        token = _make_token()
        resp = auth_app.get('/optional', headers={
            'Authorization': f'Bearer {token}',
        })
        assert resp.status_code == 200
        assert resp.get_json()['user_id'] == TEST_USER_ID

    def test_invalid_token_falls_back_to_anonymous(self, auth_app):
        resp = auth_app.get('/optional', headers={
            'Authorization': 'Bearer bad-token',
        })
        assert resp.status_code == 200
        assert resp.get_json()['user_id'] == 'anonymous'
