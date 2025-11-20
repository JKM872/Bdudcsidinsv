import React from 'react'

export default function Header() {
  return (
    <header className="bg-slate-800 border-b border-slate-700 shadow-lg">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-white mb-1">
              🎯 Sports Prediction Dashboard
            </h1>
            <p className="text-slate-400">
              4-Source Consensus Engine: LiveSport • Forebet • SofaScore • Gemini AI
            </p>
          </div>
          <div className="flex gap-4">
            <div className="text-right">
              <div className="text-sm text-slate-400">System Status</div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
                <span className="text-green-400 font-semibold">Online</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  )
}
