import type { LucideIcon } from 'lucide-react'
import { CloudOff, RotateCw } from 'lucide-react'
import type { ReactNode } from 'react'

import { Button } from '@/components/ui/button'
import { errorMessage } from '@/lib/errors'
import { cn } from '@/lib/utils'

type EmptyStateProps = {
  icon?: LucideIcon
  title: string
  description?: ReactNode
  /** Usually one Button: the single next step */
  action?: ReactNode
  className?: string
}

/** Shown when there's nothing here yet. Always says what to do next. */
export function EmptyState({ icon: Icon, title, description, action, className }: EmptyStateProps) {
  return (
    <div
      className={cn(
        'flex flex-col items-center rounded-xl border border-dashed px-6 py-12 text-center',
        className,
      )}
    >
      {Icon && (
        <span className="mb-4 grid size-12 place-items-center rounded-full bg-secondary">
          <Icon className="size-6 text-muted-foreground" aria-hidden />
        </span>
      )}
      <h2 className="text-base font-semibold">{title}</h2>
      {description && (
        <p className="mt-1 max-w-sm text-sm text-muted-foreground">{description}</p>
      )}
      {action && <div className="mt-6 w-full sm:w-auto">{action}</div>}
    </div>
  )
}

type ErrorStateProps = {
  error: unknown
  onRetry?: () => void
  retrying?: boolean
  className?: string
}

/** Shown when loading failed. Plain language plus a retry, never a stack trace. */
export function ErrorState({ error, onRetry, retrying = false, className }: ErrorStateProps) {
  return (
    <div
      role="alert"
      className={cn('flex flex-col items-center rounded-xl border px-6 py-12 text-center', className)}
    >
      <span className="mb-4 grid size-12 place-items-center rounded-full bg-secondary">
        <CloudOff className="size-6 text-muted-foreground" aria-hidden />
      </span>
      <h2 className="text-base font-semibold">Couldn’t load this</h2>
      <p className="mt-1 max-w-sm text-sm text-muted-foreground">{errorMessage(error)}</p>
      {onRetry && (
        <Button
          variant="outline"
          className="mt-6 h-11 w-full sm:w-auto"
          onClick={onRetry}
          disabled={retrying}
        >
          <RotateCw className={cn(retrying && 'animate-spin')} aria-hidden />
          {retrying ? 'Trying again…' : 'Try again'}
        </Button>
      )}
    </div>
  )
}
