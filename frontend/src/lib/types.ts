/** Shapes returned by the API. Mirror backend/app/schemas. */

export type Outcome = 'done' | 'partial' | 'skipped'
export type SkipReason = 'too_tired' | 'out_of_time' | 'forgot' | 'not_important' | 'other'

export type TaskSummary = { id: number; goal_id: number | null; title: string; category: string }

export type Completion = {
  outcome: Outcome
  actual_minutes: number
  skip_reason: SkipReason | null
  note: string | null
  completed_at: string
}

export type PlanItem = {
  id: number
  position: number
  scheduled_start: string | null // "HH:MM:SS"
  planned_minutes: number
  reason: string | null
  task: TaskSummary
  completion: Completion | null
}

export type Plan = {
  id: number
  date: string // "YYYY-MM-DD"
  status: 'proposed' | 'accepted'
  rationale: string | null
  items: PlanItem[]
}
