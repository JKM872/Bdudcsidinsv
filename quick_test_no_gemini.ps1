# QUICK TEST - Run scraper without Gemini for basic H2H testing
# This tests ChromeDriver and basic scraping functionality

Write-Host "🚀 QUICK TEST - Basic H2H Scraping (No Gemini)" -ForegroundColor Cyan
Write-Host "=" * 60

python livesport_h2h_scraper.py `
    --mode auto `
    --date 2025-11-16 `
    --sports football `
    --output-suffix QUICK_TEST

Write-Host "`n✅ Test zakończony!" -ForegroundColor Green
Write-Host "📊 Sprawdź wyniki w outputs\livesport_h2h_2025-11-16_QUICK_TEST.csv"
