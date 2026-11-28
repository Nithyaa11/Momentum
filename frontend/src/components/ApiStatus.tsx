import { useQuery } from '@tanstack/react-query'

import { api, type Health } from '@/lib/api'
import { cn } from '@/lib/utils'

/** Dot showing whether the backend and database are reachable.
 *  `compact` hides the text (used in the mobile top bar), keeping it for screen readers. */
export function ApiStatus({ compact = false }: { compact?: boolean }) {
  const { data, isPending, isError } = useQuery({
    queryKey: ['health'],
    queryFn: () => api<Health>('/health'),
    refetchInterval: 30_000,
    retry: false,
  })

  const ok = data?.status === 'ok'
  const label = isPending ? 'Connecting…' : ok ? 'API connected' : 'API unavailable'

  return (
    <div
      className="flex items-center gap-2 text-xs text-muted-foreground"
      role="status"
      title={label}
    >
      <span
        className={cn(
          'size-2 rounded-full',
          isPending && 'bg-muted-foreground/40',
          ok && 'bg-success',
          (isError || (data && !ok)) && 'bg-destructive',
        )}
        aria-hidden
      />
      <span className={cn(compact && 'sr-only')}>{label}</span>
    </div>
  )
}
