import { useQuery } from '@tanstack/react-query'

import { api } from '@/lib/api'
import type { Plan } from '@/lib/types'

/** Query keys in one place, so invalidation after a mutation can't miss one. */
export const keys = {
  todayPlan: ['plans', 'today'] as const,
}

export function useTodayPlan() {
  return useQuery({ queryKey: keys.todayPlan, queryFn: () => api<Plan>('/api/plans/today') })
}
