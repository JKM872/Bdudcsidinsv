// ============================================================================
// LeagueGroup – Collapsible league section (FlashScore-style)
// ============================================================================
'use client'

import { useState } from 'react'
import { ChevronDown } from 'lucide-react'
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible'
import { cn } from '@/lib/utils'

interface Props {
  league: string
  country?: string | null
  matchCount: number
  hasLive?: boolean
  defaultOpen?: boolean
  children: React.ReactNode
}

export function LeagueGroup({
  league,
  country,
  matchCount,
  hasLive = false,
  defaultOpen = true,
  children,
}: Props) {
  const [open, setOpen] = useState(defaultOpen)

  return (
    <Collapsible open={open} onOpenChange={setOpen} className="mb-0.5">
      <CollapsibleTrigger asChild>
        <button
          className={cn(
            'flex w-full items-center gap-2 px-3 sm:px-4 py-2 text-left transition-colors',
            'bg-muted/50 hover:bg-muted/80',
            'sticky top-[148px] z-20',
            'border-b border-border/40',
            hasLive && 'bg-red-500/5',
          )}
        >
          {/* Live indicator */}
          {hasLive && (
            <span className="relative flex h-2 w-2 shrink-0">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-500 opacity-75" />
              <span className="relative inline-flex rounded-full h-2 w-2 bg-red-500" />
            </span>
          )}

          {/* Country flag placeholder + league name */}
          <div className="flex items-center gap-1.5 min-w-0 flex-1">
            {country && (
              <span className="text-[11px] text-muted-foreground/70 uppercase shrink-0">
                {country}
              </span>
            )}
            {country && <span className="text-muted-foreground/30">·</span>}
            <span className="text-xs font-semibold text-foreground/90 truncate">
              {league}
            </span>
          </div>

          {/* Match count */}
          <span className="text-[10px] text-muted-foreground tabular-nums shrink-0">
            {matchCount}
          </span>

          {/* Chevron */}
          <ChevronDown
            className={cn(
              'h-3.5 w-3.5 text-muted-foreground/50 transition-transform duration-200 shrink-0',
              open && 'rotate-180',
            )}
          />
        </button>
      </CollapsibleTrigger>

      <CollapsibleContent>
        <div className="bg-background">
          {children}
        </div>
      </CollapsibleContent>
    </Collapsible>
  )
}
