# 🗄️ SUPABASE SETUP GUIDE

## Step-by-Step Database Configuration

### 📍 Your Supabase Project
**URL:** https://atdyvzpjlfexqqjxokgq.supabase.co
**API Key:** eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... (already configured)

---

## 🚀 QUICK SETUP (5 minutes)

### Step 1: Open Supabase SQL Editor
1. Go to: https://atdyvzpjlfexqqjxokgq.supabase.co/project/_/sql
2. Click "New Query"

### Step 2: Run Schema Script
1. Open file: `supabase_schema.sql`
2. Copy **ALL** content (Ctrl+A, Ctrl+C)
3. Paste into Supabase SQL Editor
4. Click **"RUN"** button (bottom right)

### Step 3: Verify Table Created
Run this query:
```sql
SELECT * FROM predictions LIMIT 10;
```

Expected result: Empty table (0 rows) with all columns

### Step 4: Test Connection
```bash
python supabase_manager.py
```

Expected output:
```
✅ Connected to Supabase: https://atdyvzpjlfexqqjxokgq.supabase.co
✅ Test save: True
```

---

## 📋 Table Structure

```sql
predictions
├─ id (BIGSERIAL PRIMARY KEY)
├─ match_date (DATE)
├─ match_time (TIME)
├─ home_team (TEXT)
├─ away_team (TEXT)
├─ sport (TEXT)
├─ league (TEXT)
│
├─ LiveSport Data:
│  ├─ livesport_h2h_home_wins (INT)
│  ├─ livesport_h2h_away_wins (INT)
│  ├─ livesport_win_rate (DECIMAL)
│  ├─ livesport_home_form (TEXT)
│  └─ livesport_away_form (TEXT)
│
├─ Forebet Data:
│  ├─ forebet_prediction (TEXT)
│  ├─ forebet_probability (DECIMAL)
│  ├─ forebet_home_odds (DECIMAL)
│  ├─ forebet_draw_odds (DECIMAL)
│  └─ forebet_away_odds (DECIMAL)
│
├─ SofaScore Data:
│  ├─ sofascore_home_win_prob (DECIMAL)
│  ├─ sofascore_draw_prob (DECIMAL)
│  ├─ sofascore_away_win_prob (DECIMAL)
│  └─ sofascore_total_votes (INT)
│
├─ Gemini AI Data:
│  ├─ gemini_prediction (TEXT)
│  ├─ gemini_confidence (DECIMAL)
│  ├─ gemini_recommendation (TEXT)
│  └─ gemini_reasoning (TEXT)
│
├─ Actual Result (filled later):
│  ├─ actual_result (TEXT) -- '1', 'X', '2'
│  ├─ home_score (INT)
│  ├─ away_score (INT)
│  └─ result_updated_at (TIMESTAMPTZ)
│
└─ Metadata:
   ├─ qualifies (BOOLEAN)
   ├─ match_url (TEXT)
   └─ created_at (TIMESTAMPTZ)
```

---

## 🔐 Security (Row Level Security)

Already configured in `supabase_schema.sql`:

- ✅ **Public READ**: Anyone can view predictions
- ✅ **Authenticated WRITE**: Only authenticated users can insert/update
- ✅ **RLS Enabled**: Row Level Security active

---

## 📊 Useful Queries

### 1. View Recent Predictions (Last 7 Days)
```sql
SELECT * FROM recent_predictions;
```

### 2. View Predictions with Results
```sql
SELECT * FROM predictions_with_results;
```

### 3. View Only Qualified Matches
```sql
SELECT * FROM qualified_predictions;
```

### 4. Count Predictions by Sport
```sql
SELECT sport, COUNT(*) as total
FROM predictions
GROUP BY sport
ORDER BY total DESC;
```

### 5. Today's Predictions
```sql
SELECT home_team, away_team, 
       livesport_win_rate,
       forebet_prediction, forebet_probability,
       sofascore_home_win_prob,
       gemini_recommendation, gemini_confidence
FROM predictions
WHERE match_date = CURRENT_DATE
ORDER BY match_time;
```

### 6. Accuracy by Source (Last 30 Days)
```sql
SELECT 
  COUNT(*) FILTER (WHERE actual_result IS NOT NULL) as total_with_results,
  COUNT(*) FILTER (WHERE forebet_prediction = actual_result) as forebet_correct,
  COUNT(*) FILTER (WHERE gemini_recommendation = 'HIGH') as gemini_high_rec
FROM predictions
WHERE match_date >= CURRENT_DATE - INTERVAL '30 days';
```

---

## 🧹 Maintenance

### Clean Old Predictions (>90 days)
```sql
DELETE FROM predictions
WHERE match_date < CURRENT_DATE - INTERVAL '90 days';
```

### Update Match Result
```sql
UPDATE predictions
SET 
  actual_result = '1',  -- '1' = home win, 'X' = draw, '2' = away win
  home_score = 2,
  away_score = 1,
  result_updated_at = NOW()
WHERE id = 123;
```

### Backup to CSV
In Supabase Dashboard:
1. Go to: Table Editor → predictions
2. Click "..." (top right)
3. Select "Export as CSV"

---

## 📈 Monitoring

### Database Size
```sql
SELECT pg_size_pretty(pg_database_size(current_database())) as size;
```

### Table Size
```sql
SELECT pg_size_pretty(pg_total_relation_size('predictions')) as size;
```

### Row Count
```sql
SELECT COUNT(*) FROM predictions;
```

---

## 🔧 Troubleshooting

### Error: "Could not find table 'predictions'"
**Solution:** Run `supabase_schema.sql` in SQL Editor

### Error: "Insufficient permissions"
**Solution:** Check RLS policies, use correct API key

### Error: "Connection timeout"
**Solution:** Check internet, verify Supabase URL

### Table exists but empty
**Solution:** Run scraper with `--use-supabase` flag:
```bash
python livesport_h2h_scraper.py --mode auto --date 2025-11-18 --sports football --use-supabase
```

---

## 📦 Free Tier Limits

Supabase Free Tier:
- ✅ 500 MB database storage
- ✅ 2 GB bandwidth per month
- ✅ 50,000 monthly active users
- ✅ Unlimited API requests

**Estimate:** 
- 1 prediction ≈ 2 KB
- 500 MB ≈ 250,000 predictions
- Daily scraping (100 matches/day) = 36,500/year ✅ (fits easily)

---

## 🚨 Important Notes

1. **API Key Security**: Don't commit `supabase_manager.py` with real key to public repos
2. **Backup**: Export data monthly
3. **Indexing**: Already optimized in schema
4. **RLS**: Protects data access

---

## ✅ Verification Checklist

- [ ] Supabase project accessible at https://atdyvzpjlfexqqjxokgq.supabase.co
- [ ] `supabase_schema.sql` executed successfully
- [ ] Table `predictions` exists with all columns
- [ ] Views created: `recent_predictions`, `predictions_with_results`, `qualified_predictions`
- [ ] Indexes created for performance
- [ ] RLS policies enabled
- [ ] Test script `python supabase_manager.py` passes
- [ ] Can insert test prediction
- [ ] Can query predictions

---

## 📞 Help

If issues persist:
1. Check Supabase logs: https://atdyvzpjlfexqqjxokgq.supabase.co/project/_/logs
2. Verify API key in `supabase_manager.py`
3. Run test: `python supabase_manager.py`

---

🔥 **Database ready for 4-source prediction tracking!** 🔥
