"""
Test SofaScore API - prawdziwe mecze z dzisiaj
"""
from sofascore_scraper import get_votes_via_api
import requests

print('Test SofaScore API...')

url = 'https://api.sofascore.com/api/v1/sport/football/scheduled-events/2024-12-14'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

try:
    r = requests.get(url, headers=headers, timeout=10)
    print(f'Status: {r.status_code}')
    
    if r.status_code == 200:
        data = r.json()
        events = data.get('events', [])
        print(f'Znaleziono {len(events)} meczow na dzisiaj')
        
        # Sprawdz pierwsze 5 meczow
        votes_found = 0
        for e in events[:10]:
            home = e.get('homeTeam', {}).get('name', 'N/A')
            away = e.get('awayTeam', {}).get('name', 'N/A')
            event_id = e.get('id')
            
            # Test pobierania glosow
            if event_id:
                votes = get_votes_via_api(event_id)
                if votes and votes.get('home_win_prob'):
                    votes_found += 1
                    print(f'  {home} vs {away}')
                    print(f'    Home: {votes.get("home_win_prob")}%')
                    print(f'    Draw: {votes.get("draw_prob")}%')
                    print(f'    Away: {votes.get("away_win_prob")}%')
                    print(f'    Votes: {votes.get("total_votes")}')
                    if votes_found >= 3:
                        break
        
        if votes_found == 0:
            print('  Nie znaleziono meczow z glosami Fan Vote')
        else:
            print(f'\nZnaleziono {votes_found} meczow z glosami!')
            
except Exception as e:
    print(f'Error: {e}')
