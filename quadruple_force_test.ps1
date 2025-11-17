# 🔥🔥🔥🔥 QUADRUPLE FORCE TEST
# Ultimate stress test with all improvements

Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "🔥🔥🔥🔥 QUADRUPLE FORCE TEST - Ultimate Stability" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host ""

# Test 1: Single match (basic)
Write-Host "📌 TEST 1: Single Match (No Gemini)" -ForegroundColor Green
Write-Host "   Testing basic stability with retry logic..."
$start1 = Get-Date

python livesport_h2h_scraper.py `
    --mode urls `
    --date 2025-11-16 `
    --input test_past_match.txt `
    --output-suffix QF_TEST1

$duration1 = (Get-Date) - $start1
Write-Host "   ✅ Test 1 completed in $($duration1.TotalSeconds)s" -ForegroundColor Green
Write-Host ""

# Small delay between tests
Start-Sleep -Seconds 3

# Test 2: Multiple matches (stress test)
Write-Host "📌 TEST 2: Multiple Football Matches" -ForegroundColor Green
Write-Host "   Testing with 3 football matches..."
$start2 = Get-Date

python livesport_h2h_scraper.py `
    --mode urls `
    --date 2025-11-17 `
    --input test_urls_football_gemini.txt `
    --output-suffix QF_TEST2

$duration2 = (Get-Date) - $start2
Write-Host "   ✅ Test 2 completed in $($duration2.TotalSeconds)s" -ForegroundColor Green
Write-Host ""

# Show results
Write-Host ("=" * 70) -ForegroundColor Cyan
Write-Host "📊 TEST RESULTS" -ForegroundColor Yellow
Write-Host ("=" * 70) -ForegroundColor Cyan

$files = Get-ChildItem outputs\*QF_TEST*.csv -ErrorAction SilentlyContinue
if ($files) {
    Write-Host "✅ Generated files:" -ForegroundColor Green
    $files | Format-Table Name, Length, LastWriteTime -AutoSize
    
    Write-Host "`n📈 Quick Stats:" -ForegroundColor Cyan
    foreach ($file in $files) {
        $lines = (Get-Content $file | Measure-Object -Line).Lines
        Write-Host "   $($file.Name): $lines lines"
    }
} else {
    Write-Host "⚠️ No output files generated" -ForegroundColor Yellow
}

$totalTime = ($duration1.TotalSeconds + $duration2.TotalSeconds)
Write-Host "`n🎯 Total test time: $([math]::Round($totalTime, 1))s" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan
