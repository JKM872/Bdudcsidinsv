import pandas as pd

df = pd.read_csv('outputs/livesport_h2h_2025-11-17_volleyball_AWAY_FOCUS_EMAIL.csv')
qual = df[df['qualifies'] == True]

print('✅ Zakwalifikowane mecze z datami ostatniego H2H:\n')
print('='*70)

for i, row in qual.iterrows():
    print(f'\n🏐 {row["home_team"]} vs {row["away_team"]}')
    print(f'   📊 H2H: {row["away_wins_in_h2h_last5"]}/{row["h2h_count"]} ({row["win_rate"]*100:.0f}%)')
    print(f'   📅 Data ostatniego meczu H2H: {row["last_h2h_date"]}')
    if row["form_advantage"]:
        print(f'   🔥 PRZEWAGA FORMY!')

print('\n' + '='*70)
print(f'Razem: {len(qual)} zakwalifikowane mecze')
