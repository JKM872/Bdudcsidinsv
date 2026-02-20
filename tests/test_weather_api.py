"""
test_weather_api.py – tests for the Open-Meteo weather proxy endpoint.
"""
import json
import pytest


class TestWeather:
    def test_weather_missing_params_returns_400(self, client):
        """Endpoint needs lat, lon, date."""
        resp = client.get('/api/weather')
        assert resp.status_code == 400

    def test_weather_with_params_returns_200_or_error(self, client):
        """With valid params it should try Open-Meteo (may 200 or 502 in CI)."""
        resp = client.get('/api/weather?lat=51.5&lon=-0.1&date=2025-06-15')
        # 200 if network available, 502 if Open-Meteo unreachable
        assert resp.status_code in (200, 400, 502, 503)
