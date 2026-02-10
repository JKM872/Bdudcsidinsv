// ============================================================================
// SPORTS DASHBOARD - Filter Store (Zustand)
// ============================================================================
import { create } from 'zustand'
import { addDays } from 'date-fns'
import type { Sport, MatchFilters } from '@/lib/types'
import { DEFAULT_FILTERS } from '@/lib/constants'

interface FilterState extends MatchFilters {
  // Derived
  activeFilterCount: number
  // Actions
  setSport: (sport: Sport | 'all') => void
  setDate: (date: Date | null) => void
  setDatePreset: (preset: 'today' | 'tomorrow') => void
  setMinConfidence: (n: number) => void
  setHasOdds: (v: boolean) => void
  setHasPredictions: (v: boolean) => void
  setHasSofascore: (v: boolean) => void
  setSearch: (q: string) => void
  setSortBy: (s: MatchFilters['sortBy']) => void
  toggleSortOrder: () => void
  resetFilters: () => void
  applyQuickFilter: (overrides: Partial<MatchFilters & { date: 'today' | 'tomorrow' }>) => void
}

function countActive(s: MatchFilters): number {
  let c = 0
  if (s.sport !== 'all') c++
  if (s.date) c++
  if (s.minConfidence > 0) c++
  if (s.hasOdds) c++
  if (s.hasPredictions) c++
  if (s.hasSofascore) c++
  if (s.search) c++
  return c
}

export const useFilterStore = create<FilterState>((set) => ({
  ...DEFAULT_FILTERS,
  activeFilterCount: 0,

  setSport: (sport) => set((s) => {
    const next = { ...s, sport }
    return { ...next, activeFilterCount: countActive(next) }
  }),
  setDate: (date) => set((s) => {
    const next = { ...s, date }
    return { ...next, activeFilterCount: countActive(next) }
  }),
  setDatePreset: (preset) => set((s) => {
    const date = preset === 'today' ? new Date() : addDays(new Date(), 1)
    const next = { ...s, date }
    return { ...next, activeFilterCount: countActive(next) }
  }),
  setMinConfidence: (minConfidence) => set((s) => {
    const next = { ...s, minConfidence }
    return { ...next, activeFilterCount: countActive(next) }
  }),
  setHasOdds: (hasOdds) => set((s) => {
    const next = { ...s, hasOdds }
    return { ...next, activeFilterCount: countActive(next) }
  }),
  setHasPredictions: (hasPredictions) => set((s) => {
    const next = { ...s, hasPredictions }
    return { ...next, activeFilterCount: countActive(next) }
  }),
  setHasSofascore: (hasSofascore) => set((s) => {
    const next = { ...s, hasSofascore }
    return { ...next, activeFilterCount: countActive(next) }
  }),
  setSearch: (search) => set((s) => {
    const next = { ...s, search }
    return { ...next, activeFilterCount: countActive(next) }
  }),
  setSortBy: (sortBy) => set({ sortBy }),
  toggleSortOrder: () => set((s) => ({ sortOrder: s.sortOrder === 'asc' ? 'desc' : 'asc' })),
  resetFilters: () => set({ ...DEFAULT_FILTERS, activeFilterCount: 0 }),
  applyQuickFilter: (overrides) => set((s) => {
    let date = s.date
    if ('date' in overrides) {
      if (overrides.date === 'today') date = new Date()
      else if (overrides.date === 'tomorrow') date = addDays(new Date(), 1)
    }
    const { date: _, ...rest } = overrides as Record<string, unknown>
    const next = { ...s, ...rest, date } as MatchFilters
    return { ...next, activeFilterCount: countActive(next) }
  }),
}))
