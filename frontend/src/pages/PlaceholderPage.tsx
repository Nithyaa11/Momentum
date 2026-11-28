import { Hammer } from 'lucide-react'

import { PageHeader } from '@/components/PageHeader'
import { EmptyState } from '@/components/states'

type Props = { title: string; comingOn: string }

/** Stand-in for screens that aren't built yet. */
export function PlaceholderPage({ title, comingOn }: Props) {
  return (
    <>
      <PageHeader title={title} />
      <EmptyState icon={Hammer} title="Not built yet" description={`Coming on ${comingOn}.`} />
    </>
  )
}
