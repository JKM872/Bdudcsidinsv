import React from 'react'
import { format } from 'date-fns'

export default function PredictionsTable({ data, loading }) {
  if (loading) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Recent Predictions</h2>
        <div className="space-y-2">
          {[1, 2, 3, 4, 5].map(i => (
            <div key={i} className="h-16 bg-slate-700 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    )
  }

  if (!data || !data.predictions || data.predictions.length === 0) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">Recent Predictions</h2>
        <p className="text-slate-400 text-center py-8">No predictions found</p>
      </div>
    )
  }

  const getConsensusLevel = (pred) => {
    let count = 0
    if (pred.livesport_win_rate >= 60) count++
    if (pred.forebet_prediction === '1') count++
    if (pred.sofascore_home_win_prob > pred.sofascore_away_win_prob) count++
    if (pred.gemini_recommendation === 'HIGH' || pred.gemini_recommendation === 'LOCK') count++
    
    if (count === 4) return { label: '🔐 LOCK', class: 'badge-lock' }
    if (count === 3) return { label: '🟢 HIGH', class: 'badge-high' }
    if (count === 2) return { label: '🟡 MEDIUM', class: 'badge-medium' }
    return { label: '❌ LOW', class: 'badge-low' }
  }

  return (
    <div className="card">
      <h2 className="text-2xl font-bold mb-6">📋 Recent Predictions</h2>
      
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-slate-700">
              <th className="text-left py-3 px-4 text-slate-300">Date</th>
              <th className="text-left py-3 px-4 text-slate-300">Match</th>
              <th className="text-left py-3 px-4 text-slate-300">Sport</th>
              <th className="text-center py-3 px-4 text-slate-300">Consensus</th>
              <th className="text-center py-3 px-4 text-slate-300">LiveSport</th>
              <th className="text-center py-3 px-4 text-slate-300">Forebet</th>
              <th className="text-center py-3 px-4 text-slate-300">SofaScore</th>
              <th className="text-center py-3 px-4 text-slate-300">Gemini</th>
              <th className="text-center py-3 px-4 text-slate-300">Result</th>
            </tr>
          </thead>
          <tbody>
            {data.predictions.map((pred, idx) => {
              const consensus = getConsensusLevel(pred)
              return (
                <tr key={idx} className="border-b border-slate-700/50 hover:bg-slate-700/30 transition-colors">
                  <td className="py-4 px-4 text-sm text-slate-400">
                    {pred.match_date}
                    <br />
                    <span className="text-xs">{pred.match_time}</span>
                  </td>
                  <td className="py-4 px-4">
                    <div className="font-semibold">{pred.home_team}</div>
                    <div className="text-sm text-slate-400">vs {pred.away_team}</div>
                  </td>
                  <td className="py-4 px-4">
                    <span className="text-sm bg-slate-700 px-2 py-1 rounded">
                      {pred.sport}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-center">
                    <span className={`badge ${consensus.class}`}>
                      {consensus.label}
                    </span>
                  </td>
                  <td className="py-4 px-4 text-center text-sm">
                    {pred.livesport_win_rate ? `${pred.livesport_win_rate.toFixed(0)}%` : '-'}
                  </td>
                  <td className="py-4 px-4 text-center text-sm">
                    {pred.forebet_probability ? `${pred.forebet_probability.toFixed(0)}%` : '-'}
                  </td>
                  <td className="py-4 px-4 text-center text-sm">
                    {pred.sofascore_home_win_prob ? `${pred.sofascore_home_win_prob.toFixed(0)}%` : '-'}
                  </td>
                  <td className="py-4 px-4 text-center text-sm">
                    {pred.gemini_confidence ? (
                      <span className="flex flex-col items-center">
                        <span>{pred.gemini_confidence.toFixed(0)}%</span>
                        <span className="text-xs text-slate-400">{pred.gemini_recommendation}</span>
                      </span>
                    ) : '-'}
                  </td>
                  <td className="py-4 px-4 text-center">
                    {pred.actual_result ? (
                      <span className="badge badge-success">
                        {pred.home_score}-{pred.away_score}
                      </span>
                    ) : (
                      <span className="text-slate-500 text-sm">Pending</span>
                    )}
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}
