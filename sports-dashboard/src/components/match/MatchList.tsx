// ============================================================================
// MatchList – responsive grid of match cards
// ============================================================================
'use client'

import { MatchCard } from './MatchCard'
import { MatchCardSkeleton } from './MatchCardSkeleton'
import { EmptyState } from '@/components/shared/EmptyState'
import type { Match } from '@/lib/types'
import { useFilterStore } from '@/store/filterStore'

interface Props {
  matches: Match[]
  isLoading?: boolean
  onSelect?: (match: Match) => void
}

function applyLocalFilters(matches: Match[], filters: ReturnType<typeof useFilterStore.getState>): Match[] {
  let result = matches

  if (filters.minConfidence > 0) {
    result = result.filter((m) => (m.confidence ?? m.forebet?.probability ?? 0) >= filters.minConfidence)
  }
  if (filters.hasOdds) {
    result = result.filter((m) => m.odds?.home != null)
  }
  if (filters.hasPredictions) {
    result = result.filter((m) => m.forebet?.prediction != null || m.sofascore?.home != null)
  }
  if (filters.hasSofascore) {
    result = result.filter((m) => m.sofascore?.home != null)
  }
  if (filters.search) {
    const q = filters.search.toLowerCase()
    result = result.filter(
      (m) =>
        m.homeTeam.toLowerCase().includes(q) ||
        m.awayTeam.toLowerCase().includes(q) ||
        (m.league?.toLowerCase().includes(q) ?? false),
    )
  }

  // Sort
  result.sort((a, b) => {
    let cmp = 0
    const confA = a.confidence ?? a.forebet?.probability ?? 0
    const confB = b.confidence ?? b.forebet?.probability ?? 0
    if (filters.sortBy === 'confidence') cmp = confB - confA
    else if (filters.sortBy === 'sport') cmp = a.sport.localeCompare(b.sport)
    else cmp = (a.time ?? '').localeCompare(b.time ?? '')
    return filters.sortOrder === 'desc' ? -cmp : cmp
  })

  return result
}

export function MatchList({ matches, isLoading, onSelect }: Props) {
  const filters = useFilterStore()
  const filtered = applyLocalFilters(matches, filters)

  if (isLoading) {
    return (
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {Array.from({ length: 6 }).map((_, i) => (
          <MatchCardSkeleton key={i} />
        ))}
      </div>
    )
  }

  if (filtered.length === 0) {
    return (
      <EmptyState
        title="No matches found"
        description="Try adjusting your filters or selecting a different date."
      />
    )
  }

  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {filtered.map((m) => (
        <MatchCard key={m.id} match={m} onSelect={onSelect} />
      ))}
    </div>
  )
}
