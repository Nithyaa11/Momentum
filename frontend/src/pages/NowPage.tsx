import { Play } from 'lucide-react'

import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

/** Placeholder. The real "Do this now" screen is built on Dec 6. */
export function NowPage() {
  return (
    <div className="space-y-6">
      <p className="text-sm text-muted-foreground">Do this now</p>
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">SQL JOIN practice</CardTitle>
          <CardDescription>40 minutes · Learn SQL</CardDescription>
        </CardHeader>
        <CardContent>
          <Button size="lg" className="w-full sm:w-auto">
            <Play aria-hidden /> Start
          </Button>
        </CardContent>
      </Card>
    </div>
  )
}
