// ============================================================================
// AIPredictionPanel — Ultra PRO match analysis display
// ============================================================================
'use client'

import {
  Brain, Shield, AlertTriangle, CheckCircle2, XCircle, TrendingUp,
  BarChart3, Target, ChevronDown, ChevronUp, Zap,
} from 'lucide-react'
import { Badge } from '@/components/ui/badge'
import { cn } from '@/lib/utils'
import { RadialProgress } from '@/components/charts/RadialProgress'
import type { AIPrediction, AIFactor } from '@/lib/types'
import { useState } from 'react'

interface Props {
  prediction: AIPrediction
  homeTeam: string
  awayTeam: string
  compact?: boolean
}

// ── Confidence tier colors ──
const TIER_COLORS: Record<string, string> = {
  'VERY HIGH': 'bg-emerald-500 text-white',
  'HIGH': 'bg-emerald-400 text-white',
  'MEDIUM': 'bg-amber-500 text-white',
  'LOW': 'bg-orange-500 text-white',
  'VERY LOW': 'bg-red-500 text-white',
}

const RISK_COLORS: Record<string, string> = {
  'LOW': 'text-emerald-600 dark:text-emerald-400',
  'MEDIUM': 'text-amber-600 dark:text-amber-400',
  'HIGH': 'text-red-600 dark:text-red-400',
}

const IMPACT_COLORS: Record<string, string> = {
  positive: 'text-emerald-600 dark:text-emerald-400',
  neutral: 'text-muted-foreground',
  negative: 'text-red-600 dark:text-red-400',
}

const VALUE_COLORS: Record<string, string> = {
  'EXCELLENT': 'bg-emerald-500/15 text-emerald-700 dark:text-emerald-400 border-emerald-500/20',
  'GOOD': 'bg-blue-500/15 text-blue-700 dark:text-blue-400 border-blue-500/20',
  'FAIR': 'bg-amber-500/15 text-amber-700 dark:text-amber-400 border-amber-500/20',
  'NONE': 'bg-muted text-muted-foreground border-border',
}

const CONSENSUS_COLORS: Record<string, string> = {
  'STRONG': 'text-emerald-600',
  'MODERATE': 'text-blue-600',
  'WEAK': 'text-amber-600',
  'DIVIDED': 'text-red-600',
  'UNKNOWN': 'text-muted-foreground',
}

// ── Compact card badge (for MatchCard) ──
export function AIPredictionBadge({ prediction }: { prediction: AIPrediction }) {
  const tier = prediction.confidenceTier
  return (
    <Badge className={cn('text-[9px] px-1.5 py-0 gap-0.5 font-semibold', TIER_COLORS[tier] ?? 'bg-zinc-500 text-white')}>
      <Brain className="h-2.5 w-2.5" />
      {prediction.compositeConfidence.toFixed(0)}%
    </Badge>
  )
}

// ── Full panel for MatchDetails ──
export function AIPredictionPanel({ prediction: p, homeTeam, awayTeam, compact }: Props) {
  const [showFactors, setShowFactors] = useState(!compact)

  return (
    <div className="space-y-4">
      {/* ── Header: Verdict + confidence ── */}
      <div className="rounded-xl border bg-card p-4 space-y-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm font-medium">
            <Brain className="h-4 w-4 text-violet-500" />
            AI Prediction
          </div>
          <Badge className={cn('text-xs', TIER_COLORS[p.confidenceTier] ?? '')}>
            {p.confidenceTier}
          </Badge>
        </div>

        {/* Pick + confidence ring */}
        <div className="flex items-center gap-4">
          <RadialProgress value={p.compositeConfidence} size={64} strokeWidth={5} color="#8b5cf6" label="AI" />
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2 mb-1">
              <Badge className="bg-violet-500 text-white">{p.pick}</Badge>
              <span className="text-sm font-semibold">{p.pickLabel}</span>
            </div>
            <p className="text-xs text-muted-foreground leading-relaxed">{p.shortVerdict}</p>
          </div>
        </div>

        {/* Probability bar  */}
        <div className="space-y-1.5">
          <div className="flex h-5 rounded-full overflow-hidden text-[10px] font-bold text-white">
            <div className="flex items-center justify-center bg-emerald-500 transition-all"
              style={{ width: `${p.probHome}%` }}>
              {p.probHome > 10 ? `${p.probHome.toFixed(0)}%` : ''}
            </div>
            {p.probDraw > 0 && (
              <div className="flex items-center justify-center bg-amber-500 transition-all"
                style={{ width: `${p.probDraw}%` }}>
                {p.probDraw > 10 ? `${p.probDraw.toFixed(0)}%` : ''}
              </div>
            )}
            <div className="flex items-center justify-center bg-rose-500 transition-all"
              style={{ width: `${p.probAway}%` }}>
              {p.probAway > 10 ? `${p.probAway.toFixed(0)}%` : ''}
            </div>
          </div>
          <div className="flex justify-between text-[10px] text-muted-foreground">
            <span>{homeTeam} {p.probHome.toFixed(0)}%</span>
            {p.probDraw > 0 && <span>Draw {p.probDraw.toFixed(0)}%</span>}
            <span>{awayTeam} {p.probAway.toFixed(0)}%</span>
          </div>
        </div>
      </div>

      {/* ── Consensus + Value + Risk grid ── */}
      <div className="grid grid-cols-3 gap-2">
        {/* Consensus */}
        <div className="rounded-xl border bg-card p-3 text-center space-y-1">
          <div className="flex items-center justify-center gap-1">
            <Target className="h-3 w-3 text-blue-500" />
            <span className="text-[10px] text-muted-foreground font-medium">Consensus</span>
          </div>
          <p className={cn('text-lg font-bold', CONSENSUS_COLORS[p.consensus.strength])}>
            {p.consensus.sources}/{p.consensus.total}
          </p>
          <p className="text-[10px] text-muted-foreground">{p.consensus.strength}</p>
        </div>

        {/* Value */}
        <div className="rounded-xl border bg-card p-3 text-center space-y-1">
          <div className="flex items-center justify-center gap-1">
            <TrendingUp className="h-3 w-3 text-emerald-500" />
            <span className="text-[10px] text-muted-foreground font-medium">Value</span>
          </div>
          <p className={cn('text-lg font-bold', p.ev > 0 ? 'text-emerald-600' : 'text-muted-foreground')}>
            {p.ev > 0 ? '+' : ''}{p.ev.toFixed(3)}
          </p>
          <Badge variant="outline" className={cn('text-[9px]', VALUE_COLORS[p.valueRating])}>
            {p.valueRating}
          </Badge>
        </div>

        {/* Risk */}
        <div className="rounded-xl border bg-card p-3 text-center space-y-1">
          <div className="flex items-center justify-center gap-1">
            <Shield className="h-3 w-3 text-amber-500" />
            <span className="text-[10px] text-muted-foreground font-medium">Risk</span>
          </div>
          <p className={cn('text-lg font-bold', RISK_COLORS[p.risk.level])}>
            {p.risk.score}/10
          </p>
          <p className="text-[10px] text-muted-foreground">{p.risk.level}</p>
        </div>
      </div>

      {/* ── Key Arguments ── */}
      {(p.keyArgumentsFor.length > 0 || p.keyArgumentsAgainst.length > 0) && (
        <div className="rounded-xl border bg-card p-4 space-y-3">
          <span className="text-sm font-medium">Key Arguments</span>
          {p.keyArgumentsFor.length > 0 && (
            <div className="space-y-1.5">
              {p.keyArgumentsFor.map((arg, i) => (
                <div key={i} className="flex items-start gap-2 text-xs">
                  <CheckCircle2 className="h-3.5 w-3.5 text-emerald-500 mt-0.5 shrink-0" />
                  <span className="text-muted-foreground">{arg}</span>
                </div>
              ))}
            </div>
          )}
          {p.keyArgumentsAgainst.length > 0 && (
            <div className="space-y-1.5">
              {p.keyArgumentsAgainst.map((arg, i) => (
                <div key={i} className="flex items-start gap-2 text-xs">
                  <XCircle className="h-3.5 w-3.5 text-red-500 mt-0.5 shrink-0" />
                  <span className="text-muted-foreground">{arg}</span>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* ── Factor Breakdown (collapsible) ── */}
      <div className="rounded-xl border bg-card overflow-hidden">
        <button
          className="flex items-center justify-between w-full px-4 py-3 text-sm font-medium hover:bg-muted/30 transition-colors"
          onClick={() => setShowFactors(prev => !prev)}
        >
          <div className="flex items-center gap-2">
            <BarChart3 className="h-4 w-4 text-violet-500" />
            Factor Analysis ({p.factors.length} factors)
          </div>
          {showFactors ? <ChevronUp className="h-4 w-4" /> : <ChevronDown className="h-4 w-4" />}
        </button>
        {showFactors && (
          <div className="px-4 pb-4 space-y-2">
            {p.factors.map((f, i) => (
              <FactorRow key={i} factor={f} />
            ))}
          </div>
        )}
      </div>

      {/* ── Full Verdict ── */}
      <div className="rounded-xl border bg-card p-4 space-y-2">
        <span className="text-xs text-muted-foreground font-medium">AI Verdict</span>
        <div className="bg-muted/50 rounded-lg p-3 text-sm leading-relaxed">
          {p.verdict}
        </div>
      </div>

      {/* ── Risk flags ── */}
      {p.risk.flags.length > 0 && (
        <div className="space-y-1.5">
          {p.risk.flags.map((flag, i) => (
            <div key={i} className="flex items-center gap-2 rounded-lg bg-amber-500/10 border border-amber-500/20 p-2.5">
              <AlertTriangle className="h-3.5 w-3.5 text-amber-500 shrink-0" />
              <span className="text-xs text-amber-700 dark:text-amber-400">{flag}</span>
            </div>
          ))}
        </div>
      )}

      {/* ── Do Not Bet warnings ── */}
      {p.doNotBetReasons.length > 0 && (
        <div className="rounded-xl border-2 border-red-500/30 bg-red-500/5 p-4 space-y-2">
          <div className="flex items-center gap-2 text-sm font-semibold text-red-600 dark:text-red-400">
            <XCircle className="h-4 w-4" /> Betting Not Recommended
          </div>
          {p.doNotBetReasons.map((r, i) => (
            <p key={i} className="text-xs text-red-600/80 dark:text-red-400/80 pl-6">&bull; {r}</p>
          ))}
        </div>
      )}

      {/* ── Data quality footer ── */}
      <div className="flex items-center justify-between text-[10px] text-muted-foreground px-1">
        <span>Data: {p.dataQualityLabel} ({(p.dataQuality * 100).toFixed(0)}%)</span>
        <span>Sources: {p.availableSources.length}/{p.availableSources.length + p.missingSources.length}</span>
        {p.edge > 0 && (
          <span className="flex items-center gap-0.5">
            <Zap className="h-3 w-3 text-amber-500" />
            Edge +{p.edge.toFixed(1)}%
          </span>
        )}
      </div>
    </div>
  )
}

// ── Factor row ──
function FactorRow({ factor: f }: { factor: AIFactor }) {
  const barWidth = Math.min(100, Math.max(5, Math.abs(f.value)))
  const impactIcon = f.impact === 'positive'
    ? <CheckCircle2 className="h-3 w-3 text-emerald-500" />
    : f.impact === 'negative'
      ? <XCircle className="h-3 w-3 text-red-500" />
      : <div className="h-3 w-3 rounded-full bg-muted-foreground/30" />

  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1.5">
          {impactIcon}
          <span className="text-xs font-medium">{f.name}</span>
          <span className="text-[10px] text-muted-foreground">({(f.weight * 100).toFixed(0)}%)</span>
        </div>
        <span className={cn('text-xs font-bold tabular-nums', IMPACT_COLORS[f.impact])}>
          {f.value > 0 ? '+' : ''}{f.value.toFixed(0)}
        </span>
      </div>
      <div className="flex items-center gap-2">
        <div className="flex-1 h-1.5 bg-muted rounded-full overflow-hidden">
          <div
            className={cn(
              'h-full rounded-full transition-all',
              f.impact === 'positive' ? 'bg-emerald-500' : f.impact === 'negative' ? 'bg-red-400' : 'bg-muted-foreground/40',
            )}
            style={{ width: `${barWidth}%` }}
          />
        </div>
        {f.quality < 1 && (
          <span className="text-[9px] text-muted-foreground/60">{(f.quality * 100).toFixed(0)}% data</span>
        )}
      </div>
      <p className="text-[10px] text-muted-foreground leading-snug">{f.description}</p>
    </div>
  )
}
