-- ============================================================================
-- MIGRATION 001: Auth & Data Integrity Hardening
-- ============================================================================
-- Run in Supabase SQL Editor AFTER the initial schema (supabase_schema.sql)
-- ============================================================================

-- 1. Add user_id column to user_bets (ownership tracking)
ALTER TABLE user_bets ADD COLUMN IF NOT EXISTS user_id UUID;

-- 2. Create index on user_id for fast per-user queries
CREATE INDEX IF NOT EXISTS idx_user_bets_user_id ON user_bets(user_id);

-- 3. Uniqueness constraint: prevent duplicate predictions for same match+date
CREATE UNIQUE INDEX IF NOT EXISTS idx_predictions_unique_match
ON predictions(match_date, home_team, away_team, sport);

-- 4. Uniqueness constraint: prevent duplicate bets by same user on same match
CREATE UNIQUE INDEX IF NOT EXISTS idx_user_bets_unique_per_user
ON user_bets(user_id, match_date, home_team, away_team, bet_selection)
WHERE user_id IS NOT NULL;

-- 5. Add composite indexes for common query patterns
CREATE INDEX IF NOT EXISTS idx_predictions_date_sport ON predictions(match_date, sport);
CREATE INDEX IF NOT EXISTS idx_user_bets_user_status ON user_bets(user_id, status);
CREATE INDEX IF NOT EXISTS idx_user_bets_match_date_status ON user_bets(match_date, status);

-- ============================================================================
-- TIGHTER RLS POLICIES
-- ============================================================================

-- Drop old permissive policies
DROP POLICY IF EXISTS "Allow public insert user_bets" ON user_bets;
DROP POLICY IF EXISTS "Allow public update user_bets" ON user_bets;
DROP POLICY IF EXISTS "Allow public read user_bets" ON user_bets;

-- New policies: users can only manage their own bets
CREATE POLICY "Users read own bets" ON user_bets
    FOR SELECT USING (
        auth.uid() = user_id OR user_id IS NULL
    );

CREATE POLICY "Users insert own bets" ON user_bets
    FOR INSERT WITH CHECK (
        auth.uid() = user_id OR auth.role() = 'service_role'
    );

CREATE POLICY "Users update own bets" ON user_bets
    FOR UPDATE USING (
        auth.uid() = user_id OR auth.role() = 'service_role'
    );

CREATE POLICY "Users delete own bets" ON user_bets
    FOR DELETE USING (
        auth.uid() = user_id OR auth.role() = 'service_role'
    );

-- Predictions remain public-read, service-role write
DROP POLICY IF EXISTS "Allow authenticated insert" ON predictions;
DROP POLICY IF EXISTS "Allow authenticated update" ON predictions;

CREATE POLICY "Service role insert predictions" ON predictions
    FOR INSERT WITH CHECK (
        auth.role() = 'service_role'
    );

CREATE POLICY "Service role update predictions" ON predictions
    FOR UPDATE USING (
        auth.role() = 'service_role'
    );

-- ============================================================================
-- UPDATED VIEWS (include user_id)
-- ============================================================================

-- Refresh user_betting_stats to filter by user
CREATE OR REPLACE VIEW user_betting_stats AS
SELECT
    user_id,
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
FROM user_bets
GROUP BY user_id;

-- ============================================================================
-- CONFIRMATION
-- ============================================================================
SELECT 'Migration 001 complete' as status;
