"""
Auth Middleware for Flask API
-----------------------------
Validates Supabase JWTs for protected endpoints.

Usage:
    from auth_middleware import require_auth

    @app.route('/api/bets', methods=['POST'])
    @require_auth
    def create_bet():
        user_id = request.user_id   # set by middleware
        ...
"""

import os
import functools
import jwt
from flask import request, jsonify

# Supabase JWT secret — the same as your project's JWT secret
# Found in Supabase Dashboard → Settings → API → JWT Secret
SUPABASE_JWT_SECRET = os.environ.get('SUPABASE_JWT_SECRET', '')


def _decode_token(token: str) -> dict | None:
    """Decode and verify a Supabase JWT. Returns payload or None."""
    if not SUPABASE_JWT_SECRET:
        # If no secret configured, skip auth (development mode)
        return {'sub': 'anonymous', 'role': 'anon'}

    try:
        payload = jwt.decode(
            token,
            SUPABASE_JWT_SECRET,
            algorithms=['HS256'],
            audience='authenticated',
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def require_auth(fn):
    """Decorator: reject requests without a valid Supabase JWT."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if not auth_header.startswith('Bearer '):
            # Allow unauthenticated in dev when no JWT secret is set
            if not SUPABASE_JWT_SECRET:
                request.user_id = 'anonymous'  # type: ignore[attr-defined]
                return fn(*args, **kwargs)
            return jsonify({'error': 'Missing Authorization header'}), 401

        token = auth_header.split(' ', 1)[1]
        payload = _decode_token(token)

        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Attach user id to request context
        request.user_id = payload.get('sub', 'anonymous')  # type: ignore[attr-defined]
        return fn(*args, **kwargs)

    return wrapper


def optional_auth(fn):
    """Decorator: parse JWT if present but don't reject unauthenticated."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', '')

        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ', 1)[1]
            payload = _decode_token(token)
            request.user_id = payload.get('sub', 'anonymous') if payload else 'anonymous'  # type: ignore[attr-defined]
        else:
            request.user_id = 'anonymous'  # type: ignore[attr-defined]

        return fn(*args, **kwargs)

    return wrapper
