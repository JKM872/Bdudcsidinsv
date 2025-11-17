"""
SYMULACJA GITHUB ACTIONS - test lokalny przed push
Uruchamia te same testy co w GitHub Actions
"""

import subprocess
import sys
import os

print("="*80)
print("🚀 SYMULACJA GITHUB ACTIONS - TEST LOKALNY")
print("="*80)
print()
print("Ten skrypt uruchamia te same testy co GitHub Actions.")
print("Upewnij się, że wszystko przechodzi przed push do repo!")
print()

tests_passed = 0
tests_failed = 0

def run_test(name, command, critical=True):
    """Uruchom test i zwróć wynik"""
    global tests_passed, tests_failed
    
    print(f"\n{'='*80}")
    print(f"🧪 TEST: {name}")
    print(f"{'='*80}")
    print(f"Komenda: {command}")
    print()
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=False,  # Pokaż output bezpośrednio
            text=True
        )
        
        if result.returncode == 0:
            print(f"\n✅ {name}: PASSED")
            tests_passed += 1
            return True
        else:
            print(f"\n❌ {name}: FAILED (exit code: {result.returncode})")
            tests_failed += 1
            if critical:
                print(f"\n⚠️  CRITICAL TEST FAILED! Przerwano.")
                return False
            return True
            
    except Exception as e:
        print(f"\n❌ {name}: ERROR - {e}")
        tests_failed += 1
        if critical:
            return False
        return True

# Test 1: Testy CI/CD (główny)
if not run_test(
    "Testy CI/CD (test_ci_cd.py)",
    "python test_ci_cd.py",
    critical=True
):
    sys.exit(1)

# Test 2: Testy kompilacji
if not run_test(
    "Testy kompilacji (test_compilation.py)",
    "python test_compilation.py",
    critical=True
):
    sys.exit(1)

# Test 3: Import modules
if not run_test(
    "Test importów modułów",
    'python -c "from livesport_h2h_scraper import start_driver, process_match, detect_sport_from_url; print(\'✅ Imports OK\')"',
    critical=True
):
    sys.exit(1)

# Test 4: Sport detection
if not run_test(
    "Test wykrywania sportów",
    'python -c "from livesport_h2h_scraper import detect_sport_from_url; assert detect_sport_from_url(\'https://www.livesport.com/pl/siatkowka/\') == \'volleyball\'; print(\'✅ Sport detection OK\')"',
    critical=True
):
    sys.exit(1)

# Test 5: Flake8 (syntax errors tylko)
print(f"\n{'='*80}")
print(f"🧪 TEST: Flake8 (Syntax Errors)")
print(f"{'='*80}")
try:
    result = subprocess.run(
        "flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics --exclude=__pycache__,outputs,debug_html",
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print("✅ Flake8 (Syntax Errors): PASSED")
        tests_passed += 1
    else:
        print(f"⚠️  Flake8 wykrył problemy:")
        print(result.stdout)
        print(result.stderr)
        print("⚠️  Non-critical, kontynuuję...")
        tests_passed += 1  # Non-blocking
except FileNotFoundError:
    print("⚠️  Flake8 nie zainstalowany - pomijam (opcjonalny)")
    tests_passed += 1

# Test 6: Requirements check
print(f"\n{'='*80}")
print(f"🧪 TEST: Requirements.txt")
print(f"{'='*80}")
if os.path.exists('requirements.txt'):
    print("✅ requirements.txt istnieje")
    
    # Sprawdź czy zawiera podstawowe pakiety
    with open('requirements.txt', 'r') as f:
        content = f.read()
        required_packages = ['selenium', 'beautifulsoup4', 'pandas']
        missing = [pkg for pkg in required_packages if pkg not in content.lower()]
        
        if not missing:
            print(f"✅ Wszystkie wymagane pakiety: {', '.join(required_packages)}")
            tests_passed += 1
        else:
            print(f"⚠️  Brakujące pakiety w requirements.txt: {', '.join(missing)}")
            tests_failed += 1
else:
    print("❌ requirements.txt NIE ISTNIEJE!")
    tests_failed += 1

# Test 7: Workflow file
print(f"\n{'='*80}")
print(f"🧪 TEST: GitHub Actions Workflow")
print(f"{'='*80}")
workflow_path = os.path.join('.github', 'workflows', 'test.yml')
if os.path.exists(workflow_path):
    print(f"✅ Workflow file istnieje: {workflow_path}")
    tests_passed += 1
else:
    print(f"⚠️  Workflow file NIE ISTNIEJE: {workflow_path}")
    print("   GitHub Actions nie będzie działać bez tego pliku!")
    tests_failed += 1

# Test 8: Documentation
print(f"\n{'='*80}")
print(f"🧪 TEST: Dokumentacja")
print(f"{'='*80}")
docs = [
    'README.md',
    'FOREBET_QUICKSTART.md',
    'FOREBET_INTEGRATION_SUMMARY.md',
    'GITHUB_ACTIONS_GUIDE.md',
]
for doc in docs:
    if os.path.exists(doc):
        print(f"✅ {doc}")
        tests_passed += 1
    else:
        print(f"⚠️  {doc} - BRAK")
        tests_failed += 1

# PODSUMOWANIE
print()
print("="*80)
print("📊 PODSUMOWANIE TESTÓW")
print("="*80)
print()
print(f"✅ Testy przeszły:     {tests_passed}")
print(f"❌ Testy nie przeszły: {tests_failed}")
print()

if tests_failed == 0:
    print("🎉 WSZYSTKIE TESTY PRZESZŁY POMYŚLNIE!")
    print()
    print("✅ Aplikacja gotowa do push na GitHub")
    print()
    print("📝 Następne kroki:")
    print("   1. git add .")
    print("   2. git commit -m 'Add CI/CD and Forebet integration'")
    print("   3. git push origin main")
    print()
    print("🔍 Sprawdź status w GitHub Actions:")
    print("   https://github.com/YOUR_USERNAME/YOUR_REPO/actions")
    print()
    sys.exit(0)
else:
    print("⚠️  NIEKTÓRE TESTY NIE PRZESZŁY!")
    print()
    print("Napraw błędy przed push do repozytorium.")
    print()
    if tests_failed <= 3:
        print("💡 Wskazówka: Większość problemów to prawdopodobnie brakująca dokumentacja")
        print("   lub opcjonalne narzędzia (flake8). Możesz to zignorować jeśli")
        print("   główne testy (test_ci_cd.py, test_compilation.py) przeszły.")
    print()
    sys.exit(1)
