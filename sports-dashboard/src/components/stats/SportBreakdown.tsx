// ============================================================================
// SportBreakdown – per-sport table with mini progress bars
// ============================================================================
'use client'

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { SPORTS } from '@/lib/constants'
import { cn } from '@/lib/utils'
import type { SportStat } from '@/lib/types'

interface SportBreakdownProps {
  sportStats: SportStat[]
}

export function SportBreakdown({ sportStats }: SportBreakdownProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Sport Breakdown</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        {sportStats.length === 0 && (
          <p className="text-sm text-muted-foreground text-center py-4">
            No data yet.
          </p>
        )}
        {sportStats.map((stat) => {
          const sport = SPORTS.find((s) => s.id === stat.sport)
          const Icon = sport?.icon
          const pct = Math.round((stat.accuracy ?? 0) * 100)

          return (
            <div key={stat.sport} className="flex items-center gap-3">
              {/* Icon */}
              <div className="shrink-0 w-8 h-8 rounded-md bg-muted flex items-center justify-center">
                {Icon && <Icon className={cn('h-4 w-4', sport?.color)} />}
              </div>

              {/* Info */}
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between mb-1">
                  <span className="text-sm font-medium capitalize">{stat.sport}</span>
                  <div className="flex items-center gap-2">
                    <Badge variant="outline" className="text-[10px]">{stat.total} matches</Badge>
                    <span className="text-sm font-mono font-semibold">{pct}%</span>
                  </div>
                </div>
                <Progress
                  value={pct}
                  className="h-2"
                />
              </div>
            </div>
          )
        })}
      </CardContent>
    </Card>
  )
}
