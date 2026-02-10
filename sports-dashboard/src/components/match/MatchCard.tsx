// ============================================================================
// MatchCard – premium card for a single match
// ============================================================================
'use client'

import { Clock, Target, BarChart3, TrendingUp, ChevronRight } from 'lucide-react'
import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '@/components/ui/tooltip'
import { cn } from '@/lib/utils'
import { SPORT_MAP, PREDICTION_COLORS, getConfidenceTier } from '@/lib/constants'
import { formatMatchTime, formatVotes, formatOdds } from '@/lib/format'
import type { Match } from '@/lib/types'

interface Props {
  match: Match
  onSelect?: (match: Match) => void
}

export function MatchCard({ match, onSelect }: Props) {
  const sportCfg = SPORT_MAP[match.sport]
  const conf = match.confidence ?? match.forebet?.probability ?? 0
  const confTier = getConfidenceTier(conf)
  const SportIcon = sportCfg?.icon

  const forebetPred = match.forebet?.prediction
  const sofaHome = match.sofascore?.home
  const sofaDraw = match.sofascore?.draw
  const sofaAway = match.sofascore?.away

  return (
    <Card
      className={cn(
        'group relative overflow-hidden transition-all duration-200 cursor-pointer',
        'hover:shadow-lg hover:scale-[1.01] hover:border-primary/50',
        match.value_bet && 'ring-2 ring-amber-400/50',
      )}
      onClick={() => onSelect?.(match)}
    >
      {/* Sport colour stripe */}
      <div className={cn('absolute inset-y-0 left-0 w-1', sportCfg?.bgColor)} />

      <CardHeader className="pb-2 pl-5">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {SportIcon && <SportIcon className={cn('h-4 w-4', sportCfg.color)} />}
            <Badge variant="outline" className="text-[10px] font-normal">
              {match.league ?? match.sport}
            </Badge>
          </div>
          <div className="flex items-center gap-1 text-xs text-muted-foreground">
            <Clock className="h-3 w-3" />
            {formatMatchTime(match.time)}
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-3 pl-5">
        {/* Teams */}
        <div className="space-y-0.5">
          <div className="flex items-center justify-between">
            <span className="font-semibold leading-tight">{match.homeTeam}</span>
            {forebetPred === '1' && (
              <Badge className={cn('text-[10px] px-1.5 py-0', PREDICTION_COLORS['1'])}>W</Badge>
            )}
          </div>
          <div className="flex items-center justify-between">
            <span className="font-semibold leading-tight">{match.awayTeam}</span>
            {forebetPred === '2' && (
              <Badge className={cn('text-[10px] px-1.5 py-0', PREDICTION_COLORS['2'])}>W</Badge>
            )}
          </div>
        </div>

        {/* Predictions row */}
        <div className="grid grid-cols-2 gap-3 border-t pt-2">
          {/* Forebet */}
          {match.forebet && (
            <div className="space-y-0.5">
              <div className="flex items-center gap-1 text-[10px] text-muted-foreground">
                <Target className="h-3 w-3" /> Forebet
              </div>
              <div className="flex items-center gap-1.5">
                {forebetPred && (
                  <Badge className={cn('text-xs', PREDICTION_COLORS[forebetPred] ?? 'bg-zinc-500 text-white')}>
                    {forebetPred}
                  </Badge>
                )}
                {match.forebet.probability != null && (
                  <span className="text-xs font-medium">{match.forebet.probability}%</span>
                )}
              </div>
            </div>
          )}

          {/* SofaScore */}
          {sofaHome != null && (
            <div className="space-y-0.5">
              <div className="flex items-center gap-1 text-[10px] text-muted-foreground">
                <BarChart3 className="h-3 w-3" /> SofaScore
              </div>
              <TooltipProvider>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <div className="flex items-center gap-1 text-xs">
                      <span className="text-emerald-600 font-medium">{sofaHome}%</span>
                      {sofaDraw != null && (
                        <>
                          <span className="text-muted-foreground">·</span>
                          <span className="text-amber-600 font-medium">{sofaDraw}%</span>
                        </>
                      )}
                      <span className="text-muted-foreground">·</span>
                      <span className="text-rose-600 font-medium">{sofaAway}%</span>
                    </div>
                  </TooltipTrigger>
                  <TooltipContent>
                    <p className="text-xs">
                      Fan vote: Home {sofaHome}% · Draw {sofaDraw ?? 0}% · Away {sofaAway}%
                      <br />
                      {match.sofascore?.votes
                        ? `${formatVotes(match.sofascore.votes)} votes`
                        : ''}
                    </p>
                  </TooltipContent>
                </Tooltip>
              </TooltipProvider>
            </div>
          )}
        </div>

        {/* Odds + value */}
        {match.odds && (
          <div className="flex items-center justify-between border-t pt-2">
            <div className="flex gap-1.5 text-xs">
              <Badge variant="outline" className="font-mono text-[10px]">1: {formatOdds(match.odds.home)}</Badge>
              {match.odds.draw != null && (
                <Badge variant="outline" className="font-mono text-[10px]">X: {formatOdds(match.odds.draw)}</Badge>
              )}
              <Badge variant="outline" className="font-mono text-[10px]">2: {formatOdds(match.odds.away)}</Badge>
            </div>
            {match.value_bet && (
              <Badge variant="secondary" className="gap-0.5 text-amber-600 border-amber-300 text-[10px]">
                <TrendingUp className="h-3 w-3" /> Value
              </Badge>
            )}
          </div>
        )}

        {/* Confidence bar */}
        <div className="flex items-center gap-2">
          <div className="flex-1 h-1 rounded-full bg-secondary overflow-hidden">
            <div
              className={cn('h-full rounded-full transition-all', confTier.bg)}
              style={{ width: `${conf}%` }}
            />
          </div>
          <span className={cn('text-[10px] font-medium', confTier.color)}>
            {conf}%
          </span>
          <ChevronRight className="h-3.5 w-3.5 text-muted-foreground opacity-0 group-hover:opacity-100 transition-opacity" />
        </div>
      </CardContent>
    </Card>
  )
}
