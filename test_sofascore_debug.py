"""
Debug script for SofaScore API issues - v2 with session test
"""
import requests
from datetime import datetime, timedelta
from typing import Optional

API_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9,pl;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'https://www.sofascore.com',
    'Referer': 'https://www.sofascore.com/',
    'Sec-Ch-Ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'X-Requested-With': 'XMLHttpRequest',
    'Cache-Control': 'no-cache',
}

def test_sofascore_api():
    print("=" * 60)
    print("TESTING SOFASCORE API v2 (Session-based)")
    print("=" * 60)
    
    # Create session and get cookies from main page
    session = requests.Session()
    session.headers.update(API_HEADERS)
    
    print("\n1. Getting cookies from main page...")
    main_page_headers = {
        'User-Agent': API_HEADERS['User-Agent'],
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        r = session.get('https://www.sofascore.com/', headers=main_page_headers, timeout=15)
        print(f"   Status: {r.status_code}")
        cookies = session.cookies.get_dict()
        print(f"   Cookies received: {len(cookies)}")
        for name, value in list(cookies.items())[:5]:
            print(f"   - {name}: {value[:30]}..." if len(value) > 30 else f"   - {name}: {value}")
    except Exception as e:
        print(f"   Error: {e}")
    
    # Test scheduled events API with session
    date = "2025-12-05"
    sport = "football"
    
    print(f"\n2. Testing scheduled events API with session:")
    url = f"https://api.sofascore.com/api/v1/sport/{sport}/scheduled-events/{date}"
    print(f"   URL: {url}")
    
    try:
        response = session.get(url, timeout=10)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            events = data.get('events', [])
            print(f"   ✅ SUCCESS! Events found: {len(events)}")
            
            if events:
                print(f"\n   First 5 events:")
                for event in events[:5]:
                    home = event.get('homeTeam', {}).get('name', 'N/A')
                    away = event.get('awayTeam', {}).get('name', 'N/A')
                    event_id = event.get('id')
                    print(f"   - {home} vs {away} (ID: {event_id})")
                    
                # Test votes API
                if events[0].get('id'):
                    event_id = events[0]['id']
                    print(f"\n3. Testing votes API for event {event_id}:")
                    votes_url = f"https://api.sofascore.com/api/v1/event/{event_id}/votes"
                    
                    votes_response = session.get(votes_url, timeout=10)
                    print(f"   Status: {votes_response.status_code}")
                    
                    if votes_response.status_code == 200:
                        votes_data = votes_response.json()
                        vote = votes_data.get('vote', {})
                        if vote:
                            print(f"   ✅ Home win: {vote.get('vote1')}%")
                            print(f"   ✅ Draw: {vote.get('voteX')}%")
                            print(f"   ✅ Away win: {vote.get('vote2')}%")
                        else:
                            print("   ⚠️ No vote data (event may not have votes yet)")
        else:
            print(f"   ❌ Failed: {response.text[:200]}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_sofascore_api()

