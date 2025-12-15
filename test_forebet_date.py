#!/usr/bin/env python3
"""
Test Forebet z datą meczu - sprawdza czy mecze są pobierane dla konkretnej daty.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from forebet_scraper import search_forebet_prediction

# Test z datą dzisiejszą i jutrzejszą
today = datetime.now().strftime('%Y-%m-%d')
tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')

print("=" * 60)
print(f"TEST FOREBET Z DATĄ")
print("=" * 60)

# Testowe mecze - weź przykładowe z logów
test_matches = [
    ("Club Brugge", "Antwerp", tomorrow),
    ("Genk", "OH Leuven", tomorrow),
    ("Gent", "St. Truiden", tomorrow),
    ("Liverpool", "Real Madrid", today),  # Test z dzisiaj
]

for home, away, date in test_matches:
    print(f"\n{'='*50}")
    print(f"🔍 Szukam: {home} vs {away} (data: {date})")
    print(f"{'='*50}")
    
    result = search_forebet_prediction(
        home_team=home,
        away_team=away,
        match_date=date,
        min_similarity=0.5,  # Niższy threshold dla testów
        timeout=30,
        sport='football'
    )
    
    if result['success']:
        print(f"✅ ZNALEZIONO!")
        print(f"   Prediction: {result['prediction']}")
        print(f"   Probability: {result['probability']}%")
        print(f"   Over/Under: {result['over_under']}")
        print(f"   BTTS: {result['btts']}")
    else:
        print(f"❌ NIE ZNALEZIONO: {result['error']}")

print("\n" + "=" * 60)
print("TEST ZAKOŃCZONY")
print("=" * 60)
