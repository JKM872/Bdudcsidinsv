#!/usr/bin/env python3
"""
Test SofaScore Scraper v3.0
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sofascore_scraper import scrape_sofascore_full, format_votes_for_display

# Test mecze
test_matches = [
    ("Fenerbahce", "Galatasaray", "football"),
    ("Motor Lublin", "Legia Warszawa", "football"),
    ("Bologna", "Cremonese", "football"),
]

print("=" * 60)
print("TEST SOFASCORE SCRAPER v3.0")
print("=" * 60)

for home, away, sport in test_matches:
    print(f"\n{'='*50}")
    print(f"🔍 Test: {home} vs {away} ({sport})")
    print(f"{'='*50}")
    
    result = scrape_sofascore_full(
        home_team=home,
        away_team=away,
        sport=sport,
        use_cache=False  # Bez cache dla testów
    )
    
    print(f"\n📊 Wynik:")
    print(f"   Found: {result.get('sofascore_found')}")
    print(f"   Home Win: {result.get('sofascore_home_win_prob')}%")
    print(f"   Draw: {result.get('sofascore_draw_prob')}%")
    print(f"   Away Win: {result.get('sofascore_away_win_prob')}%")
    print(f"   Votes: {result.get('sofascore_total_votes')}")
    print(f"   URL: {result.get('sofascore_url')}")
    print(f"\n   {format_votes_for_display(result)}")

print("\n" + "=" * 60)
print("TEST ZAKOŃCZONY")
print("=" * 60)
