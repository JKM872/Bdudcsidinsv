from supabase_manager import SupabaseManager

mgr = SupabaseManager()
result = mgr.client.table('predictions').select('*').execute()
print(f'✅ Total predictions in DB: {len(result.data)}')

recent = mgr.client.table('predictions').select('*').order('created_at', desc=True).limit(5).execute()
print(f'\n📊 Recent 5 predictions:')
for i, p in enumerate(recent.data, 1):
    print(f'  {i}. {p["home_team"]} vs {p["away_team"]}')
    print(f'     Date: {p["match_date"]} | Sport: {p["sport"]}')
    print(f'     H2H: {p.get("livesport_win_rate", "N/A")}% | Forebet: {p.get("forebet_probability", "N/A")}%')
    print(f'     SofaScore: {p.get("sofascore_home_win_prob", "N/A")}% | Gemini: {p.get("gemini_confidence", "N/A")}%')
    print()
