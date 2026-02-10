// ============================================================================
// My Bets Page – personal bet tracker (localStorage-based MVP)
// ============================================================================
'use client'

import { useState, useEffect, useCallback } from 'react'
import {
  Plus, Trash2, TrendingUp, TrendingDown, Minus,
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import {
  Select, SelectContent, SelectItem, SelectTrigger, SelectValue,
} from '@/components/ui/select'
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogClose,
} from '@/components/ui/dialog'
import type { UserBet } from '@/lib/types'

const LS_KEY = 'sports-dashboard-bets'

function loadBets(): UserBet[] {
  if (typeof window === 'undefined') return []
  try {
    return JSON.parse(localStorage.getItem(LS_KEY) || '[]')
  } catch {
    return []
  }
}
function saveBets(bets: UserBet[]) {
  localStorage.setItem(LS_KEY, JSON.stringify(bets))
}

export default function MyBetsPage() {
  const [bets, setBets] = useState<UserBet[]>([])
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setBets(loadBets())
    setMounted(true)
  }, [])

  const persist = useCallback((next: UserBet[]) => {
    setBets(next)
    saveBets(next)
  }, [])

  // Add bet form state
  const [match, setMatch] = useState('')
  const [pick, setPick] = useState('')
  const [odds, setOdds] = useState('')
  const [stake, setStake] = useState('')

  const addBet = () => {
    if (!match || !pick) return
    const bet: UserBet = {
      id: crypto.randomUUID(),
      matchLabel: match,
      pick,
      odds: parseFloat(odds) || undefined,
      stake: parseFloat(stake) || undefined,
      result: 'pending',
      createdAt: new Date().toISOString(),
    }
    persist([bet, ...bets])
    setMatch('')
    setPick('')
    setOdds('')
    setStake('')
  }

  const setResult = (id: string, result: UserBet['result']) => {
    persist(bets.map((b) => (b.id === id ? { ...b, result } : b)))
  }

  const removeBet = (id: string) => {
    persist(bets.filter((b) => b.id !== id))
  }

  // stats
  const total = bets.length
  const won = bets.filter((b) => b.result === 'won').length
  const lost = bets.filter((b) => b.result === 'lost').length
  const pending = bets.filter((b) => b.result === 'pending').length
  const profit = bets.reduce((acc, b) => {
    if (b.result === 'won' && b.odds && b.stake) return acc + b.stake * (b.odds - 1)
    if (b.result === 'lost' && b.stake) return acc - b.stake
    return acc
  }, 0)

  if (!mounted) return null

  return (
    <div className="container py-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">My Bets</h1>
          <p className="text-muted-foreground mt-1">
            Track your picks and measure performance over time.
          </p>
        </div>

        <Dialog>
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
              <div className="space-y-1.5">
                <Label>Match</Label>
                <Input
                  placeholder="e.g. Barcelona vs Real Madrid"
                  value={match}
                  onChange={(e) => setMatch(e.target.value)}
                />
              </div>
              <div className="space-y-1.5">
                <Label>Pick</Label>
                <Input
                  placeholder="e.g. 1, X, Over 2.5"
                  value={pick}
                  onChange={(e) => setPick(e.target.value)}
                />
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
            <DialogClose asChild>
              <Button className="w-full" onClick={addBet} disabled={!match || !pick}>
                Save Bet
              </Button>
            </DialogClose>
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
            <span className={`text-2xl font-bold tabular-nums ${profit >= 0 ? 'text-emerald-500' : 'text-red-500'}`}>
              {profit >= 0 ? '+' : ''}{profit.toFixed(2)}
            </span>
          </CardContent>
        </Card>
      </div>

      {/* Bet list */}
      <div className="space-y-3">
        {bets.length === 0 && (
          <Card>
            <CardContent className="py-12 text-center text-muted-foreground">
              No bets tracked yet. Tap &quot;Add Bet&quot; to get started.
            </CardContent>
          </Card>
        )}
        {bets.map((bet) => (
          <Card key={bet.id} className="flex items-center gap-4 p-4">
            {/* Result icon */}
            <div className="shrink-0">
              {bet.result === 'won' && <TrendingUp className="h-5 w-5 text-emerald-500" />}
              {bet.result === 'lost' && <TrendingDown className="h-5 w-5 text-red-500" />}
              {bet.result === 'pending' && <Minus className="h-5 w-5 text-muted-foreground" />}
            </div>

            {/* Details */}
            <div className="flex-1 min-w-0">
              <p className="font-medium text-sm truncate">{bet.matchLabel}</p>
              <p className="text-xs text-muted-foreground">
                Pick: <span className="font-mono">{bet.pick}</span>
                {bet.odds && <> &middot; Odds: <span className="font-mono">{bet.odds}</span></>}
                {bet.stake && <> &middot; Stake: <span className="font-mono">{bet.stake}</span></>}
              </p>
            </div>

            {/* Actions */}
            <div className="flex items-center gap-1 shrink-0">
              <Select value={bet.result} onValueChange={(v) => setResult(bet.id, v as UserBet['result'])}>
                <SelectTrigger className="h-8 w-[100px] text-xs">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="pending">Pending</SelectItem>
                  <SelectItem value="won">Won</SelectItem>
                  <SelectItem value="lost">Lost</SelectItem>
                  <SelectItem value="void">Void</SelectItem>
                </SelectContent>
              </Select>
              <Button variant="ghost" size="icon" className="h-8 w-8" onClick={() => removeBet(bet.id)}>
                <Trash2 className="h-3.5 w-3.5 text-muted-foreground" />
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  )
}
