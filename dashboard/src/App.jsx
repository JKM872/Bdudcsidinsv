import React, { useState } from 'react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import Dashboard from './components/Dashboard'
import Header from './components/Header'

const queryClient = new QueryClient()

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-slate-900">
        <Header />
        <main className="container mx-auto px-4 py-8">
          <Dashboard />
        </main>
      </div>
    </QueryClientProvider>
  )
}

export default App
