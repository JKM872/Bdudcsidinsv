// ============================================================================
// RecommendationBadge – Gemini AI recommendation indicator
// ============================================================================
'use client'

import { Flame, TrendingUp, Minus } from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import type { GeminiRecommendation } from '@/lib/types'

interface Props {
  recommendation: GeminiRecommendation | null | undefined
  size?: 'sm' | 'md' | 'lg'
  showLabel?: boolean
}

const CONFIG: Record<string, {
  label: string
  icon: typeof Flame
  className: string
  pulse?: boolean
}> = {
  HIGH: {
    label: 'TOP PICK',
    icon: Flame,
    className: 'bg-red-500 text-white border-red-400 shadow-red-500/25 shadow-md',
    pulse: true,
  },
  MEDIUM: {
    label: 'MEDIUM',
    icon: TrendingUp,
    className: 'bg-amber-500 text-white border-amber-400',
  },
  LOW: {
    label: 'LOW',
    icon: Minus,
    className: 'bg-zinc-400 text-white border-zinc-300',
  },
}

export function RecommendationBadge({ recommendation, size = 'sm', showLabel = true }: Props) {
  if (!recommendation || recommendation === 'SKIP' || !CONFIG[recommendation]) return null

  const cfg = CONFIG[recommendation]
  const Icon = cfg.icon
  const isLarge = size === 'lg'
  const isMd = size === 'md'

  return (
    <Badge
      className={cn(
        'gap-0.5 font-bold uppercase tracking-wide',
        cfg.className,
        cfg.pulse && 'animate-pulse',
        isLarge ? 'text-sm px-3 py-1' : isMd ? 'text-xs px-2 py-0.5' : 'text-[10px] px-1.5 py-0',
      )}
    >
      <Icon className={cn(isLarge ? 'h-4 w-4' : 'h-3 w-3')} />
      {showLabel && cfg.label}
    </Badge>
  )
}
