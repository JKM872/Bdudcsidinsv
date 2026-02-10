// ============================================================================
// StatsOverview  – top-level KPI cards
// ============================================================================
'use client'

import {
  BarChart3, Target, TrendingUp, Trophy, Percent, Clock,
} from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import type { StatsData } from '@/lib/types'

interface StatCardProps {
  label: string
  value: string | number
  subtitle?: string
  icon: React.ElementType
  trend?: number // positive = green, negative = red, undefined = neutral
}

function StatCard({ label, value, subtitle, icon: Icon, trend }: StatCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
        <CardTitle className="text-sm font-medium text-muted-foreground">{label}</CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold tabular-nums">{value}</div>
        {subtitle && (
          <p className="text-xs text-muted-foreground mt-1 flex items-center gap-1">
            {trend !== undefined && (
              <span className={trend >= 0 ? 'text-emerald-500' : 'text-red-500'}>
                {trend >= 0 ? '+' : ''}{trend}%
              </span>
            )}
            {subtitle}
          </p>
        )}
      </CardContent>
    </Card>
  )
}

interface StatsOverviewProps {
  data: StatsData
}

export function StatsOverview({ data }: StatsOverviewProps) {
  const accuracy = data.accuracy_30d != null ? data.accuracy_30d.toFixed(1) : '0.0'
  const bestSport = data.sport_breakdown?.length
    ? data.sport_breakdown.reduce((best, cur) =>
        (cur.accuracy ?? 0) > (best.accuracy ?? 0) ? cur : best
      )
    : null

  return (
    <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
      <StatCard
        icon={BarChart3}
        label="Total Matches"
        value={data.total_matches.toLocaleString()}
        subtitle="scraped overall"
      />
      <StatCard
        icon={Target}
        label="With Predictions"
        value={data.matches_with_predictions.toLocaleString()}
        subtitle="from Forebet"
      />
      <StatCard
        icon={Percent}
        label="Accuracy (30d)"
        value={`${accuracy}%`}
        subtitle="correct picks"
        trend={data.accuracy_30d != null && data.accuracy_30d > 50 ? +(data.accuracy_30d - 50).toFixed(1) : data.accuracy_30d != null ? -(50 - data.accuracy_30d) : undefined}
      />
      <StatCard
        icon={Trophy}
        label="Best Sport"
        value={bestSport ? bestSport.sport.charAt(0).toUpperCase() + bestSport.sport.slice(1) : '–'}
        subtitle="highest accuracy"
      />
      <StatCard
        icon={TrendingUp}
        label="With Odds"
        value={data.matches_with_odds ?? 0}
        subtitle="bookmaker odds"
      />
      <StatCard
        icon={Clock}
        label="ROI (30d)"
        value={data.roi_30d != null ? `${data.roi_30d.toFixed(1)}%` : '–'}
        subtitle="return on investment"
      />
    </div>
  )
}
