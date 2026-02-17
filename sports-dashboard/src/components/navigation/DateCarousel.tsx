// ============================================================================
// DateCarousel – FlashScore-style date navigation
// ============================================================================
'use client'

import { ChevronLeft, ChevronRight, CalendarDays } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Popover, PopoverContent, PopoverTrigger } from '@/components/ui/popover'
import { Calendar } from '@/components/ui/calendar'
import { cn } from '@/lib/utils'
import { useFilterStore } from '@/store/filterStore'
import {
  format,
  addDays,
  subDays,
  isToday,
  isTomorrow,
  isYesterday,
  startOfDay,
  isSameDay,
} from 'date-fns'

function getDateLabel(date: Date): string {
  if (isToday(date)) return 'Today'
  if (isTomorrow(date)) return 'Tomorrow'
  if (isYesterday(date)) return 'Yesterday'
  return format(date, 'd MMM')
}

function getWeekdayLabel(date: Date): string {
  if (isToday(date)) return ''
  return format(date, 'EEE')
}

export function DateCarousel() {
  const { date: filterDate, setDate } = useFilterStore()

  // Centre date – use filter date if set, else today
  const centre = filterDate ? startOfDay(filterDate) : startOfDay(new Date())

  // Generate 5-day range centred on selection
  const days = Array.from({ length: 5 }, (_, i) => addDays(centre, i - 2))

  const goBack = () => setDate(subDays(centre, 1))
  const goForward = () => setDate(addDays(centre, 1))
  const selectDay = (d: Date) => {
    // Clicking "today" when already selected clears the date (show latest)
    if (isSameDay(d, centre) && isToday(d)) {
      setDate(null)
    } else {
      setDate(d)
    }
  }

  return (
    <div className="sticky top-[100px] z-30 w-full border-b bg-muted/30 backdrop-blur supports-[backdrop-filter]:bg-muted/20">
      <div className="mx-auto max-w-7xl px-4 sm:px-6">
        <div className="flex items-center justify-center gap-1 py-1.5">
          {/* Back arrow */}
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 shrink-0"
            onClick={goBack}
          >
            <ChevronLeft className="h-4 w-4" />
          </Button>

          {/* Date buttons */}
          <div className="flex items-center gap-0.5 overflow-x-auto">
            {days.map((day) => {
              const isSelected = isSameDay(day, centre)
              const isTodayDate = isToday(day)
              const weekday = getWeekdayLabel(day)

              return (
                <button
                  key={day.toISOString()}
                  onClick={() => selectDay(day)}
                  className={cn(
                    'flex flex-col items-center rounded-lg px-3 py-1.5 text-xs transition-all min-w-[56px]',
                    'hover:bg-accent',
                    isSelected && 'bg-primary text-primary-foreground shadow-sm hover:bg-primary/90',
                    !isSelected && isTodayDate && 'font-bold',
                    !isSelected && !isTodayDate && 'text-muted-foreground',
                  )}
                >
                  {weekday && (
                    <span className={cn(
                      'text-[10px] uppercase leading-tight',
                      isSelected ? 'text-primary-foreground/70' : 'text-muted-foreground',
                    )}>
                      {weekday}
                    </span>
                  )}
                  <span className="font-medium leading-tight">
                    {getDateLabel(day)}
                  </span>
                  <span className={cn(
                    'text-[10px] leading-tight tabular-nums',
                    isSelected ? 'text-primary-foreground/70' : 'text-muted-foreground/70',
                  )}>
                    {format(day, 'd/MM')}
                  </span>
                </button>
              )
            })}
          </div>

          {/* Forward arrow */}
          <Button
            variant="ghost"
            size="icon"
            className="h-8 w-8 shrink-0"
            onClick={goForward}
          >
            <ChevronRight className="h-4 w-4" />
          </Button>

          {/* Calendar picker */}
          <Popover>
            <PopoverTrigger asChild>
              <Button variant="ghost" size="icon" className="h-8 w-8 shrink-0 ml-1">
                <CalendarDays className="h-4 w-4" />
              </Button>
            </PopoverTrigger>
            <PopoverContent className="w-auto p-0" align="end">
              <Calendar
                mode="single"
                selected={filterDate ?? undefined}
                onSelect={(d) => {
                  if (d) setDate(d)
                }}
                initialFocus
              />
            </PopoverContent>
          </Popover>
        </div>
      </div>
    </div>
  )
}
