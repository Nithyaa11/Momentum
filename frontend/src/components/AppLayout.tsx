import { ChartLine, ListChecks, Play, Target } from 'lucide-react'
import { NavLink, Outlet } from 'react-router'

import { ApiStatus } from '@/components/ApiStatus'
import { cn } from '@/lib/utils'

const NAV = [
  { to: '/', label: 'Now', icon: Play, end: true },
  { to: '/today', label: 'Today', icon: ListChecks },
  { to: '/goals', label: 'Goals', icon: Target },
  { to: '/progress', label: 'Progress', icon: ChartLine },
]

/** Temporary shell; the real design (sidebar on desktop, bottom tabs on mobile) comes on Dec 2. */
export function AppLayout() {
  return (
    <div className="min-h-svh bg-background text-foreground">
      <header className="border-b">
        <div className="mx-auto flex max-w-3xl items-center justify-between gap-4 px-4 py-3">
          <span className="font-semibold tracking-tight">Momentum</span>
          <nav className="flex gap-1">
            {NAV.map(({ to, label, icon: Icon, end }) => (
              <NavLink
                key={to}
                to={to}
                end={end}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-1.5 rounded-md px-3 py-1.5 text-sm transition-colors',
                    isActive
                      ? 'bg-secondary text-secondary-foreground font-medium'
                      : 'text-muted-foreground hover:text-foreground',
                  )
                }
              >
                <Icon className="size-4" aria-hidden />
                <span className="hidden sm:inline">{label}</span>
              </NavLink>
            ))}
          </nav>
        </div>
      </header>

      <main className="mx-auto max-w-3xl px-4 py-8">
        <Outlet />
      </main>

      <footer className="mx-auto max-w-3xl px-4 pb-6">
        <ApiStatus />
      </footer>
    </div>
  )
}
