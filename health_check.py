"""
🔥 Health Check Script - Pre-flight verification
Checks all dependencies and configurations before running scraper
"""

import sys
import os
from pathlib import Path

def health_check():
    """Comprehensive health check for the scraper"""
    print("=" * 70)
    print("🏥 HEALTH CHECK - Pre-flight Verification")
    print("=" * 70)
    print()
    
    issues = []
    warnings = []
    
    # Check 1: Python version
    print("✓ Python version:", sys.version.split()[0])
    py_version = sys.version_info
    if py_version.major < 3 or (py_version.major == 3 and py_version.minor < 9):
        issues.append("Python 3.9+ required")
    
    # Check 2: Required packages
    print("\n📦 Checking packages...")
    required_packages = {
        'selenium': 'selenium',
        'bs4': 'beautifulsoup4',
        'pandas': 'pandas',
        'webdriver_manager': 'webdriver-manager',
    }
    
    optional_packages = {
        'google.generativeai': 'google-generativeai (Gemini AI)',
    }
    
    for module, package_name in required_packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ❌ {package_name} - MISSING")
            issues.append(f"Install: pip install {package_name}")
    
    for module, package_name in optional_packages.items():
        try:
            __import__(module)
            print(f"   ✅ {package_name}")
        except ImportError:
            print(f"   ⚠️  {package_name} - OPTIONAL (not available)")
            warnings.append(f"For AI features: pip install {package_name}")
    
    # Check 3: ChromeDriver
    print("\n🚗 Checking ChromeDriver...")
    cache_pattern = Path.home() / ".wdm" / "drivers" / "chromedriver"
    if cache_pattern.exists():
        drivers = list(cache_pattern.rglob("chromedriver.exe"))
        if drivers:
            print(f"   ✅ Found {len(drivers)} ChromeDriver(s)")
            for driver in drivers:
                print(f"      - {driver.parent.name}")
        else:
            warnings.append("No ChromeDriver in cache - will download on first run")
    else:
        warnings.append("ChromeDriver cache not found - will download on first run")
    
    # Check 4: Configuration files
    print("\n⚙️  Checking configuration...")
    config_files = [
        'gemini_config.py',
        'email_config.py',
    ]
    
    for config_file in config_files:
        if Path(config_file).exists():
            print(f"   ✅ {config_file}")
        else:
            print(f"   ⚠️  {config_file} - NOT FOUND (optional)")
            warnings.append(f"Create {config_file} from {config_file}.example if needed")
    
    # Check 5: Output directory
    print("\n📁 Checking directories...")
    outputs_dir = Path("outputs")
    if outputs_dir.exists():
        csv_count = len(list(outputs_dir.glob("*.csv")))
        print(f"   ✅ outputs/ directory exists ({csv_count} CSV files)")
    else:
        print(f"   ⚠️  outputs/ directory not found - will be created")
        warnings.append("outputs/ will be created automatically")
    
    # Check 6: Test files
    print("\n🧪 Checking test files...")
    test_files = [
        'test_urls_football_gemini.txt',
        'test_urls_volleyball_gemini.txt',
    ]
    
    found_tests = 0
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"   ✅ {test_file}")
            found_tests += 1
    
    if found_tests == 0:
        warnings.append("No test files found - create test_*.txt with URLs")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    
    if not issues and not warnings:
        print("✅ ALL CHECKS PASSED - System ready!")
        return True
    
    if warnings:
        print(f"\n⚠️  {len(warnings)} warning(s):")
        for warning in warnings:
            print(f"   - {warning}")
    
    if issues:
        print(f"\n❌ {len(issues)} critical issue(s):")
        for issue in issues:
            print(f"   - {issue}")
        print("\n❌ Please fix critical issues before running the scraper")
        return False
    
    print("\n✅ System ready (with warnings)")
    return True


if __name__ == "__main__":
    success = health_check()
    sys.exit(0 if success else 1)
