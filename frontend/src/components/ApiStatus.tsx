import { useQuery } from '@tanstack/react-query'

import { api, type Health } from '@/lib/api'
import { cn } from '@/lib/utils'

/** Tiny dot showing whether the backend and database are reachable. */
export function ApiStatus() {
  const { data, isPending, isError } = useQuery({
    queryKey: ['health'],
    queryFn: () => api<Health>('/health'),
    refetchInterval: 30_000,
    retry: false,
  })

  const ok = data?.status === 'ok'
  const label = isPending ? 'Connecting…' : ok ? 'API connected' : 'API unavailable'

  return (
    <div className="flex items-center gap-2 text-xs text-muted-foreground" role="status">
      <span
        className={cn(
          'size-2 rounded-full',
          isPending && 'bg-muted-foreground/40',
          ok && 'bg-emerald-500',
          (isError || (data && !ok)) && 'bg-red-500',
        )}
      />
      {label}
    </div>
  )
}
