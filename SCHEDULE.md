# Momentum: Daily Schedule

**30–60 minutes a day · weeks run Monday → Sunday · V1 release: Fri, Jan 8, 2027** (original target Jan 11; we're ahead)

## How each day works

1. Open this file and find today's row.
2. Ask Claude to build that day's task. Claude writes the code.
3. **You** review it, run it, try it in the browser, and steer: "this feels slow", "move this button", and so on.
4. Commit and push when "Done when" is met.

If a day runs over, finish it the next day and use a buffer day (🧩) to catch up. If you finish early, move on to the next row and **re-date the rest of the schedule from the actual date**.

## Milestones

| Milestone | Date | Status |
| --- | --- | --- |
| Backend core: goals, tasks, plans, check-ins | Sat, Nov 28 | ✅ Done |
| Frontend skeleton running | Sat, Nov 28 | ✅ Done |
| Core loop works in the UI (plan → do → check in) | Tue, Dec 8 | |
| AI planning live; **you start using Momentum daily** | Tue, Dec 15 | |
| Behavior model + replanning (the differentiator) | Mon, Dec 21 | |
| Wins and progress page | Sun, Dec 27 | |
| **V1 released: `v1.0.0`, with about 3.5 weeks of your own usage data** | **Fri, Jan 8, 2027** | |
| Spare days before the original Jan 11 target | Sat, Jan 9 – Mon, Jan 11 | |

---

## Week 1 (Mon Nov 23 – Sun Nov 29): Project start and backend core

| Date | Task | Status |
| --- | --- | --- |
| Fri Nov 27 | Product docs: README, plan, schedule | ✅ Done |
| Fri Nov 27 | Backend skeleton: FastAPI, config, `/health`; PostgreSQL in Docker | ✅ Done |
| Fri Nov 27 | SQLAlchemy + Alembic; all V1 models; first migration | ✅ Done |
| Fri Nov 27 | Pydantic schemas; goals and tasks API; Postgres-backed tests | ✅ Done |
| Sat Nov 28 | Plans and check-in API (done / partial / skipped, undo) | ✅ Done |
| Sat Nov 28 | Frontend skeleton: Vite, React, TypeScript, Tailwind, shadcn/ui, React Router, TanStack Query. **Week 1 review** (`docs/log.md`) | ✅ Done (a day early) |
| Sat Nov 28 | App shell: sidebar on desktop, bottom tabs with labels on mobile (pulled forward) | ✅ Done |
| Sat Nov 28 | Frontend in `docker-compose.yml` + dev seed script + "Getting started" in the README (pulled forward) | ✅ Done |
| Sat Nov 28 | 🧩 Buffer: clean start from a fresh clone + seed; API key passed to the backend container (pulled forward) | ✅ Done |
| Sun Nov 29 | Free day: week closes | n/a |

## Week 2 (Mon Nov 30 – Sun Dec 6): Shared states, onboarding, first screens

| Date | Task | Done when |
| --- | --- | --- |
| Mon Nov 30 | Shared states: skeletons, empty states, error states, toasts | Used on every page |
| Tue Dec 1 | Profile API (`/api/me`) + **onboarding:** goals, available hours per weekday, best time of day | Completes in under 2 minutes |
| Wed Dec 2 | **Goals page:** add, edit, archive | Fully working |
| Thu Dec 3 | **Today page:** the day's plan, accept it, see what's checked in | Fully working |
| Fri Dec 4 | **Now page:** "Do this now" card with a timer | Fully working |
| Sat Dec 5 | 🧩 Buffer | Rough edges fixed |
| Sun Dec 6 | **Week 2 review** | Notes in `docs/log.md` |

The theme stays black and white (shadcn neutral) until you pick your own colors.

## Week 3 (Mon Dec 7 – Sun Dec 13): Core loop in the UI, then the AI agent

| Date | Task | Done when |
| --- | --- | --- |
| Mon Dec 7 | **Check-in sheet:** Done / Partial / Can't do it, reason chips, time; optimistic update + Undo | Check-in takes under 5 seconds |
| Tue Dec 8 | ✅ Run a full day manually; fix the 3 worst UX issues | Loop works end to end |
| Wed Dec 9 | LLM client: provider wrapper, cheap/strong model routing, token and cost logging | Test call logs usage |
| Thu Dec 10 | Agent tools + tool-calling loop (max steps) + mocked-LLM tests | Tests green |
| Fri Dec 11 | **Goal breakdown:** goal → tasks with estimates; preview and edit before saving | Works in the UI |
| Sat Dec 12 | `propose_plan`: fits available hours (enforced in code) + one-line reason per item | Never over-books |
| Sun Dec 13 | **Plan review UI:** Accept / Edit / Regenerate; store the user's edits. Week review | Fully working |

## Week 4 (Mon Dec 14 – Sun Dec 20): Start using it, then the behavior model

| Date | Task | Done when |
| --- | --- | --- |
| Mon Dec 14 | Fallback: if the LLM fails, build a simple rule-based plan | App never breaks |
| Tue Dec 15 | ✅ Deploy a personal instance (Render or Railway) → **start using Momentum daily** | Works on your phone |
| Wed Dec 16 | Stats: estimate ratio per category; completion rate by time of day and weekday | Unit tests |
| Thu Dec 17 | Long-session drop-off, skip reasons; `compute_profile` + nightly job | Snapshot written each night |
| Fri Dec 18 | Behavior summary fed into the planner; **"Why this plan?"** UI | Plan changes when behavior changes |
| Sat Dec 19 | `replan_day`: shrink / move / split / drop missed tasks, with a reason | Tests for each case |
| Sun Dec 20 | "Here's a lighter plan" sheet; "Still important?" after 3 skips; **Fresh start** button. Week review | Fully working |

## Week 5 (Mon Dec 21 – Sun Dec 27): Wins and progress

| Date | Task | Done when |
| --- | --- | --- |
| Mon Dec 21 | ✅ End-of-day check-in reminder (browser notification) | You receive it |
| Tue Dec 22 | Wins: automatic (sessions, streaks, milestones) + "log a win" | Fully working |
| Wed Dec 23 | Progress API: plan completion rate, estimate accuracy, streaks | Tests green |
| Thu Dec 24 | **Progress page:** completion-rate trend (headline) + estimate accuracy chart | Fully working |
| Fri Dec 25 | 🎄 Rest | n/a |
| Sat Dec 26 | Streaks per goal, wins list, weekly summary card | Fully working |
| Sun Dec 27 | ✅ Subtle completion and streak celebrations. Week review | Feels rewarding, not noisy |

## Week 6 (Mon Dec 28 – Sun Jan 3): Tune and polish

| Date | Task | Done when |
| --- | --- | --- |
| Mon Dec 28 | 🧩 Buffer / catch-up | n/a |
| Tue Dec 29 | Review your own 2 weeks of data; tune prompts and replan rules | Notes in `docs/log.md` |
| Wed Dec 30 | Mobile UX pass across every screen: spacing, copy, tap targets | Checklist done |
| Thu Dec 31 | Accessibility: keyboard navigation, focus, contrast, labels | Lighthouse a11y ≥ 95 |
| Fri Jan 1 | 🎆 Rest | n/a |
| Sat Jan 2 | PWA (installable) + performance pass | Installs on phone; Lighthouse perf ≥ 90 |
| Sun Jan 3 | 🧩 Fix bugs found during your own use. Week review | Bug list cleared |

## Week 7 (Mon Jan 4 – Sun Jan 10): Release

| Date | Task | Done when |
| --- | --- | --- |
| Mon Jan 4 | Demo seed script (2 weeks of realistic history) | Demo tells the story in 2 minutes |
| Tue Jan 5 | README: screenshots, a GIF of the core loop, final "Getting started" | Repo looks professional |
| Wed Jan 6 | Ask 2 friends to try onboarding and a check-in without help | Feedback noted |
| Thu Jan 7 | Fix the friends' top issues | Committed |
| **Fri Jan 8** | 🚀 Tag **`v1.0.0`**; write `docs/v1-results.md` with your own week-1 vs. week-3 completion rate | **V1 released** |
| Sat Jan 9 – Sun Jan 10 | 🧩 Spare | n/a |

---

## What was cut to fit (it comes back later)

| Cut or simplified | Why it's OK |
| --- | --- |
| Drag-to-reorder on Today | Up/down buttons are enough for V1 |
| Email reminders | Browser notifications only |
| LLM-written weekly recap | The stats card carries the message |
| Multi-user accounts | Single-user mode for V1 |
| External test users | Moved to right after V1 (below) |

---

## After V1, at the same 30–60 min/day

| Dates | What |
| --- | --- |
| Jan 11 – Jan 24 | **V1.1:** simple accounts + 5–10 test users; fix what they hit |
| Jan 25 – Feb 21 | **V2a:** learning companion (resources, explanations, practice questions) |
| Feb 22 – Mar 7 | **V2b:** Google Calendar sync + rewards |
| Mar 8 – Mar 21 | **V2c:** deeper insights, voice check-ins; tag `v2.0.0` |
| Later, optional | **V3:** proactive nudges, site-blocking extension, mobile app. Only if V1/V2 prove the idea |
