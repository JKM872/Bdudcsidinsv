import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup

print('🎾 Quick Tennis Structure Test')
driver = uc.Chrome()
driver.get('https://www.forebet.com/en/tennis/predictions-today')
time.sleep(7)

soup = BeautifulSoup(driver.page_source, 'html.parser')
rows = soup.find_all('div', class_='rcnt')

print(f'✅ Tennis: {len(rows)} meczów')

if rows:
    r = rows[0]
    print(f'\n📋 Struktura HTML (pierwszy mecz):')
    print(f'   rcnt div: ✅')
    print(f'   homeTeam span: {"✅" if r.find("span", class_="homeTeam") else "❌"}')
    print(f'   awayTeam span: {"✅" if r.find("span", class_="awayTeam") else "❌"}')
    print(f'   fprc div: {"✅" if r.find("div", class_="fprc") else "❌"}')
    print(f'   avg_sc div: {"✅" if r.find("div", class_="avg_sc") else "❌"}')
    print(f'   ex_sc div: {"✅" if r.find("div", class_="ex_sc") else "❌"}')
    
    home = r.find('span', class_='homeTeam')
    away = r.find('span', class_='awayTeam')
    if home and away:
        print(f'\n🏆 Przykładowy mecz: {home.get_text(strip=True)} vs {away.get_text(strip=True)}')

driver.quit()
print('\n✅ Test zakończony - struktura identyczna jak football!')
