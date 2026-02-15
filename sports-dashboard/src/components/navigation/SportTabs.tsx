// ============================================================================
// SportTabs – FlashScore-style horizontal sport navigation
// ============================================================================
'use client'

import { Activity } from 'lucide-react'
import { cn } from '@/lib/utils'
import { SPORTS } from '@/lib/constants'
import { useFilterStore } from '@/store/filterStore'
import { ScrollArea, ScrollBar } from '@/components/ui/scroll-area'

interface Props {
  sportCounts?: Record<string, number>
}

export function SportTabs({ sportCounts = {} }: Props) {
  const { sport: activeSport, setSport } = useFilterStore()

  const allCount = Object.values(sportCounts).reduce((a, b) => a + b, 0)

  const tabs = [
    { id: 'all' as const, name: 'All', icon: Activity, color: 'text-foreground', count: allCount },
    ...SPORTS.map(s => ({ ...s, count: sportCounts[s.id] ?? 0 })),
  ]

  return (
    <div className="sticky top-14 z-40 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <ScrollArea className="w-full">
          <div className="flex items-center gap-1 py-1">
            {tabs.map(({ id, name, icon: Icon, color, count }) => {
              const isActive = activeSport === id
              return (
                <button
                  key={id}
                  onClick={() => setSport(id)}
                  className={cn(
                    'group flex items-center gap-1.5 whitespace-nowrap rounded-md px-3 py-2 text-sm font-medium transition-all',
                    'hover:bg-accent hover:text-accent-foreground',
                    isActive
                      ? 'bg-primary text-primary-foreground shadow-sm'
                      : 'text-muted-foreground',
                  )}
                >
                  <Icon className={cn('h-4 w-4', isActive ? 'text-primary-foreground' : color)} />
                  <span className="hidden sm:inline">{name}</span>
                  {count > 0 && (
                    <span className={cn(
                      'ml-0.5 text-[10px] tabular-nums rounded-full px-1.5 py-0.5 font-medium',
                      isActive
                        ? 'bg-primary-foreground/20 text-primary-foreground'
                        : 'bg-muted text-muted-foreground',
                    )}>
                      {count}
                    </span>
                  )}
                </button>
              )
            })}
          </div>
          <ScrollBar orientation="horizontal" className="h-1.5" />
        </ScrollArea>
      </div>
    </div>
  )
}
