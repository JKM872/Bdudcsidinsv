"""
Quick test of FlashScore odds scraping
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import re

print('Starting FlashScore match test...')

options = Options()
options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=options)
driver.set_page_load_timeout(30)

try:
    print('Opening FlashScore...')
    driver.get('https://www.flashscore.com/football/')
    time.sleep(5)
    
    # Znajdź pierwszy mecz - użyj innego selektora
    elements = driver.find_elements(By.CSS_SELECTOR, 'div[id^="g_1_"]')
    print(f'Found {len(elements)} matches')
    
    if elements:
        first_match = elements[0]
        match_id = first_match.get_attribute('id').replace('g_1_', '')
        print(f'First match ID: {match_id}')
        
        # Otwórz stronę meczu z kursami
        odds_url = f'https://www.flashscore.com/match/{match_id}/#/odds-comparison/1x2-odds/full-time'
        print(f'Opening: {odds_url}')
        driver.get(odds_url)
        time.sleep(5)
        
        page_source = driver.page_source
        
        # Szukaj kursów
        odds_pattern = r'>(\d+\.\d{2})<'
        odds = re.findall(odds_pattern, page_source)
        valid_odds = [o for o in odds if 1.01 <= float(o) <= 50.0]
        
        if valid_odds:
            print(f'Found {len(valid_odds)} odds values!')
            print(f'Sample: {valid_odds[:15]}')
            
            # Sprawdź czy są 1X2 (3 kursy razem)
            if len(valid_odds) >= 3:
                print(f'1X2 example: Home={valid_odds[0]}, Draw={valid_odds[1]}, Away={valid_odds[2]}')
        else:
            print('No odds found on match page')
        
        # Sprawdź bukmacherów
        for bookie in ['pinnacle', 'bet365', 'betway', 'unibet']:
            if bookie.lower() in page_source.lower():
                print(f'Bookmaker on page: {bookie}')
    else:
        print('No matches found on page')
except Exception as e:
    print(f'Error: {e}')
finally:
    driver.quit()
    print('Done!')
