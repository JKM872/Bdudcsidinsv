import React from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function AccuracyChart({ data, loading }) {
  if (loading) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Source Accuracy</h2>
        <div className="h-80 bg-slate-700 rounded animate-pulse"></div>
      </div>
    )
  }

  if (!data || !data.sources) return null

  const chartData = Object.entries(data.sources).map(([source, stats]) => ({
    name: source.charAt(0).toUpperCase() + source.slice(1),
    accuracy: parseFloat(stats.accuracy || 0),
    total: stats.total_predictions || 0,
    correct: stats.correct_predictions || 0
  }))

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">📊 Source Accuracy Comparison</h2>
        <span className="text-sm text-slate-400">Last {data.period_days} days</span>
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="name" stroke="#94a3b8" />
          <YAxis stroke="#94a3b8" />
          <Tooltip 
            contentStyle={{ 
              backgroundColor: '#1e293b', 
              border: '1px solid #334155',
              borderRadius: '8px',
              color: '#e2e8f0'
            }}
          />
          <Legend />
          <Bar dataKey="accuracy" fill="#3b82f6" name="Accuracy %" />
        </BarChart>
      </ResponsiveContainer>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-6">
        {chartData.map((source, idx) => (
          <div key={idx} className="bg-slate-700/50 rounded-lg p-4">
            <div className="text-slate-400 text-sm">{source.name}</div>
            <div className="text-2xl font-bold text-blue-400 mt-1">
              {source.accuracy.toFixed(1)}%
            </div>
            <div className="text-xs text-slate-500 mt-1">
              {source.correct}/{source.total} correct
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
