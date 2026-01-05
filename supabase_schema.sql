-- ============================================================================
-- SUPABASE DATABASE SCHEMA
-- ============================================================================
-- Run this SQL in Supabase SQL Editor: https://atdyvzpjlfexqqjxokgq.supabase.co
-- 
-- This creates the 'predictions' table for storing match predictions
-- from multiple sources (LiveSport, Forebet, SofaScore, Gemini AI)
-- ============================================================================

CREATE TABLE IF NOT EXISTS predictions (
    id BIGSERIAL PRIMARY KEY,
    
    -- Match info
    match_date DATE NOT NULL,
    match_time TIME,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    sport TEXT NOT NULL DEFAULT 'football',
    league TEXT,
    
    -- LiveSport data
    livesport_h2h_home_wins INT,
    livesport_h2h_away_wins INT,
    livesport_win_rate DECIMAL(5,2),
    livesport_home_form TEXT,
    livesport_away_form TEXT,
    
    -- Forebet data
    forebet_prediction TEXT,
    forebet_probability DECIMAL(5,2),
    forebet_home_odds DECIMAL(6,2),
    forebet_draw_odds DECIMAL(6,2),
    forebet_away_odds DECIMAL(6,2),
    
    -- SofaScore data
    sofascore_home_win_prob DECIMAL(5,2),
    sofascore_draw_prob DECIMAL(5,2),
    sofascore_away_win_prob DECIMAL(5,2),
    sofascore_total_votes INT,
    
    -- Gemini AI data
    gemini_prediction TEXT,
    gemini_confidence DECIMAL(5,2),
    gemini_recommendation TEXT,
    gemini_reasoning TEXT,
    
    -- Actual result (filled after match ends)
    actual_result TEXT,  -- '1', 'X', '2'
    home_score INT,
    away_score INT,
    result_updated_at TIMESTAMPTZ,
    
    -- Metadata
    qualifies BOOLEAN DEFAULT FALSE,
    match_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_predictions_match_date ON predictions(match_date);
CREATE INDEX IF NOT EXISTS idx_predictions_sport ON predictions(sport);
CREATE INDEX IF NOT EXISTS idx_predictions_actual_result ON predictions(actual_result);
CREATE INDEX IF NOT EXISTS idx_predictions_created_at ON predictions(created_at);
CREATE INDEX IF NOT EXISTS idx_predictions_qualifies ON predictions(qualifies);

-- Enable Row Level Security (RLS)
ALTER TABLE predictions ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public read
CREATE POLICY IF NOT EXISTS "Allow public read" ON predictions
    FOR SELECT USING (true);

-- Policy: Allow authenticated insert/update
CREATE POLICY IF NOT EXISTS "Allow authenticated insert" ON predictions
    FOR INSERT WITH CHECK (true);

CREATE POLICY IF NOT EXISTS "Allow authenticated update" ON predictions
    FOR UPDATE USING (true);

-- ============================================================================
-- USER BETS TABLE - Rejestrowanie zakładów użytkownika
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_bets (
    id BIGSERIAL PRIMARY KEY,
    
    -- Referencja do meczu (może być prediction_id lub bezpośrednie dane)
    prediction_id BIGINT REFERENCES predictions(id) ON DELETE SET NULL,
    
    -- Dane meczu (backup jeśli prediction_id jest null)
    match_date DATE NOT NULL,
    match_time TIME,
    home_team TEXT NOT NULL,
    away_team TEXT NOT NULL,
    sport TEXT NOT NULL DEFAULT 'football',
    league TEXT,
    
    -- Zakład użytkownika
    bet_selection TEXT NOT NULL,  -- '1' (home), 'X' (draw), '2' (away)
    odds_at_bet DECIMAL(6,2) NOT NULL,  -- Kurs w momencie postawienia
    stake DECIMAL(10,2) NOT NULL DEFAULT 10.00,  -- Stawka
    
    -- Status zakładu
    status TEXT NOT NULL DEFAULT 'pending',  -- 'pending', 'won', 'lost', 'void'
    
    -- Wynik (wypełniane po zakończeniu meczu)
    actual_result TEXT,  -- '1', 'X', '2'
    home_score INT,
    away_score INT,
    profit DECIMAL(10,2),  -- Zysk/strata (stake * (odds-1) lub -stake)
    
    -- Metadane
    created_at TIMESTAMPTZ DEFAULT NOW(),
    settled_at TIMESTAMPTZ,
    notes TEXT
);

-- Indeksy dla user_bets
CREATE INDEX IF NOT EXISTS idx_user_bets_match_date ON user_bets(match_date);
CREATE INDEX IF NOT EXISTS idx_user_bets_status ON user_bets(status);
CREATE INDEX IF NOT EXISTS idx_user_bets_created_at ON user_bets(created_at);
CREATE INDEX IF NOT EXISTS idx_user_bets_prediction_id ON user_bets(prediction_id);

-- RLS dla user_bets
ALTER TABLE user_bets ENABLE ROW LEVEL SECURITY;

CREATE POLICY IF NOT EXISTS "Allow public read user_bets" ON user_bets
    FOR SELECT USING (true);

CREATE POLICY IF NOT EXISTS "Allow public insert user_bets" ON user_bets
    FOR INSERT WITH CHECK (true);

CREATE POLICY IF NOT EXISTS "Allow public update user_bets" ON user_bets
    FOR UPDATE USING (true);

-- ============================================================================
-- VIEWS FOR ANALYTICS
-- ============================================================================

-- View: Recent predictions (last 7 days)
CREATE OR REPLACE VIEW recent_predictions AS
SELECT *
FROM predictions
WHERE match_date >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY match_date DESC, match_time DESC;

-- View: Predictions with results (for accuracy calculation)
CREATE OR REPLACE VIEW predictions_with_results AS
SELECT *
FROM predictions
WHERE actual_result IS NOT NULL;

-- View: Qualified predictions only
CREATE OR REPLACE VIEW qualified_predictions AS
SELECT *
FROM predictions
WHERE qualifies = true
ORDER BY match_date DESC, match_time DESC;

-- ============================================================================
-- VIEWS FOR USER BETS
-- ============================================================================

-- View: Recent user bets (last 30 days)
CREATE OR REPLACE VIEW recent_user_bets AS
SELECT *
FROM user_bets
WHERE match_date >= CURRENT_DATE - INTERVAL '30 days'
ORDER BY created_at DESC;

-- View: Pending bets
CREATE OR REPLACE VIEW pending_bets AS
SELECT *
FROM user_bets
WHERE status = 'pending'
ORDER BY match_date ASC, match_time ASC;

-- View: Settled bets with profit
CREATE OR REPLACE VIEW settled_bets AS
SELECT *
FROM user_bets
WHERE status IN ('won', 'lost')
ORDER BY settled_at DESC;

-- View: User betting stats
CREATE OR REPLACE VIEW user_betting_stats AS
SELECT 
    COUNT(*) as total_bets,
    COUNT(*) FILTER (WHERE status = 'pending') as pending_bets,
    COUNT(*) FILTER (WHERE status = 'won') as won_bets,
    COUNT(*) FILTER (WHERE status = 'lost') as lost_bets,
    COALESCE(SUM(stake), 0) as total_staked,
    COALESCE(SUM(profit) FILTER (WHERE status IN ('won', 'lost')), 0) as total_profit,
    CASE 
        WHEN COUNT(*) FILTER (WHERE status IN ('won', 'lost')) > 0 
        THEN ROUND(
            (COUNT(*) FILTER (WHERE status = 'won')::DECIMAL / 
             COUNT(*) FILTER (WHERE status IN ('won', 'lost')) * 100), 2
        )
        ELSE 0 
    END as win_rate_percent,
    CASE 
        WHEN COALESCE(SUM(stake) FILTER (WHERE status IN ('won', 'lost')), 0) > 0 
        THEN ROUND(
            (COALESCE(SUM(profit) FILTER (WHERE status IN ('won', 'lost')), 0) / 
             SUM(stake) FILTER (WHERE status IN ('won', 'lost')) * 100), 2
        )
        ELSE 0 
    END as roi_percent
FROM user_bets;

-- ============================================================================
-- CONFIRMATION
-- ============================================================================

-- Check if tables were created
SELECT 'predictions' as table_name, COUNT(*) as row_count FROM predictions
UNION ALL
SELECT 'user_bets' as table_name, COUNT(*) as row_count FROM user_bets;

-- Show user_bets table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'user_bets' 
ORDER BY ordinal_position;
