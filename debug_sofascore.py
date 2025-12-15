#!/usr/bin/env python3
"""
Debug SofaScore - sprawdza co jest na stronie
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re

chrome_options = Options()
# chrome_options.add_argument('--headless=new')  # Bez headless dla debugowania
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

driver = webdriver.Chrome(options=chrome_options)

try:
    url = 'https://www.sofascore.com/football/match/galatasaray-fenerbahce/clbsllb#id:14109730'
    print(f"Loading: {url}")
    driver.get(url)
    
    print("Waiting 8 seconds...")
    time.sleep(8)
    
    # Scroll
    for i in range(10):
        driver.execute_script('window.scrollBy(0, 400);')
        time.sleep(0.5)
    
    driver.execute_script('window.scrollTo(0, 0);')
    time.sleep(2)
    
    page = driver.page_source
    print(f"\nPage length: {len(page)}")
    
    # Szukaj różnych wzorców
    patterns = [
        'Who will win',
        'who will win', 
        'Fan vote',
        'fan vote',
        'Total votes',
        'total votes',
        '%</span>',
        'vote1',
        'vote2',
    ]
    
    for p in patterns:
        if p.lower() in page.lower():
            idx = page.lower().find(p.lower())
            print(f"\n✅ FOUND: '{p}' at index {idx}")
            # Pokaż kontekst
            print(f"   Context: ...{page[max(0,idx-50):idx+100]}...")
        else:
            print(f"❌ NOT FOUND: '{p}'")
    
    # Szukaj wszystkich procentów
    percentages = re.findall(r'>(\d{1,3})%<', page)
    print(f"\n📊 All percentages found: {percentages[:20]}")
    
    # Zapisz stronę do pliku dla analizy
    with open('sofascore_debug.html', 'w', encoding='utf-8') as f:
        f.write(page)
    print("\n📄 Page saved to sofascore_debug.html")
    
    input("\nPress Enter to close browser...")
    
finally:
    driver.quit()
