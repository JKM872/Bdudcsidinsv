"""
Multi-sport test - sprawdza czy Forebet ma predykcje dla różnych sportów
"""
import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup
import sys

# Sporty do testowania
sports_to_test = {
    'tennis': 'https://www.forebet.com/en/tennis/predictions-today',
    'basketball': 'https://www.forebet.com/en/basketball/predictions-today',
    'handball': 'https://www.forebet.com/en/handball/predictions-today',
    'hockey': 'https://www.forebet.com/en/hockey/predictions-today',
    'rugby': 'https://www.forebet.com/en/rugby/predictions-today',
    'volleyball': 'https://www.forebet.com/en/volleyball/predictions-today',
}

# Wybierz sport z argumentu lub test wszystkich
if len(sys.argv) > 1:
    sport_arg = sys.argv[1].lower()
    if sport_arg in sports_to_test:
        sports_to_test = {sport_arg: sports_to_test[sport_arg]}
    else:
        print(f'❌ Nieznany sport: {sport_arg}')
        print(f'Dostępne: {", ".join(sports_to_test.keys())}')
        sys.exit(1)

print('🎯 Forebet Multi-Sport Test')
print('='*70)
print(f'Testowanie {len(sports_to_test)} sportów...\n')

results = {}

for sport, url in sports_to_test.items():
    print(f'🔍 {sport.upper()}...')
    
    try:
        options = uc.ChromeOptions()
        driver = uc.Chrome(options=options)
        
        driver.get(url)
        time.sleep(5)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        rows = soup.find_all('div', class_='rcnt')
        
        match_count = len(rows)
        results[sport] = match_count
        
        if match_count > 0:
            print(f'   ✅ {match_count} meczów')
            
            # Pokaż pierwszy mecz
            if rows:
                first_row = rows[0]
                home_elem = first_row.find('span', class_='homeTeam')
                away_elem = first_row.find('span', class_='awayTeam')
                
                if home_elem and away_elem:
                    print(f'   Przykład: {home_elem.get_text(strip=True)} vs {away_elem.get_text(strip=True)}')
        else:
            print(f'   ⚠️  Brak meczów dzisiaj')
        
        driver.quit()
        print()
        
    except Exception as e:
        print(f'   ❌ Error: {e}')
        results[sport] = -1
        try:
            driver.quit()
        except:
            pass
        print()

print('='*70)
print('📊 PODSUMOWANIE:')
print('='*70)

for sport, count in results.items():
    emoji = '✅' if count > 0 else '⚠️' if count == 0 else '❌'
    status = f'{count} meczów' if count >= 0 else 'ERROR'
    print(f'{emoji} {sport.upper():15} - {status}')

print('='*70)
