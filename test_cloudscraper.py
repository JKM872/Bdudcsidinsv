"""
Quick test of SofaScore API access
Tests both direct API and cloudscraper methods
"""
import requests
from datetime import datetime

print("=" * 60)
print("TESTING SOFASCORE API ACCESS")
print("=" * 60)

# Today's date
today = datetime.now().strftime('%Y-%m-%d')

# Method 1: Direct API with browser-like headers
print("\n1. Testing direct API with browser headers...")
API_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://www.sofascore.com/',
    'Origin': 'https://www.sofascore.com',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
}

try:
    api_url = f"https://api.sofascore.com/api/v1/sport/football/scheduled-events/{today}"
    r = requests.get(api_url, headers=API_HEADERS, timeout=15)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        events = data.get('events', [])
        print(f"   ✅ SUCCESS! {len(events)} football events found!")
        if events[:3]:
            for event in events[:3]:
                home = event.get('homeTeam', {}).get('name', 'N/A')
                away = event.get('awayTeam', {}).get('name', 'N/A')
                print(f"      - {home} vs {away}")
    else:
        print(f"   ❌ Failed: {r.status_code}")
        print(f"   Response: {r.text[:200]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 2: Try cloudscraper for main page
print("\n2. Testing cloudscraper with SofaScore main page...")
try:
    import cloudscraper
    scraper = cloudscraper.create_scraper(
        browser={
            'browser': 'chrome',
            'platform': 'windows',
            'desktop': True
        }
    )
    
    r = scraper.get('https://www.sofascore.com/', timeout=20)
    print(f"   Status: {r.status_code}")
    print(f"   Cookies: {len(scraper.cookies.get_dict())}")
    if r.status_code == 200:
        # Check if we got real content
        if 'SofaScore' in r.text and len(r.text) > 10000:
            print(f"   ✅ Main page loaded! ({len(r.text)} chars)")
        else:
            print(f"   ⚠️ Page loaded but content seems wrong ({len(r.text)} chars)")
    else:
        print(f"   ❌ Failed: {r.status_code}")
except ImportError:
    print("   ⚠️ cloudscraper not installed")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 3: Test basketball API
print("\n3. Testing basketball events API...")
try:
    api_url = f"https://api.sofascore.com/api/v1/sport/basketball/scheduled-events/{today}"
    r = requests.get(api_url, headers=API_HEADERS, timeout=15)
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        data = r.json()
        events = data.get('events', [])
        print(f"   ✅ SUCCESS! {len(events)} basketball events found!")
        if events[:3]:
            for event in events[:3]:
                home = event.get('homeTeam', {}).get('name', 'N/A')
                away = event.get('awayTeam', {}).get('name', 'N/A')
                print(f"      - {home} vs {away}")
    else:
        print(f"   ❌ Failed: {r.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Method 4: Test Forebet with cloudflare_bypass
print("\n4. Testing Forebet cloudflare bypass...")
try:
    from cloudflare_bypass import CloudflareBypass
    bypass = CloudflareBypass(debug=True)
    
    # Quick test - just check if module loads
    print(f"   ✅ CloudflareBypass module loaded successfully!")
    print(f"   Available methods: {[k for k,v in bypass.__class__.__dict__.items() if k.startswith('_try_')]}")
except ImportError as e:
    print(f"   ⚠️ CloudflareBypass import error: {e}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
