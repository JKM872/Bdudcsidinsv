// ============================================================================
// TopPicksSection – Hero section showing AI HIGH recommendations
// ============================================================================
'use client'

import { Flame, ChevronRight, Sparkles } from 'lucide-react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { cn } from '@/lib/utils'
import { SPORT_MAP, PREDICTION_COLORS } from '@/lib/constants'
import { formatMatchTime, formatOdds } from '@/lib/format'
import { RecommendationBadge } from '@/components/match/RecommendationBadge'
import type { Match } from '@/lib/types'

interface Props {
  matches: Match[]
  onSelect?: (match: Match) => void
  isLoading?: boolean
}

function TopPickCard({ match, onSelect }: { match: Match; onSelect?: (m: Match) => void }) {
  const sportCfg = SPORT_MAP[match.sport]
  const SportIcon = sportCfg?.icon
  const forebetPred = match.forebet?.prediction
  const geminiConf = match.gemini?.confidence ?? match.forebet?.probability ?? 0

  return (
    <Card
      className={cn(
        'relative overflow-hidden cursor-pointer transition-all duration-200',
        'hover:shadow-xl hover:scale-[1.02]',
        'border-2 border-red-500/30 bg-gradient-to-br from-background to-red-500/5',
      )}
      onClick={() => onSelect?.(match)}
    >
      {/* Top accent bar */}
      <div className="absolute inset-x-0 top-0 h-1 bg-gradient-to-r from-red-500 via-orange-500 to-amber-500" />

      <CardHeader className="pb-2 pt-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {SportIcon && <SportIcon className={cn('h-4 w-4', sportCfg.color)} />}
            <Badge variant="outline" className="text-[10px] font-normal">
              {match.league ?? match.sport}
            </Badge>
          </div>
          <RecommendationBadge recommendation={match.gemini?.recommendation} size="md" />
        </div>
      </CardHeader>

      <CardContent className="space-y-3">
        {/* Teams */}
        <div className="space-y-1">
          <div className="flex items-center justify-between">
            <span className="font-bold text-base leading-tight">{match.homeTeam}</span>
            {forebetPred === '1' && (
              <Badge className={cn('text-[10px] px-1.5 py-0', PREDICTION_COLORS['1'])}>W</Badge>
            )}
          </div>
          <p className="text-xs text-muted-foreground">vs</p>
          <div className="flex items-center justify-between">
            <span className="font-bold text-base leading-tight">{match.awayTeam}</span>
            {forebetPred === '2' && (
              <Badge className={cn('text-[10px] px-1.5 py-0', PREDICTION_COLORS['2'])}>W</Badge>
            )}
          </div>
        </div>

        {/* Key info row */}
        <div className="flex items-center justify-between border-t pt-2">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>{formatMatchTime(match.time)}</span>
            {match.forebet?.prediction && (
              <>
                <span>·</span>
                <Badge className={cn('text-[10px]', PREDICTION_COLORS[match.forebet.prediction] ?? '')}>
                  {match.forebet.prediction}
                </Badge>
                {match.forebet.probability != null && (
                  <span className="font-medium text-foreground">{match.forebet.probability}%</span>
                )}
              </>
            )}
          </div>
          {match.odds && (
            <span className="text-xs font-mono text-muted-foreground">
              {formatOdds(match.odds.home)} / {formatOdds(match.odds.away)}
            </span>
          )}
        </div>

        {/* AI Confidence bar */}
        <div className="flex items-center gap-2">
          <span className="text-[10px] text-muted-foreground">AI</span>
          <div className="flex-1 h-1.5 rounded-full bg-secondary overflow-hidden">
            <div
              className="h-full rounded-full bg-gradient-to-r from-red-500 to-amber-500 transition-all"
              style={{ width: `${geminiConf}%` }}
            />
          </div>
          <span className="text-[11px] font-bold text-red-500">{geminiConf}%</span>
          <ChevronRight className="h-3.5 w-3.5 text-muted-foreground" />
        </div>

        {/* Gemini reasoning snippet */}
        {match.gemini?.reasoning && (
          <p className="text-[11px] text-muted-foreground line-clamp-2 italic">
            {match.gemini.reasoning}
          </p>
        )}
      </CardContent>
    </Card>
  )
}

export function TopPicksSection({ matches, onSelect, isLoading }: Props) {
  // Filter for HIGH recommendations only
  const topPicks = matches
    .filter((m) => m.gemini?.recommendation === 'HIGH')
    .sort((a, b) => (b.gemini?.confidence ?? 0) - (a.gemini?.confidence ?? 0))
    .slice(0, 5)

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <Flame className="h-5 w-5 text-red-500" />
          <h2 className="text-xl font-bold">Top Picks Today</h2>
        </div>
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {[1, 2, 3].map((i) => (
            <Card key={i} className="h-48 animate-pulse bg-muted" />
          ))}
        </div>
      </div>
    )
  }

  if (topPicks.length === 0) {
    return (
      <Card className="border-dashed border-2 border-muted-foreground/20">
        <CardContent className="flex flex-col items-center justify-center py-8 text-center">
          <Sparkles className="h-8 w-8 text-muted-foreground/50 mb-2" />
          <p className="text-sm font-medium text-muted-foreground">
            No high-priority AI picks today
          </p>
          <p className="text-xs text-muted-foreground/70 mt-1">
            Gemini AI will highlight the best opportunities when they appear.
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Flame className="h-5 w-5 text-red-500" />
          <h2 className="text-xl font-bold">Top Picks Today</h2>
          <Badge className="bg-red-500 text-white text-xs">{topPicks.length}</Badge>
        </div>
        <Button variant="ghost" size="sm" className="text-xs text-muted-foreground">
          AI-powered recommendations
        </Button>
      </div>
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {topPicks.map((m) => (
          <TopPickCard key={m.id} match={m} onSelect={onSelect} />
        ))}
      </div>
    </div>
  )
}
