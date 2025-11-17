"""
Quick test - volleyball + Gemini AI
Test na 1 meczu z dzisiaj
"""

import subprocess
import sys

# Uruchom scraper z 1 meczem volleyball + Gemini
cmd = [
    sys.executable,
    "livesport_h2h_scraper.py",
    "--mode", "auto",
    "--date", "2025-11-17",
    "--sports", "volleyball",
    "--use-gemini"
    # BEZ --headless aby szybciej
]

print("🤖 GEMINI AI TEST - 1 mecz volleyball")
print("=" * 60)

result = subprocess.run(cmd, capture_output=False)

if result.returncode == 0:
    print("\n✅ TEST ZAKOŃCZONY!")
    print("📁 Sprawdź: outputs/livesport_h2h_2025-11-17_volleyball.csv")
else:
    print("\n❌ TEST FAILED")
    sys.exit(1)
