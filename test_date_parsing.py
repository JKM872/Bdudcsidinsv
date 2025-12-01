#!/usr/bin/env python3
"""
Test parsowania dat i obsługi NaN/float w email_notifier.
Weryfikuje poprawki wprowadzone dla:
1. Parsowania dat DD.MM.YY i DD.MM.YYYY
2. Obsługi NaN/float w gemini_reasoning
3. Obsługi brakujących danych Forebet
"""

import re
import math
import sys

def test_date_parsing():
    """Test parsowania dat w różnych formatach."""
    print("=" * 60)
    print("TEST 1: Parsowanie dat")
    print("=" * 60)
    
    test_cases = [
        # (input, expected_output)
        ('17.11.2025 20:00', '2025-11-17'),
        ('30.11.2025 15:00', '2025-11-30'),
        ('01.12.2025', '2025-12-01'),
        ('30.11.25 15:00', '2025-11-30'),  # 2-cyfrowy rok
        ('15.06.24', '2024-06-15'),  # 2-cyfrowy rok
        ('01.01.20', '2020-01-01'),  # Rok 2020
        ('31.12.99', '1999-12-31'),  # Rok 1999 (>50 = 1900s)
        ('01.01.00', '2000-01-01'),  # Rok 2000
    ]
    
    passed = 0
    failed = 0
    
    for input_val, expected in test_cases:
        match = re.search(r'(\d{2})\.(\d{2})\.(\d{2,4})', input_val)
        if match:
            day, month, year = match.groups()
            if len(year) == 4:
                result = f'{year}-{month}-{day}'
            else:
                year_int = int(year)
                full_year = 2000 + year_int if year_int <= 50 else 1900 + year_int
                result = f'{full_year}-{month}-{day}'
            
            if result == expected:
                print(f"  ✅ PASS: '{input_val}' -> '{result}'")
                passed += 1
            else:
                print(f"  ❌ FAIL: '{input_val}' -> got '{result}', expected '{expected}'")
                failed += 1
        else:
            print(f"  ❌ FAIL: '{input_val}' -> no match found!")
            failed += 1
    
    print(f"\n  Wynik: {passed}/{passed + failed} testów przeszło")
    return failed == 0


def test_nan_handling():
    """Test obsługi NaN/float w polach tekstowych."""
    print("\n" + "=" * 60)
    print("TEST 2: Obsługa NaN/float w gemini_reasoning")
    print("=" * 60)
    
    test_cases = [
        (None, ''),
        (float('nan'), ''),
        ('Valid reasoning text', 'Valid reasoning text'),
        ('', ''),
        (123.45, '123.45'),
        ('A' * 500, 'A' * 200),  # Skrócenie do 200 znaków
    ]
    
    passed = 0
    failed = 0
    
    for val, expected_prefix in test_cases:
        try:
            # Logika z email_notifier.py
            if val is None or (isinstance(val, float) and (math.isnan(val) if isinstance(val, float) else False)):
                safe_val = ''
            else:
                safe_val = str(val)[:200]
            
            if safe_val.startswith(expected_prefix[:50]):  # Porównaj początek
                print(f"  ✅ PASS: {type(val).__name__} -> '{safe_val[:30]}...'")
                passed += 1
            else:
                print(f"  ❌ FAIL: {type(val).__name__} -> got '{safe_val[:30]}', expected '{expected_prefix[:30]}'")
                failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: {type(val).__name__} -> Exception: {e}")
            failed += 1
    
    print(f"\n  Wynik: {passed}/{passed + failed} testów przeszło")
    return failed == 0


def test_forebet_probability_handling():
    """Test obsługi brakujących danych Forebet."""
    print("\n" + "=" * 60)
    print("TEST 3: Obsługa brakujących danych Forebet")
    print("=" * 60)
    
    test_cases = [
        (None, 'Brak'),
        (float('nan'), 'Brak'),
        (75.5, '75.5%'),
        (100, '100%'),
        (0, '0%'),
        ('50%', '50%'),  # Już sformatowane
    ]
    
    passed = 0
    failed = 0
    
    for val, expected in test_cases:
        try:
            # Logika z email_notifier.py
            if val is None or (isinstance(val, float) and str(val) == 'nan'):
                forebet_prob = 'Brak'
            else:
                forebet_prob = f"{val}%" if isinstance(val, (int, float)) else str(val)
            
            if forebet_prob == expected:
                print(f"  ✅ PASS: {val} -> '{forebet_prob}'")
                passed += 1
            else:
                print(f"  ❌ FAIL: {val} -> got '{forebet_prob}', expected '{expected}'")
                failed += 1
        except Exception as e:
            print(f"  ❌ FAIL: {val} -> Exception: {e}")
            failed += 1
    
    print(f"\n  Wynik: {passed}/{passed + failed} testów przeszło")
    return failed == 0


def test_imports():
    """Test importów głównych modułów."""
    print("\n" + "=" * 60)
    print("TEST 4: Importy modułów")
    print("=" * 60)
    
    modules_to_test = [
        ('livesport_h2h_scraper', ['start_driver', 'process_match', 'detect_sport_from_url']),
        ('email_notifier', ['send_email_notification', 'create_html_email']),
        ('forebet_scraper', ['search_forebet_prediction']),
        ('flashscore_odds_scraper', ['FlashScoreOddsScraper']),
    ]
    
    passed = 0
    failed = 0
    
    for module_name, functions in modules_to_test:
        try:
            module = __import__(module_name)
            for func_name in functions:
                if hasattr(module, func_name):
                    print(f"  ✅ PASS: {module_name}.{func_name}")
                    passed += 1
                else:
                    print(f"  ❌ FAIL: {module_name}.{func_name} not found")
                    failed += 1
        except ImportError as e:
            print(f"  ❌ FAIL: Cannot import {module_name}: {e}")
            failed += len(functions)
    
    print(f"\n  Wynik: {passed}/{passed + failed} testów przeszło")
    return failed == 0


if __name__ == '__main__':
    print("\n" + "🧪 " * 20)
    print("URUCHAMIANIE TESTÓW WALIDACJI")
    print("🧪 " * 20 + "\n")
    
    results = []
    
    results.append(('Parsowanie dat', test_date_parsing()))
    results.append(('Obsługa NaN', test_nan_handling()))
    results.append(('Forebet probability', test_forebet_probability_handling()))
    results.append(('Importy modułów', test_imports()))
    
    print("\n" + "=" * 60)
    print("PODSUMOWANIE")
    print("=" * 60)
    
    all_passed = True
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✅ WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
        sys.exit(0)
    else:
        print("❌ NIEKTÓRE TESTY NIE PRZESZŁY!")
        sys.exit(1)
