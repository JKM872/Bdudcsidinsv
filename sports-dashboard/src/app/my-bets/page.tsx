// ============================================================================
// My Bets Page – personal bet tracker backed by Heroku API
// ============================================================================
'use client'

import { useState } from 'react'
import {
  Plus, Trash2, TrendingUp, TrendingDown, Minus, Loader2, AlertCircle,
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select'
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogClose,
} from '@/components/ui/dialog'
import { cn } from '@/lib/utils'
import { useBets, useBetStats, useCreateBet, useDeleteBet } from '@/hooks/useMatches'
import type { ApiBet } from '@/lib/api'

export default function MyBetsPage() {
  const { data, isLoading, isError, error } = useBets({ limit: 200 })
  const { data: betStats } = useBetStats()
  const createBet = useCreateBet()
  const deleteBetMut = useDeleteBet()

  const bets = data?.bets ?? []

  // Add bet form state
  const [homeTeam, setHomeTeam] = useState('')
  const [awayTeam, setAwayTeam] = useState('')
  const [pick, setPick] = useState<'1' | 'X' | '2' | ''>('')
  const [odds, setOdds] = useState('')
  const [stake, setStake] = useState('')
  const [dialogOpen, setDialogOpen] = useState(false)

  const addBet = () => {
    if (!homeTeam || !awayTeam || !pick) return
    createBet.mutate(
      {
        home_team: homeTeam,
        away_team: awayTeam,
        match_date: new Date().toISOString().slice(0, 10),
        bet_selection: pick,
        odds_at_bet: parseFloat(odds) || 1.5,
        stake: parseFloat(stake) || 10,
      },
      {
        onSuccess: () => {
          setHomeTeam('')
          setAwayTeam('')
          setPick('')
          setOdds('')
          setStake('')
          setDialogOpen(false)
        },
      },
    )
  }

  const removeBet = (id: number) => {
    deleteBetMut.mutate(id)
  }

  // stats from API
  const total = betStats?.total_bets ?? bets.length
  const won = betStats?.won ?? 0
  const lost = betStats?.lost ?? 0
  const profit = betStats?.total_profit ?? 0

  return (
    <div className="container py-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Bets</h1>
          <p className="text-muted-foreground mt-1">
            Track your picks and measure performance over time.
          </p>
        </div>

        <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
          <DialogTrigger asChild>
            <Button>
              <Plus className="h-4 w-4 mr-2" /> Add Bet
            </Button>
          </DialogTrigger>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>New Bet</DialogTitle>
            </DialogHeader>
            <div className="grid gap-4 py-2">
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <Label>Home Team</Label>
                  <Input
                    placeholder="e.g. Barcelona"
                    value={homeTeam}
                    onChange={(e) => setHomeTeam(e.target.value)}
                  />
                </div>
                <div className="space-y-1.5">
                  <Label>Away Team</Label>
                  <Input
                    placeholder="e.g. Real Madrid"
                    value={awayTeam}
                    onChange={(e) => setAwayTeam(e.target.value)}
                  />
                </div>
              </div>
              <div className="space-y-1.5">
                <Label>Pick</Label>
                <Select value={pick} onValueChange={(v) => setPick(v as '1' | 'X' | '2')}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select outcome" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="1">1 — Home Win</SelectItem>
                    <SelectItem value="X">X — Draw</SelectItem>
                    <SelectItem value="2">2 — Away Win</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div className="space-y-1.5">
                  <Label>Odds</Label>
                  <Input
                    type="number"
                    step="0.01"
                    placeholder="2.10"
                    value={odds}
                    onChange={(e) => setOdds(e.target.value)}
                  />
                </div>
                <div className="space-y-1.5">
                  <Label>Stake</Label>
                  <Input
                    type="number"
                    step="0.01"
                    placeholder="10.00"
                    value={stake}
                    onChange={(e) => setStake(e.target.value)}
                  />
                </div>
              </div>
            </div>
            <Button
              className="w-full"
              onClick={addBet}
              disabled={!homeTeam || !awayTeam || !pick || createBet.isPending}
            >
              {createBet.isPending ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
              Save Bet
            </Button>
            {createBet.isError && (
              <p className="text-xs text-destructive text-center mt-1">
                {(createBet.error as Error)?.message ?? 'Failed to save bet'}
              </p>
            )}
          </DialogContent>
        </Dialog>
      </div>

      {/* Summary cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm text-muted-foreground">Total</CardTitle></CardHeader>
          <CardContent><span className="text-2xl font-bold">{total}</span></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm text-muted-foreground">Won</CardTitle></CardHeader>
          <CardContent><span className="text-2xl font-bold text-emerald-500">{won}</span></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm text-muted-foreground">Lost</CardTitle></CardHeader>
          <CardContent><span className="text-2xl font-bold text-red-500">{lost}</span></CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2"><CardTitle className="text-sm text-muted-foreground">Profit/Loss</CardTitle></CardHeader>
          <CardContent>
            <span className={cn('text-2xl font-bold tabular-nums', profit >= 0 ? 'text-emerald-500' : 'text-red-500')}>
              {profit >= 0 ? '+' : ''}{profit.toFixed(2)}
            </span>
          </CardContent>
        </Card>
      </div>

      {/* Error state */}
      {isError && (
        <div className="flex items-center gap-3 rounded-xl border border-destructive/50 bg-destructive/10 p-4">
          <AlertCircle className="h-5 w-5 text-destructive shrink-0" />
          <div>
            <p className="text-sm font-medium text-destructive">Failed to load bets</p>
            <p className="text-xs text-muted-foreground">{(error as Error)?.message ?? 'Backend unavailable'}</p>
          </div>
        </div>
      )}

      {/* Loading */}
      {isLoading && (
        <div className="flex items-center justify-center py-16">
          <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
        </div>
      )}

      {/* Bet list */}
      {!isLoading && (
        <div className="space-y-3">
          {bets.length === 0 && !isError && (
            <Card>
              <CardContent className="py-12 text-center text-muted-foreground">
                No bets tracked yet. Tap &quot;Add Bet&quot; to get started.
              </CardContent>
            </Card>
          )}
          {bets.map((bet: ApiBet) => (
            <Card key={bet.id} className="flex items-center gap-4 p-4">
              {/* Result icon */}
              <div className="shrink-0">
                {bet.status === 'won' && <TrendingUp className="h-5 w-5 text-emerald-500" />}
                {bet.status === 'lost' && <TrendingDown className="h-5 w-5 text-red-500" />}
                {bet.status === 'pending' && <Minus className="h-5 w-5 text-muted-foreground" />}
                {bet.status === 'void' && <Minus className="h-5 w-5 text-yellow-500" />}
              </div>

              {/* Details */}
              <div className="flex-1 min-w-0">
                <p className="font-medium text-sm truncate">{bet.home_team} vs {bet.away_team}</p>
                <p className="text-xs text-muted-foreground">
                  Pick: <span className="font-mono font-semibold">{bet.bet_selection}</span>
                  {bet.odds_at_bet != null && <> &middot; Odds: <span className="font-mono">{bet.odds_at_bet}</span></>}
                  {bet.stake != null && <> &middot; Stake: <span className="font-mono">{bet.stake}</span></>}
                  {bet.match_date && <> &middot; <span className="text-muted-foreground/60">{bet.match_date}</span></>}
                </p>
              </div>

              {/* Status badge */}
              <span className={cn(
                'text-xs font-medium px-2 py-0.5 rounded-full shrink-0',
                bet.status === 'won' && 'bg-emerald-500/10 text-emerald-600',
                bet.status === 'lost' && 'bg-red-500/10 text-red-600',
                bet.status === 'pending' && 'bg-muted text-muted-foreground',
                bet.status === 'void' && 'bg-yellow-500/10 text-yellow-600',
              )}>
                {bet.status}
              </span>

              {/* Delete */}
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 shrink-0"
                onClick={() => removeBet(bet.id)}
                disabled={deleteBetMut.isPending}
              >
                <Trash2 className="h-3.5 w-3.5 text-muted-foreground" />
              </Button>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
