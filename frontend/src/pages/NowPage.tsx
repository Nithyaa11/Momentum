import { CalendarPlus, Clock, ListChecks, Play, Sparkles } from 'lucide-react'
import { Link } from 'react-router'

import { PageHeader } from '@/components/PageHeader'
import { EmptyState, ErrorState } from '@/components/states'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Skeleton } from '@/components/ui/skeleton'
import { isNotFound } from '@/lib/errors'
import { notify } from '@/lib/notify'
import { useTodayPlan } from '@/lib/queries'
import type { Plan, PlanItem } from '@/lib/types'

/** "Do this now": the single next thing from today's plan. The timer arrives on Dec 3. */
export function NowPage() {
  return (
    <>
      <PageHeader title="Do this now" subtitle="One thing. Then the next." />
      <NowContent />
    </>
  )
}

function NowContent() {
  const { data: plan, error, isPending, refetch, isRefetching } = useTodayPlan()

  if (isPending) return <NowSkeleton />

  if (isNotFound(error)) {
    return (
      <EmptyState
        icon={CalendarPlus}
        title="No plan for today yet"
        description="Add a goal and Momentum will suggest a realistic plan for your day."
        action={<LinkButton to="/goals">Add a goal</LinkButton>}
      />
    )
  }

  if (error) return <ErrorState error={error} onRetry={() => refetch()} retrying={isRefetching} />

  if (plan.status === 'proposed') {
    return (
      <EmptyState
        icon={ListChecks}
        title="Your plan is ready to review"
        description="Have a look, change anything you like, then accept it."
        action={<LinkButton to="/today">Review today’s plan</LinkButton>}
      />
    )
  }

  const next = plan.items.find((item) => item.completion === null)
  if (!next) {
    return (
      <EmptyState
        icon={Sparkles}
        title={plan.items.length ? 'That’s everything for today' : 'Nothing planned today'}
        description={plan.items.length ? 'Nice work. Rest counts too.' : 'Enjoy the free time.'}
        action={<LinkButton to="/today" variant="outline">See today</LinkButton>}
      />
    )
  }

  return <NextUpCard item={next} plan={plan} />
}

function NextUpCard({ item, plan }: { item: PlanItem; plan: Plan }) {
  const done = plan.items.filter((i) => i.completion !== null).length

  return (
    <Card className="gap-6">
      <CardHeader className="space-y-2">
        <CardDescription className="flex justify-between text-xs font-medium tracking-wide uppercase">
          <span>{item.task.category}</span>
          <span>
            {done + 1} of {plan.items.length}
          </span>
        </CardDescription>
        <CardTitle className="text-2xl leading-tight md:text-3xl">{item.task.title}</CardTitle>
        <p className="flex items-center gap-1.5 text-sm text-muted-foreground">
          <Clock className="size-4" aria-hidden />
          {item.planned_minutes} minutes
          {item.scheduled_start && <> · from {item.scheduled_start.slice(0, 5)}</>}
        </p>
        {item.reason && <p className="text-sm">{item.reason}</p>}
      </CardHeader>
      <CardContent>
        {/* Full width on phones: the main action should be easy to hit with a thumb */}
        <Button
          size="lg"
          className="h-12 w-full text-base sm:w-auto sm:px-8"
          onClick={() => notify.success('The focus timer arrives on Dec 3.')}
        >
          <Play aria-hidden /> Start
        </Button>
      </CardContent>
    </Card>
  )
}

/** Same shape as the real card, so nothing jumps when data arrives. */
function NowSkeleton() {
  return (
    <Card className="gap-6" aria-busy="true" aria-label="Loading your next task">
      <CardHeader className="space-y-3">
        <Skeleton className="h-3 w-24" />
        <Skeleton className="h-8 w-3/4" />
        <Skeleton className="h-4 w-32" />
      </CardHeader>
      <CardContent>
        <Skeleton className="h-12 w-full sm:w-36" />
      </CardContent>
    </Card>
  )
}

function LinkButton({
  to,
  children,
  variant = 'default',
}: {
  to: string
  children: React.ReactNode
  variant?: 'default' | 'outline'
}) {
  return (
    <Button asChild variant={variant} className="h-11 w-full sm:w-auto">
      <Link to={to}>{children}</Link>
    </Button>
  )
}
