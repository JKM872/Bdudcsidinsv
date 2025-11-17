from bs4 import BeautifulSoup

soup = BeautifulSoup(open('forebet_debug.html', 'r', encoding='utf-8').read(), 'html.parser')
rows = soup.find_all('div', class_='rcnt')

print(f'✅ Znaleziono {len(rows)} meczów na Forebet\n')
print('Pierwsze 10 meczów:')
print('='*70)

for i, row in enumerate(rows[:10], 1):
    # Szukaj nazw drużyn w div.rcnt
    home_span = row.find('span', class_='homeTeam')
    away_span = row.find('span', class_='awayTeam')
    
    if home_span and away_span:
        home = home_span.get_text(strip=True)
        away = away_span.get_text(strip=True)
        
        # Szukaj predykcji
        pred_elem = row.find('div', class_='fprc')
        pred = pred_elem.get_text(strip=True) if pred_elem else 'N/A'
        
        # Szukaj prawdopodobieństwa
        prob_elem = row.find('div', class_='proba')
        prob = prob_elem.get_text(strip=True) if prob_elem else 'N/A'
        
        print(f'{i}. {home} vs {away}')
        print(f'   Pred: {pred} | Prob: {prob}')
    else:
        print(f'{i}. [Nie znaleziono drużyn]')
