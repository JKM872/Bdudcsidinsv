"""
Quick test of cloudscraper with SofaScore
"""
import cloudscraper

print("=" * 60)
print("TESTING CLOUDSCRAPER WITH SOFASCORE")
print("=" * 60)

# Create scraper
scraper = cloudscraper.create_scraper(
    browser={
        'browser': 'chrome',
        'platform': 'windows',
        'desktop': True
    }
)

print("\n1. Testing main page...")
try:
    r = scraper.get('https://www.sofascore.com/', timeout=20)
    print(f"   Status: {r.status_code}")
    print(f"   Cookies: {len(scraper.cookies.get_dict())}")
    if r.status_code == 200:
        print("   ✅ Main page OK!")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n2. Testing API with cloudscraper session...")
try:
    # Use the same scraper for API
    api_url = "https://api.sofascore.com/api/v1/sport/football/scheduled-events/2025-12-05"
    r = scraper.get(api_url, timeout=15)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        events = data.get('events', [])
        print(f"   ✅ SUCCESS! {len(events)} events found!")
        if events:
            for event in events[:3]:
                home = event.get('homeTeam', {}).get('name', 'N/A')
                away = event.get('awayTeam', {}).get('name', 'N/A')
                print(f"      - {home} vs {away}")
    else:
        print(f"   ❌ Failed: {r.text[:300]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
