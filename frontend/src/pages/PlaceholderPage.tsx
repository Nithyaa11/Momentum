type Props = { title: string; comingOn: string }

/** Stand-in for screens that aren't built yet. */
export function PlaceholderPage({ title, comingOn }: Props) {
  return (
    <div className="space-y-2">
      <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
      <p className="text-muted-foreground">Coming on {comingOn}.</p>
    </div>
  )
}
