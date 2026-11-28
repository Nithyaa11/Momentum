import { Compass } from 'lucide-react'
import { Link } from 'react-router'

import { PageHeader } from '@/components/PageHeader'
import { EmptyState } from '@/components/states'
import { Button } from '@/components/ui/button'

export function NotFoundPage() {
  return (
    <>
      <PageHeader title="Page not found" />
      <EmptyState
        icon={Compass}
        title="There’s nothing at this address"
        description="The link may be old or mistyped."
        action={
          <Button asChild className="h-11 w-full sm:w-auto">
            <Link to="/">Go to Now</Link>
          </Button>
        }
      />
    </>
  )
}
