// ============================================================================
// Auth Store — Zustand store for Supabase auth state
// ============================================================================
'use client'

import { create } from 'zustand'
import { supabase } from '@/lib/supabase'
import type { User, Session } from '@supabase/supabase-js'

interface AuthState {
  user: User | null
  session: Session | null
  loading: boolean
  initialized: boolean

  init: () => Promise<void>
  signIn: (email: string, password: string) => Promise<{ error: string | null }>
  signUp: (email: string, password: string) => Promise<{ error: string | null }>
  signOut: () => Promise<void>

  /** Convenience: returns Bearer token or empty string */
  getToken: () => string
}

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  session: null,
  loading: true,
  initialized: false,

  init: async () => {
    if (get().initialized) return
    if (!supabase) {
      set({ loading: false, initialized: true })
      return
    }

    // Get current session
    const { data } = await supabase.auth.getSession()
    set({
      user: data.session?.user ?? null,
      session: data.session ?? null,
      loading: false,
      initialized: true,
    })

    // Listen for auth changes
    supabase.auth.onAuthStateChange((_event, session) => {
      set({ user: session?.user ?? null, session })
    })
  },

  signIn: async (email, password) => {
    if (!supabase) return { error: 'Supabase not configured' }
    set({ loading: true })
    const { error } = await supabase.auth.signInWithPassword({ email, password })
    set({ loading: false })
    return { error: error?.message ?? null }
  },

  signUp: async (email, password) => {
    if (!supabase) return { error: 'Supabase not configured' }
    set({ loading: true })
    const { error } = await supabase.auth.signUp({ email, password })
    set({ loading: false })
    return { error: error?.message ?? null }
  },

  signOut: async () => {
    if (!supabase) return
    await supabase.auth.signOut()
    set({ user: null, session: null })
  },

  getToken: () => {
    const session = get().session
    return session?.access_token ? `Bearer ${session.access_token}` : ''
  },
}))
