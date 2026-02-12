// ============================================================================
// H2HBar – Horizontal stacked bar for head-to-head stats
// ============================================================================
'use client'

import { cn } from '@/lib/utils'
import {
  Tooltip,
  TooltipContent,
  TooltipProvider,
  TooltipTrigger,
} from '@/components/ui/tooltip'

interface Props {
  home: number
  draw: number
  away: number
  homeTeam?: string
  awayTeam?: string
  className?: string
  showLabels?: boolean
}

export function H2HBar({
  home,
  draw,
  away,
  homeTeam = 'Home',
  awayTeam = 'Away',
  className,
  showLabels = true,
}: Props) {
  const total = home + draw + away
  if (total === 0) return null

  const homePct = (home / total) * 100
  const drawPct = (draw / total) * 100
  const awayPct = (away / total) * 100

  return (
    <TooltipProvider>
      <div className={cn('space-y-1.5', className)}>
        {showLabels && (
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>{homeTeam}</span>
            <span>{total} matches</span>
            <span>{awayTeam}</span>
          </div>
        )}

        <div className="flex h-6 w-full rounded-full overflow-hidden">
          {/* Home wins */}
          {homePct > 0 && (
            <Tooltip>
              <TooltipTrigger asChild>
                <div
                  className="flex items-center justify-center bg-emerald-500 text-white text-[10px] font-bold transition-all duration-500"
                  style={{ width: `${homePct}%` }}
                >
                  {home > 0 && home}
                </div>
              </TooltipTrigger>
              <TooltipContent>
                {homeTeam}: {home} wins ({Math.round(homePct)}%)
              </TooltipContent>
            </Tooltip>
          )}

          {/* Draws */}
          {drawPct > 0 && (
            <Tooltip>
              <TooltipTrigger asChild>
                <div
                  className="flex items-center justify-center bg-amber-500 text-white text-[10px] font-bold transition-all duration-500"
                  style={{ width: `${drawPct}%` }}
                >
                  {draw > 0 && draw}
                </div>
              </TooltipTrigger>
              <TooltipContent>
                Draws: {draw} ({Math.round(drawPct)}%)
              </TooltipContent>
            </Tooltip>
          )}

          {/* Away wins */}
          {awayPct > 0 && (
            <Tooltip>
              <TooltipTrigger asChild>
                <div
                  className="flex items-center justify-center bg-rose-500 text-white text-[10px] font-bold transition-all duration-500"
                  style={{ width: `${awayPct}%` }}
                >
                  {away > 0 && away}
                </div>
              </TooltipTrigger>
              <TooltipContent>
                {awayTeam}: {away} wins ({Math.round(awayPct)}%)
              </TooltipContent>
            </Tooltip>
          )}
        </div>

        {showLabels && (
          <div className="flex items-center justify-between text-[10px]">
            <span className="text-emerald-500 font-semibold">{Math.round(homePct)}%</span>
            <span className="text-amber-500 font-semibold">{Math.round(drawPct)}%</span>
            <span className="text-rose-500 font-semibold">{Math.round(awayPct)}%</span>
          </div>
        )}
      </div>
    </TooltipProvider>
  )
}
