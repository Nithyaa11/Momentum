# Momentum: Build Plan

This is the step-by-step plan for building **V1**, the smallest version that tests the core hypothesis:

> **Learning from planned vs. actual makes plans more realistic and improves follow-through.**

Timeline: **30–60 minutes a day, Nov 28, 2026 – Jan 11, 2027.** Daily self-use starts Dec 18, so V1 ships with about 3 weeks of real usage data. Test users follow in V1.1 (Jan 12–25).

👉 **The day-by-day schedule is in [SCHEDULE.md](SCHEDULE.md).** This file explains *what* each phase builds and *why*.

---

## Tech stack

| Layer | Technology |
| --- | --- |
| Frontend | React + TypeScript + Tailwind (Vite) |
| UI components | shadcn/ui, lucide icons, Recharts, Framer Motion, Sonner |
| Frontend data / routing | TanStack Query, React Router |
| Backend | Python + FastAPI |
| Config / validation | pydantic-settings, Pydantic |
| Database | PostgreSQL 17 (Docker, host port 5433) |
| ORM / migrations | SQLAlchemy 2 + psycopg 3, Alembic |
| Background jobs | APScheduler |
| AI | LLM API with tool calling, behind our own wrapper so the provider can be swapped. Start on the **Gemini API free tier**; **OpenRouter free models** as a fallback |
| Testing | Pytest |
| Python tooling | uv |
| Deployment | Docker Compose locally; Render or Railway for hosting |

---

## UI/UX standards

Momentum has to be something people **want** to open every day. A clunky UI kills a follow-through app faster than anything else. These are requirements, not extras.

### Principles

1. **One primary action per screen.** The Now screen shows *one* task and *one* big button. No lists to choose from.
2. **Check-in in under 5 seconds.** One tap for the outcome, one tap for the reason, with a sensible default for time.
3. **No guilt.** No red overdue counters and no "You failed 4 tasks." Missed tasks become "Here's a lighter plan," and the user can always take a fresh start.
4. **Always explain changes.** Every AI plan change shows a one-line reason ("Shortened, since evening sessions have been running short").
5. **Celebrate progress.** Wins, streaks and an improving completion rate get the most visual weight. Celebrations stay subtle, not noisy.
6. **Feels instant.** Optimistic updates, skeleton loaders, and Undo instead of confirmation dialogs.
7. **Mobile-first.** Most check-ins happen on a phone. Design at 375px first, then scale up; installable as a PWA.
8. **Accessible.** Keyboard navigation, visible focus, WCAG AA contrast, labels for screen readers.

### UI stack

| Need | Choice |
| --- | --- |
| Components | **shadcn/ui** (Radix primitives + Tailwind), accessible and fully customizable |
| Icons | lucide-react |
| Data fetching / cache | TanStack Query (optimistic updates, retries) |
| Routing | React Router |
| Charts | Recharts |
| Animation | Framer Motion (sparingly) |
| Toasts | Sonner |

### Screens

| Screen | Purpose | Key UX detail |
| --- | --- | --- |
| **Onboarding** | Goals, available hours, best time of day | Under 2 minutes; visual hour picker |
| **Now** | "Do this now" plus a timer | One card, one button |
| **Today** | Today's plan with statuses | Drag to reorder; "Why this plan?" link |
| **Plan review** | Accept or edit the AI's proposed plan | Each item shows its reason |
| **Check-in sheet** | Done / Partial / Can't do it + reason | Bottom sheet on mobile; Undo toast |
| **Goals** | Add, edit and archive goals; AI task breakdown preview | Edit AI tasks before saving |
| **Progress** | Completion-rate trend, estimate accuracy, streaks, wins | Headline is "you're getting better" |

### Quality bar before V1 ships

- Lighthouse: accessibility ≥ 95, performance ≥ 90
- Every screen has loading, empty and error states
- Tested at 375px, 768px and 1440px, in light and dark mode
- At least 2 people outside the project complete onboarding and a check-in without help

---

## Guiding rules

1. **Build the loop end to end first, then make it smart.** A dumb plan you can check in against is worth more than a clever plan with no feedback.
2. **No LLM where code will do.** Stats, streaks and the behavior profile are plain Python with tests.
3. **The agent proposes; the user accepts.** Never let the LLM write final state without validation.
4. **Use it yourself from Week 4 onward.** Your own data is the first test.
5. **Don't add V2 features until V1's metric is measured.**

---

## Repository layout

```
momentum/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # settings (env vars)
│   │   ├── db.py                # SQLAlchemy engine/session
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── api/                 # routers: goals, tasks, plans, checkins, progress
│   │   ├── services/
│   │   │   ├── goal_service.py
│   │   │   ├── task_service.py
│   │   │   ├── plan_service.py
│   │   │   ├── progress_service.py
│   │   │   └── behavior_service.py
│   │   ├── agent/
│   │   │   ├── agent.py         # LLM loop with tool calling
│   │   │   ├── tools.py         # typed tool functions
│   │   │   ├── prompts.py
│   │   │   └── llm_client.py    # provider wrapper + model routing
│   │   └── jobs/
│   │       └── scheduler.py     # APScheduler: nightly reflection, reminders
│   ├── alembic/
│   ├── tests/
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── pages/               # Now, Goals, Plan, CheckIn, Progress
│   │   ├── components/
│   │   └── api/                 # API client
│   └── package.json
├── scripts/
│   └── seed_demo.py             # 2 weeks of realistic history for demos
├── docker-compose.yml
├── README.md
└── PLAN.md
```

---

## Phase 0: Setup (Week 1)

**Goal:** an empty app that runs with one command.

- [ ] Init the git repo, `.gitignore`, `.env.example`
- [ ] FastAPI skeleton with a `/health` endpoint
- [ ] PostgreSQL + SQLAlchemy + Alembic wired up
- [ ] React + Vite + Tailwind skeleton
- [ ] `docker-compose.yml`: `db`, `backend`, `frontend`
- [ ] Pytest running with a test database
- [ ] Single-user mode for V1 (one hard-coded user; real auth later)

**Done when:** `docker compose up` serves the frontend, the backend reports healthy, and `pytest` passes.

---

## Phase 1: Data model and CRUD (Week 2)

**Goal:** goals, tasks and plans can be stored and edited without any AI.

- [ ] Models: `users`, `goals`, `tasks`, `plans`, `plan_items`, `completions`, `wins`, `behavior_snapshots` (see the README's data model section)
- [ ] First Alembic migration
- [ ] Pydantic schemas
- [ ] Endpoints:
  - `POST/GET/PATCH /goals`
  - `POST/GET/PATCH /tasks`
  - `GET /plans/{date}`, `POST /plans/{date}/accept`
  - `POST /plan-items/{id}/checkin` with body `{outcome, actual_minutes, skip_reason}`
- [ ] Service-layer tests

**Done when:** you can create a goal, add tasks, build a day plan by hand, and check in on it through the API.

---

## Phase 2: The core screens (Week 3)

**Goal:** the loop works in the UI, even with manual planning.

- [ ] **Onboarding:** available hours per weekday, best time of day, timezone
- [ ] **Goals page:** add and edit goals
- [ ] **Now page:** the single "Do this now" card, with Start, Done and Can't do it buttons
- [ ] **Check-in:** one tap for the outcome, a quick actual-time picker, and reason chips (*too tired · ran out of time · forgot · not important anymore · did part of it*)
- [ ] **Today page:** today's plan list with statuses

**Done when:** you can run through a full day in the browser, from plan to execute to check-in.

---

## Phase 3: The AI agent (Weeks 4–5)

**Goal:** the agent breaks goals into tasks and proposes daily plans.

### Agent tools

| Tool | What it does |
| --- | --- |
| `get_goals()` | Active goals with progress |
| `get_open_tasks(goal_id?)` | Unfinished tasks |
| `get_availability(date)` | Available minutes and preferred times |
| `get_behavior_profile()` | Compact summary from the behavior service |
| `create_tasks(goal_id, tasks[])` | Adds tasks (validated) |
| `propose_plan(date, items[], rationale)` | Writes a **proposed** plan. The user still has to accept it |
| `replan_day(date, reason)` | Rebuilds the rest of today after a skip |

### Work items

- [ ] LLM client wrapper with **model routing** (cheap vs. strong model)
- [ ] Agent loop with tool calling and a max-steps limit
- [ ] **Goal breakdown:** goal → tasks with estimates and categories
- [ ] **Daily planning:** fit tasks into availability; never exceed available minutes (enforced in code, not only in the prompt)
- [ ] Plan **rationale** shown in the UI
- [ ] Accept / edit / regenerate a proposed plan
- [ ] Log every LLM call (tokens, latency, model) for cost tracking
- [ ] Tests with a mocked LLM

**Done when:** you type a goal, get sensible tasks, and get a proposed plan for tomorrow that fits your hours.

**Start using Momentum daily yourself at this point.**

---

## Phase 4: The behavior model, the differentiator (Week 6)

**Goal:** Momentum learns from planned vs. actual.

### Signals (plain Python, no LLM)

| Signal | How it's computed |
| --- | --- |
| Estimate ratio per category | median(actual_minutes / planned_minutes) over the last 14 days, per category |
| Completion rate by time block | completed / planned, grouped by morning, afternoon, evening and night |
| Completion rate by weekday | completed / planned, grouped by weekday |
| Long-session drop-off | completion rate for sessions over 60 min vs. under 60 min |
| Top skip reasons | counts over the last 7 days |
| Overall plan completion rate | sum(actual) / sum(planned), by day and by week |

### Work items

- [ ] `behavior_service.compute_profile(user_id)` that writes a `behavior_snapshot`
- [ ] Minimum-data rules (e.g. ignore a category until it has 3 or more data points; use defaults before then)
- [ ] Nightly APScheduler job: compute the snapshot and pre-generate tomorrow's proposed plan
- [ ] `get_behavior_profile()` returns a **short text summary** for the prompt, e.g.:
  ```
  - Coding tasks take ~1.6x estimate (n=9)
  - Evening (after 8pm) completion: 28%; morning: 81%
  - Sessions >60 min usually cut short (completion 35%)
  - Top skip reason this week: too tired (4)
  ```
- [ ] Planner prompt updated to **apply** these adjustments and **explain** them
- [ ] Unit tests for every statistic

**Done when:** after a week of real use, tomorrow's plan visibly changes because of your history, and it tells you why.

---

## Phase 5: Replanning and recovery (Week 7)

**Goal:** missing a task leads to a better plan, not a growing backlog.

- [ ] On "Can't do it": record the reason → call `replan_day` for the rest of today
- [ ] Rules for what happens to missed tasks: **shrink**, **move**, **split** or **drop** (the agent picks one and explains it)
- [ ] Rollover limit: a task skipped 3 times triggers a "Is this still important?" prompt
- [ ] **Fresh start** button: clears overdue guilt and rebuilds a light plan after a bad stretch
- [ ] End-of-day check-in reminder (email or browser notification)

**Done when:** skipping a task produces a sensible change with an explanation, and the backlog never piles up silently.

---

## Phase 6: Wins and progress (Week 8)

**Goal:** show users they're getting better.

- [ ] Automatic wins (completed session, streak milestones, goal milestones) and manual wins ("hit protein goal")
- [ ] **Progress page:**
  - Plan completion rate over time (the headline chart)
  - Estimate accuracy over time
  - Streaks per goal
  - Wins this week
- [ ] Weekly summary (an optional short LLM-written recap, generated from the stats)
- [ ] `scripts/seed_demo.py`: a two-week realistic history for demos

**Done when:** the Progress page shows your own plan completion rate trending, and the demo account tells the full story in two minutes.

---

## Phase 7: Validate (Weeks 9–13)

| Period | Activity |
| --- | --- |
| Weeks 9–11 | Use it yourself every day. Fix friction. Write down what's annoying. |
| Weeks 12–13 | 5–10 test users (students or early-career professionals). Short interview before and after. |

**Track:**

- Plan completion rate, week 1 vs. week 3
- Check-in rate (are people still logging?)
- Estimate accuracy over time
- Qualitative: "Did the plan feel more realistic over time?" and "Did you trust the changes?"

**Decision point:**

- Metric improved and users trust the changes → move to V2.
- Metric flat → look at why: bad stats, bad prompts, or check-in friction. Fix before adding anything new.

---

## After V1

Only after Phase 7 shows results:

| Version | Features |
| --- | --- |
| **V2** | Learning companion (resources, questions, comprehension checks), rewards, Google Calendar sync, deeper pattern insights, voice check-ins, real auth and multiple users |
| **V3** | App and site blocking during focus sessions, proactive nudges, mobile app |

---

## Demo script (for interviews and pitches)

1. **Problem (20s):** "People don't fail at planning; they fail at follow-through, and their tools never notice the plan itself is wrong."
2. **Seeded user (60s):** show 3 evenings of planned 120 min vs. actual 30 min, marked "too tired."
3. **The difference (40s):** show tomorrow's plan, with 40-minute sessions, one moved to Saturday morning, and the explanation.
4. **Progress (20s):** the plan completion rate climbs from 30% to 75% over two weeks.
5. **Close:** "Other tools reschedule your tasks. Momentum corrects your plan."
