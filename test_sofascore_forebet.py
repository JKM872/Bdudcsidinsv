"""
Test SofaScore i Forebet scrapers
"""
import sys
import os

print('='*60)
print('TEST SOFASCORE')
print('='*60)

try:
    from sofascore_scraper import scrape_sofascore_full
    
    # Użyj mock drivera lub testuj API directly
    # SofaScore API test
    from sofascore_scraper import get_votes_via_api, search_event_via_api
    
    # Test wyszukiwania meczu
    print('\n1. Test wyszukiwania meczu via API...')
    result = search_event_via_api('Barcelona', 'Real Madrid', 'football')
    if result:
        print(f'   ✅ Znaleziono event ID: {result}')
        
        # Test pobierania głosów
        print('\n2. Test pobierania głosów...')
        votes = get_votes_via_api(result)
        if votes:
            print(f'   ✅ Głosy: {votes}')
        else:
            print('   ⚠️ Brak głosów dla tego meczu')
    else:
        print('   ⚠️ Nie znaleziono meczu (może nie być na dziś)')
        
except ImportError as e:
    print(f'   ❌ Błąd importu: {e}')
except Exception as e:
    print(f'   ❌ Błąd: {e}')

print('\n' + '='*60)
print('TEST FOREBET')
print('='*60)

try:
    from forebet_scraper import normalize_team_name, similarity_score, prefetch_forebet_html
    
    # Test normalizacji nazw
    print('\n1. Test normalizacji nazw drużyn...')
    test_names = [
        ('FC Barcelona', 'barcelona'),
        ('Real Madrid CF', 'real madrid'),
        ('Manchester United FC', 'manchester united'),
        ('Hamburg Towers', 'hamburg towers'),
    ]
    
    all_passed = True
    for original, expected in test_names:
        result = normalize_team_name(original)
        status = '✅' if expected in result else '❌'
        print(f'   {status} "{original}" -> "{result}"')
        if expected not in result:
            all_passed = False
    
    # Test similarity
    print('\n2. Test similarity scoring...')
    test_pairs = [
        ('Barcelona', 'FC Barcelona', 0.7),
        ('Hamburg', 'Hamburg Towers', 0.6),
        ('Real Madrid', 'Real Madrid CF', 0.7),
        ('Bayern', 'Bayern Munich', 0.6),
    ]
    
    for name1, name2, min_score in test_pairs:
        score = similarity_score(name1, name2)
        status = '✅' if score >= min_score else '❌'
        print(f'   {status} "{name1}" vs "{name2}" = {score:.2f} (min: {min_score})')
    
    print('\n3. Test Forebet prefetch (wymaga połączenia)...')
    print('   ⏭️ Pominięto (wymaga FlareSolverr)')
        
except ImportError as e:
    print(f'   ❌ Błąd importu: {e}')
except Exception as e:
    print(f'   ❌ Błąd: {e}')

print('\n' + '='*60)
print('PODSUMOWANIE')
print('='*60)
