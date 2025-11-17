# QUADRUPLE FORCE TEST - Simplified version
Write-Host "======================================================================"
Write-Host "QUADRUPLE FORCE TEST - Ultimate Stability" -ForegroundColor Yellow
Write-Host "======================================================================"
Write-Host ""

# Test 1
Write-Host "TEST 1: Single Match" -ForegroundColor Green
python livesport_h2h_scraper.py --mode urls --date 2025-11-16 --input test_past_match.txt --output-suffix QF_TEST1
Write-Host ""

Start-Sleep -Seconds 3

# Test 2
Write-Host "TEST 2: Multiple Matches" -ForegroundColor Green
python livesport_h2h_scraper.py --mode urls --date 2025-11-17 --input test_urls_football_gemini.txt --output-suffix QF_TEST2
Write-Host ""

# Results
Write-Host "======================================================================"
Write-Host "RESULTS" -ForegroundColor Yellow
Write-Host "======================================================================"

Get-ChildItem outputs\*QF_TEST*.csv -ErrorAction SilentlyContinue | Format-Table Name, Length, LastWriteTime
