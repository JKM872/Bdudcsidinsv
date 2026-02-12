// ============================================================================
// Home Page – SofaScore-style matches layout
// ============================================================================
'use client'

import { useState } from 'react'
import { MatchList } from '@/components/match/MatchList'
import { MatchDetails } from '@/components/match/MatchDetails'
import { TopPicksSection } from '@/components/match/TopPicksSection'
import { FilterBar } from '@/components/filters/FilterBar'
import { useMatches, useLiveScores } from '@/hooks/useMatches'
import type { Match } from '@/lib/types'

export default function HomePage() {
  const { data, isLoading, isError, error } = useMatches()
  const { data: liveScores } = useLiveScores()
  const [selectedMatch, setSelectedMatch] = useState<Match | null>(null)

  const matches = data?.data ?? []

  return (
    <div className="container max-w-6xl py-6 space-y-6">
      {/* Page heading */}
      <div className="flex items-end justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">
            Today&apos;s Matches
          </h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Live predictions, odds &amp; AI analysis
          </p>
        </div>
        <span className="text-xs text-muted-foreground tabular-nums">
          {matches.length} matches
        </span>
      </div>

      {/* AI Top Picks – horizontal scroll */}
      <TopPicksSection
        matches={matches}
        onSelect={setSelectedMatch}
        isLoading={isLoading}
      />

      {/* Main grid: filters sidebar + matches */}
      <div className="grid grid-cols-1 lg:grid-cols-[260px_1fr] gap-6">
        <aside className="order-2 lg:order-1">
          <div className="lg:sticky lg:top-20 space-y-4">
            <FilterBar />
          </div>
        </aside>

        <section className="order-1 lg:order-2">
          {isError && (
            <div className="rounded-xl border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
              Failed to load matches: {(error as Error)?.message ?? 'Unknown error'}
            </div>
          )}

          <MatchList
            matches={matches}
            liveScores={liveScores ?? []}
            isLoading={isLoading}
            onSelect={setSelectedMatch}
          />
        </section>
      </div>

      {/* Match Details Dialog */}
      <MatchDetails
        match={selectedMatch}
        open={!!selectedMatch}
        onOpenChange={(open) => !open && setSelectedMatch(null)}
      />
    </div>
  )
}
