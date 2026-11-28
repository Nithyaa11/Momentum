import { Clock, Play } from 'lucide-react'

import { PageHeader } from '@/components/PageHeader'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

/** Placeholder data. The real "Do this now" screen is built on Dec 6. */
export function NowPage() {
  return (
    <>
      <PageHeader title="Do this now" subtitle="One thing. Then the next." />

      <Card className="gap-6">
        <CardHeader className="space-y-2">
          <CardDescription className="text-xs font-medium tracking-wide uppercase">
            Learn SQL
          </CardDescription>
          <CardTitle className="text-2xl leading-tight md:text-3xl">SQL JOIN practice</CardTitle>
          <p className="flex items-center gap-1.5 text-sm text-muted-foreground">
            <Clock className="size-4" aria-hidden /> 40 minutes
          </p>
        </CardHeader>
        <CardContent>
          {/* Full width on phones: the main action should be easy to hit with a thumb */}
          <Button size="lg" className="h-12 w-full text-base sm:w-auto sm:px-8">
            <Play aria-hidden /> Start
          </Button>
        </CardContent>
      </Card>
    </>
  )
}
