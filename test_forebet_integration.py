"""
Test integracji Forebet z głównym scraperem - siatkówka
"""

from livesport_h2h_scraper import start_driver, process_match, detect_sport_from_url
import sys

# Test URL siatkówki z dzisiaj
test_url = "https://www.livesport.com/pl/siatkowka/polska/tauron-liga/rozwoj-katowice-cuprum-lubin/YnU0eEvT/"

print("="*70)
print("🧪 TEST INTEGRACJI FOREBET - SIATKÓWKA")
print("="*70)
print(f"📍 URL: {test_url}")
print()

# Test wykrywania sportu
sport = detect_sport_from_url(test_url)
print(f"✅ Wykryty sport: {sport}")
print()

# Uruchom scraper
print("🚀 Uruchamiam scraper z Forebet...")
print("⚠️  Otworzy się widoczna przeglądarka (wymagane dla Cloudflare)")
print()

driver = start_driver(headless=False)  # Musi być widoczna dla Forebet

try:
    info = process_match(test_url, driver, away_team_focus=False, use_forebet=True, sport=sport)
    
    print("\n" + "="*70)
    print("📊 WYNIKI")
    print("="*70)
    
    # Podstawowe info
    print(f"🏐 Mecz: {info['home_team']} vs {info['away_team']}")
    print(f"📅 Data: {info.get('match_time', 'N/A')}")
    print(f"✅ Kwalifikuje: {info['qualifies']}")
    
    # H2H
    if info.get('h2h_count'):
        print(f"\n📈 H2H (ostatnie 5):")
        print(f"   Gospodarze: {info['home_wins_in_h2h_last5']}/{info['h2h_count']} ({info['win_rate']:.1f}%)")
        if info.get('last_h2h_date'):
            print(f"   Ostatni H2H: {info['last_h2h_date']}")
    
    # FOREBET
    print(f"\n🎯 FOREBET PREDICTIONS:")
    if info.get('forebet_prediction'):
        print(f"   Predykcja: {info['forebet_prediction']}")
        print(f"   Prawdopodobieństwo: {info.get('forebet_probability', 'N/A')}%")
        print(f"   Dokładny wynik: {info.get('forebet_exact_score', 'N/A')}")
        print(f"   Over/Under: {info.get('forebet_over_under', 'N/A')}")
        print(f"   BTTS: {info.get('forebet_btts', 'N/A')}")
        print(f"   Średnia goli: {info.get('forebet_avg_goals', 'N/A')}")
    else:
        print("   ⚠️ Brak danych Forebet (może nie być predykcji dla tego meczu)")
    
    print("\n✅ Test zakończony pomyślnie!")
    
except Exception as e:
    print(f"\n❌ BŁĄD: {e}")
    import traceback
    traceback.print_exc()
    
finally:
    driver.quit()
    print("\n🔒 Przeglądarka zamknięta")
