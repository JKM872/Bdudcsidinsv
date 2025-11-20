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
-- CONFIRMATION
-- ============================================================================

-- Check if table was created
SELECT 'predictions' as table_name, 
       COUNT(*) as row_count 
FROM predictions;

-- Show table structure
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'predictions' 
ORDER BY ordinal_position;
