# 🎯 FOREBET - SZYBKI START

## Co to jest Forebet?

Forebet.com to serwis z **automatycznymi predykcjami meczów** opartymi na AI/statystykach. 
Teraz możesz **automatycznie pobierać te predykcje** razem z danymi H2H!

---

## 🚀 JAK URUCHOMIĆ?

### Krok 1: Dodaj flagę `--use-forebet`

**PRZED (bez Forebet):**
```bash
python livesport_h2h_scraper.py --date 2025-11-17 --sports volleyball
```

**TERAZ (z Forebet):**
```bash
python livesport_h2h_scraper.py --date 2025-11-17 --sports volleyball --use-forebet
```

### Krok 2: Poczekaj (otworzy się przeglądarka)

⚠️ **UWAGA:** Forebet wymaga widocznej przeglądarki (nie działa headless)!

Zobaczysz Chrome otwierającego się automatycznie - to NORMALNE.  
Cloudflare wymaga "prawdziwej" przeglądarki.

### Krok 3: Zobacz wyniki

```
🎯 Forebet: Goście (50%) | Wynik: 1-3 | O/U: Over 2.5 | BTTS: Yes | Avg: 3.2
```

---

## 📧 Z EMAILEM

```bash
python scrape_and_notify.py ^
  --date 2025-11-17 ^
  --sports volleyball ^
  --use-forebet ^
  --to jakub.majka.zg@gmail.com ^
  --from-email jakub.majka.zg@gmail.com ^
  --password "vurb tcai zaaq itjx" ^
  --max-matches 5
```

---

## 📊 CO DOSTANIESZ?

### Każdy mecz będzie miał:

1. **Predykcja** (`forebet_prediction`): 
   - `1` = Wygrana gospodarzy
   - `X` = Remis
   - `2` = Wygrana gości

2. **Prawdopodobieństwo** (`forebet_probability`): 
   - np. `50.0` = 50% szans

3. **Dokładny wynik** (`forebet_exact_score`): 
   - np. `1-3` (gospodarze 1, goście 3)

4. **Over/Under** (`forebet_over_under`): 
   - np. `Over 2.5` = ponad 2.5 gola w meczu

5. **BTTS** (`forebet_btts`): 
   - `Yes` = obie drużyny strzelą
   - `No` = tylko jedna (lub żadna) strzeli

6. **Średnia goli** (`forebet_avg_goals`): 
   - np. `3.2` = średnio 3.2 gola w meczu

---

## ⚽ WSPIERANE SPORTY

- ✅ **Football** (piłka nożna)
- ✅ **Volleyball** (siatkówka) 
- ✅ **Basketball** (koszykówka)
- ✅ **Tennis** (tenis)
- ✅ **Hockey** (hokej)
- ✅ **Handball** (piłka ręczna)
- ✅ **Rugby**

**Ta sama składnia dla WSZYSTKICH sportów!**

---

## ⚙️ OPCJE

### Tylko mecze z przewagą formy + Forebet:
```bash
python livesport_h2h_scraper.py --date 2025-11-17 --sports volleyball ^
  --use-forebet --only-form-advantage
```

### Fokus na gości + Forebet:
```bash
python livesport_h2h_scraper.py --date 2025-11-17 --sports volleyball ^
  --use-forebet --away-team-focus
```

### Pomijaj mecze bez kursów + Forebet:
```bash
python livesport_h2h_scraper.py --date 2025-11-17 --sports volleyball ^
  --use-forebet --skip-no-odds
```

### Wszystko naraz:
```bash
python livesport_h2h_scraper.py --date 2025-11-17 --sports volleyball ^
  --use-forebet --away-team-focus --skip-no-odds --sort time
```

---

## ⚠️ UWAGI

### 1. Widoczna przeglądarka
Forebet **WYMAGA** widocznej przeglądarki. Nie próbuj `--headless` z `--use-forebet`.

### 2. Wolniejsze działanie
Każdy mecz z Forebet zajmuje ~5-10 sekund więcej (Cloudflare bypass).

### 3. Nie zawsze są predykcje
Forebet może nie mieć predykcji dla:
- Małych/lokalnych lig
- Meczów juniorskich
- Meczów bez historii

W takich przypadkach pola Forebet będą `null`.

### 4. Działa tylko dla sportów drużynowych
Tennis używa innej logiki (advanced scoring system), więc Forebet nie jest dodawany automatycznie dla tenisa.

---

## 🔍 PRZYKŁAD WYJŚCIA CSV

```csv
home_team,away_team,match_time,h2h_count,home_wins_in_h2h_last5,win_rate,forebet_prediction,forebet_probability,forebet_exact_score,forebet_over_under,forebet_btts,forebet_avg_goals
"Rozwój Katowice","Cuprum Lubin","20:30",5,3,60.0,"1",45.0,"3-1","Over 2.5","Yes",3.8
```

---

## 🛠️ ROZWIĄZYWANIE PROBLEMÓW

### "forebet_scraper not available"
Sprawdź czy masz `undetected-chromedriver`:
```bash
pip install undetected-chromedriver
```

### Przeglądarka się nie otwiera
1. Sprawdź czy masz Chrome zainstalowane
2. Spróbuj zaktualizować selenium:
```bash
pip install --upgrade selenium
```

### Cloudflare blokuje
To normalne - może się zdarzyć. Spróbuj:
1. Odczekać 30 sekund i spróbować ponownie
2. Zrestartować komputer
3. Uruchomić bez VPN

### Brak predykcji dla meczu
To normalne - Forebet nie ma predykcji dla wszystkich meczów. Sprawdź ręcznie na forebet.com czy mecz jest tam dostępny.

---

## 🎉 GOTOWE!

Teraz każdy mecz będzie miał dodatkowo dane Forebet!

**Poprzednie dane (tylko H2H):**
```
✅ KWALIFIKUJE SIĘ! Rozwój Katowice vs Cuprum Lubin
   H2H: 3/5 (60.0%)
```

**Nowe dane (H2H + Forebet):**
```
✅ KWALIFIKUJE SIĘ! Rozwój Katowice vs Cuprum Lubin
   H2H: 3/5 (60.0%)
   🎯 Forebet: Gospodarze (45%) | Wynik: 3-1 | O/U: Over 2.5 | BTTS: Yes | Avg: 3.8
```

**Masz wszystko w jednym miejscu!** 🚀

---

## 📚 Więcej informacji

- `FOREBET_INTEGRATION_SUMMARY.md` - szczegóły techniczne
- `forebet_scraper.py` - kod źródłowy
- `API_EXAMPLES.md` - przykłady użycia API
- `FAQ.md` - najczęstsze pytania

---

## 💡 Wskazówka

Kombinuj Forebet z filtrami dla najlepszych wyników:

```bash
python livesport_h2h_scraper.py ^
  --date 2025-11-17 ^
  --sports volleyball basketball handball ^
  --use-forebet ^
  --away-team-focus ^
  --skip-no-odds ^
  --sort wins
```

**Wynik:** Mecze gdzie:
- ✅ Goście mają ≥60% H2H
- ✅ Są kursy bukmacherskie
- ✅ Są predykcje Forebet
- ✅ Posortowane po liczbie wygranych

**Perfect! 🎯**
