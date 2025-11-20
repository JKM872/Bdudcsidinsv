import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import StatsOverview from './StatsOverview'
import AccuracyChart from './AccuracyChart'
import PredictionsTable from './PredictionsTable'
import ConsensusPicks from './ConsensusPicks'
import { fetchStats, fetchAccuracy, fetchRecentPredictions, fetchConsensusPicks } from '../api'

export default function Dashboard() {
  const [selectedDays, setSelectedDays] = useState(7)
  const [selectedSport, setSelectedSport] = useState('all')
  
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ['stats', selectedDays],
    queryFn: () => fetchStats(selectedDays)
  })
  
  const { data: accuracy, isLoading: accuracyLoading } = useQuery({
    queryKey: ['accuracy', selectedDays],
    queryFn: () => fetchAccuracy(selectedDays)
  })
  
  const { data: predictions, isLoading: predictionsLoading } = useQuery({
    queryKey: ['predictions', selectedDays, selectedSport],
    queryFn: () => fetchRecentPredictions(selectedDays, selectedSport === 'all' ? null : selectedSport)
  })
  
  const { data: consensusPicks, isLoading: consensusLoading } = useQuery({
    queryKey: ['consensus', selectedDays],
    queryFn: () => fetchConsensusPicks(selectedDays, 3)
  })

  return (
    <div className="space-y-8">
      {/* Filters */}
      <div className="card">
        <div className="flex gap-4 items-center">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Time Period
            </label>
            <select 
              value={selectedDays}
              onChange={(e) => setSelectedDays(Number(e.target.value))}
              className="bg-slate-700 border border-slate-600 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value={1}>Today</option>
              <option value={7}>Last 7 days</option>
              <option value={14}>Last 14 days</option>
              <option value={30}>Last 30 days</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2">
              Sport
            </label>
            <select 
              value={selectedSport}
              onChange={(e) => setSelectedSport(e.target.value)}
              className="bg-slate-700 border border-slate-600 text-white rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Sports</option>
              <option value="football">⚽ Football</option>
              <option value="basketball">🏀 Basketball</option>
              <option value="volleyball">🏐 Volleyball</option>
              <option value="tennis">🎾 Tennis</option>
            </select>
          </div>
        </div>
      </div>

      {/* Stats Overview */}
      <StatsOverview data={stats} loading={statsLoading} />

      {/* Consensus Picks */}
      <ConsensusPicks data={consensusPicks} loading={consensusLoading} />

      {/* Accuracy Chart */}
      <AccuracyChart data={accuracy} loading={accuracyLoading} />

      {/* Predictions Table */}
      <PredictionsTable data={predictions} loading={predictionsLoading} />
    </div>
  )
}
