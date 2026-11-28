# Build Log

Weekly reviews: what got done, what was learned, what changes next week.

---

## Week 1 (Mon Nov 23 – Sun Nov 29)

**Planned:** backend skeleton → frontend skeleton (6 tasks, Nov 28 – Dec 2 in the original schedule).
**Actual:** all 6 done by Sat Nov 28, about 3 days ahead.

### Done
- Product docs: README (pitch, differentiation vs. Motion, architecture), PLAN, SCHEDULE
- Backend: FastAPI + PostgreSQL in Docker, `/health`
- Data model: 8 tables with database-level rules (e.g. a skip must have a reason) + Alembic migrations
- API: goals, tasks, daily plans, check-ins (done / partial / skipped, change, undo)
- 34 tests against a real test database
- Frontend: Vite + React + TypeScript + Tailwind + shadcn/ui, routing, TanStack Query, API proxy

### Problems and fixes
- Port 5432 was taken by another project's Postgres → Momentum uses host port **5433**.
- Docker restarted overnight and tests hung waiting for the database → containers now auto-restart and DB connections time out after 5s.
- Tests caught PATCH requiring every field, and null crashing required fields → fixed with tests.

### Decisions
- LLM: start with the **Gemini API free tier**, behind our own wrapper; OpenRouter as fallback. OpenCode Zen free models aren't suitable for the app.
- Weeks run Mon–Sun; the schedule gets re-dated from real progress.
- V1 release moved up to **Fri Jan 8** (from Jan 11).

### Next week focus
Dev setup polish, design system, onboarding, Goals / Today / Now screens.
