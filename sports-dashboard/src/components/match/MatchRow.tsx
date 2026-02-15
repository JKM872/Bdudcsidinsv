// ============================================================================
// MatchRow – FlashScore-style compact match row
// ============================================================================
'use client'

import { Clock, ChevronRight, TrendingUp, Zap } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import { SPORT_MAP, PREDICTION_COLORS, getConfidenceTier } from '@/lib/constants'
import { formatMatchTime, formatOdds } from '@/lib/format'
import { LiveScoreBadge } from './LiveScoreBadge'
import { TeamLogo } from './TeamLogo'
import type { Match, LiveScore } from '@/lib/types'

interface Props {
  match: Match
  liveScore?: LiveScore | null
  onSelect?: (match: Match) => void
}

export function MatchRow({ match, liveScore, onSelect }: Props) {
  const conf = match.gemini?.confidence ?? match.confidence ?? match.forebet?.probability ?? 0
  const confTier = getConfidenceTier(conf)
  const isLive = liveScore?.status === 'live' || liveScore?.status === 'halftime'
  const isFinished = liveScore?.status === 'finished'
  const recommendation = match.gemini?.recommendation
  const forebetPred = match.forebet?.prediction

  return (
    <div
      onClick={() => onSelect?.(match)}
      className={cn(
        'group flex items-center gap-2 sm:gap-3 px-3 sm:px-4 py-2.5 cursor-pointer transition-colors',
        'border-b border-border/40 last:border-b-0',
        'hover:bg-accent/50',
        isLive && 'bg-red-500/5 hover:bg-red-500/10',
        recommendation === 'HIGH' && !isLive && 'bg-amber-500/5',
      )}
    >
      {/* Time / Status */}
      <div className="flex items-center justify-center w-[52px] shrink-0">
        {isLive ? (
          <LiveScoreBadge liveScore={liveScore} className="text-[10px] px-1.5 py-0" />
        ) : isFinished ? (
          <span className="text-[11px] text-muted-foreground font-medium">FT</span>
        ) : (
          <span className="flex items-center gap-1 text-[12px] text-muted-foreground tabular-nums">
            <Clock className="h-3 w-3" />
            {formatMatchTime(match.time)}
          </span>
        )}
      </div>

      {/* Teams */}
      <div className="flex-1 min-w-0 flex flex-col gap-1">
        {/* Home team row */}
        <div className="flex items-center gap-2 min-w-0">
          <TeamLogo name={match.homeTeam} size="xs" />
          <span className={cn(
            'text-sm font-medium truncate leading-tight',
            forebetPred === '1' && 'text-emerald-600 dark:text-emerald-400',
            isFinished && liveScore && liveScore.homeScore > liveScore.awayScore && 'font-bold',
          )}>
            {match.homeTeam}
          </span>
          {/* Home form mini */}
          {match.homeForm?.length > 0 && (
            <div className="hidden md:flex items-center gap-0.5 ml-auto">
              {match.homeForm.slice(-3).map((r, i) => (
                <span
                  key={i}
                  className={cn(
                    'h-2 w-2 rounded-full',
                    r === 'W' && 'bg-emerald-500',
                    r === 'D' && 'bg-amber-500',
                    r === 'L' && 'bg-rose-500',
                  )}
                />
              ))}
            </div>
          )}
        </div>
        {/* Away team row */}
        <div className="flex items-center gap-2 min-w-0">
          <TeamLogo name={match.awayTeam} size="xs" />
          <span className={cn(
            'text-sm font-medium truncate leading-tight',
            forebetPred === '2' && 'text-rose-600 dark:text-rose-400',
            isFinished && liveScore && liveScore.awayScore > liveScore.homeScore && 'font-bold',
          )}>
            {match.awayTeam}
          </span>
          {/* Away form mini */}
          {match.awayForm?.length > 0 && (
            <div className="hidden md:flex items-center gap-0.5 ml-auto">
              {match.awayForm.slice(-3).map((r, i) => (
                <span
                  key={i}
                  className={cn(
                    'h-2 w-2 rounded-full',
                    r === 'W' && 'bg-emerald-500',
                    r === 'D' && 'bg-amber-500',
                    r === 'L' && 'bg-rose-500',
                  )}
                />
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Score (when live/finished) */}
      {(isLive || isFinished) && liveScore && (
        <div className="flex flex-col items-center w-[40px] shrink-0">
          <span className={cn(
            'text-sm font-bold tabular-nums',
            isLive && 'text-red-600',
          )}>
            {liveScore.homeScore}
          </span>
          <span className={cn(
            'text-sm font-bold tabular-nums',
            isLive && 'text-red-600',
          )}>
            {liveScore.awayScore}
          </span>
        </div>
      )}

      {/* Odds (desktop) */}
      {match.odds && (
        <div className="hidden lg:flex items-center gap-1 shrink-0">
          <span className={cn(
            'inline-flex items-center justify-center rounded px-1.5 py-0.5',
            'bg-muted text-[10px] font-mono font-medium tabular-nums min-w-[36px]',
            forebetPred === '1' && 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-400',
          )}>
            {formatOdds(match.odds.home)}
          </span>
          {match.odds.draw != null && (
            <span className={cn(
              'inline-flex items-center justify-center rounded px-1.5 py-0.5',
              'bg-muted text-[10px] font-mono font-medium tabular-nums min-w-[36px]',
              forebetPred === 'X' && 'bg-amber-500/15 text-amber-700 dark:text-amber-400',
            )}>
              {formatOdds(match.odds.draw)}
            </span>
          )}
          <span className={cn(
            'inline-flex items-center justify-center rounded px-1.5 py-0.5',
            'bg-muted text-[10px] font-mono font-medium tabular-nums min-w-[36px]',
            forebetPred === '2' && 'bg-rose-500/15 text-rose-700 dark:text-rose-400',
          )}>
            {formatOdds(match.odds.away)}
          </span>
        </div>
      )}

      {/* Prediction / Confidence badges */}
      <div className="hidden sm:flex items-center gap-1 shrink-0 w-[80px] justify-end">
        {forebetPred && (
          <Badge className={cn('text-[9px] px-1.5 py-0', PREDICTION_COLORS[forebetPred] ?? 'bg-zinc-500 text-white')}>
            {forebetPred}
          </Badge>
        )}
        {conf > 0 && (
          <span className={cn('text-[11px] font-medium tabular-nums', confTier.color)}>
            {Math.round(conf)}%
          </span>
        )}
      </div>

      {/* Recommendation */}
      <div className="w-[28px] shrink-0 flex items-center justify-center">
        {recommendation === 'HIGH' ? (
          <Zap className="h-3.5 w-3.5 text-amber-500 fill-amber-500" />
        ) : recommendation === 'MEDIUM' ? (
          <TrendingUp className="h-3.5 w-3.5 text-blue-500" />
        ) : null}
      </div>

      {/* Arrow */}
      <ChevronRight className="h-4 w-4 text-muted-foreground/30 group-hover:text-foreground/60 transition-colors shrink-0" />
    </div>
  )
}

// ── Skeleton for loading state ──
export function MatchRowSkeleton() {
  return (
    <div className="flex items-center gap-3 px-4 py-2.5 border-b border-border/40 animate-pulse">
      <div className="w-[52px] h-4 bg-muted rounded" />
      <div className="flex-1 space-y-1.5">
        <div className="h-3.5 w-32 bg-muted rounded" />
        <div className="h-3.5 w-28 bg-muted rounded" />
      </div>
      <div className="hidden lg:flex gap-1">
        <div className="h-5 w-9 bg-muted rounded" />
        <div className="h-5 w-9 bg-muted rounded" />
        <div className="h-5 w-9 bg-muted rounded" />
      </div>
      <div className="h-4 w-10 bg-muted rounded" />
      <div className="h-4 w-4 bg-muted rounded" />
    </div>
  )
}
