// ============================================================================
// Home Page – matches grid + filter sidebar
// ============================================================================
'use client'

import { MatchList } from '@/components/match/MatchList'
import { FilterBar } from '@/components/filters/FilterBar'
import { useMatches } from '@/hooks/useMatches'

export default function HomePage() {
  const { data, isLoading, isError, error } = useMatches()

  return (
    <div className="container py-6 space-y-6">
      {/* Page heading */}
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Today&apos;s Matches
        </h1>
        <p className="text-muted-foreground mt-1">
          Live predictions, odds & fan sentiment across multiple sports.
        </p>
      </div>

      {/* Main grid: filters sidebar + matches */}
      <div className="grid grid-cols-1 lg:grid-cols-[280px_1fr] gap-6">
        <aside className="order-2 lg:order-1">
          <div className="lg:sticky lg:top-20">
            <FilterBar />
          </div>
        </aside>

        <section className="order-1 lg:order-2">
          {isError && (
            <div className="rounded-lg border border-destructive/50 bg-destructive/10 p-4 text-sm text-destructive">
              Failed to load matches: {(error as Error)?.message ?? 'Unknown error'}
            </div>
          )}

          <MatchList
            matches={data?.data ?? []}
            isLoading={isLoading}
          />
        </section>
      </div>
    </div>
  )
}
