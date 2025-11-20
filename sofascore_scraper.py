"""
SofaScore Scraper
-----------------
Pobiera dane z SofaScore.com:
- "Who will win?" probabilities (community voting)
- Statistical predictions
- Multi-bookmaker odds aggregation
- H2H data from SofaScore

UWAGA: Sporty bez remisów (volleyball, tennis, basketball OT) mają tylko 2 opcje!
"""

import time
import re
from typing import Dict, Optional, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

# Sporty BEZ REMISÓW (tylko Home/Away win)
SPORTS_WITHOUT_DRAW = ['volleyball', 'tennis', 'basketball', 'handball', 'hockey', 'ice-hockey']

# Mapowanie nazw sportów na SofaScore URL slugs
SOFASCORE_SPORT_SLUGS = {
    'football': 'football',
    'soccer': 'football',
    'basketball': 'basketball',
    'volleyball': 'volleyball',
    'handball': 'handball',
    'rugby': 'rugby-union',
    'hockey': 'ice-hockey',
    'ice-hockey': 'ice-hockey',
    'tennis': 'tennis',
}


def normalize_team_name(name: str) -> str:
    """
    Normalizuje nazwę drużyny do porównania
    - lowercase
    - usuwa znaki specjalne
    - usuwa U21, U19, B, II itp.
    """
    if not name:
        return ""
    
    # Lowercase
    name = name.lower()
    
    # Usuń sufiksy typu U21, U19, B, II
    name = re.sub(r'\s+(u21|u19|u18|b|ii|iii|iv)\s*$', '', name, flags=re.IGNORECASE)
    
    # Usuń znaki specjalne
    name = re.sub(r'[^a-z0-9\s]', '', name)
    
    # Usuń wielokrotne spacje
    name = re.sub(r'\s+', ' ', name).strip()
    
    return name


def teams_match(team1: str, team2: str, threshold: float = 0.7) -> bool:
    """
    Sprawdza czy dwie nazwy drużyn są podobne
    Używa prostego word matching
    """
    norm1 = normalize_team_name(team1)
    norm2 = normalize_team_name(team2)
    
    if not norm1 or not norm2:
        return False
    
    # Dokładne dopasowanie
    if norm1 == norm2:
        return True
    
    # Sprawdź ile słów się zgadza
    words1 = set(norm1.split())
    words2 = set(norm2.split())
    
    if not words1 or not words2:
        return False
    
    # Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    similarity = intersection / union if union > 0 else 0
    
    return similarity >= threshold


def search_sofascore_match(
    driver: webdriver.Chrome,
    home_team: str,
    away_team: str,
    sport: str = 'football',
    date_str: str = None
) -> Optional[str]:
    """
    Szuka meczu na SofaScore i zwraca URL
    
    Args:
        driver: Selenium WebDriver
        home_team: Nazwa gospodarzy
        away_team: Nazwa gości
        sport: Sport (football, volleyball, etc.)
        date_str: Data w formacie YYYY-MM-DD
    
    Returns:
        URL meczu na SofaScore lub None
    """
    sport_slug = SOFASCORE_SPORT_SLUGS.get(sport, 'football')
    
    # Spróbuj wyszukać przez search bar
    try:
        # Format zapytania: "home vs away"
        search_query = f"{home_team} vs {away_team}"
        search_url = f"https://www.sofascore.com/search?q={search_query.replace(' ', '+')}"
        
        print(f"🔍 Searching SofaScore: {search_query}")
        driver.get(search_url)
        time.sleep(2)
        
        # Poczekaj na wyniki wyszukiwania
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "sc-fqkvVR"))
        )
        
        # Znajdź wszystkie wyniki
        results = driver.find_elements(By.CSS_SELECTOR, "a[href*='/match/']")
        
        for result in results[:5]:  # Sprawdź top 5 wyników
            try:
                match_url = result.get_attribute('href')
                
                # Sprawdź czy URL zawiera właściwy sport
                if sport_slug not in match_url:
                    continue
                
                # Pobierz nazwy drużyn z wyniku
                team_elements = result.find_elements(By.CLASS_NAME, "sc-fqkvVR")
                
                if len(team_elements) >= 2:
                    result_home = team_elements[0].text
                    result_away = team_elements[1].text
                    
                    # Sprawdź dopasowanie
                    if teams_match(home_team, result_home) and teams_match(away_team, result_away):
                        print(f"✅ Found match: {match_url}")
                        return match_url
            except Exception as e:
                continue
        
        print(f"⚠️ No exact match found on SofaScore")
        return None
        
    except Exception as e:
        print(f"❌ Error searching SofaScore: {e}")
        return None


def extract_sofascore_predictions(
    driver: webdriver.Chrome,
    match_url: str,
    sport: str = 'football'
) -> Dict:
    """
    Pobiera predykcje z SofaScore ("Who will win?")
    
    Returns:
        Dict z kluczami:
        - sofascore_home_win_prob: % (0-100)
        - sofascore_draw_prob: % (0-100) lub None jeśli brak remisów
        - sofascore_away_win_prob: % (0-100)
        - sofascore_total_votes: liczba głosów
        - sofascore_url: URL meczu
    """
    has_draw = sport not in SPORTS_WITHOUT_DRAW
    
    result = {
        'sofascore_home_win_prob': None,
        'sofascore_draw_prob': None if not has_draw else None,
        'sofascore_away_win_prob': None,
        'sofascore_total_votes': 0,
        'sofascore_url': match_url,
    }
    
    try:
        print(f"📊 Extracting SofaScore predictions from: {match_url}")
        driver.get(match_url)
        time.sleep(3)
        
        # Scroll do sekcji "Who will win?"
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            time.sleep(2)
        except:
            pass
        
        # Znajdź sekcję z predykcjami
        # SofaScore używa różnych selektorów, spróbujmy kilku
        prediction_selectors = [
            "div[class*='whoWillWin']",
            "div[class*='prediction']",
            "div[class*='vote']",
            "section[class*='poll']",
        ]
        
        prediction_section = None
        for selector in prediction_selectors:
            try:
                prediction_section = driver.find_element(By.CSS_SELECTOR, selector)
                break
            except:
                continue
        
        if not prediction_section:
            print("⚠️ No prediction section found")
            return result
        
        # Pobierz percentages
        # Format zależy od sportu:
        # - Z remisem: [Home%, Draw%, Away%]
        # - Bez remisu: [Home%, Away%]
        
        percentage_elements = prediction_section.find_elements(By.CSS_SELECTOR, "div[class*='percentage']")
        
        if len(percentage_elements) >= 2:
            if has_draw and len(percentage_elements) >= 3:
                # Sport Z remisem (football, rugby)
                home_pct = percentage_elements[0].text.strip('%')
                draw_pct = percentage_elements[1].text.strip('%')
                away_pct = percentage_elements[2].text.strip('%')
                
                result['sofascore_home_win_prob'] = float(home_pct) if home_pct else None
                result['sofascore_draw_prob'] = float(draw_pct) if draw_pct else None
                result['sofascore_away_win_prob'] = float(away_pct) if away_pct else None
                
            else:
                # Sport BEZ remisu (volleyball, tennis, basketball)
                home_pct = percentage_elements[0].text.strip('%')
                away_pct = percentage_elements[1].text.strip('%')
                
                result['sofascore_home_win_prob'] = float(home_pct) if home_pct else None
                result['sofascore_away_win_prob'] = float(away_pct) if away_pct else None
        
        # Pobierz total votes jeśli dostępne
        try:
            votes_element = prediction_section.find_element(By.CSS_SELECTOR, "span[class*='votes']")
            votes_text = votes_element.text
            votes_match = re.search(r'(\d+)', votes_text)
            if votes_match:
                result['sofascore_total_votes'] = int(votes_match.group(1))
        except:
            pass
        
        print(f"✅ SofaScore predictions: Home={result['sofascore_home_win_prob']}%, "
              f"Draw={result['sofascore_draw_prob']}%, Away={result['sofascore_away_win_prob']}%")
        
        return result
        
    except Exception as e:
        print(f"❌ Error extracting SofaScore predictions: {e}")
        return result


def get_sofascore_odds(
    driver: webdriver.Chrome,
    match_url: str,
    sport: str = 'football'
) -> Dict:
    """
    Pobiera kursy z wielu bukmacherów agregowane przez SofaScore
    
    Returns:
        Dict z kluczami:
        - sofascore_home_odds_avg: średni kurs na gospodarzy
        - sofascore_draw_odds_avg: średni kurs na remis (lub None)
        - sofascore_away_odds_avg: średni kurs na gości
        - sofascore_best_home_odds: najlepszy kurs na gospodarzy
        - sofascore_best_away_odds: najlepszy kurs na gości
    """
    has_draw = sport not in SPORTS_WITHOUT_DRAW
    
    result = {
        'sofascore_home_odds_avg': None,
        'sofascore_draw_odds_avg': None if not has_draw else None,
        'sofascore_away_odds_avg': None,
        'sofascore_best_home_odds': None,
        'sofascore_best_away_odds': None,
    }
    
    try:
        # Przejdź do zakładki "Odds" jeśli istnieje
        odds_tab_selectors = [
            "a[href*='odds']",
            "button[class*='odds']",
            "div[class*='oddsTab']",
        ]
        
        for selector in odds_tab_selectors:
            try:
                odds_tab = driver.find_element(By.CSS_SELECTOR, selector)
                odds_tab.click()
                time.sleep(2)
                break
            except:
                continue
        
        # Znajdź tabelę z kursami
        odds_table = driver.find_element(By.CSS_SELECTOR, "div[class*='oddsTable']")
        
        # Pobierz wszystkie kursy dla 1X2 (lub 12 bez remisu)
        home_odds_list = []
        draw_odds_list = []
        away_odds_list = []
        
        odds_rows = odds_table.find_elements(By.CSS_SELECTOR, "div[class*='oddsRow']")
        
        for row in odds_rows[:10]:  # Top 10 bookmakers
            odds_cells = row.find_elements(By.CSS_SELECTOR, "span[class*='odd']")
            
            if len(odds_cells) >= 2:
                try:
                    home_odd = float(odds_cells[0].text)
                    home_odds_list.append(home_odd)
                    
                    if has_draw and len(odds_cells) >= 3:
                        draw_odd = float(odds_cells[1].text)
                        draw_odds_list.append(draw_odd)
                        away_odd = float(odds_cells[2].text)
                    else:
                        away_odd = float(odds_cells[1].text)
                    
                    away_odds_list.append(away_odd)
                except:
                    continue
        
        # Oblicz średnie i max
        if home_odds_list:
            result['sofascore_home_odds_avg'] = round(sum(home_odds_list) / len(home_odds_list), 2)
            result['sofascore_best_home_odds'] = round(max(home_odds_list), 2)
        
        if away_odds_list:
            result['sofascore_away_odds_avg'] = round(sum(away_odds_list) / len(away_odds_list), 2)
            result['sofascore_best_away_odds'] = round(max(away_odds_list), 2)
        
        if has_draw and draw_odds_list:
            result['sofascore_draw_odds_avg'] = round(sum(draw_odds_list) / len(draw_odds_list), 2)
        
        print(f"💰 SofaScore odds: Home={result['sofascore_home_odds_avg']}, "
              f"Away={result['sofascore_away_odds_avg']}")
        
        return result
        
    except Exception as e:
        print(f"⚠️ Could not extract SofaScore odds: {e}")
        return result


def scrape_sofascore_full(
    driver: webdriver.Chrome,
    home_team: str,
    away_team: str,
    sport: str = 'football',
    date_str: str = None
) -> Dict:
    """
    Pełne scrapowanie SofaScore:
    1. Szukaj meczu
    2. Pobierz "Who will win?" predictions
    3. Pobierz odds z wielu bukmacherów
    
    Args:
        driver: Selenium WebDriver
        home_team: Nazwa gospodarzy
        away_team: Nazwa gości
        sport: Sport
        date_str: Data meczu (YYYY-MM-DD)
    
    Returns:
        Dict ze wszystkimi danymi SofaScore
    """
    result = {
        'sofascore_home_win_prob': None,
        'sofascore_draw_prob': None,
        'sofascore_away_win_prob': None,
        'sofascore_total_votes': 0,
        'sofascore_home_odds_avg': None,
        'sofascore_draw_odds_avg': None,
        'sofascore_away_odds_avg': None,
        'sofascore_best_home_odds': None,
        'sofascore_best_away_odds': None,
        'sofascore_url': None,
        'sofascore_found': False,
    }
    
    try:
        # 1. Znajdź mecz
        match_url = search_sofascore_match(driver, home_team, away_team, sport, date_str)
        
        if not match_url:
            print(f"⚠️ Match not found on SofaScore: {home_team} vs {away_team}")
            return result
        
        result['sofascore_url'] = match_url
        result['sofascore_found'] = True
        
        # 2. Pobierz predykcje
        predictions = extract_sofascore_predictions(driver, match_url, sport)
        result.update(predictions)
        
        # 3. Pobierz odds (opcjonalnie, może nie być dostępne)
        try:
            odds = get_sofascore_odds(driver, match_url, sport)
            result.update(odds)
        except Exception as e:
            print(f"⚠️ Odds not available: {e}")
        
        return result
        
    except Exception as e:
        print(f"❌ SofaScore scraping error: {e}")
        return result


# ============================================================================
# TESTING / CLI
# ============================================================================

if __name__ == "__main__":
    import argparse
    from selenium.webdriver.chrome.options import Options
    
    parser = argparse.ArgumentParser(description='Test SofaScore scraper')
    parser.add_argument('--home', required=True, help='Home team name')
    parser.add_argument('--away', required=True, help='Away team name')
    parser.add_argument('--sport', default='football', help='Sport')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    
    args = parser.parse_args()
    
    # Setup Chrome
    chrome_options = Options()
    if args.headless:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        print(f"\n{'='*60}")
        print(f"TESTING SOFASCORE SCRAPER")
        print(f"{'='*60}\n")
        
        result = scrape_sofascore_full(
            driver=driver,
            home_team=args.home,
            away_team=args.away,
            sport=args.sport
        )
        
        print(f"\n{'='*60}")
        print(f"RESULTS:")
        print(f"{'='*60}")
        for key, value in result.items():
            print(f"{key}: {value}")
        
    finally:
        driver.quit()
