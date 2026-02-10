// ============================================================================
// Leaderboard Page – top tipsters / accuracy ranking (placeholder data)
// ============================================================================
'use client'

import { Trophy, Medal, ArrowUpRight } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Avatar, AvatarFallback } from '@/components/ui/avatar'
import { Progress } from '@/components/ui/progress'
import { cn } from '@/lib/utils'

interface LeaderboardEntry {
  rank: number
  name: string
  accuracy: number
  totalBets: number
  profit: number
  streak: number
}

// Placeholder data until backend leaderboard API is ready
const LEADERBOARD_DATA: LeaderboardEntry[] = [
  { rank: 1, name: 'ProTipster', accuracy: 72.3, totalBets: 156, profit: 342.50, streak: 8 },
  { rank: 2, name: 'GoalMaster', accuracy: 68.9, totalBets: 201, profit: 287.10, streak: 5 },
  { rank: 3, name: 'OddsFinder', accuracy: 65.4, totalBets: 178, profit: 198.75, streak: 3 },
  { rank: 4, name: 'ValueBetKing', accuracy: 63.1, totalBets: 143, profit: 156.20, streak: 4 },
  { rank: 5, name: 'ScorePredict', accuracy: 61.8, totalBets: 189, profit: 124.30, streak: 2 },
  { rank: 6, name: 'BetAnalyst', accuracy: 59.5, totalBets: 132, profit: 89.60, streak: 1 },
  { rank: 7, name: 'MatchGuru', accuracy: 58.2, totalBets: 167, profit: 67.40, streak: 0 },
  { rank: 8, name: 'PredictorX', accuracy: 56.7, totalBets: 198, profit: 45.90, streak: 2 },
  { rank: 9, name: 'TipMaster', accuracy: 55.1, totalBets: 121, profit: 23.10, streak: 0 },
  { rank: 10, name: 'WinStreak', accuracy: 53.8, totalBets: 145, profit: -12.50, streak: 0 },
]

function getRankBadge(rank: number) {
  if (rank === 1) return <Trophy className="h-5 w-5 text-yellow-500" />
  if (rank === 2) return <Medal className="h-5 w-5 text-gray-400" />
  if (rank === 3) return <Medal className="h-5 w-5 text-amber-700" />
  return <span className="text-sm font-mono text-muted-foreground w-5 text-center">{rank}</span>
}

export default function LeaderboardPage() {
  return (
    <div className="container py-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Leaderboard</h1>
        <p className="text-muted-foreground mt-1">
          Top predictors ranked by accuracy and profit.
        </p>
      </div>

      {/* Leader podium */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        {LEADERBOARD_DATA.slice(0, 3).map((entry) => (
          <Card
            key={entry.rank}
            className={cn(
              'relative overflow-hidden',
              entry.rank === 1 && 'border-yellow-500/50 bg-yellow-500/5',
              entry.rank === 2 && 'border-gray-400/50 bg-gray-400/5',
              entry.rank === 3 && 'border-amber-700/50 bg-amber-700/5',
            )}
          >
            <CardHeader className="pb-2">
              <div className="flex items-center justify-between">
                {getRankBadge(entry.rank)}
                <Badge variant="secondary" className="text-xs">
                  {entry.streak > 0 ? `${entry.streak} win streak` : 'No streak'}
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="space-y-3">
              <div className="flex items-center gap-3">
                <Avatar className="h-10 w-10">
                  <AvatarFallback className="font-semibold text-sm">
                    {entry.name.slice(0, 2).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div>
                  <p className="font-semibold">{entry.name}</p>
                  <p className="text-xs text-muted-foreground">{entry.totalBets} bets</p>
                </div>
              </div>
              <div>
                <div className="flex items-center justify-between text-sm mb-1">
                  <span className="text-muted-foreground">Accuracy</span>
                  <span className="font-mono font-semibold">{entry.accuracy}%</span>
                </div>
                <Progress value={entry.accuracy} className="h-2" />
              </div>
              <p className={cn('text-sm font-mono font-semibold', entry.profit >= 0 ? 'text-emerald-500' : 'text-red-500')}>
                {entry.profit >= 0 ? '+' : ''}{entry.profit.toFixed(2)} units
              </p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Full table */}
      <Card>
        <CardHeader>
          <CardTitle>Full Rankings</CardTitle>
          <CardDescription>All-time performance across verified predictions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {LEADERBOARD_DATA.map((entry) => (
              <div key={entry.rank} className="flex items-center gap-4 px-3 py-2.5 rounded-lg hover:bg-muted/50 transition-colors">
                <div className="w-8 flex justify-center shrink-0">
                  {getRankBadge(entry.rank)}
                </div>
                <Avatar className="h-8 w-8 shrink-0">
                  <AvatarFallback className="text-xs font-medium">
                    {entry.name.slice(0, 2).toUpperCase()}
                  </AvatarFallback>
                </Avatar>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{entry.name}</p>
                </div>
                <div className="hidden sm:block w-24 text-right">
                  <span className="text-sm font-mono">{entry.accuracy}%</span>
                </div>
                <div className="hidden md:block w-20 text-right">
                  <span className="text-xs text-muted-foreground">{entry.totalBets} bets</span>
                </div>
                <div className="w-24 text-right">
                  <span className={cn('text-sm font-mono', entry.profit >= 0 ? 'text-emerald-500' : 'text-red-500')}>
                    {entry.profit >= 0 ? '+' : ''}{entry.profit.toFixed(2)}
                  </span>
                </div>
                {entry.streak > 0 && (
                  <Badge variant="outline" className="text-[10px] shrink-0">
                    <ArrowUpRight className="h-3 w-3 mr-0.5" />
                    {entry.streak}
                  </Badge>
                )}
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <p className="text-xs text-center text-muted-foreground">
        Leaderboard data is currently using placeholder values. Connect to backend API for live rankings.
      </p>
    </div>
  )
}
