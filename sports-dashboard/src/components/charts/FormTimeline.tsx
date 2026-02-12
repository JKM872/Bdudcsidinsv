// ============================================================================
// FormTimeline – Colored W/D/L boxes (SofaScore style)
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
  form: string[] // e.g. ["W", "D", "L", "W", "W"]
  teamName?: string
  maxItems?: number
  className?: string
}

const FORM_CONFIG: Record<string, { color: string; label: string }> = {
  W: { color: 'bg-emerald-500', label: 'Win' },
  D: { color: 'bg-amber-500', label: 'Draw' },
  L: { color: 'bg-rose-500', label: 'Loss' },
}

export function FormTimeline({ form, teamName, maxItems = 5, className }: Props) {
  if (!form || form.length === 0) return null

  const items = form.slice(-maxItems)

  return (
    <TooltipProvider>
      <div className={cn('flex items-center gap-0.5', className)}>
        {items.map((result, i) => {
          const cfg = FORM_CONFIG[result.toUpperCase()] ?? FORM_CONFIG.D

          return (
            <Tooltip key={i}>
              <TooltipTrigger asChild>
                <div
                  className={cn(
                    'flex items-center justify-center rounded-sm text-white font-bold',
                    'h-5 w-5 text-[9px] leading-none',
                    cfg.color,
                  )}
                >
                  {result.toUpperCase()}
                </div>
              </TooltipTrigger>
              <TooltipContent side="top" className="text-xs">
                {teamName ? `${teamName}: ${cfg.label}` : cfg.label}
              </TooltipContent>
            </Tooltip>
          )
        })}
      </div>
    </TooltipProvider>
  )
}
