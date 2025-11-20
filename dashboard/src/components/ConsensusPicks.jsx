import React from 'react'

export default function ConsensusPicks({ data, loading }) {
  if (loading) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">🔐 Top Consensus Picks</h2>
        <div className="space-y-3">
          {[1, 2, 3].map(i => (
            <div key={i} className="h-24 bg-slate-700 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    )
  }

  if (!data || !data.picks || data.picks.length === 0) {
    return (
      <div className="card">
        <h2 className="text-2xl font-bold mb-4">🔐 Top Consensus Picks</h2>
        <p className="text-slate-400 text-center py-8">No consensus picks available</p>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold">🔐 Top Consensus Picks</h2>
        <span className="text-sm text-slate-400">
          {data.count} picks with {data.min_agreement}+ sources agreeing
        </span>
      </div>

      <div className="space-y-4">
        {data.picks.slice(0, 5).map((pick, idx) => (
          <div 
            key={idx}
            className="bg-gradient-to-r from-purple-900/20 to-blue-900/20 border-2 border-purple-500/50 rounded-lg p-5 hover:border-purple-400 transition-colors"
          >
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="badge badge-lock text-lg px-4">
                    {pick.consensus_count}/4 SOURCES AGREE
                  </span>
                  <span className="text-sm bg-slate-700 px-3 py-1 rounded">
                    {pick.sport}
                  </span>
                </div>
                
                <h3 className="text-xl font-bold mb-1">
                  {pick.home_team} vs {pick.away_team}
                </h3>
                
                <div className="text-sm text-slate-400 mb-3">
                  {pick.match_date} • {pick.match_time} • {pick.league || 'League TBD'}
                </div>

                <div className="flex flex-wrap gap-2 mb-3">
                  {pick.sources_agreeing.map((source, i) => (
                    <span key={i} className="text-xs bg-green-600/30 text-green-300 px-3 py-1 rounded-full border border-green-500/50">
                      ✓ {source}
                    </span>
                  ))}
                </div>

                <div className="grid grid-cols-4 gap-4 text-sm">
                  <div>
                    <div className="text-slate-400 text-xs">LiveSport</div>
                    <div className="font-semibold text-blue-400">
                      {pick.livesport_win_rate ? `${pick.livesport_win_rate.toFixed(0)}%` : '-'}
                    </div>
                  </div>
                  <div>
                    <div className="text-slate-400 text-xs">Forebet</div>
                    <div className="font-semibold text-green-400">
                      {pick.forebet_probability ? `${pick.forebet_probability.toFixed(0)}%` : '-'}
                    </div>
                  </div>
                  <div>
                    <div className="text-slate-400 text-xs">SofaScore</div>
                    <div className="font-semibold text-purple-400">
                      {pick.sofascore_home_win_prob ? `${pick.sofascore_home_win_prob.toFixed(0)}%` : '-'}
                    </div>
                  </div>
                  <div>
                    <div className="text-slate-400 text-xs">Gemini AI</div>
                    <div className="font-semibold text-yellow-400">
                      {pick.gemini_confidence ? `${pick.gemini_confidence.toFixed(0)}%` : '-'}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
