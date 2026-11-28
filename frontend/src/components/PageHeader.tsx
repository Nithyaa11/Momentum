type Props = { title: string; subtitle?: string }

/** Consistent page title block for every screen. */
export function PageHeader({ title, subtitle }: Props) {
  return (
    <header className="mb-6 space-y-1">
      <h1 className="text-2xl font-semibold tracking-tight md:text-3xl">{title}</h1>
      {subtitle && <p className="text-sm text-muted-foreground">{subtitle}</p>}
    </header>
  )
}
