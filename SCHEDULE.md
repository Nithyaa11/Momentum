# Momentum: Daily Schedule

One small, finished piece of work **every day**, about **1–2 hours** on weekdays. **Sundays are lighter:** review the week, record a short demo for yourself, and plan the next week.

Each day ends with a **commit**. If a day slips, use the next buffer day; don't skip ahead.

| Milestone | Target date |
| --- | --- |
| Project kickoff | Sat, Nov 28, 2026 |
| Core loop works in the UI (no AI) | Sun, Dec 27, 2026 |
| AI planning works and daily self-use begins | Sun, Jan 10, 2027 |
| Behavior model live (the differentiator) | Sun, Jan 17, 2027 |
| **V1 feature-complete and polished** | **Sun, Feb 7, 2027** |
| Self-use (dogfooding) done | Sun, Feb 28, 2027 |
| **V1 validated with test users** | **Sun, Mar 14, 2027** |
| V2 complete | Mon, May 31, 2027 |
| V3 complete | Tue, Aug 31, 2027 |

---

## Kickoff weekend

| Date | Task | Done when |
| --- | --- | --- |
| Sat Nov 28 | Create the GitHub repo, push docs, set up a project board from this schedule | Repo is live and the board has Week 1 cards |
| Sun Nov 29 | **UX research:** try Motion/Sunsama/Todoist for 30 min each; note 5 things you like and 5 you don't. Sketch the 5 screens on paper (Now, Today, Goals, Check-in, Progress) | Sketches photographed into `docs/design/` |

---

## Week 1 (Nov 30 – Dec 6): Project setup

| Date | Task | Done when |
| --- | --- | --- |
| Mon Nov 30 | Backend skeleton: FastAPI, `pyproject.toml`, `/health`, config from `.env` | `uvicorn` serves `/health` |
| Tue Dec 1 | PostgreSQL in Docker Compose, SQLAlchemy engine and session, Alembic init | `alembic upgrade head` runs |
| Wed Dec 2 | Pytest with a test database, plus one smoke test | `pytest` is green |
| Thu Dec 3 | Frontend skeleton: Vite + React + TypeScript + Tailwind | Dev server shows a styled page |
| Fri Dec 4 | Install shadcn/ui, lucide icons, TanStack Query, React Router; app shell with nav | Empty pages route correctly |
| Sat Dec 5 | Full `docker-compose.yml` (db, backend, frontend); README "Getting started" section | `docker compose up` runs everything |
| Sun Dec 6 | 🔁 Review week, plan Week 2 | Notes in `docs/log.md` |

## Week 2 (Dec 7 – Dec 13): Data model and API

| Date | Task | Done when |
| --- | --- | --- |
| Mon Dec 7 | Models: `users`, `goals`, `tasks` and the first migration | Tables exist |
| Tue Dec 8 | Models: `plans`, `plan_items`, `completions`, `wins`, `behavior_snapshots` | Migration applied |
| Wed Dec 9 | Pydantic schemas plus goal endpoints (CRUD) | Tests pass for goals |
| Thu Dec 10 | Task endpoints (CRUD) | Tests pass for tasks |
| Fri Dec 11 | Plan endpoints: get a day plan, add items, accept | Tests pass |
| Sat Dec 12 | Check-in endpoint: outcome, actual minutes, skip reason | You can check in through the API docs at `/docs` |
| Sun Dec 13 | 🔁 Review, plus a seed script with one user and sample goals | `scripts/seed_dev.py` runs |

## Week 3 (Dec 14 – Dec 20): Design system and UI foundation

This week is about making the app **feel good** before adding features.

| Date | Task | Done when |
| --- | --- | --- |
| Mon Dec 14 | Design tokens: colors (light and dark), type scale, spacing, radius in Tailwind config | `docs/design/tokens.md` |
| Tue Dec 15 | Core components: Button, Card, Chip, Input, Sheet/Dialog, Toast | Component preview page |
| Wed Dec 16 | Responsive layout: sidebar on desktop, bottom tab bar on mobile | Works at 375px and 1440px |
| Thu Dec 17 | Loading skeletons, empty states, error states (shared components) | Each has a preview |
| Fri Dec 18 | Onboarding flow, step 1: name, timezone, goals in free text | Saves to the API |
| Sat Dec 19 | Onboarding, step 2: available hours per weekday, best time of day (visual picker) | Saves to the API |
| Sun Dec 20 | 🔁 Review: try onboarding on your phone and fix the 3 worst issues | Committed |

## Week 4 (Dec 21 – Dec 27): Core screens, the loop without AI

| Date | Task | Done when |
| --- | --- | --- |
| Mon Dec 21 | **Goals page:** list, add, edit, archive | Fully working |
| Tue Dec 22 | **Today page:** today's plan with statuses, reorder by drag | Fully working |
| Wed Dec 23 | **Now page:** one large "Do this now" card with Start and a timer | Fully working |
| Thu Dec 24 | **Check-in sheet:** Done / Partial / Can't do it, reason chips, actual-time picker | Check-in takes under 5 seconds |
| Fri Dec 25 | 🎄 Buffer / rest | n/a |
| Sat Dec 26 | Optimistic updates and toasts with Undo on check-in | Instant feel, undo works |
| Sun Dec 27 | 🔁 **Milestone:** run a full day manually (plan → do → check in) | Loop works end to end |

## Week 5 (Dec 28 – Jan 3): AI agent, part 1

| Date | Task | Done when |
| --- | --- | --- |
| Mon Dec 28 | LLM client wrapper: provider, model routing, token and cost logging | Test call logs usage |
| Tue Dec 29 | Agent tools: `get_goals`, `get_open_tasks`, `get_availability` with typed inputs and outputs | Unit tests |
| Wed Dec 30 | Agent loop with tool calling and a max-steps limit; mocked-LLM tests | Tests pass |
| Thu Dec 31 | **Goal breakdown:** goal → tasks with estimates and categories (`create_tasks`) | Real goal produces sensible tasks |
| Fri Jan 1 | 🎆 Buffer / rest | n/a |
| Sat Jan 2 | Goal breakdown UI: preview the AI's tasks, edit or remove, then save | Works in the UI |
| Sun Jan 3 | 🔁 Review prompt quality on 5 different goals | Notes plus prompt fixes |

## Week 6 (Jan 4 – Jan 10): AI agent, part 2, and starting self-use

| Date | Task | Done when |
| --- | --- | --- |
| Mon Jan 4 | `propose_plan`: fit tasks into availability, with a code-enforced time limit | Never over-books |
| Tue Jan 5 | Plan rationale: the agent explains each choice in one line | Shown in the API response |
| Wed Jan 6 | **Plan review UI:** proposed plan with reasons; Accept, Edit, Regenerate | Fully working |
| Thu Jan 7 | Record user edits to proposed plans (as learning data) | Stored in the DB |
| Fri Jan 8 | Error handling: LLM timeout or failure falls back to a simple rule-based plan | App never breaks |
| Sat Jan 9 | Deploy a personal instance (Render, Railway or a VPS) so you can use it from your phone | Live URL works |
| Sun Jan 10 | 🔁 **Milestone:** start using Momentum daily for real | First real day logged |

## Week 7 (Jan 11 – Jan 17): Behavior model (the differentiator)

| Date | Task | Done when |
| --- | --- | --- |
| Mon Jan 11 | Estimate ratio per category (median actual / planned, 14 days, n ≥ 3) | Unit tests |
| Tue Jan 12 | Completion rate by time block and weekday | Unit tests |
| Wed Jan 13 | Long-session drop-off plus top skip reasons | Unit tests |
| Thu Jan 14 | `compute_profile` writes `behavior_snapshots`; nightly APScheduler job | Job runs |
| Fri Jan 15 | `get_behavior_profile()` returns a compact text summary; planner prompt uses it | Plan changes when the profile changes |
| Sat Jan 16 | **"Why this plan?" UI:** show the adjustments ("Shortened, evenings run short") | Visible on the plan |
| Sun Jan 17 | 🔁 **Milestone:** check whether your own plan changed because of your behavior | Screenshot in `docs/log.md` |

## Week 8 (Jan 18 – Jan 24): Replanning and recovery

| Date | Task | Done when |
| --- | --- | --- |
| Mon Jan 18 | `replan_day`: after "Can't do it", rebuild the rest of today | Works through the API |
| Tue Jan 19 | Shrink / move / split / drop logic for missed tasks, with an explanation | Tests for each case |
| Wed Jan 20 | Replan UI: a calm "Here's the new plan" sheet, not an error | Fully working |
| Thu Jan 21 | Task skipped 3 times → "Is this still important?" prompt | Fully working |
| Fri Jan 22 | **Fresh start** button: clear the backlog guilt and build a light plan | Fully working |
| Sat Jan 23 | End-of-day check-in reminder (browser notification and/or email) | You receive it |
| Sun Jan 24 | 🔁 Review a week of real replans; tune the prompts | Notes plus fixes |

## Week 9 (Jan 25 – Jan 31): Wins and progress

| Date | Task | Done when |
| --- | --- | --- |
| Mon Jan 25 | Automatic wins (session done, streaks, milestones) and manual "log a win" | Fully working |
| Tue Jan 26 | Progress API: plan completion rate, estimate accuracy, streaks, by day and week | Tests |
| Wed Jan 27 | **Progress page:** completion-rate trend chart (the headline) | Fully working |
| Thu Jan 28 | Progress page: estimate accuracy chart, streaks per goal, wins list | Fully working |
| Fri Jan 29 | Weekly summary card (stats plus a short LLM recap) | Fully working |
| Sat Jan 30 | Small celebrations: a subtle animation on completion and streak milestones | Feels rewarding, not noisy |
| Sun Jan 31 | 🔁 Review: is the progress page motivating? Ask a friend to look | Feedback noted |

## Week 10 (Feb 1 – Feb 7): Polish and ship V1

| Date | Task | Done when |
| --- | --- | --- |
| Mon Feb 1 | UX pass: walk through every screen on mobile and fix spacing, copy and tap targets | Checklist done |
| Tue Feb 2 | Accessibility: keyboard navigation, focus rings, contrast (WCAG AA), aria labels | Lighthouse a11y ≥ 95 |
| Wed Feb 3 | Dark mode check plus PWA (installable to the home screen) | Installs on phone |
| Thu Feb 4 | Performance: bundle size, API query optimization, loading states | Lighthouse perf ≥ 90 |
| Fri Feb 5 | Demo seed script (2 weeks of realistic history) plus a demo account | Demo tells the story in 2 minutes |
| Sat Feb 6 | README screenshots, a GIF of the core loop, final deploy | Repo looks professional |
| Sun Feb 7 | 🚀 **V1 feature-complete.** Tag `v1.0.0` | Tagged release |

## Weeks 11–13 (Feb 8 – Feb 28): Self-use (dogfooding)

Use it every day, then fix **one** friction point per day (30–60 min).

| Week | Focus |
| --- | --- |
| Feb 8–14 | Check-in friction and notification timing |
| Feb 15–21 | Plan quality and prompt tuning; replan explanations |
| Feb 22–28 | Progress page and wins; measure your own week 1 vs. week 3 completion rate |

## Weeks 14–15 (Mar 1 – Mar 14): Test users

| Date | Task |
| --- | --- |
| Mar 1–3 | Basic multi-user accounts (simple email login), invite 5–10 users |
| Mar 4–6 | 15-minute onboarding call with each user |
| Mar 7–13 | Daily: watch metrics, fix bugs, note feedback |
| Sun Mar 14 | ✅ **V1 validated.** Write `docs/v1-results.md`: metrics, quotes, decision on V2 |

---

## V2 (Mar 15 – May 31, 2027): smarter and more helpful

Plan each week in detail at the start of that week, using what V1 taught you.

| Weeks | Feature |
| --- | --- |
| Mar 15 – Mar 28 | Proper auth (OAuth), multi-user hardening, settings page |
| Mar 29 – Apr 18 | **Learning companion:** resources, concept explanations, practice questions, comprehension checks |
| Apr 19 – May 2 | **Google Calendar sync:** read busy times, write focus blocks |
| May 3 – May 16 | **Rewards:** user-defined rewards unlocked by real progress |
| May 17 – May 31 | Deeper insights (monthly patterns), voice check-ins; tag `v2.0.0` |

## V3 (Jun 1 – Aug 31, 2027): proactive intervention

| Weeks | Feature |
| --- | --- |
| Jun 1 – Jun 30 | Proactive nudges ("You usually skip after 9 pm; start now?") |
| Jul 1 – Jul 31 | Focus protection: browser extension that blocks distracting sites during sessions |
| Aug 1 – Aug 31 | Mobile app (React Native / Expo) or a hardened PWA; tag `v3.0.0` |

---

## Daily routine

1. Open this file and find today's row.
2. Work for 1–2 hours and stop when "Done when" is met.
3. Commit with a clear message (`feat: check-in sheet with reason chips`).
4. Push.
5. Once self-use starts (from Jan 10), **check in on Momentum itself.** Your own app should be planning your Momentum work.
