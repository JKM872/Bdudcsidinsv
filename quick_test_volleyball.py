"""
Quick test - sprawdza czy Forebet ma volleyball predictions
"""
import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup

print('🏐 Test Forebet Volleyball')
print('='*70)

options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

url = 'https://www.forebet.com/en/volleyball/predictions-today'
print(f'Ładuję: {url}')

driver.get(url)
time.sleep(5)

soup = BeautifulSoup(driver.page_source, 'html.parser')
rows = soup.find_all('div', class_='rcnt')

print(f'\n✅ Znaleziono {len(rows)} meczów volleyball\n')

if rows:
    print('Pierwsze 5 meczów:')
    print('-'*70)
    for i, row in enumerate(rows[:5], 1):
        home_elem = row.find('span', class_='homeTeam')
        away_elem = row.find('span', class_='awayTeam')
        
        if home_elem and away_elem:
            home = home_elem.get_text(strip=True)
            away = away_elem.get_text(strip=True)
            
            # Prediction
            fprc_div = row.find('div', class_='fprc')
            pred = 'N/A'
            if fprc_div:
                spans = fprc_div.find_all('span')
                if len(spans) >= 3:
                    try:
                        probs = [int(s.get_text(strip=True)) for s in spans]
                        max_prob = max(probs)
                        max_idx = probs.index(max_prob)
                        pred_map = {0: '1 (Home)', 1: 'X (Draw)', 2: '2 (Away)'}
                        pred = f'{pred_map.get(max_idx, "?")} {max_prob}%'
                    except:
                        pass
            
            print(f'{i}. {home} vs {away}')
            print(f'   Prediction: {pred}')
else:
    print('❌ Brak meczów volleyball na Forebet')
    print('ℹ️  Forebet może nie obsługiwać volleyball lub dzisiaj brak meczów')

driver.quit()
print('\n' + '='*70)
