import { ChartLine, ListChecks, Play, Target, type LucideIcon } from 'lucide-react'

export type NavItem = { to: string; label: string; icon: LucideIcon; end?: boolean }

/** Main destinations, shared by the mobile tab bar and the desktop sidebar. */
export const NAV_ITEMS: NavItem[] = [
  { to: '/', label: 'Now', icon: Play, end: true },
  { to: '/today', label: 'Today', icon: ListChecks },
  { to: '/goals', label: 'Goals', icon: Target },
  { to: '/progress', label: 'Progress', icon: ChartLine },
]
