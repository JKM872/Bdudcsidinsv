"""
Gemini Results Analyzer & Filter
---------------------------------
Filtruje i analizuje wyniki scrapingu z Gemini AI predictions

Funkcje:
1. Filtrowanie po gemini_confidence >= threshold (default 80%)
2. Filtrowanie po gemini_recommendation == 'HIGH'
3. Kombinacje: HIGH recommendation + Forebet > 60%
4. Statystyki: średnia confidence, top recommendations
5. Export filtrowanych wyników do nowego CSV
6. Summary report (HTML + console)

Usage:
    python analyze_gemini_results.py outputs/livesport_h2h_2025-11-17.csv
    python analyze_gemini_results.py outputs/livesport_h2h_2025-11-17.csv --min-confidence 85
    python analyze_gemini_results.py outputs/livesport_h2h_2025-11-17.csv --high-only
    python analyze_gemini_results.py outputs/livesport_h2h_2025-11-17.csv --combo  # HIGH + Forebet>60%
"""

import sys
import argparse
import pandas as pd
from pathlib import Path
from typing import Dict, List
from datetime import datetime


def analyze_gemini_results(
    csv_path: str,
    min_confidence: int = 80,
    high_only: bool = False,
    combo_filter: bool = False,
    forebet_threshold: float = 60.0
) -> Dict:
    """
    Analizuje CSV z wynikami Gemini AI
    
    Args:
        csv_path: Ścieżka do CSV
        min_confidence: Minimalny confidence score (0-100)
        high_only: Tylko HIGH recommendations
        combo_filter: HIGH + Forebet > threshold
        forebet_threshold: Min prawdopodobieństwo Forebet (%)
    
    Returns:
        Dict ze statystykami i filtrowanym DataFrame
    """
    
    print(f"\n📊 Analyzing: {csv_path}")
    print("=" * 70)
    
    # Wczytaj CSV
    try:
        df = pd.read_csv(csv_path, encoding='utf-8-sig')
    except Exception as e:
        print(f"❌ Error loading CSV: {e}")
        return None
    
    total_matches = len(df)
    qualifying_matches = len(df[df['qualifies'] == True])
    
    print(f"📈 Total matches: {total_matches}")
    print(f"✅ Qualifying (H2H≥60%): {qualifying_matches}")
    
    # Filtruj mecze z Gemini predictions
    gemini_matches = df[df['gemini_prediction'].notna()]
    gemini_count = len(gemini_matches)
    
    print(f"🤖 With Gemini AI: {gemini_count}")
    
    if gemini_count == 0:
        print("\n⚠️  No Gemini predictions found in CSV")
        return {
            'total_matches': total_matches,
            'qualifying_matches': qualifying_matches,
            'gemini_count': 0,
            'filtered_df': pd.DataFrame()
        }
    
    # Konwersje typów
    gemini_matches['gemini_confidence'] = pd.to_numeric(gemini_matches['gemini_confidence'], errors='coerce')
    gemini_matches['forebet_probability'] = pd.to_numeric(gemini_matches['forebet_probability'], errors='coerce')
    
    # Statystyki Gemini
    print(f"\n🎯 GEMINI STATISTICS:")
    print(f"   Average confidence: {gemini_matches['gemini_confidence'].mean():.1f}%")
    print(f"   Max confidence: {gemini_matches['gemini_confidence'].max():.0f}%")
    print(f"   Min confidence: {gemini_matches['gemini_confidence'].min():.0f}%")
    
    # Recommendations breakdown
    print(f"\n📊 RECOMMENDATIONS:")
    if 'gemini_recommendation' in gemini_matches.columns:
        rec_counts = gemini_matches['gemini_recommendation'].value_counts()
        for rec, count in rec_counts.items():
            print(f"   {rec}: {count} ({count/gemini_count*100:.1f}%)")
    
    # FILTERING
    filtered = gemini_matches.copy()
    filters_applied = []
    
    # Filter 1: Confidence threshold
    if min_confidence > 0:
        before = len(filtered)
        filtered = filtered[filtered['gemini_confidence'] >= min_confidence]
        after = len(filtered)
        filters_applied.append(f"confidence≥{min_confidence}%")
        print(f"\n🔍 Filter: confidence ≥ {min_confidence}%")
        print(f"   Matches: {before} → {after} (-{before-after})")
    
    # Filter 2: HIGH recommendations only
    if high_only:
        before = len(filtered)
        filtered = filtered[filtered['gemini_recommendation'] == 'HIGH']
        after = len(filtered)
        filters_applied.append("recommendation=HIGH")
        print(f"\n🔍 Filter: HIGH recommendations only")
        print(f"   Matches: {before} → {after} (-{before-after})")
    
    # Filter 3: COMBO (HIGH + Forebet > threshold)
    if combo_filter:
        before = len(filtered)
        filtered = filtered[
            (filtered['gemini_recommendation'] == 'HIGH') &
            (filtered['forebet_probability'] > forebet_threshold)
        ]
        after = len(filtered)
        filters_applied.append(f"HIGH+Forebet>{forebet_threshold}%")
        print(f"\n🔍 Filter: HIGH + Forebet > {forebet_threshold}%")
        print(f"   Matches: {before} → {after} (-{before-after})")
    
    # RESULTS
    print(f"\n" + "=" * 70)
    print(f"✅ FILTERED RESULTS: {len(filtered)} matches")
    if filters_applied:
        print(f"   Filters: {', '.join(filters_applied)}")
    
    # Top matches
    if len(filtered) > 0:
        print(f"\n🏆 TOP MATCHES (by confidence):")
        top_matches = filtered.nlargest(5, 'gemini_confidence')
        for idx, row in top_matches.iterrows():
            home = row.get('home_team', 'Unknown')
            away = row.get('away_team', 'Unknown')
            conf = row.get('gemini_confidence', 0)
            rec = row.get('gemini_recommendation', 'N/A')
            pred = row.get('gemini_prediction', 'N/A')
            
            # Truncate prediction
            if len(str(pred)) > 60:
                pred = str(pred)[:60] + "..."
            
            print(f"\n   {home} vs {away}")
            print(f"   ├─ Confidence: {conf:.0f}%")
            print(f"   ├─ Recommendation: {rec}")
            print(f"   └─ Prediction: {pred}")
    
    return {
        'total_matches': total_matches,
        'qualifying_matches': qualifying_matches,
        'gemini_count': gemini_count,
        'filtered_count': len(filtered),
        'filtered_df': filtered,
        'filters_applied': filters_applied
    }


def export_filtered_results(results: Dict, output_path: str):
    """Exportuje filtrowane wyniki do nowego CSV"""
    
    if results is None or len(results['filtered_df']) == 0:
        print("\n⚠️  No results to export")
        return
    
    df = results['filtered_df']
    
    # Wybierz najważniejsze kolumny dla czytelności
    important_cols = [
        'home_team', 'away_team', 'match_time',
        'home_wins_in_h2h_last5', 'h2h_count', 'win_rate',
        'gemini_prediction', 'gemini_confidence', 'gemini_recommendation',
        'forebet_prediction', 'forebet_probability',
        'home_odds', 'away_odds',
        'match_url'
    ]
    
    # Filtruj tylko istniejące kolumny
    export_cols = [col for col in important_cols if col in df.columns]
    df_export = df[export_cols]
    
    # Zapisz
    df_export.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"\n💾 Exported to: {output_path}")
    print(f"   Columns: {len(export_cols)}")
    print(f"   Rows: {len(df_export)}")


def generate_html_report(results: Dict, output_path: str):
    """Generuje HTML report ze statystykami"""
    
    if results is None:
        return
    
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Gemini AI Analysis Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        h1 {{ color: #1a73e8; }}
        .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 30px 0; }}
        .stat-box {{ background: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #1a73e8; }}
        .stat-label {{ color: #666; margin-top: 10px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 30px 0; }}
        th {{ background: #1a73e8; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        tr:hover {{ background: #f5f5f5; }}
        .confidence-high {{ color: #0f9d58; font-weight: bold; }}
        .confidence-medium {{ color: #f4b400; }}
        .confidence-low {{ color: #db4437; }}
        .rec-high {{ background: #0f9d58; color: white; padding: 4px 8px; border-radius: 4px; }}
        .rec-medium {{ background: #f4b400; color: white; padding: 4px 8px; border-radius: 4px; }}
        .rec-low {{ background: #db4437; color: white; padding: 4px 8px; border-radius: 4px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Gemini AI Analysis Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        
        <div class="stats">
            <div class="stat-box">
                <div class="stat-value">{results['total_matches']}</div>
                <div class="stat-label">Total Matches</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{results['qualifying_matches']}</div>
                <div class="stat-label">Qualifying (H2H≥60%)</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{results['gemini_count']}</div>
                <div class="stat-label">With Gemini AI</div>
            </div>
            <div class="stat-box">
                <div class="stat-value">{results['filtered_count']}</div>
                <div class="stat-label">Filtered Results</div>
            </div>
        </div>
        
        <h2>🏆 Top Matches</h2>
        <table>
            <tr>
                <th>Match</th>
                <th>Confidence</th>
                <th>Recommendation</th>
                <th>Prediction</th>
            </tr>
"""
    
    # Top 10 matches
    if len(results['filtered_df']) > 0:
        top = results['filtered_df'].nlargest(10, 'gemini_confidence')
        for idx, row in top.iterrows():
            home = row.get('home_team', 'Unknown')
            away = row.get('away_team', 'Unknown')
            conf = row.get('gemini_confidence', 0)
            rec = row.get('gemini_recommendation', 'N/A')
            pred = str(row.get('gemini_prediction', 'N/A'))
            
            # Color coding
            conf_class = 'confidence-high' if conf >= 80 else 'confidence-medium' if conf >= 60 else 'confidence-low'
            rec_class = f'rec-{rec.lower()}' if rec in ['HIGH', 'MEDIUM', 'LOW'] else ''
            
            # Truncate
            if len(pred) > 100:
                pred = pred[:100] + "..."
            
            html += f"""
            <tr>
                <td><strong>{home}</strong> vs {away}</td>
                <td class="{conf_class}">{conf:.0f}%</td>
                <td><span class="{rec_class}">{rec}</span></td>
                <td>{pred}</td>
            </tr>
"""
    
    html += """
        </table>
    </div>
</body>
</html>
"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n📄 HTML report: {output_path}")


def main():
    parser = argparse.ArgumentParser(description='Analyze Gemini AI results from CSV')
    parser.add_argument('csv_file', help='Path to CSV file with Gemini predictions')
    parser.add_argument('--min-confidence', type=int, default=80, 
                       help='Minimum confidence score (0-100, default: 80)')
    parser.add_argument('--high-only', action='store_true',
                       help='Show only HIGH recommendations')
    parser.add_argument('--combo', action='store_true',
                       help='Combo filter: HIGH + Forebet > 60%%')
    parser.add_argument('--forebet-threshold', type=float, default=60.0,
                       help='Minimum Forebet probability for combo (default: 60.0)')
    parser.add_argument('--export', help='Export filtered results to CSV')
    parser.add_argument('--html-report', help='Generate HTML report')
    
    args = parser.parse_args()
    
    # Validate CSV exists
    if not Path(args.csv_file).exists():
        print(f"❌ Error: File not found: {args.csv_file}")
        sys.exit(1)
    
    # Analyze
    results = analyze_gemini_results(
        csv_path=args.csv_file,
        min_confidence=args.min_confidence,
        high_only=args.high_only,
        combo_filter=args.combo,
        forebet_threshold=args.forebet_threshold
    )
    
    if results is None:
        sys.exit(1)
    
    # Export filtered CSV
    if args.export:
        export_filtered_results(results, args.export)
    
    # Generate HTML report
    if args.html_report:
        generate_html_report(results, args.html_report)
    
    print("\n✅ Analysis complete!")


if __name__ == '__main__':
    main()
