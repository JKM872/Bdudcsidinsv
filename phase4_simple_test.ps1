#!/usr/bin/env powershell
<#
.SYNOPSIS
    Phase 4 Simple Testing Suite
    
.DESCRIPTION
    Simplified test suite - generate, filter, report, validate
#>

$ErrorActionPreference = "Stop"

Write-Host "`n🔥🔥🔥 PHASE 4 TESTING SUITE - SIMPLIFIED 🔥🔥🔥`n" -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$testSuffix = "PHASE4_FULL_$timestamp"
$outputDir = "outputs"

# ============================================================================
# PHASE 1: Generate CSV with Gemini
# ============================================================================

Write-Host "`n📊 PHASE 1: GENERATE CSV WITH GEMINI PREDICTIONS" -ForegroundColor Magenta
Write-Host ("=" * 70)

Write-Host "`n[1/6] Generating CSV with Gemini AI - Football..." -ForegroundColor Yellow

python livesport_h2h_scraper.py --mode auto --date 2025-11-17 --sports football --use-gemini --output-suffix $testSuffix --headless

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ FAILED: CSV generation failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PASSED: CSV generated successfully" -ForegroundColor Green

# Find generated CSV
$csvFiles = Get-ChildItem -Path $outputDir -Filter "*$testSuffix*.csv" | Sort-Object LastWriteTime -Descending

if ($csvFiles.Count -eq 0) {
    Write-Host "❌ No CSV files found with suffix: $testSuffix" -ForegroundColor Red
    exit 1
}

$mainCsv = $csvFiles[0].FullName
Write-Host "`n📄 Found CSV: $mainCsv" -ForegroundColor Cyan

# ============================================================================
# PHASE 2: Apply Smart Filters
# ============================================================================

Write-Host "`n🎯 PHASE 2: APPLY SMART FILTERS" -ForegroundColor Magenta
Write-Host ("=" * 70)

Write-Host "`n[2/6] Applying filter - ALL strategies..." -ForegroundColor Yellow

$filterAll = "$outputDir/smart_filter_all_$timestamp.csv"
python smart_filter.py $mainCsv --strategy all --output $filterAll

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ FAILED: Smart filter failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PASSED: Smart filter ALL completed" -ForegroundColor Green

Write-Host "`n[3/6] Applying filter - BEST_PICKS..." -ForegroundColor Yellow

$filterBest = "$outputDir/smart_filter_best_picks_$timestamp.csv"
python smart_filter.py $mainCsv --strategy best_picks --output $filterBest

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ FAILED: BEST_PICKS filter failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PASSED: Smart filter BEST_PICKS completed" -ForegroundColor Green

Write-Host "`n[4/6] Applying filter - HIGH_CONFIDENCE..." -ForegroundColor Yellow

$filterHigh = "$outputDir/smart_filter_high_confidence_$timestamp.csv"
python smart_filter.py $mainCsv --strategy high_confidence --output $filterHigh

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ FAILED: HIGH_CONFIDENCE filter failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PASSED: Smart filter HIGH_CONFIDENCE completed" -ForegroundColor Green

# ============================================================================
# PHASE 3: Generate HTML Reports
# ============================================================================

Write-Host "`n🎨 PHASE 3: GENERATE HTML REPORTS" -ForegroundColor Magenta
Write-Host ("=" * 70)

Write-Host "`n[5/6] Generating HTML report - All Matches..." -ForegroundColor Yellow

$reportMain = "$outputDir/report_all_matches_$timestamp.html"
python generate_html_report.py $mainCsv --title "Phase 4 Full Test - All Matches" --output $reportMain --max-cards 30

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ FAILED: HTML report generation failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PASSED: HTML report ALL generated" -ForegroundColor Green

Write-Host "`n[6/6] Generating HTML report - Filtered Picks..." -ForegroundColor Yellow

$reportFiltered = "$outputDir/report_filtered_$timestamp.html"
python generate_html_report.py $filterAll --title "Phase 4 Full Test - Smart Filtered" --output $reportFiltered

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ FAILED: Filtered HTML report generation failed" -ForegroundColor Red
    exit 1
}

Write-Host "✅ PASSED: HTML report FILTERED generated" -ForegroundColor Green

# ============================================================================
# PHASE 4: Validation
# ============================================================================

Write-Host "`n✅ PHASE 4: VALIDATION" -ForegroundColor Magenta
Write-Host ("=" * 70)

$allFiles = @(
    @{Path=$mainCsv; Type="Main CSV"},
    @{Path=$filterAll; Type="Filter ALL"},
    @{Path=$filterBest; Type="Filter BEST"},
    @{Path=$filterHigh; Type="Filter HIGH"},
    @{Path=$reportMain; Type="Report Main"},
    @{Path=$reportFiltered; Type="Report Filtered"}
)

$allValid = $true

foreach ($file in $allFiles) {
    if (Test-Path $file.Path) {
        $size = (Get-Item $file.Path).Length
        $sizeKB = [math]::Round($size/1KB, 2)
        Write-Host "✅ $($file.Type): $sizeKB KB" -ForegroundColor Green
    } else {
        Write-Host "❌ $($file.Type): NOT FOUND" -ForegroundColor Red
        $allValid = $false
    }
}

# ============================================================================
# FINAL REPORT
# ============================================================================

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "🏁 PHASE 4 TESTING COMPLETE" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan

if ($allValid) {
    Write-Host "`n🎉 ALL TESTS PASSED! PHASE 4 COMPLETE! 🎉" -ForegroundColor Green
    Write-Host "`n🔥🔥🔥 TRIPLE FORCE SUCCESS 🔥🔥🔥" -ForegroundColor Cyan
} else {
    Write-Host "`n⚠️ SOME FILES MISSING - REVIEW ERRORS ABOVE" -ForegroundColor Yellow
}

Write-Host "`n✨ Generated Files:" -ForegroundColor Yellow
Write-Host "   📄 Main CSV: $mainCsv" -ForegroundColor Gray
Write-Host "   🎯 Filtered CSVs: 3 files" -ForegroundColor Gray
Write-Host "   🎨 HTML Reports: 2 files" -ForegroundColor Gray

Write-Host "`n🌐 Open HTML Reports:" -ForegroundColor Magenta
Write-Host "   file:///$reportMain" -ForegroundColor Cyan
Write-Host "   file:///$reportFiltered" -ForegroundColor Cyan

Write-Host "`n🚀 Next: Open reports in browser to view results!" -ForegroundColor Yellow

# Open reports automatically
Write-Host "`n📂 Opening reports in browser..." -ForegroundColor Cyan
Start-Process $reportMain
Start-Sleep -Seconds 1
Start-Process $reportFiltered

exit 0
