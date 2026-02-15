import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"
import type { Match } from './types'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// ---------------------------------------------------------------------------
// Match grouping helpers (FlashScore-style)
// ---------------------------------------------------------------------------

/**
 * Group matches by league name.
 */
export function groupMatchesByLeague(matches: Match[]): Record<string, Match[]> {
  return matches.reduce<Record<string, Match[]>>((groups, match) => {
    const key = match.league || 'Other'
    if (!groups[key]) groups[key] = []
    groups[key].push(match)
    return groups
  }, {})
}

/**
 * Sort league groups: live leagues first, then alphabetically.
 */
export function sortLeagueGroups(
  groups: Record<string, Match[]>,
  liveMatchIds?: Set<string | number>,
): [string, Match[]][] {
  return Object.entries(groups).sort(([leagueA, matchesA], [leagueB, matchesB]) => {
    const hasLiveA = liveMatchIds
      ? matchesA.some(m => liveMatchIds.has(m.id))
      : false
    const hasLiveB = liveMatchIds
      ? matchesB.some(m => liveMatchIds.has(m.id))
      : false
    if (hasLiveA && !hasLiveB) return -1
    if (!hasLiveA && hasLiveB) return 1
    // Then by match count (more matches first), then alphabetically
    if (matchesB.length !== matchesA.length) return matchesB.length - matchesA.length
    return leagueA.localeCompare(leagueB)
  })
}
