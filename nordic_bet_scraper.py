"""
Nordic Bet Odds Scraper
Scrapes odds from Nordic Bet and other bookmakers
"""

import re
import time
from typing import Dict, Optional, List
import cloudscraper
from bs4 import BeautifulSoup


class NordicBetScraper:
    """Scraper for Nordic Bet odds"""
    
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        self.base_url = "https://www.nordicbet.com"
        
    def search_match(self, home_team: str, away_team: str, sport: str = 'football') -> Optional[str]:
        """Search for a match on Nordic Bet"""
        try:
            # Normalize team names
            home_clean = self._normalize_team_name(home_team)
            away_clean = self._normalize_team_name(away_team)
            
            # Map sport to Nordic Bet category
            sport_map = {
                'football': 'fotboll',
                'hockey': 'ishockey',
                'basketball': 'basket',
                'handball': 'handboll',
                'volleyball': 'volleyboll',
                'tennis': 'tennis'
            }
            
            sport_path = sport_map.get(sport.lower(), 'fotboll')
            search_url = f"{self.base_url}/sv/odds/{sport_path}"
            
            response = self.scraper.get(search_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find match in listings
            matches = soup.find_all('div', class_=['event-item', 'match-row'])
            
            for match in matches:
                match_text = match.get_text().lower()
                if home_clean in match_text and away_clean in match_text:
                    link = match.find('a', href=True)
                    if link:
                        return self.base_url + link['href']
            
            return None
            
        except Exception as e:
            print(f"❌ Nordic Bet search error: {e}")
            return None
    
    def get_odds(self, home_team: str, away_team: str, sport: str = 'football') -> Dict:
        """Get odds for a match"""
        result = {
            'nordic_bet_home_odds': None,
            'nordic_bet_draw_odds': None,
            'nordic_bet_away_odds': None,
            'nordic_bet_found': False
        }
        
        try:
            match_url = self.search_match(home_team, away_team, sport)
            
            if not match_url:
                print(f"⚠️ Nordic Bet: Match not found - {home_team} vs {away_team}")
                return result
            
            # Get match page
            response = self.scraper.get(match_url, timeout=15)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find 1X2 odds
            odds_sections = soup.find_all('div', class_=['odds-row', 'market-row'])
            
            for section in odds_sections:
                market_name = section.find(['h3', 'span'], class_=['market-name', 'market-title'])
                if market_name and '1x2' in market_name.get_text().lower():
                    odds_buttons = section.find_all(['button', 'div'], class_=['odd-button', 'odd-value'])
                    
                    if len(odds_buttons) >= 2:
                        result['nordic_bet_home_odds'] = self._extract_odd_value(odds_buttons[0])
                        
                        # Check if sport has draws
                        if sport.lower() not in ['basketball', 'volleyball', 'tennis', 'handball', 'hockey']:
                            if len(odds_buttons) >= 3:
                                result['nordic_bet_draw_odds'] = self._extract_odd_value(odds_buttons[1])
                                result['nordic_bet_away_odds'] = self._extract_odd_value(odds_buttons[2])
                        else:
                            result['nordic_bet_away_odds'] = self._extract_odd_value(odds_buttons[1])
                        
                        result['nordic_bet_found'] = True
                        break
            
            if result['nordic_bet_found']:
                print(f"✅ Nordic Bet: {home_team} vs {away_team} - {result['nordic_bet_home_odds']}/{result['nordic_bet_draw_odds']}/{result['nordic_bet_away_odds']}")
            else:
                print(f"⚠️ Nordic Bet: Odds not found for {home_team} vs {away_team}")
                
            return result
            
        except Exception as e:
            print(f"❌ Nordic Bet scraping error: {e}")
            return result
    
    def _normalize_team_name(self, team: str) -> str:
        """Normalize team name for matching"""
        # Remove common suffixes
        team = re.sub(r'\s+(FC|CF|SC|IF|BK|IK|AIK|DIF|U\d+|II|B)\b', '', team, flags=re.IGNORECASE)
        team = team.lower().strip()
        # Remove special characters
        team = re.sub(r'[^\w\s]', '', team)
        return team
    
    def _extract_odd_value(self, element) -> Optional[float]:
        """Extract odd value from element"""
        try:
            text = element.get_text().strip()
            # Extract number (format: 1.85 or 1,85)
            match = re.search(r'(\d+[.,]\d+)', text)
            if match:
                value = match.group(1).replace(',', '.')
                return float(value)
        except:
            pass
        return None


class BookmakersAggregator:
    """Aggregate odds from multiple bookmakers"""
    
    def __init__(self):
        self.scraper = cloudscraper.create_scraper()
        
    def get_odds_comparison(self, home_team: str, away_team: str, sport: str = 'football') -> Dict:
        """Get odds from multiple bookmakers"""
        result = {
            'best_home_odds': None,
            'best_draw_odds': None,
            'best_away_odds': None,
            'odds_sources': []
        }
        
        # Try Nordic Bet
        nordic_scraper = NordicBetScraper()
        nordic_odds = nordic_scraper.get_odds(home_team, away_team, sport)
        
        if nordic_odds['nordic_bet_found']:
            result['odds_sources'].append('Nordic Bet')
            
            # Update best odds
            if nordic_odds['nordic_bet_home_odds']:
                result['best_home_odds'] = nordic_odds['nordic_bet_home_odds']
            if nordic_odds['nordic_bet_draw_odds']:
                result['best_draw_odds'] = nordic_odds['nordic_bet_draw_odds']
            if nordic_odds['nordic_bet_away_odds']:
                result['best_away_odds'] = nordic_odds['nordic_bet_away_odds']
        
        # Add other bookmakers here (Pinnacle, Betfair, etc.)
        # For now, return Nordic Bet results
        
        return {**result, **nordic_odds}


def scrape_nordic_bet(home_team: str, away_team: str, sport: str = 'football') -> Dict:
    """Main function to scrape Nordic Bet odds"""
    scraper = NordicBetScraper()
    return scraper.get_odds(home_team, away_team, sport)


def get_bookmakers_odds(home_team: str, away_team: str, sport: str = 'football') -> Dict:
    """Get odds from multiple bookmakers"""
    aggregator = BookmakersAggregator()
    return aggregator.get_odds_comparison(home_team, away_team, sport)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) >= 3:
        home = sys.argv[1]
        away = sys.argv[2]
        sport = sys.argv[3] if len(sys.argv) > 3 else 'football'
        
        print(f"\n🔍 Searching Nordic Bet for: {home} vs {away} ({sport})")
        result = scrape_nordic_bet(home, away, sport)
        
        print(f"\n📊 Results:")
        print(f"Home odds: {result.get('nordic_bet_home_odds', 'N/A')}")
        print(f"Draw odds: {result.get('nordic_bet_draw_odds', 'N/A')}")
        print(f"Away odds: {result.get('nordic_bet_away_odds', 'N/A')}")
        print(f"Found: {result.get('nordic_bet_found', False)}")
    else:
        print("Usage: python nordic_bet_scraper.py 'Home Team' 'Away Team' [sport]")
