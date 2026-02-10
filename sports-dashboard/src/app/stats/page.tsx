// ============================================================================
// Stats Page – analytics & accuracy breakdowns
// ============================================================================
'use client'

import { Loader2 } from 'lucide-react'
import { StatsOverview } from '@/components/stats/StatsOverview'
import { AccuracyChart } from '@/components/stats/AccuracyChart'
import { SportBreakdown } from '@/components/stats/SportBreakdown'
import { useStats } from '@/hooks/useMatches'

export default function StatsPage() {
  const { data, isLoading, isError, error } = useStats()

  return (
    <div className="container py-6 space-y-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Statistics</h1>
        <p className="text-muted-foreground mt-1">
          Prediction accuracy, sport breakdowns, and performance trends.
        </p>
      </div>

      {isLoading && (
        <div className="flex items-center justify-center py-20">
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        </div>
      )}

      {isError && (
        <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
          Failed to load stats: {(error as Error)?.message ?? 'Unknown error'}
        </div>
      )}

      {data && (
        <>
          <StatsOverview data={data} />

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AccuracyChart sportStats={data.sport_breakdown ?? []} />
            <SportBreakdown sportStats={data.sport_breakdown ?? []} />
          </div>
        </>
      )}
    </div>
  )
}
