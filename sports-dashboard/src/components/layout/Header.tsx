// ============================================================================
// Header – top navigation bar
// ============================================================================
'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import {
  Trophy, BarChart3, Ticket, Users, Sun, Moon, Menu,
} from 'lucide-react'
import { useTheme } from 'next-themes'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'

const NAV_ITEMS = [
  { href: '/',            label: 'Matches',     icon: Trophy     },
  { href: '/stats',       label: 'Statistics',  icon: BarChart3  },
  { href: '/my-bets',     label: 'My Bets',     icon: Ticket     },
  { href: '/leaderboard', label: 'Leaderboard', icon: Users      },
]

function NavLinks({ mobile, onNavigate }: { mobile?: boolean; onNavigate?: () => void }) {
  const pathname = usePathname()
  return (
    <>
      {NAV_ITEMS.map(({ href, label, icon: Icon }) => {
        const active = pathname === href
        return (
          <Link
            key={href}
            href={href}
            onClick={onNavigate}
            className={cn(
              'flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium transition-colors',
              mobile ? 'w-full' : '',
              active
                ? 'bg-primary text-primary-foreground'
                : 'text-muted-foreground hover:bg-accent hover:text-accent-foreground',
            )}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        )
      })}
    </>
  )
}

export function Header() {
  const { theme, setTheme } = useTheme()

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="mx-auto flex h-14 max-w-7xl items-center gap-4 px-4 sm:px-6">
        {/* Mobile menu */}
        <Sheet>
          <SheetTrigger asChild>
            <Button variant="ghost" size="icon" className="md:hidden">
              <Menu className="h-5 w-5" />
              <span className="sr-only">Menu</span>
            </Button>
          </SheetTrigger>
          <SheetContent side="left" className="w-64 pt-10">
            <nav className="flex flex-col gap-1">
              <NavLinks mobile />
            </nav>
          </SheetContent>
        </Sheet>

        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 font-bold text-lg whitespace-nowrap">
          <Trophy className="h-5 w-5 text-primary" />
          <span className="hidden sm:inline">Sports Predictor</span>
          <span className="sm:hidden">SP</span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1 ml-6">
          <NavLinks />
        </nav>

        {/* Spacer */}
        <div className="flex-1" />

        {/* Theme toggle */}
        <Button
          variant="ghost"
          size="icon"
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        >
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </div>
    </header>
  )
}
