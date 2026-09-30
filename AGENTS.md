# AGENTS.md

FastShip — FastAPI + SQLModel backend (`backend/`) and Vite + React 19 frontend (`frontend/`).
Learning project: expect incomplete/abandoned code paths and commented-out experiments.

Scope: repo-weit. `backend/AGENTS.md` hat zusätzlich die Backend-only Details (Imports, Fixtures, Modelle).

## Commands (verified)

Run everything from the package dir; there is no workspace/codegen step at the repo root.

```bash
# backend — MUST be run with cwd = backend/ (see "Import path" below)
cd backend
uv sync                                                  # install from pyproject.toml + uv.lock
uv run python -m uvicorn app.main:app --reload            # :8000, needs DATABASE_URL set
uv run pytest tests/ -v                                  # 14 tests; bare `uv run pytest` is broken
uv run pytest tests/services/ -q                         # single dir / single file
uv run ruff check . && uv run ruff format .              # lint + format

# frontend
cd frontend
pnpm install
pnpm dev            # vite --port 4200 --open
pnpm run typecheck  # ← NO-OP, see below. Use `pnpm run build` as the real gate.
pnpm run lint
pnpm run build      # ← tsc -b && vite build. This is the real typecheck.

# both at once (repo root)
npm run dev          # concurrently: backend :8000 + frontend :4200
```

Docker (5 services: postgres, backend, frontend/nginx, prometheus :9090, grafana :3000 admin/admin):
`docker compose up --build` · `docker compose down -v` (clears volumes).

## Baselines: lint and tests are RED on `main`

Do not assume you broke something. Current state:

| Check | Result |
|---|---|
| `uv run ruff check .` (backend) | passes |
| `uv run ruff format --check .` (backend) | **fails** — 5 unformatted files |
| `uv run pytest tests/` (backend) | **fails** — 2 failed, 11 passed, 1 error |
| `pnpm run build` (frontend) | passes |
| `pnpm run lint` (frontend) | **fails** — 1 error |
| `pnpm run typecheck` (frontend) | passes **vacuously** — checks zero files |

Known failures and their causes:
- `test_settings.py::test_default_database_url` — asserts the old Postgres default; `config.py` now defaults to SQLite (that edit is uncommitted in the working tree).
- `test_settings.py::test_email_test_user` — references `Settings.EMAIL_TEST_USER`, which was never implemented.
- `test_seller_service.py::test_create_seller` — **order-dependent** `KeyError: 'DATABASE_URL'`. `test_settings.py` does `os.environ.pop("DATABASE_URL")`, which breaks the `db` fixture in `conftest.py` (it reads `os.environ["DATABASE_URL"]`). Passes in isolation or when `tests/services/` runs before `tests/core/`.
- `pnpm run lint` — `react-refresh/only-export-components` in `src/contexts/AuthContext.tsx` (exports both `AuthProvider` and `useAuth`).

CI (`.github/workflows/ci.yaml`) runs `ruff check` + `ruff format --check` then `pytest tests/`, so the lint step fails there too. `mypy` is `|| true` and isn't even a declared dependency. `ci_docker.yaml` runs frontend lint with `|| true` and skips backend tests entirely.

## Frontend: `pnpm run typecheck` is a no-op

`frontend/tsconfig.json` is solution-style — `"files": []` plus `references` to `tsconfig.app.json` / `tsconfig.node.json`. `tsc --noEmit` on that compiles **nothing**; `tsc --noEmit --listFiles` returns zero non-`node_modules` files. **Use `pnpm run build` (`tsc -b`) as the typecheck gate.** A green `typecheck` means nothing.

Related: no `tsconfig.*.json` sets `strict`, so type errors are only caught where explicitly annotated. `tsconfig.app.json` declares a `~/*` → `./src/*` path alias and `vite-tsconfig-paths` is installed, but **`vite.config.ts` never wires the plugin** — a `~/...` import would typecheck but fail in Vite. No `~/` imports exist today.

## Gotchas that will bite you

**Import path — `app` must be top-level.** `app/core/db.py` and friends use absolute imports (`from app.models.seller import ...`), so Python must resolve `app` from `backend/`. Run uvicorn/pytest with cwd=`backend/`. `.vscode/launch.json` is wrong (uses `backend.app.main:app` with `PYTHONPATH=${workspaceFolder}`) and will not import — don't copy it.

**`backend/.env` is never loaded.** `Settings.model_config` sets `env_file="../.env"`, which pydantic-settings resolves relative to the **CWD**. From `backend/` that points at the repo root, and there is no root `.env`. So `backend/.env` has no effect: `FIRST_SUPERUSER_PASSWORD` is the code default `admin` (not the `0000` in `backend/.env`), and `DATABASE_URL` falls back to `sqlite+aiosqlite:///fastship.db`. Config must come from real env vars — which is why `npm run dev:backend` sets `DATABASE_URL` inline.

**`npm run dev:backend` is Windows-only** — uses cmd.exe `set VAR=... &&` syntax. On Linux/macOS export the var yourself.

**Mixed package managers, no root lockfile.** `concurrently` is an *npm* devDependency at the root, but the root scripts call `pnpm --filter frontend ...`, and the frontend is a pnpm package (`packageManager: pnpm@10.33.2`, pinned via corepack in the Dockerfile). There is no `pnpm-workspace.yaml` and no root `package-lock.json` / `pnpm-lock.yaml`, so the `concurrently` version floats. `npm install` at root + `pnpm install` in `frontend/` are both required. `pnpm --filter frontend` does work without a workspace file.

**Frontend needs `frontend/.env` or the API is unreachable.** `frontend/.env` is gitignored and **`.env.example` does not exist** (the `!frontend/.env.example` negation in `.gitignore` points at nothing). Without it `import.meta.env.VITE_API_URL` is undefined and `AuthContext` falls back to `""` → requests go to the Vite origin `:4200`. `vite.config.ts` defines **no `server.proxy`**, so those requests 404. Create `frontend/.env` with `VITE_API_URL=http://localhost:8000` for local dev. `backend/.env` also contains `VITE_API_URL`/`VITE_APP_TITLE` keys, which are dead there — Vite only reads `frontend/`.

**Two unsynced dependency sources.** `pyproject.toml` + `uv.lock` drive local dev; `requirements.txt` drives the Dockerfiles. They have already drifted. Critically, `asyncpg`, `argon2-cffi`, and `bcrypt` exist only in `requirements.txt` — so `postgresql+asyncpg://` works in Docker but fails locally. After `uv add`, regenerate with `uv export --format requirements-txt --no-hashes > requirements.txt`.

**No migrations.** `create_db_and_tables()` runs `SQLModel.metadata.create_all` on lifespan startup. A `SQLModel` field rename silently leaves the old column in place — delete `backend/fastship.db` (`*.db` is gitignored) to pick up schema changes.

**Model registration matters.** `app/models/__init__.py` re-exports all four models; that import chain is what registers every table on `SQLModel.metadata`. A new model that isn't imported there (or transitively via a router → service → model) never gets its table created.

**JWT key is hardcoded.** `app/core/utils.py` signs with a literal `_key = "ANY_KEY_GHISLAIN"` and ignores `settings.authjwt_secret_key`. Token `exp` is hardcoded to 10 minutes, ignoring `authjwt_access_token_expires`. Setting either env var does nothing until `utils.py` is wired to `settings`.

**`testpaths` in `backend/pyproject.toml` is wrong.** It says `backend/tests`, but rootdir *is* `backend/`, so it resolves to `backend/backend/tests`. Bare `uv run pytest` warns and recurses from cwd instead. Always pass `tests/` explicitly. `backend/test_seed.py` is a scratch script at the package root whose name matches the `test_*.py` glob — keep it out of collection scope.

**Ruff's default rule set is only `E4`, `E7`, `E9`, `F`.** Line length (`E501`) is *not* checked, and there is no `[tool.ruff]` section or `ruff.toml` — so `ruff check .` passing does not mean the code is within 88 columns (`app/core/db.py` already violates it twice).

**`routeTree.gen.ts` is generated but committed.** Regenerated by `TanStackRouterVite` on `pnpm dev`/`build`. Never hand-edit it; edit the files under `src/routes/`.

**Docker frontend only proxies `/auth`.** `frontend/nginx.conf` forwards `/auth` to `backend:8000`; everything else 404s. Use `VITE_API_URL=http://localhost:8000` for direct calls, or add nginx locations. CORS in `app/main.py` allowlists `4200` and `5173` — a new frontend port must be added there.

**`backend/prometheus.yaml` scrapes `backend:8000`**, a Docker-internal DNS name. Prometheus config only works inside the compose network.

**Python version skew.** `pyproject.toml` requires `>=3.12`; `backend/Dockerfile` is `python:3.11-slim`; `ci_docker.yaml` uses 3.11, `ci.yaml` uses 3.12. Docker is unaffected (it installs from `requirements.txt`).

## Architecture

Layered, one direction only: `routers/` → `services/` → `models/` + `schemas/`.

- `app/main.py` — app entrypoint (`[tool.fastapi] entrypoint = "app.main:app"`). Assembles CORS, Prometheus `Instrumentator` (`/metrics`), `CustomMiddleware`, and four routers. Also serves `/` (healthcheck target) and `/scalar` (API docs). Startup `lifespan` runs `create_db_and_tables()` then `seed_db_if_empty()`, which creates the `FIRST_SUPERUSER` seller if that email is missing.
- `app/routers/` — thin HTTP layer, one router per domain: `auth_routes` (`/auth`), `seller_router` (`/sellers`), `order_routes` (`/order`), `shipment` (`/shipments`).
- `app/services/` — plain classes constructed with an `AsyncSession`. All business logic and DB queries live here. **Router bodies should not query the DB directly**; add the method to the service.
- `app/models/` — SQLModel `table=True` DB models. `app/schemas/` — pydantic in/out models. Both are required; don't return `models` directly from routes.
- `app/core/dependencies.py` — service DI. Services are built by `@lru_cache`-decorated `get_*_service()` functions using `Depends(get_async_session)`, exposed as `Annotated` aliases (`SellerServiceDep`, `OrderServiceDep`, `ShipmentServiceDep`). Add new services here.
- `app/core/db.py` — engine + `async_session_maker` + `get_async_session` (the override point for tests).

Routes: `/`, `/metrics`, `/scalar`, `/auth/token`, `/auth/signup`, `/sellers/`, `/shipments`, `/order/`.

Frontend: React 19 + Vite 8 + Tailwind v4 (`@tailwindcss/vite`, no `tailwind.config.js` — theme lives in `src/styles.css`). TanStack Router file-based (`src/routes/` → `routeTree.gen.ts`) plus TanStack Query. Shadcn-style primitives in `src/components/ui/` (note the typo in `src/librarz/`). `eslint.config.js` exempts `src/routes/**` from `react-refresh/only-export-components`; component files are not exempt.

## Auth

OAuth2 password flow, FastAPI-native (no `fastapi-jwt-auth` despite the comments). `POST /auth/token` takes an OAuth2 password-request-form body (`username` = email, `password`) and returns `{access_token, type}` with a PyJWT HS256 token whose payload nests the user under a `user` key.

Passwords hash with `passlib` **argon2**, not bcrypt (the `# passlib[bcrypt] must be installed` comments are wrong).

`order_routes.py` annotates with `OAuth2PasswordBearer` instead of using `Depends(oauth2_scheme)`, so that route is not actually protected. Nothing else enforces auth yet.

Frontend: `src/contexts/AuthContext.tsx` decodes the JWT client-side with `atob` and stores it in `localStorage["fastship_token"]`. No `Authorization` header plumbing exists yet.

## Docs

`README.md` and `Dev.md` are the author's learning notes, not a spec — they drift from the code. Trust config, scripts, and CI over them.
