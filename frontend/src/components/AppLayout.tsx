import { NavLink, Outlet } from 'react-router'

import { ApiStatus } from '@/components/ApiStatus'
import { NAV_ITEMS } from '@/components/nav'
import { cn } from '@/lib/utils'

/**
 * Responsive app shell.
 * - Phone: slim top bar + fixed bottom tab bar (icon + label), thumb-reachable.
 * - Desktop (md+): left sidebar with icon + label.
 */
export function AppLayout() {
  return (
    <div className="min-h-svh bg-background text-foreground md:flex">
      <DesktopSidebar />

      <div className="flex min-w-0 flex-1 flex-col">
        <MobileTopBar />
        {/* Bottom padding keeps content clear of the mobile tab bar + iPhone home indicator */}
        <main className="mx-auto w-full max-w-2xl flex-1 px-4 pt-6 pb-[calc(5.5rem+env(safe-area-inset-bottom))] md:px-8 md:pt-10 md:pb-10">
          <Outlet />
        </main>
      </div>

      <MobileTabBar />
    </div>
  )
}

function Wordmark() {
  return (
    <span className="flex items-center gap-2 font-semibold tracking-tight">
      <span className="grid size-7 place-items-center rounded-lg bg-primary text-sm font-bold text-primary-foreground">
        M
      </span>
      Momentum
    </span>
  )
}

function MobileTopBar() {
  return (
    <header className="sticky top-0 z-20 border-b bg-background/85 pt-[env(safe-area-inset-top)] backdrop-blur-md md:hidden">
      <div className="flex h-14 items-center justify-between px-4">
        <Wordmark />
        <ApiStatus compact />
      </div>
    </header>
  )
}

function MobileTabBar() {
  return (
    <nav
      aria-label="Main"
      className="fixed inset-x-0 bottom-0 z-30 border-t bg-background/90 pb-[env(safe-area-inset-bottom)] backdrop-blur-md md:hidden"
    >
      <ul className="mx-auto grid max-w-md grid-cols-4">
        {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
          <li key={to}>
            <NavLink
              to={to}
              end={end}
              className={({ isActive }) =>
                cn(
                  'group flex min-h-16 flex-col items-center justify-center gap-1 text-[11px] font-medium transition-colors',
                  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-inset',
                  isActive ? 'text-foreground' : 'text-muted-foreground',
                )
              }
            >
              {({ isActive }) => (
                <>
                  <span
                    className={cn(
                      'flex h-8 w-14 items-center justify-center rounded-full transition-colors',
                      isActive ? 'bg-secondary' : 'group-active:bg-secondary/60',
                    )}
                  >
                    <Icon className="size-5" strokeWidth={isActive ? 2.4 : 2} aria-hidden />
                  </span>
                  {label}
                </>
              )}
            </NavLink>
          </li>
        ))}
      </ul>
    </nav>
  )
}

function DesktopSidebar() {
  return (
    <aside className="sticky top-0 hidden h-svh w-60 shrink-0 flex-col border-r px-3 py-5 md:flex">
      <div className="px-3 pb-6">
        <Wordmark />
      </div>

      <nav aria-label="Main" className="flex-1">
        <ul className="space-y-1">
          {NAV_ITEMS.map(({ to, label, icon: Icon, end }) => (
            <li key={to}>
              <NavLink
                to={to}
                end={end}
                className={({ isActive }) =>
                  cn(
                    'flex items-center gap-3 rounded-lg px-3 py-2 text-sm transition-colors',
                    'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
                    isActive
                      ? 'bg-secondary font-medium text-secondary-foreground'
                      : 'text-muted-foreground hover:bg-secondary/60 hover:text-foreground',
                  )
                }
              >
                <Icon className="size-[18px]" aria-hidden />
                {label}
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      <div className="px-3">
        <ApiStatus />
      </div>
    </aside>
  )
}
