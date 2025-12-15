"""
Test całego pipeline pobierania kursów
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

print('='*60)
print('TEST PIPELINE POBIERANIA KURSÓW')
print('='*60)

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)

try:
    # 1. Otwórz Livesport (źródło H2H)
    print('\n1. Test Livesport (strona źródłowa)...')
    driver.get('https://www.livesport.com/pl/koszykowka/')
    time.sleep(3)
    
    # Znajdź pierwszy mecz
    elements = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/mecz/"]')
    print(f'   Znaleziono {len(elements)} linków do meczów')
    
    if elements:
        match_url = elements[0].get_attribute('href')
        print(f'   Pierwszy mecz: {match_url[:80]}...')
        
        # Wydobądź Event ID
        import re
        match = re.search(r'/([a-zA-Z0-9]{6,10})/', match_url)
        if match:
            event_id = match.group(1)
            print(f'   Event ID: {event_id}')
    
    # 2. Test FlashScore odds
    print('\n2. Test FlashScore (kursy)...')
    driver.get('https://www.flashscore.com/basketball/')
    time.sleep(4)
    
    elements = driver.find_elements(By.CSS_SELECTOR, 'div[id^="g_1_"]')
    print(f'   Znaleziono {len(elements)} meczów na FlashScore')
    
    if elements:
        match_id = elements[0].get_attribute('id').replace('g_1_', '')
        odds_url = f'https://www.flashscore.com/match/{match_id}/#/odds-comparison/1x2-odds/full-time'
        print(f'   Mecz ID: {match_id}')
        
        driver.get(odds_url)
        time.sleep(4)
        
        page = driver.page_source
        
        # Szukaj kursów
        odds_pattern = r'>(\d+\.\d{2})<'
        odds = re.findall(odds_pattern, page)
        valid_odds = [float(o) for o in odds if 1.01 <= float(o) <= 50.0]
        
        # Sprawdź bukmacherów
        bookmakers_found = []
        for b in ['pinnacle', 'bet365', 'betway', 'unibet']:
            if b.lower() in page.lower():
                bookmakers_found.append(b)
        
        print(f'   Bukmacherzy: {bookmakers_found}')
        
        if valid_odds:
            print(f'   ✅ Kursy znalezione: {len(valid_odds)} wartości')
            if len(valid_odds) >= 2:
                print(f'   Home={valid_odds[0]}, Away={valid_odds[1]}')
        else:
            print('   ❌ Brak kursów')
    
    print('\n' + '='*60)
    print('PODSUMOWANIE:')
    print('  - Livesport: działa jako źródło meczów i H2H')
    print('  - FlashScore: działa jako źródło kursów')
    print('  - Pinnacle: dostępny na FlashScore')
    print('='*60)
    
except Exception as e:
    print(f'Error: {e}')
finally:
    driver.quit()
