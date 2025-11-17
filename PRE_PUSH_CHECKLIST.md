# ✅ CHECKLIST PRZED PUSH DO GITHUB

## Szybka weryfikacja przed wrzuceniem kodu na GitHub

### 1. ✅ Uruchom testy lokalne

```bash
python test_github_actions_simulation.py
```

**Oczekiwany wynik:**
```
🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!
✅ Aplikacja gotowa do push na GitHub
```

### 2. ✅ Sprawdź pliki

Upewnij się że istnieją:
- [ ] `.github/workflows/test.yml` - workflow CI/CD
- [ ] `test_ci_cd.py` - testy jednostkowe
- [ ] `test_compilation.py` - testy kompilacji
- [ ] `requirements.txt` - zależności
- [ ] `README.md` - dokumentacja główna
- [ ] `FOREBET_QUICKSTART.md` - quick start Forebet
- [ ] `GITHUB_ACTIONS_GUIDE.md` - przewodnik CI/CD

### 3. ✅ Sprawdź .gitignore

Upewnij się że `.gitignore` zawiera:
```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
outputs/
*.log
.env
email_config.py
app_integration_config.json
*.csv
*.json
debug_html/
.vscode/
.idea/
```

### 4. ✅ Commit i push

```bash
# Dodaj wszystkie pliki
git add .

# Commit z opisowym komunikatem
git commit -m "Add Forebet integration and GitHub Actions CI/CD

- Integracja predykcji Forebet dla wszystkich sportów
- Automatyczne testy GitHub Actions (Python 3.9-3.13)
- Graceful degradation (działa z i bez Forebet)
- Pełna dokumentacja (FOREBET_QUICKSTART.md, GITHUB_ACTIONS_GUIDE.md)
- Testy CI/CD kompatybilne z headless mode
"

# Push do remote
git push origin main
```

### 5. ✅ Sprawdź GitHub Actions

1. Przejdź do: `https://github.com/YOUR_USERNAME/YOUR_REPO/actions`
2. Poczekaj na zakończenie testów (~3-5 minut)
3. Sprawdź czy wszystkie testy przeszły ✅

**Oczekiwany wynik:**
```
✅ Tests (Python 3.9)
✅ Tests (Python 3.10)
✅ Tests (Python 3.11)
✅ Tests (Python 3.12)
✅ Tests (Python 3.13)
✅ Lint
✅ Security
```

### 6. ✅ (Opcjonalnie) Dodaj badge do README

W `README.md` zamień:
```markdown
![Tests](https://img.shields.io/badge/tests-passing-brightgreen)
```

na:
```markdown
![Tests](https://github.com/YOUR_USERNAME/YOUR_REPO/workflows/Tests/badge.svg)
```

---

## ⚠️ CO ZROBIĆ GDY TESTY NIE PRZECHODZĄ?

### Problem: test_ci_cd.py fails

```bash
# Sprawdź szczegóły
python test_ci_cd.py

# Najczęstsze problemy:
# 1. Brak Chrome/ChromeDriver - zainstaluj Chrome
# 2. Brak zależności - pip install -r requirements.txt
# 3. Import error - sprawdź czy wszystkie pliki istnieją
```

### Problem: Flake8 errors

```bash
# Sprawdź błędy składniowe
flake8 . --select=E9,F63,F7,F82

# Napraw problemy i uruchom ponownie
```

### Problem: GitHub Actions fails

1. Sprawdź logi w GitHub Actions
2. Porównaj z lokalnymi testami
3. Najczęściej: różnice między lokalnym środowiskiem a CI/CD

---

## 💡 WSKAZÓWKI

### Testuj lokalnie przed każdym push

```bash
# Szybki test (2-3 minuty)
python test_ci_cd.py

# Pełna symulacja GitHub Actions (5-7 minut)
python test_github_actions_simulation.py
```

### Używaj opisowych commitów

❌ Źle:
```bash
git commit -m "fixes"
```

✅ Dobrze:
```bash
git commit -m "Fix: Cloudflare bypass in Forebet scraper

- Added undetected-chromedriver
- Disabled headless mode for Forebet
- Added retry logic with delays
"
```

### Sprawdzaj status często

```bash
# Status repozytorium
git status

# Historia commitów
git log --oneline -5

# Remote branches
git branch -r
```

---

## 🚀 GOTOWE!

Po wykonaniu wszystkich kroków:

✅ Kod jest na GitHub  
✅ Testy CI/CD działają  
✅ Aplikacja gotowa do użycia  
✅ Dokumentacja kompletna  

**Możesz przejść do następnego etapu!** 🎉

---

## 📚 Zobacz także

- [GITHUB_ACTIONS_GUIDE.md](GITHUB_ACTIONS_GUIDE.md) - Szczegółowy przewodnik CI/CD
- [FOREBET_INTEGRATION_SUMMARY.md](FOREBET_INTEGRATION_SUMMARY.md) - Podsumowanie integracji Forebet
- [README.md](README.md) - Dokumentacja główna
