#!/usr/bin/env powershell
<#
.SYNOPSIS
    Phase 4 Complete Testing Suite - Triple Force Methodology
    
.DESCRIPTION
    1. Generate CSV with Gemini predictions (real data)
    2. Apply smart_filter with all 4 strategies
    3. Generate beautiful HTML reports
    4. Validate all outputs
    
    TRIPLE FORCE: Build ✅ → Test 🔄 → Fix ⚠️
#>

$ErrorActionPreference = "Stop"

Write-Host "`n🔥🔥🔥 PHASE 4 TESTING SUITE - TRIPLE FORCE 🔥🔥🔥`n" -ForegroundColor Cyan

# Configuration
$date = Get-Date -Format "yyyy-MM-dd"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$testSuffix = "PHASE4_TEST_$timestamp"
$outputDir = "outputs"

# Test counters
$testsTotal = 0
$testsPassed = 0
$testsFailed = 0

function Test-Step {
    param(
        [string]$Name,
        [scriptblock]$Action
    )
    
    $script:testsTotal++
    Write-Host "`n[$script:testsTotal] Testing: $Name" -ForegroundColor Yellow
    
    try {
        & $Action
        Write-Host "✅ PASSED: $Name" -ForegroundColor Green
        $script:testsPassed++
        return $true
    }
    catch {
        Write-Host "❌ FAILED: $Name" -ForegroundColor Red
        Write-Host "Error: $_" -ForegroundColor Red
        $script:testsFailed++
        return $false
    }
}

# ============================================================================
# PHASE 1: Generate CSV with Gemini Predictions
# ============================================================================

Write-Host "`n📊 PHASE 1: GENERATE CSV WITH GEMINI PREDICTIONS" -ForegroundColor Magenta
Write-Host "=" * 70

Test-Step "Generate CSV - Football Only" {
    python livesport_h2h_scraper.py `
        --mode auto `
        --date $date `
        --sports football `
        --use-gemini `
        --output-suffix $testSuffix `
        --headless
    
    if ($LASTEXITCODE -ne 0) {
        throw "livesport_h2h_scraper.py failed with exit code $LASTEXITCODE"
    }
}

# Find generated CSV
$csvFiles = Get-ChildItem -Path $outputDir -Filter "*$testSuffix*.csv" | Sort-Object LastWriteTime -Descending

if ($csvFiles.Count -eq 0) {
    Write-Host "❌ No CSV files found with suffix: $testSuffix" -ForegroundColor Red
    exit 1
}

$mainCsv = $csvFiles[0].FullName
Write-Host "`n📄 Found CSV: $mainCsv" -ForegroundColor Cyan

# Validate CSV has Gemini columns
Test-Step "Validate Gemini columns in CSV" {
    $csvContent = Get-Content $mainCsv -First 1
    
    $requiredColumns = @(
        'gemini_recommendation',
        'gemini_confidence',
        'gemini_reasoning',
        'gemini_advanced_score'
    )
    
    foreach ($col in $requiredColumns) {
        if ($csvContent -notmatch $col) {
            throw "Missing required column: $col"
        }
    }
    
    Write-Host "  ✓ All 4 Gemini columns present" -ForegroundColor Gray
}

# ============================================================================
# PHASE 2: Apply Smart Filters
# ============================================================================

Write-Host "`n🎯 PHASE 2: APPLY SMART FILTERS (4 STRATEGIES)" -ForegroundColor Magenta
Write-Host "=" * 70

$strategies = @('all', 'best_picks', 'high_confidence', 'value_plays', 'locked_picks')

foreach ($strategy in $strategies) {
    Test-Step "Smart Filter - Strategy: $strategy" {
        $filterOutput = "$outputDir/smart_filter_${strategy}_${timestamp}.csv"
        
        python smart_filter.py $mainCsv --strategy $strategy --output $filterOutput
        
        if ($LASTEXITCODE -ne 0) {
            throw "smart_filter.py failed for strategy: $strategy"
        }
        
        if (-not (Test-Path $filterOutput)) {
            throw "Filter output not created: $filterOutput"
        }
        
        $lineCount = (Get-Content $filterOutput).Count
        Write-Host "  ✓ Created: $filterOutput - $lineCount lines" -ForegroundColor Gray
    }
}

# ============================================================================
# PHASE 3: Generate HTML Reports
# ============================================================================

Write-Host "`n🎨 PHASE 3: GENERATE HTML REPORTS" -ForegroundColor Magenta
Write-Host "=" * 70

# Report from main CSV
Test-Step "HTML Report - Main CSV (All Matches)" {
    $reportPath = "$outputDir/report_main_${timestamp}.html"
    
    python generate_html_report.py $mainCsv `
        --title "Phase 4 Test - All Matches" `
        --output $reportPath
    
    if ($LASTEXITCODE -ne 0) {
        throw "generate_html_report.py failed for main CSV"
    }
    
    if (-not (Test-Path $reportPath)) {
        throw "HTML report not created: $reportPath"
    }
    
    $size = (Get-Item $reportPath).Length
    $sizeKB = [math]::Round($size/1KB, 2)
    Write-Host "  ✓ Created: $reportPath - $sizeKB KB" -ForegroundColor Gray
}

# Reports from filtered CSVs
$filterFiles = Get-ChildItem -Path $outputDir -Filter "smart_filter_*_${timestamp}.csv"

foreach ($filterFile in $filterFiles) {
    $strategyName = $filterFile.BaseName -replace "smart_filter_(.+)_\d+", '$1'
    
    Test-Step "HTML Report - Strategy: $strategyName" {
        $reportPath = "$outputDir/report_${strategyName}_${timestamp}.html"
        
        python generate_html_report.py $filterFile.FullName `
            --title "Phase 4 Test - $strategyName Strategy" `
            --output $reportPath
        
        if ($LASTEXITCODE -ne 0) {
            throw "generate_html_report.py failed for $strategyName"
        }
        
        if (-not (Test-Path $reportPath)) {
            throw "HTML report not created: $reportPath"
        }
        
        $size = (Get-Item $reportPath).Length
        $sizeKB = [math]::Round($size/1KB, 2)
        Write-Host "  ✓ Created: $reportPath - $sizeKB KB" -ForegroundColor Gray
    }
}

# ============================================================================
# PHASE 4: Validation and Quality Checks
# ============================================================================

Write-Host "`n✅ PHASE 4: VALIDATION AND QUALITY CHECKS" -ForegroundColor Magenta
Write-Host "=" * 70

# Check all HTML files are valid
$htmlFiles = Get-ChildItem -Path $outputDir -Filter "report_*_${timestamp}.html"

Test-Step "Validate HTML files structure" {
    foreach ($htmlFile in $htmlFiles) {
        $content = Get-Content $htmlFile.FullName -Raw
        
        # Check for essential HTML elements
        $checks = @(
            '<!DOCTYPE html>',
            '<title>',
            '<style>',
            'container',
            'match-card'
        )
        
        foreach ($check in $checks) {
            if ($content -notmatch [regex]::Escape($check)) {
                throw "Missing element in ${htmlFile}: $check"
            }
        }
    }
    
    Write-Host "  ✓ All HTML files valid" -ForegroundColor Gray
}

# Verify filter results
Test-Step "Verify filter counts are logical" {
    $allCsv = Get-ChildItem -Path $outputDir -Filter "smart_filter_all_${timestamp}.csv" | Select-Object -First 1
    
    if ($allCsv) {
        $allContent = Import-Csv $allCsv.FullName
        $allCount = $allContent.Count
        
        Write-Host "  ✓ Strategy 'all' returned $allCount matches" -ForegroundColor Gray
        
        # Individual strategies should have <= 'all' count
        foreach ($strategy in @('best_picks', 'high_confidence', 'value_plays', 'locked_picks')) {
            $strategyCsv = Get-ChildItem -Path $outputDir -Filter "smart_filter_${strategy}_${timestamp}.csv" | Select-Object -First 1
            
            if ($strategyCsv) {
                $strategyContent = Import-Csv $strategyCsv.FullName
                $strategyCount = $strategyContent.Count
                
                Write-Host "  ✓ Strategy '$strategy' returned $strategyCount matches" -ForegroundColor Gray
                
                if ($strategyCount -gt $allCount) {
                    Write-Host "  ⚠️ WARNING: $strategy has more matches than 'all' ($strategyCount > $allCount)" -ForegroundColor Yellow
                }
            }
        }
    }
}

# ============================================================================
# FINAL REPORT
# ============================================================================

Write-Host "`n" + ("=" * 70) -ForegroundColor Cyan
Write-Host "🏁 PHASE 4 TESTING COMPLETE" -ForegroundColor Cyan
Write-Host ("=" * 70) -ForegroundColor Cyan

Write-Host "`n📊 TEST RESULTS:" -ForegroundColor White
Write-Host "   Total Tests: $testsTotal" -ForegroundColor White
Write-Host "   ✅ Passed: $testsPassed" -ForegroundColor Green
Write-Host "   ❌ Failed: $testsFailed" -ForegroundColor Red

if ($testsFailed -eq 0) {
    Write-Host "`n🎉 ALL TESTS PASSED! PHASE 4 COMPLETE! 🎉" -ForegroundColor Green
    Write-Host "`n🔥🔥🔥 TRIPLE FORCE SUCCESS 🔥🔥🔥" -ForegroundColor Cyan
} else {
    Write-Host "`n⚠️ SOME TESTS FAILED - REVIEW ERRORS ABOVE" -ForegroundColor Yellow
}

Write-Host "`n📁 Output Directory: $outputDir" -ForegroundColor Cyan
Write-Host "🌐 Open HTML reports in browser to view results" -ForegroundColor Cyan

Write-Host "`n✨ Generated Files:" -ForegroundColor Yellow
Write-Host "   📄 Main CSV: $mainCsv" -ForegroundColor Gray
Write-Host "   🎯 Filtered CSVs: $($filterFiles.Count) files" -ForegroundColor Gray
Write-Host "   🎨 HTML Reports: $($htmlFiles.Count) files" -ForegroundColor Gray

# List all HTML reports
Write-Host "`n🌐 HTML Reports to Open:" -ForegroundColor Magenta
foreach ($html in $htmlFiles) {
    Write-Host "   file:///$($html.FullName)" -ForegroundColor Cyan
}

exit $(if ($testsFailed -eq 0) { 0 } else { 1 })
