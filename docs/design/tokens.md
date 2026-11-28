# Design tokens

Source of truth: [`frontend/src/index.css`](../../frontend/src/index.css). Use the Tailwind class names below, and never raw colors like `bg-purple-500`, so light and dark mode stay consistent.

## Palette: lavender + plum, with mint / peach / rose accents

| Token | Tailwind classes | Light | Dark | Use for |
| --- | --- | --- | --- | --- |
| background | `bg-background` | soft lavender mist | deep aubergine | Page background |
| foreground | `text-foreground` | deep plum ink | near-white lavender | Body text |
| card | `bg-card` | white | dark plum | Cards, sheets |
| primary | `bg-primary` `text-primary` | lavender-violet | light lavender | Main action, active tab, logo |
| secondary | `bg-secondary` `text-secondary-foreground` | pale lavender | muted plum | Pills, chips, active nav background |
| muted | `bg-muted` `text-muted-foreground` | faint lavender / grey-plum | | Secondary text, placeholders |
| success | `text-success` `bg-success-soft` | mint | mint | Wins, "done", streaks |
| warning | `text-warning` `bg-warning-soft` | peach | peach | Gentle nudges (never guilt) |
| destructive | `text-destructive` | rose | rose | Errors, delete |
| chart-1…5 | `fill-chart-1` etc. | lavender, mint, peach, rose, periwinkle | | Progress charts |

## Rules

- **Contrast:** every text/background pair above meets **WCAG AA (≥ 4.5:1)** in both modes.
- **Missed tasks use warning (peach), not destructive (rose).** Rose is only for real errors. This follows the "no guilt" UX principle.
- **Dark mode** follows the device setting automatically (`src/lib/theme.ts`).
- **Radius:** `--radius` = 0.75rem; cards use `rounded-xl`.
