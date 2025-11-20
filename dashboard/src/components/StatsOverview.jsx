import React from 'react'

export default function StatsOverview({ data, loading }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map(i => (
          <div key={i} className="card animate-pulse">
            <div className="h-20 bg-slate-700 rounded"></div>
          </div>
        ))}
      </div>
    )
  }

  if (!data) return null

  const stats = [
    {
      label: 'Total Predictions',
      value: data.total_predictions || 0,
      icon: '📊',
      color: 'text-blue-400'
    },
    {
      label: 'Qualified Picks',
      value: data.qualified_predictions || 0,
      icon: '✅',
      color: 'text-green-400'
    },
    {
      label: 'With Results',
      value: data.predictions_with_results || 0,
      icon: '🎯',
      color: 'text-purple-400'
    },
    {
      label: 'Success Rate',
      value: data.predictions_with_results > 0 
        ? `${Math.round((data.predictions_with_results / data.total_predictions) * 100)}%`
        : '0%',
      icon: '📈',
      color: 'text-yellow-400'
    }
  ]

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
      {stats.map((stat, idx) => (
        <div key={idx} className="card hover:border-blue-500 transition-colors">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm font-medium">{stat.label}</p>
              <p className={`text-3xl font-bold mt-2 ${stat.color}`}>
                {stat.value}
              </p>
            </div>
            <div className="text-4xl">{stat.icon}</div>
          </div>
        </div>
      ))}
    </div>
  )
}
