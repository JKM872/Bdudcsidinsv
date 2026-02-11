// ============================================================================
// MatchDetails – full‑screen dialog for a single match
// ============================================================================
'use client'

import {
  Dialog, DialogContent, DialogHeader, DialogTitle,
} from '@/components/ui/dialog'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Separator } from '@/components/ui/separator'
import { Progress } from '@/components/ui/progress'
import {
  Target, BarChart3, TrendingUp, History, Brain,
} from 'lucide-react'
import { cn } from '@/lib/utils'
import { SPORT_MAP, PREDICTION_COLORS, getConfidenceTier } from '@/lib/constants'
import { formatMatchTime, formatOdds, formatVotes } from '@/lib/format'
import { RecommendationBadge } from './RecommendationBadge'
import type { Match } from '@/lib/types'

interface Props {
  match: Match | null
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function MatchDetails({ match, open, onOpenChange }: Props) {
  if (!match) return null

  const sportCfg = SPORT_MAP[match.sport]
  const conf = match.gemini?.confidence ?? match.confidence ?? match.forebet?.probability ?? 0
  const confTier = getConfidenceTier(conf)
  const SportIcon = sportCfg?.icon

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-center gap-2 mb-1">
            {SportIcon && <SportIcon className={cn('h-5 w-5', sportCfg.color)} />}
            <Badge variant="outline">{match.league ?? match.sport}</Badge>
            <span className="text-sm text-muted-foreground ml-auto">
              {formatMatchTime(match.time)}
            </span>
            <RecommendationBadge recommendation={match.gemini?.recommendation} size="md" />
          </div>
          <DialogTitle className="text-xl">
            {match.homeTeam} vs {match.awayTeam}
          </DialogTitle>
        </DialogHeader>

        {/* Confidence bar */}
        <div className="flex items-center gap-3 py-2">
          <span className="text-sm text-muted-foreground">Confidence</span>
          <Progress value={conf} className="flex-1 h-2" />
          <Badge variant="secondary" className={cn('text-xs', confTier.color)}>
            {confTier.label} ({conf}%)
          </Badge>
        </div>

        <Separator />

        <Tabs defaultValue="predictions" className="mt-2">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="predictions" className="text-xs gap-1"><Target className="h-3 w-3" /> Predictions</TabsTrigger>
            <TabsTrigger value="odds" className="text-xs gap-1"><TrendingUp className="h-3 w-3" /> Odds</TabsTrigger>
            <TabsTrigger value="h2h" className="text-xs gap-1"><History className="h-3 w-3" /> H2H</TabsTrigger>
            <TabsTrigger value="ai" className="text-xs gap-1"><Brain className="h-3 w-3" /> AI</TabsTrigger>
          </TabsList>

          {/* ── Predictions tab ── */}
          <TabsContent value="predictions" className="space-y-4 mt-4">
            {/* Forebet */}
            {match.forebet && (
              <div className="rounded-lg border p-4 space-y-3">
                <div className="flex items-center gap-2 font-medium">
                  <Target className="h-4 w-4 text-blue-500" /> Forebet Prediction
                </div>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-sm">
                  <div>
                    <p className="text-muted-foreground text-xs">Prediction</p>
                    {match.forebet.prediction && (
                      <Badge className={cn('mt-1', PREDICTION_COLORS[match.forebet.prediction] ?? '')}>
                        {match.forebet.prediction}
                      </Badge>
                    )}
                  </div>
                  <div>
                    <p className="text-muted-foreground text-xs">Probability</p>
                    <p className="font-semibold mt-1">{match.forebet.probability ?? '-'}%</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground text-xs">Exact Score</p>
                    <p className="font-semibold mt-1">{match.forebet.exactScore ?? '-'}</p>
                  </div>
                  <div>
                    <p className="text-muted-foreground text-xs">Over / Under</p>
                    <p className="font-semibold mt-1">{match.forebet.overUnder ?? '-'}</p>
                  </div>
                </div>
                {match.forebet.btts && (
                  <div>
                    <span className="text-xs text-muted-foreground">BTTS: </span>
                    <Badge variant="outline">{match.forebet.btts}</Badge>
                  </div>
                )}
              </div>
            )}

            {/* SofaScore */}
            {match.sofascore?.home != null && (
              <div className="rounded-lg border p-4 space-y-3">
                <div className="flex items-center gap-2 font-medium">
                  <BarChart3 className="h-4 w-4 text-orange-500" /> SofaScore Fan Vote
                </div>
                <div className="space-y-2">
                  {/* Home */}
                  <div className="flex items-center gap-3">
                    <span className="w-14 text-xs text-right">Home</span>
                    <Progress value={match.sofascore.home ?? 0} className="flex-1 h-3" />
                    <span className="w-10 text-xs font-semibold text-emerald-600">{match.sofascore.home}%</span>
                  </div>
                  {/* Draw */}
                  {match.sofascore.draw != null && (
                    <div className="flex items-center gap-3">
                      <span className="w-14 text-xs text-right">Draw</span>
                      <Progress value={match.sofascore.draw} className="flex-1 h-3" />
                      <span className="w-10 text-xs font-semibold text-amber-600">{match.sofascore.draw}%</span>
                    </div>
                  )}
                  {/* Away */}
                  <div className="flex items-center gap-3">
                    <span className="w-14 text-xs text-right">Away</span>
                    <Progress value={match.sofascore.away ?? 0} className="flex-1 h-3" />
                    <span className="w-10 text-xs font-semibold text-rose-600">{match.sofascore.away}%</span>
                  </div>
                </div>
                <p className="text-xs text-muted-foreground">
                  {formatVotes(match.sofascore.votes)} total votes
                </p>
              </div>
            )}

            {!match.forebet && !match.sofascore?.home && (
              <p className="text-sm text-muted-foreground text-center py-6">No predictions available for this match.</p>
            )}
          </TabsContent>

          {/* ── Odds tab ── */}
          <TabsContent value="odds" className="mt-4">
            {match.odds ? (
              <div className="rounded-lg border p-4 space-y-3">
                <p className="text-sm font-medium">Match Odds {match.odds.bookmaker && <span className="text-muted-foreground font-normal">({match.odds.bookmaker})</span>}</p>
                <div className="grid grid-cols-3 gap-3">
                  <div className="text-center rounded-md border p-3">
                    <p className="text-xs text-muted-foreground mb-1">Home</p>
                    <p className="text-lg font-bold">{formatOdds(match.odds.home)}</p>
                  </div>
                  {match.odds.draw != null && (
                    <div className="text-center rounded-md border p-3">
                      <p className="text-xs text-muted-foreground mb-1">Draw</p>
                      <p className="text-lg font-bold">{formatOdds(match.odds.draw)}</p>
                    </div>
                  )}
                  <div className="text-center rounded-md border p-3">
                    <p className="text-xs text-muted-foreground mb-1">Away</p>
                    <p className="text-lg font-bold">{formatOdds(match.odds.away)}</p>
                  </div>
                </div>
                {match.value_bet && (
                  <Badge className="gap-1 bg-amber-500 text-white">
                    <TrendingUp className="h-3 w-3" /> Value Bet Detected
                  </Badge>
                )}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-6">No odds data available.</p>
            )}
          </TabsContent>

          {/* ── H2H tab ── */}
          <TabsContent value="h2h" className="mt-4">
            {match.h2h ? (
              <div className="rounded-lg border p-4 space-y-4">
                <p className="text-sm font-medium">Head to Head ({match.h2h.total} matches)</p>
                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="rounded-md border p-3">
                    <p className="text-xs text-muted-foreground mb-1">Home Wins</p>
                    <p className="text-2xl font-bold text-emerald-600">{match.h2h.home}</p>
                  </div>
                  <div className="rounded-md border p-3">
                    <p className="text-xs text-muted-foreground mb-1">Draws</p>
                    <p className="text-2xl font-bold text-amber-600">{match.h2h.draw}</p>
                  </div>
                  <div className="rounded-md border p-3">
                    <p className="text-xs text-muted-foreground mb-1">Away Wins</p>
                    <p className="text-2xl font-bold text-rose-600">{match.h2h.away}</p>
                  </div>
                </div>
                {match.h2h.winRate > 0 && (
                  <div className="flex items-center gap-3">
                    <span className="text-xs text-muted-foreground">Home win rate</span>
                    <Progress value={match.h2h.winRate} className="flex-1 h-2" />
                    <span className="text-xs font-semibold">{match.h2h.winRate}%</span>
                  </div>
                )}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-6">No head-to-head data available.</p>
            )}
          </TabsContent>

          {/* ── AI Analysis tab ── */}
          <TabsContent value="ai" className="mt-4">
            {match.gemini ? (
              <div className="rounded-lg border p-4 space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 font-medium">
                    <Brain className="h-4 w-4 text-violet-500" /> Gemini AI Analysis
                  </div>
                  <RecommendationBadge recommendation={match.gemini.recommendation} size="lg" />
                </div>
                {match.gemini.prediction && (
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">Prediction:</span>
                    <Badge>{match.gemini.prediction}</Badge>
                    {match.gemini.confidence && (
                      <span className="text-sm">({match.gemini.confidence}% confidence)</span>
                    )}
                  </div>
                )}
                {match.gemini.reasoning && (
                  <div className="bg-muted rounded-md p-3 text-sm leading-relaxed">
                    {match.gemini.reasoning}
                  </div>
                )}
              </div>
            ) : (
              <p className="text-sm text-muted-foreground text-center py-6">No AI analysis available for this match.</p>
            )}
          </TabsContent>
        </Tabs>
      </DialogContent>
    </Dialog>
  )
}
