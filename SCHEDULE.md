# Momentum: Daily Schedule

**30–60 minutes a day · V1 done by Sun, Jan 11, 2027**

## How each day works

1. Open this file and find today's row.
2. Ask Claude to build that day's task. Claude writes the code.
3. **You** review it, run it, try it in the browser, and steer: "this feels slow", "move this button", and so on.
4. Commit and push when "Done when" is met.

If a day runs over, finish it the next day and use a buffer day (🧩) to catch up. Don't skip ahead.

## Milestones

| Milestone | Date |
| --- | --- |
| Backend + frontend running | Fri, Dec 4 |
| Core loop works in the UI (plan → do → check in) | Fri, Dec 11 |
| AI planning live; **you start using Momentum daily** | Fri, Dec 18 |
| Behavior model + replanning (the differentiator) | Thu, Dec 24 |
| Wins and progress page | Wed, Dec 30 |
| **V1 released: `v1.0.0`, with 3 weeks of your own usage data** | **Mon, Jan 11, 2027** |

---

## Week 1 (Nov 28 – Dec 4): Foundation

| Date | Task | Done when |
| --- | --- | --- |
| Sat Nov 28 | Backend skeleton: FastAPI, config, `/health`; PostgreSQL in Docker | `/health` responds, DB container runs |
| Sun Nov 29 | SQLAlchemy + Alembic; all V1 models; first migration | `alembic upgrade head` creates all tables |
| Mon Nov 30 | Pydantic schemas; goals and tasks CRUD; Pytest setup | Tests green |
| Tue Dec 1 | Plans, plan items and check-in endpoints | Tests green; can check in via `/docs` |
| Wed Dec 2 | Frontend skeleton: Vite, React, TypeScript, Tailwind, shadcn/ui, React Router, TanStack Query | Styled page with routes |
| Thu Dec 3 | Full `docker-compose.yml` + dev seed script + "Getting started" section in the README | `docker compose up` runs everything |
| Fri Dec 4 | 🧩 Buffer: run everything fresh and fix rough edges | Clean start from scratch works |

## Week 2 (Dec 5 – Dec 11): Design system and core screens

| Date | Task | Done when |
| --- | --- | --- |
| Sat Dec 5 | Design tokens (light and dark) + app shell: sidebar on desktop, bottom tabs on mobile | Looks right at 375px and 1440px |
| Sun Dec 6 | Shared states: skeletons, empty states, error states, toasts | Used on every page |
| Mon Dec 7 | **Onboarding:** goals, available hours per weekday, best time of day | Completes in under 2 minutes |
| Tue Dec 8 | **Goals page:** add, edit, archive | Fully working |
| Wed Dec 9 | **Today page** + **Now page** ("Do this now" card with a timer) | Fully working |
| Thu Dec 10 | **Check-in sheet:** Done / Partial / Can't do it, reason chips, time; optimistic update + Undo | Check-in takes under 5 seconds |
| Fri Dec 11 | ✅ Run a full day manually; fix the 3 worst UX issues | Loop works end to end |

## Week 3 (Dec 12 – Dec 18): AI agent

| Date | Task | Done when |
| --- | --- | --- |
| Sat Dec 12 | LLM client: provider wrapper, cheap/strong model routing, token and cost logging | Test call logs usage |
| Sun Dec 13 | Agent tools + tool-calling loop (max steps) + mocked-LLM tests | Tests green |
| Mon Dec 14 | **Goal breakdown:** goal → tasks with estimates; preview and edit before saving | Works in the UI |
| Tue Dec 15 | `propose_plan`: fits available hours (enforced in code) + one-line reason per item | Never over-books |
| Wed Dec 16 | **Plan review UI:** Accept / Edit / Regenerate; store the user's edits | Fully working |
| Thu Dec 17 | Fallback: if the LLM fails, build a simple rule-based plan | App never breaks |
| Fri Dec 18 | ✅ Deploy a personal instance (Render or Railway) → **start using Momentum daily** | Works on your phone |

## Week 4 (Dec 19 – Dec 25): Behavior model and replanning

| Date | Task | Done when |
| --- | --- | --- |
| Sat Dec 19 | Stats: estimate ratio per category; completion rate by time block and weekday | Unit tests |
| Sun Dec 20 | Long-session drop-off, top skip reasons; `compute_profile` + nightly job | Snapshot written each night |
| Mon Dec 21 | Behavior summary fed into the planner; **"Why this plan?"** UI | Plan changes when behavior changes |
| Tue Dec 22 | `replan_day`: shrink / move / split / drop missed tasks, with a reason | Tests for each case |
| Wed Dec 23 | Calm "Here's a lighter plan" sheet; "Still important?" prompt after 3 skips; **Fresh start** button | Fully working |
| Thu Dec 24 | ✅ End-of-day check-in reminder (browser notification) | You receive it |
| Fri Dec 25 | 🎄 Rest | n/a |

## Week 5 (Dec 26 – Jan 1): Wins and progress

| Date | Task | Done when |
| --- | --- | --- |
| Sat Dec 26 | Wins: automatic (sessions, streaks, milestones) + "log a win" | Fully working |
| Sun Dec 27 | Progress API: plan completion rate, estimate accuracy, streaks | Tests green |
| Mon Dec 28 | **Progress page:** completion-rate trend (headline) + estimate accuracy chart | Fully working |
| Tue Dec 29 | Streaks per goal, wins list, weekly summary card | Fully working |
| Wed Dec 30 | ✅ Subtle completion and streak celebrations | Feels rewarding, not noisy |
| Thu Dec 31 | 🧩 Buffer / catch-up | n/a |
| Fri Jan 1 | 🎆 Rest | n/a |

## Week 6 (Jan 2 – Jan 11): Polish and release

| Date | Task | Done when |
| --- | --- | --- |
| Sat Jan 2 | Review your own 2 weeks of data; tune prompts and replan rules | Notes in `docs/log.md` |
| Sun Jan 3 | Mobile UX pass across every screen: spacing, copy, tap targets | Checklist done |
| Mon Jan 4 | Accessibility: keyboard navigation, focus, contrast, labels | Lighthouse a11y ≥ 95 |
| Tue Jan 5 | PWA (installable) + performance pass | Installs on phone; Lighthouse perf ≥ 90 |
| Wed Jan 6 | 🧩 Fix bugs found during your own use | Bug list cleared |
| Thu Jan 7 | Demo seed script (2 weeks of realistic history) | Demo tells the story in 2 minutes |
| Fri Jan 8 | README: screenshots, a GIF of the core loop, final "Getting started" | Repo looks professional |
| Sat Jan 9 | Ask 2 friends to try onboarding and a check-in without help | Feedback noted |
| Sun Jan 10 | Fix the friends' top issues | Committed |
| **Mon Jan 11** | 🚀 Tag **`v1.0.0`**; write `docs/v1-results.md` with your own week-1 vs. week-3 completion rate | **V1 released** |

---

## What was cut to fit Jan 11 (it comes back later)

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
| Jan 12 – Jan 25 | **V1.1:** simple accounts + 5–10 test users; fix what they hit |
| Jan 26 – Feb 22 | **V2a:** learning companion (resources, explanations, practice questions) |
| Feb 23 – Mar 8 | **V2b:** Google Calendar sync + rewards |
| Mar 9 – Mar 21 | **V2c:** deeper insights, voice check-ins; tag `v2.0.0` |
| Later, optional | **V3:** proactive nudges, site-blocking extension, mobile app. Only if V1/V2 prove the idea |
