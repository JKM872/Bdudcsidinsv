// ============================================================================
// AccuracyChart – sport-level accuracy line / bar chart (Recharts)
// ============================================================================
'use client'

import {
  ResponsiveContainer,
  BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Cell,
} from 'recharts'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card'
import type { SportStat } from '@/lib/types'

interface AccuracyChartProps {
  sportStats: SportStat[]
}

// Resolve sport colour from constants or fallback
function getSportColor(sportId: string) {
  // map tailwind-style classname to a plain hex; we keep a small palette
  const palette: Record<string, string> = {
    football: '#22c55e',
    basketball: '#f97316',
    tennis: '#eab308',
    hockey: '#3b82f6',
    handball: '#a855f7',
    volleyball: '#ef4444',
  }
  return palette[sportId] ?? '#64748b'
}

export function AccuracyChart({ sportStats }: AccuracyChartProps) {
  const data = sportStats.map((s) => ({
    sport: s.sport.charAt(0).toUpperCase() + s.sport.slice(1),
    id: s.sport,
    accuracy: Number(((s.accuracy ?? 0) * 100).toFixed(1)),
    total: s.total,
  }))

  return (
    <Card>
      <CardHeader>
        <CardTitle>Prediction Accuracy by Sport</CardTitle>
        <CardDescription>
          Based on resolved matches with Forebet predictions
        </CardDescription>
      </CardHeader>
      <CardContent>
        {data.length === 0 ? (
          <p className="text-sm text-muted-foreground text-center py-6">
            No stat data available yet.
          </p>
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data} margin={{ top: 8, right: 8, bottom: 0, left: -16 }}>
              <CartesianGrid strokeDasharray="3 3" className="stroke-border" />
              <XAxis dataKey="sport" tick={{ fontSize: 12 }} />
              <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} unit="%" />
              <Tooltip
                content={({ active, payload }) => {
                  if (!active || !payload?.length) return null
                  const d = payload[0].payload
                  return (
                    <div className="bg-popover text-popover-foreground border rounded-lg shadow-lg px-3 py-2 text-sm">
                      <p className="font-semibold">{d.sport}</p>
                      <p>Accuracy: <span className="font-mono">{d.accuracy}%</span></p>
                      <p className="text-muted-foreground text-xs">{d.total} matches</p>
                    </div>
                  )
                }}
              />
              <Bar dataKey="accuracy" radius={[6, 6, 0, 0]} maxBarSize={48}>
                {data.map((entry) => (
                  <Cell key={entry.id} fill={getSportColor(entry.id)} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        )}
      </CardContent>
    </Card>
  )
}
