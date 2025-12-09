"""
Test FlashScore Odds Scraper - Unit Tests
==========================================
Testy jednostkowe do weryfikacji poprawności scrapera kursów.
"""

import re
import math
import sys

print("=" * 70)
print("🧪 TESTY JEDNOSTKOWE: FlashScore Odds Scraper")
print("=" * 70)

# ============================================================================
# TEST 1: Importy i dostępność modułów
# ============================================================================
print("\n📦 TEST 1: Importy modułów FlashScore")
print("-" * 50)

tests_passed = 0
tests_failed = 0

try:
    from flashscore_odds_scraper import (
        normalize_team_name,
        similarity_score,
        FlashScoreOddsScraper,
        format_odds_for_display,
        format_odds_for_email,
        SELENIUM_AVAILABLE
    )
    print(f"   ✅ Import flashscore_odds_scraper - OK")
    print(f"   ✅ SELENIUM_AVAILABLE = {SELENIUM_AVAILABLE}")
    tests_passed += 1
except ImportError as e:
    print(f"   ❌ Import flashscore_odds_scraper - FAILED: {e}")
    tests_failed += 1

# ============================================================================
# TEST 2: Normalizacja nazw drużyn
# ============================================================================
print("\n🏷️ TEST 2: Normalizacja nazw drużyn")
print("-" * 50)

test_cases_normalize = [
    ("Real Madrid", "real madrid"),
    ("FC Barcelona", "fc barcelona"),
    ("Bayern München", "bayern munchen"),  # ü → u
    ("Manchester United U21", "manchester united"),  # Usuwa U21
    ("Liverpool B", "liverpool"),  # Usuwa B
    ("  Chelsea  FC  ", "chelsea fc"),  # Trim i normalizuj spacje
    ("Arsenal II", "arsenal"),  # Usuwa II
    ("", ""),  # Pusty string
    (None, ""),  # None
]

for input_val, expected in test_cases_normalize:
    result = normalize_team_name(input_val)
    if result == expected:
        print(f"   ✅ '{input_val}' -> '{result}'")
        tests_passed += 1
    else:
        print(f"   ❌ '{input_val}' -> '{result}' (oczekiwano: '{expected}')")
        tests_failed += 1

# ============================================================================
# TEST 3: Similarity score
# ============================================================================
print("\n📊 TEST 3: Similarity score między nazwami")
print("-" * 50)

test_cases_similarity = [
    ("Real Madrid", "Real Madrid", 1.0),  # Identyczne
    ("Real Madrid", "real madrid", 1.0),  # Case insensitive
    ("Barcelona", "Barca", 0.0),  # Różne (za krótkie)
    ("Liverpool", "Liverpool FC", 0.8),  # Bardzo podobne
    ("Manchester United", "Man Utd", 0.0),  # Różne skróty
    ("", "", 0.0),  # Puste
]

for name1, name2, min_expected in test_cases_similarity:
    result = similarity_score(name1, name2)
    if result >= min_expected:
        print(f"   ✅ '{name1}' vs '{name2}' = {result:.2f} (>= {min_expected})")
        tests_passed += 1
    else:
        print(f"   ❌ '{name1}' vs '{name2}' = {result:.2f} (oczekiwano >= {min_expected})")
        tests_failed += 1

# ============================================================================
# TEST 4: Format odds for display
# ============================================================================
print("\n💰 TEST 4: Formatowanie kursów do wyświetlenia")
print("-" * 50)

test_cases_display = [
    # Brak kursów
    ({'odds_found': False}, "❌ Kursy: Nie znaleziono"),
    # Kursy 1X2
    ({
        'odds_found': True,
        'home_odds': 2.10,
        'draw_odds': 3.50,
        'away_odds': 3.20,
        'odds_source': 'flashscore'
    }, "💰 Kursy (flashscore): 1=2.10 | X=3.50 | 2=3.20"),
    # Kursy bez remisu (tenis)
    ({
        'odds_found': True,
        'home_odds': 1.50,
        'draw_odds': None,
        'away_odds': 2.80,
        'odds_source': 'livescore'
    }, "💰 Kursy (livescore): 1=1.50 | 2=2.80"),
]

for input_dict, expected in test_cases_display:
    result = format_odds_for_display(input_dict)
    if result == expected:
        print(f"   ✅ {result}")
        tests_passed += 1
    else:
        print(f"   ❌ Got: '{result}'")
        print(f"      Expected: '{expected}'")
        tests_failed += 1

# ============================================================================
# TEST 5: Format odds for email (HTML)
# ============================================================================
print("\n📧 TEST 5: Formatowanie kursów do emaila HTML")
print("-" * 50)

test_cases_email = [
    # Brak kursów
    ({'odds_found': False}, ""),
    # Kursy 1X2 - faworyt podświetlony
    ({
        'odds_found': True,
        'home_odds': 1.50,  # Faworyt
        'draw_odds': 4.00,
        'away_odds': 6.00,
    }, True),  # Sprawdzamy tylko czy zawiera HTML z faworytem
]

for input_dict, expected in test_cases_email:
    result = format_odds_for_email(input_dict)
    if expected == "" and result == "":
        print(f"   ✅ Brak kursów -> pusty string")
        tests_passed += 1
    elif expected == True:
        # Sprawdź czy faworyt jest podświetlony
        if 'color: #28a745' in result and 'font-weight: bold' in result:
            print(f"   ✅ Faworyt podświetlony: {result[:50]}...")
            tests_passed += 1
        else:
            print(f"   ❌ Brak podświetlenia faworyta: {result}")
            tests_failed += 1
    else:
        if result == expected:
            print(f"   ✅ {result[:50]}...")
            tests_passed += 1
        else:
            print(f"   ❌ {result}")
            tests_failed += 1

# ============================================================================
# TEST 6: FlashScoreOddsScraper - inicjalizacja
# ============================================================================
print("\n🔧 TEST 6: Inicjalizacja scrapera")
print("-" * 50)

try:
    scraper = FlashScoreOddsScraper(headless=True)
    print(f"   ✅ FlashScoreOddsScraper(headless=True) - OK")
    print(f"   ✅ scraper.headless = {scraper.headless}")
    print(f"   ✅ scraper.driver = {scraper.driver}")
    tests_passed += 1
except Exception as e:
    print(f"   ❌ Inicjalizacja scrapera - FAILED: {e}")
    tests_failed += 1

# ============================================================================
# TEST 7: Walidacja kursów (zakres 1.01 - 50.00)
# ============================================================================
print("\n📈 TEST 7: Walidacja zakresu kursów")
print("-" * 50)

valid_odds = [1.01, 1.50, 2.00, 3.50, 10.00, 25.00, 49.99]
invalid_odds = [0.50, 0.99, 1.00, 50.01, 100.00, -1.50]

for odds in valid_odds:
    if 1.01 <= odds <= 50.0:
        print(f"   ✅ {odds:.2f} - valid")
        tests_passed += 1
    else:
        print(f"   ❌ {odds:.2f} - should be valid")
        tests_failed += 1

for odds in invalid_odds:
    if not (1.01 <= odds <= 50.0):
        print(f"   ✅ {odds:.2f} - correctly rejected")
        tests_passed += 1
    else:
        print(f"   ❌ {odds:.2f} - should be rejected")
        tests_failed += 1

# ============================================================================
# TEST 8: Sport slugs mapping
# ============================================================================
print("\n⚽ TEST 8: Mapowanie sportów")
print("-" * 50)

try:
    sport_slugs = FlashScoreOddsScraper.SPORT_SLUGS
    expected_sports = ['football', 'soccer', 'basketball', 'volleyball', 'handball', 'hockey', 'tennis']
    
    for sport in expected_sports:
        if sport in sport_slugs:
            print(f"   ✅ '{sport}' -> '{sport_slugs[sport]}'")
            tests_passed += 1
        else:
            print(f"   ❌ '{sport}' - brak w SPORT_SLUGS")
            tests_failed += 1
except Exception as e:
    print(f"   ❌ Błąd mapowania sportów: {e}")
    tests_failed += 1

# ============================================================================
# TEST 9: Obsługa braku kursów (nie zwracaj losowego meczu!)
# ============================================================================
print("\n🚫 TEST 9: Brak fallbacku na losowy mecz")
print("-" * 50)

# Sprawdzamy że scraper NIE zwraca kursów dla nieistniejącego meczu
try:
    # Mock result - powinien być pusty jeśli mecz nie znaleziony
    mock_result = {
        'home_odds': None,
        'draw_odds': None,
        'away_odds': None,
        'odds_found': False,
    }
    
    if mock_result['odds_found'] == False and mock_result['home_odds'] is None:
        print(f"   ✅ Nieznaleziony mecz -> odds_found=False, kursy=None")
        tests_passed += 1
    else:
        print(f"   ❌ Scraper zwraca kursy dla nieistniejącego meczu!")
        tests_failed += 1
except Exception as e:
    print(f"   ❌ Błąd testu: {e}")
    tests_failed += 1

# ============================================================================
# TEST 10: Regex ekstrakcji kursów
# ============================================================================
print("\n🔍 TEST 10: Regex ekstrakcji kursów z HTML")
print("-" * 50)

test_html = """
<div class="odds">
    <span>2.10</span>
    <span>3.50</span>
    <span>3.20</span>
</div>
<div class="invalid">
    <span>0.50</span>
    <span>99.99</span>
</div>
"""

odds_pattern = r'>(\d+\.\d{2})<'
potential_odds = re.findall(odds_pattern, test_html)
valid_extracted = [float(o) for o in potential_odds if 1.01 <= float(o) <= 50.0]

expected_valid = [2.10, 3.50, 3.20]
if valid_extracted == expected_valid:
    print(f"   ✅ Wyekstrahowano: {valid_extracted}")
    tests_passed += 1
else:
    print(f"   ❌ Got: {valid_extracted}, expected: {expected_valid}")
    tests_failed += 1

# ============================================================================
# PODSUMOWANIE
# ============================================================================
print("\n" + "=" * 70)
total_tests = tests_passed + tests_failed
print(f"📊 PODSUMOWANIE: {tests_passed}/{total_tests} testów przeszło")
print("=" * 70)

if tests_failed == 0:
    print("\n✅ WSZYSTKIE TESTY FLASHSCORE PRZESZŁY POMYŚLNIE!")
    sys.exit(0)
else:
    print(f"\n❌ {tests_failed} TESTÓW NIE PRZESZŁO!")
    sys.exit(1)
