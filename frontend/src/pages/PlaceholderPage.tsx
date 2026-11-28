import { PageHeader } from '@/components/PageHeader'

type Props = { title: string; comingOn: string }

/** Stand-in for screens that aren't built yet. */
export function PlaceholderPage({ title, comingOn }: Props) {
  return (
    <>
      <PageHeader title={title} />
      <div className="rounded-xl border border-dashed p-8 text-center text-sm text-muted-foreground">
        Coming on {comingOn}.
      </div>
    </>
  )
}
