# Changelog

Wszystkie istotne zmiany w projekcie będą dokumentowane w tym pliku.

## [5.0.0-tennis-rebuild] - 2026-02-28

### 🎾 Tennis Scoring Engine v4 (nowy)

- **Unified 5-factor probability model** (Player A / Player B – bez bias home/away):
  - H2H recency-weighted (30%), forma bieżąca (25%), forma na nawierzchni (20%), ranking gap (15%), odds-implied (10%)
- **Temperature-calibrated softmax** – konfigurowalna kalibracja (domyślnie T=1.10)
- **Pełne wyjście**: `prob_a`, `prob_b`, EV, edge, Kelly, `best_pick`, `advanced_score` (0–100)
- Plik kalibracji: `outputs/tennis_calibration.json`

### ⚙️ Przebudowa process_match_tennis

- Usunięto syntetyczne dane (`extract_player_form_simple`, `calculate_surface_stats_from_h2h`)
- Dodano `_extract_real_form_badges()` – wyłącznie prawdziwe badge z HTML
- Dodano `_finalise()` helper – compatibility fields na WSZYSTKICH ścieżkach wyjścia
- Zamieniono substring matching na `_teams_match()` dla H2H

### 🔧 Poprawki field-name w pipeline

- `away_wins_in_h2h` → `away_wins_in_h2h_last5` (scraper + scrape_and_notify)
- `time` → `match_time`, `url` → `match_url`, `forebet_score` → `forebet_exact_score` (JSON export)
- `focus_team` z `row.get()` zamiast hardcoded klucza

### 📧 Email notifier

- Etykieta "Tennis Engine (5-factor)" dla meczów tenisowych
- Prawdopodobieństwo wyświetlane jako "A: X% | B: Y%" (bez draw)
- Próg advanced_score obniżony z 50 → 45

### ✅ Testy regresyjne (58 nowych)

- `test_tennis_scoring_engine.py` – 38 testów (silnik, features, kalibracja, utility)
- `test_tennis_fixes.py` – 20 testów (field names, brak syntetycznych danych, compatibility)
- CI workflow zaktualizowany o 2 nowe kroki

### 📊 Podsumowanie testów

- 58/58 nowych testów tenisowych ✅
- 29/29 istniejących testów piłkarskich ✅
- Łącznie 87 testów passing

---

## [2.0.0] - 2025-10-05

### ✨ Dodano (Multi-Sport Edition)

- **Wsparcie dla 6 sportów**: piłka nożna, koszykówka, siatkówka, piłka ręczna, rugby, hokej
- **Automatyczne zbieranie linków** (`--mode auto`) z filtr owaniem po sportach
- **Filtrowanie po ligach** (`--leagues`) - możliwość zawężenia do konkretnych rozgrywek
- **Zaawansowany tryb zbierania** (`--advanced`) dla lepszej niezawodności
- **Predefined ligi** - słownik popularnych lig dla każdego sportu
- **Kolorowe logi** z emoji dla lepszej czytelności
- **Szczegółowe podsumowanie** po zakończeniu scrapowania
- **Adaptacyjny rate limiting** - inteligentne opóźnienia między requestami
- **Generator URLi** (`generate_urls.py`) - pomocniczy skrypt do tworzenia szablonów
- **Quick launch scripts** - `.bat` dla Windows, `.sh` dla Linux/Mac
- **Rozbudowana dokumentacja**:
  - README.md - pełna dokumentacja
  - QUICKSTART.md - szybki start w 5 minut
  - CHANGELOG.md - historia zmian
- **Przykładowe pliki**:
  - match_urls.txt - szablon z przykładami
  - .gitignore - ignorowane pliki

### 🔧 Zmieniono

- Ulepszone parsowanie H2H - więcej heurystyk
- Lepsza normalizacja URLi
- Wsparcie dla różnych formatów daty w URLach
- Ulepszona obsługa błędów z informacyjnymi komunikatami

### 🐛 Naprawiono

- Problem z duplikatami URLi
- Lepsza obsługa meczów bez danych H2H
- Encoding UTF-8-BOM dla poprawnego wyświetlania polskich znaków w Excel

---

## [1.0.0] - 2025-10-04 (Wersja bazowa)

### ✨ Dodano

- Podstawowy scraper dla Livesport.com
- Tryb `urls` - przetwarzanie z pliku
- Tryb `auto` - automatyczne zbieranie linków
- Parsowanie H2H (bezpośrednie spotkania)
- Filtrowanie meczów gdzie gospodarze wygrali ≥2/5 H2H
- Export do CSV
- Selenium WebDriver z Chrome
- Podstawowa dokumentacja

### 📋 Wymagania

- selenium, beautifulsoup4, pandas, webdriver-manager
- Chrome + Chromedriver

