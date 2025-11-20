"""Analyze why Gemini gave SKIP recommendation"""
import pandas as pd

csv_file = 'outputs/livesport_h2h_2025-11-17_football_PHASE4_QUICK.csv'
df = pd.read_csv(csv_file)

skip_matches = df[df['gemini_recommendation'] == 'SKIP']

print("\n🔴 SKIP MATCH ANALYSIS")
print("=" * 80)

for idx, match in skip_matches.iterrows():
    print(f"\n📊 Match: {match['home_team']} vs {match['away_team']}")
    print(f"   🎯 Gemini Prediction: {match['gemini_prediction']}")
    print(f"   📈 Confidence: {match['gemini_confidence']}%")
    print(f"   ❌ Recommendation: {match['gemini_recommendation']}")
    
    print(f"\n   📋 Statistics:")
    print(f"      H2H Win Rate: {match['win_rate']:.1f}%")
    print(f"      Away Wins in H2H: {match['away_wins_in_h2h_last5']}/{match['h2h_last5']}")
    print(f"      Forebet Prediction: {match.get('forebet_prediction', 'N/A')}")
    print(f"      Forebet Probability: {match.get('forebet_probability', 'N/A')}")
    print(f"      Away Odds: {match.get('away_odds', 'N/A')}")
    print(f"      Qualifies: {match['qualifies']}")
    
    print(f"\n   🤖 Gemini Reasoning:")
    reasoning = match['gemini_reasoning']
    if pd.notna(reasoning):
        print(f"      {reasoning}")
    else:
        print("      (No reasoning provided)")
    
    print("\n" + "-" * 80)

print(f"\n✅ Total SKIP matches: {len(skip_matches)}")
