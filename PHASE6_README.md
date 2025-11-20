# 🚀 PHASE 6 - MULTI-SOURCE PREDICTION ENGINE

## 📊 Overview

Phase 6 adds **4-source consensus prediction** with database tracking:

```
┌─────────────────────────────────────────────────────────────┐
│           PREDICTION ENGINE v2.0 - 4 SOURCES                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  LiveSport     Forebet       SofaScore      Gemini AI      │
│  ─────────     ───────       ──────────     ─────────      │
│  • H2H (5)     • 1/X/2 (%)   • Who Win %    • Analysis     │
│  • Form        • O/U 2.5     • Community    • Reasoning    │
│  • Goals Avg   • BTTS        • Odds Agg     • Confidence   │
│                                                             │
│            ↓           ↓            ↓             ↓         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │        CONSENSUS ENGINE (4-Source Voting)           │   │
│  │        • All 4 agree = LOCK PICK 🔐                │   │
│  │        • 3/4 agree = HIGH CONFIDENCE 🟢            │   │
│  │        • 2/4 agree = MEDIUM 🟡                     │   │
│  │        • Disagree = SKIP ❌                        │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ↓                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   SUPABASE DATABASE - Historical Tracking           │   │
│  │   • All predictions saved                           │   │
│  │   • Accuracy tracking per source                    │   │
│  │   • ROI calculations                                │   │
│  │   • Result updates after matches                    │   │
│  └─────────────────────────────────────────────────────┘   │
│                         ↓                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │   EMAIL + DASHBOARD + STATS                         │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 🆕 New Components

### 1. **`sofascore_scraper.py`** (542 lines)
Scrapes SofaScore.com for:
- "Who will win?" community predictions
- Statistical probabilities
- Multi-bookmaker odds aggregation
- Handles sports WITHOUT draws (volleyball, tennis, basketball)

**Usage:**
```bash
python sofascore_scraper.py --home "Team A" --away "Team B" --sport football --headless
```

**Functions:**
- `search_sofascore_match()` - Finds match on SofaScore
- `extract_sofascore_predictions()` - Gets "Who will win?" percentages
- `get_sofascore_odds()` - Aggregates odds from multiple bookmakers
- `scrape_sofascore_full()` - Complete scraping pipeline

**Output:**
```python
{
    'sofascore_home_win_prob': 62.0,    # %
    'sofascore_draw_prob': 20.0,        # % (None for volleyball/tennis)
    'sofascore_away_win_prob': 18.0,    # %
    'sofascore_total_votes': 1543,      # Community votes
    'sofascore_home_odds_avg': 1.85,    # Average odds
    'sofascore_best_home_odds': 1.92,   # Best odds
    'sofascore_url': 'https://...',     # Match URL
    'sofascore_found': True
}
```

---

### 2. **`supabase_manager.py`** (450+ lines)
Database manager for Supabase PostgreSQL:

**Features:**
- Save predictions to database
- Bulk insert (batch operations)
- Update match results after completion
- Calculate source accuracy (LiveSport, Forebet, SofaScore, Gemini)
- ROI tracking per source

**Usage:**
```python
from supabase_manager import SupabaseManager

manager = SupabaseManager()

# Save prediction
manager.save_prediction(match_data)

# Save multiple
manager.save_bulk_predictions([match1, match2, ...])

# Update result after match
manager.update_match_result(match_id=123, actual_result='1', home_score=2, away_score=1)

# Get accuracy stats
accuracy = manager.get_all_sources_accuracy(days=30)
print(accuracy)
# {
#   'livesport': {'accuracy': 65.2, 'roi': 12.5, 'total_predictions': 150},
#   'forebet': {'accuracy': 58.7, 'roi': -5.3, 'total_predictions': 150},
#   'sofascore': {'accuracy': 61.4, 'roi': 8.2, 'total_predictions': 150},
#   'gemini': {'accuracy': 72.1, 'roi': 24.6, 'total_predictions': 85}
# }
```

**Database:** https://atdyvzpjlfexqqjxokgq.supabase.co

---

### 3. **Updated `livesport_h2h_scraper.py`**

**New Flags:**
```bash
--use-sofascore     # Fetch SofaScore "Who will win?" predictions
--use-supabase      # Save results to Supabase database
```

**Example:**
```bash
python livesport_h2h_scraper.py \
  --mode auto \
  --date 2025-11-18 \
  --sports football \
  --use-forebet \
  --use-gemini \
  --use-sofascore \
  --use-supabase \
  --headless
```

**Process Flow:**
1. Scrape LiveSport (H2H, form)
2. Scrape Forebet (predictions, odds)
3. Scrape SofaScore (community vote, odds) ← NEW
4. Analyze with Gemini AI (reasoning, confidence)
5. Save to CSV
6. Save to Supabase ← NEW
7. Send email (optional)

---

## 🗄️ Database Setup

### Step 1: Create Supabase Project
Already done! Database: https://atdyvzpjlfexqqjxokgq.supabase.co

### Step 2: Create Table
Run SQL from `supabase_schema.sql` in Supabase SQL Editor:

1. Go to: https://atdyvzpjlfexqqjxokgq.supabase.co/project/_/sql
2. Copy-paste content from `supabase_schema.sql`
3. Click "Run"

This creates:
- `predictions` table (main storage)
- Indexes for performance
- Row Level Security policies
- Helpful views:
  - `recent_predictions` (last 7 days)
  - `predictions_with_results` (with actual outcomes)
  - `qualified_predictions` (qualifies=true only)

### Step 3: Verify
```sql
SELECT COUNT(*) FROM predictions;
```

---

## 🏀 Sports Without Draws

Some sports don't have draw option (volleyball, tennis, basketball OT, etc.).

**Handled automatically:**
- `SPORTS_WITHOUT_DRAW = ['volleyball', 'tennis', 'basketball', 'handball', 'hockey']`
- Forebet: Only shows 1/2 (no X)
- SofaScore: Only 2 percentages (Home/Away)
- Gemini: Knows sport rules

**Example - Volleyball:**
```python
# Forebet
forebet_prediction: '1' or '2'  # No 'X'
forebet_draw_odds: None

# SofaScore
sofascore_home_win_prob: 62.0
sofascore_draw_prob: None       # ← No draw option
sofascore_away_win_prob: 38.0
```

---

## 🧪 Testing

### Test 1: SofaScore Only
```bash
python sofascore_scraper.py --home "Barcelona" --away "Real Madrid" --sport football --headless
```

### Test 2: Supabase Connection
```bash
python supabase_manager.py
```

### Test 3: Full Pipeline
```bash
python test_full_pipeline.py --home "Morocco B" --away "Djibouti" --sport football
```

### Test 4: Real Scraping with All Sources
```bash
python livesport_h2h_scraper.py \
  --mode urls \
  --input test_match.txt \
  --date 2025-11-18 \
  --use-forebet \
  --use-gemini \
  --use-sofascore \
  --use-supabase \
  --headless
```

---

## 📧 Email Integration (Phase 6.6 - TODO)

Email will show **4-source consensus**:

```
┌────────────────────────────────────────────┐
│ 🔍 4-SOURCE CONSENSUS ANALYSIS            │
├────────────────────────────────────────────┤
│                                            │
│ MAROKO B vs DŻIBUTI                       │
│                                            │
│ LiveSport H2H:        ✅ 100% Home        │
│ Forebet Prediction:   ✅ 65% Home         │
│ SofaScore Community:  ✅ 72% Home         │
│ Gemini AI Analysis:   ✅ HIGH (95%)       │
│                                            │
│ 🟢 CONSENSUS: 4/4 AGREE → LOCK PICK! 🔐  │
│ Expected Value: +24% above odds           │
│                                            │
└────────────────────────────────────────────┘
```

**Consensus Levels:**
- 🔐 **LOCK (4/4)**: All sources agree → Highest confidence
- 🟢 **HIGH (3/4)**: Strong majority → High confidence
- 🟡 **MEDIUM (2/4)**: Split decision → Moderate confidence
- ❌ **SKIP (0-1/4)**: Disagree → Don't bet

---

## 🤖 GitHub Actions (Phase 6.5 - TODO)

Update `.github/workflows/` to use all sources:

```yaml
name: Daily Scraper - Full Pipeline

on:
  schedule:
    - cron: '0 11 * * *'  # 11:00 AM daily
  workflow_dispatch:

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run Full Scraper
        env:
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        run: |
          python livesport_h2h_scraper.py \
            --mode auto \
            --date $(date +%Y-%m-%d) \
            --sports football basketball volleyball \
            --use-forebet \
            --use-gemini \
            --use-sofascore \
            --use-supabase \
            --headless
      
      - name: Send Email
        run: |
          python email_notifier.py \
            --csv outputs/*.csv \
            --to jakub.majka.zg@gmail.com \
            --from-email jakub.majka.zg@gmail.com \
            --password "${{ secrets.EMAIL_PASSWORD }}"
```

---

## 📊 Accuracy Tracking

After matches finish, update results manually or via script:

```python
from supabase_manager import SupabaseManager

manager = SupabaseManager()

# Update result
manager.update_match_result(
    match_id=123,
    actual_result='1',  # Home win
    home_score=2,
    away_score=1
)

# Get accuracy for last 30 days
accuracy = manager.get_all_sources_accuracy(days=30)

for source, stats in accuracy.items():
    print(f"{source}: {stats['accuracy']}% (ROI: {stats['roi']}%)")
```

---

## 🔧 Configuration

### Supabase Credentials
Already configured in `supabase_manager.py`:
```python
SUPABASE_URL = "https://atdyvzpjlfexqqjxokgq.supabase.co"
SUPABASE_KEY = "eyJhbGc..."  # Anon key
```

### Gemini AI
`gemini_config.py`:
```python
API_KEY = "your_key_here"
```

### Email
`email_config.py`:
```python
FROM_EMAIL = "jakub.majka.zg@gmail.com"
TO_EMAIL = "jakub.majka.zg@gmail.com"
PASSWORD = "vurb tcai zaaq itjx"  # App password
PROVIDER = "gmail"
```

---

## 📦 New Dependencies

Updated `requirements.txt`:
```
supabase>=2.0.0  # ← NEW
```

Install:
```bash
pip install -r requirements.txt
```

---

## 🚀 Quick Start

### 1. Setup Database
```bash
# Run supabase_schema.sql in Supabase SQL Editor
# URL: https://atdyvzpjlfexqqjxokgq.supabase.co/project/_/sql
```

### 2. Install Dependencies
```bash
pip install supabase
```

### 3. Test Components
```bash
# Test SofaScore
python sofascore_scraper.py --home "Barcelona" --away "Real Madrid" --sport football

# Test Supabase
python supabase_manager.py

# Test Full Pipeline
python test_full_pipeline.py --home "Team A" --away "Team B"
```

### 4. Run Full Scraper
```bash
python livesport_h2h_scraper.py \
  --mode auto \
  --date 2025-11-18 \
  --sports football \
  --use-forebet \
  --use-gemini \
  --use-sofascore \
  --use-supabase \
  --headless
```

---

## 📈 Roadmap

- [x] Phase 6.1: SofaScore scraper
- [x] Phase 6.2: Supabase integration
- [x] Phase 6.3: Main scraper integration
- [ ] Phase 6.4: Integration testing
- [ ] Phase 6.5: GitHub Actions update
- [ ] Phase 6.6: Email 4-source consensus display
- [ ] Phase 6.7: Dashboard (Flask/React)
- [ ] Phase 6.8: ML model for source weighting

---

## 🐛 Known Issues

1. **SofaScore scraping**: Can fail due to dynamic selectors (needs maintenance)
2. **Rate limiting**: SofaScore may block after many requests
3. **Match not found**: Team name matching is fuzzy, may miss some matches

**Workarounds:**
- Use `--use-sofascore` only for important matches
- Add delays between requests
- Improve team name normalization in `sofascore_scraper.py`

---

## 💡 Tips

1. **Start small**: Test with single match before full day scraping
2. **Monitor Supabase**: Check database size (free tier = 500 MB)
3. **Clean old data**: Delete predictions older than 90 days
4. **Backup**: Export CSV regularly as backup

---

## 📞 Support

Issues? Check:
1. Supabase logs: https://atdyvzpjlfexqqjxokgq.supabase.co/project/_/logs
2. Test scripts: `python test_full_pipeline.py`
3. Debug mode: Remove `--headless` flag to see browser

---

🔥 **Phase 6 brings 4-source consensus prediction with full database tracking!** 🔥
