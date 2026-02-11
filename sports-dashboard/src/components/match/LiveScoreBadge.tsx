// ============================================================================
// LiveScoreBadge – shows live/finished score on match cards
// ============================================================================
'use client'

import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import type { LiveScore } from '@/lib/types'

interface Props {
  liveScore: LiveScore | null | undefined
  className?: string
}

export function LiveScoreBadge({ liveScore, className }: Props) {
  if (!liveScore) return null

  const isLive = liveScore.status === 'live' || liveScore.status === 'halftime'
  const isFinished = liveScore.status === 'finished'

  if (!isLive && !isFinished) return null

  return (
    <Badge
      className={cn(
        'gap-1 font-mono font-bold text-xs px-2 py-0.5',
        isLive
          ? 'bg-red-600 text-white border-red-500 animate-pulse'
          : 'bg-zinc-600 text-white border-zinc-500',
        className,
      )}
    >
      {isLive && (
        <span className="relative flex h-2 w-2">
          <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-white opacity-75" />
          <span className="relative inline-flex rounded-full h-2 w-2 bg-white" />
        </span>
      )}
      {isLive ? 'LIVE' : 'FT'}
      <span className="ml-0.5">
        {liveScore.homeScore} - {liveScore.awayScore}
      </span>
      {isLive && liveScore.time && (
        <span className="text-red-200 text-[10px] ml-0.5">{liveScore.time}&apos;</span>
      )}
    </Badge>
  )
}
