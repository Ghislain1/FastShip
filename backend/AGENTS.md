# AGENTS.md — `backend/`

Scope: FastAPI + SQLModel backend only. Repo-weite Themen (Frontend, Docker-Compose, Ports, CORS) stehen im Root-`AGENTS.md`.

Learning project: incomplete code paths, `@TODO@Ghis`-Kommentare und toter Code sind normal — nicht "aufräumen", außer gefragt.

## Befehle

cwd **muss** `backend/` sein (siehe "Import-Pfad"). Es gibt keine Codegen-Stufe.

```bash
uv sync                                        # aus pyproject.toml + uv.lock
uv run python -m uvicorn app.main:app --reload  # :8000
uv run pytest tests/ -v                        # 14 Tests
uv run pytest tests/services/ -q               # einzelnes Verzeichnis / Datei
uv run pytest tests/services/test_seller_service.py -q
uv run ruff check .                            # ✓ grün
uv run ruff format .                           # formatiert um (aktuell 5 Dateien fällig)
```

## Baseline: Tests und `ruff format --check` sind rot auf `main`

`uv run pytest tests/` → **2 failed, 11 passed, 1 error**. Nicht dein Fehler, wenn du nichts angefasst hast.

| Fehler | Ursache |
|---|---|
| `test_default_database_url` | Test erwartet die alte Postgres-Default; `config.py` nutzt jetzt SQLite (uncommitteter Edit im Working Tree) |
| `test_email_test_user` | Referenziert `Settings.EMAIL_TEST_USER` — existiert nicht, nie implementiert |
| `test_create_seller` (ERROR) | **Reihenfolgeabhängig**: `KeyError: 'DATABASE_URL'`, siehe "Test-Isolation" |
| `ruff format --check` | 5 Dateien: `app/models/__init__.py`, `app/schemas/shipment.py`, `test_seed.py`, `tests/conftest.py`, `tests/utils/utils.py` |

`uv run ruff check .` ist dagegen grün. `mypy` läuft in CI nur mit `|| true` und ist gar keine deklarierte Dependency — nicht als Gate verwenden.

**Ruff-Defaults sind `E4`, `E7`, `E9`, `F`.** Es gibt weder `[tool.ruff]` in `pyproject.toml` noch eine `ruff.toml`, also ist `E501` (Zeilenlänge) **nicht** aktiv. `ruff check .` grün heißt nicht "unter 88 Spalten" — `app/core/db.py:15` und `:20` verletzen das bereits. Mit `uv run ruff check --select E501 .` sichtbar.

## Import-Pfad: `app` muss top-level sein

`app/core/db.py`, `app/models/order.py` und Co. benutzen absolute Imports (`from app.models.seller import ...`). Python muss `app` also aus `backend/` auflösen können.

- uvicorn/pytest immer mit cwd=`backend/`.
- `.vscode/launch.json` ist **falsch** (`backend.app.main:app` + `PYTHONPATH=${workspaceFolder}`) und wird nicht importieren. Nicht als Vorlage übernehmen.
- `tests/conftest.py` patcht das mit `sys.path.insert(...)`, weshalb pytest ohne `PYTHONPATH` trotzdem läuft. Uvicorn tut das nicht.

## Env: `backend/.env` wird nie gelesen

`Settings.model_config` setzt `env_file="../.env"`, und pydantic-settings löst das **relativ zum CWD** auf. Von `backend/` aus zeigt das auf das Repo-Root — dort existiert keine `.env`. Folge:

- `FIRST_SUPERUSER_PASSWORD` ist der Code-Default `admin`, **nicht** die `0000` aus `backend/.env`.
- `DATABASE_URL` fällt auf `sqlite+aiosqlite:///fastship.db` zurück.
- Nur echte Env-Variablen wirken. Deshalb setzt das Root-Skript `npm run dev:backend` `DATABASE_URL` inline (cmd.exe-Syntax, **nur Windows**).

## Tests & Fixtures

`[tool.pytest.ini_options]` in `pyproject.toml`: `asyncio_mode = "auto"` → **`@pytest.mark.asyncio` ist überflüssig**, der Marker in `test_seller_service.py` ist Altlast.

`testpaths = ["backend/tests"]` ist **falsch**: rootdir *ist* `backend/`, also zeigt es auf `backend/backend/tests`. Bare `uv run pytest` warnt und sucht rekursiv ab cwd. Immer explizit `tests/` übergeben.

`backend/test_seed.py` ist ein Scratch-Skript auf Package-Ebene, dessen Name dem Glob `test_*.py` entspricht. Aus der Collection-Scope halten.

Fixtures in `conftest.py` (setzt `os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"` **auf Modulebene**, vor dem Import von `app.core.db`):
- `db` — function-scoped, eigener `create_async_engine`, `create_all` / `drop_all` pro Test
- `client` — `TestClient(app)` **ohne** `with` → `lifespan` läuft **nicht**
- `test_client` — `with TestClient(app)` → `lifespan` **läuft**; überschreibt `get_async_session` via `app.dependency_overrides`

**Zwei verschiedene In-Memory-DBs:** `app/core/db.py` baut beim Import ein Modul-Level-`engine` aus `settings.DATABASE_URL` (eben `:memory:`). Die `db`-Fixture legt ein **zweites**, eigenes Engine-Objekt an. `sqlite+aiosqlite:///:memory:` ist pro-Verbindung eine frische DB — die beiden Engines teilen keine Daten. Deshalb sieht ein Test über `test_client` die von `seed_db_if_empty()` im Lifespan angelegte Superuser-Zeile **nicht**. Nur die `dependency_overrides`-Route nutzt die Fixture-DB.

**Test-Isolation ist kaputt:** `test_settings.py::test_default_database_url` macht `os.environ.pop("DATABASE_URL", None)` und lässt das für alle folgenden Tests weg. Die `db`-Fixture liest `os.environ["DATABASE_URL"]` → `KeyError`. Deshalb schlägt `test_create_seller` nur fehl, wenn `tests/core/` vor `tests/services/` läuft (alphabetische Collection). Neu geschriebene Settings-Tests dürfen `os.environ` nicht mutieren.

## Architektur

Eine Richtung, `routers/` → `services/` → `models/` + `schemas/`.

- `app/main.py` — Entrypoint (`[tool.fastapi] entrypoint="app.main:app"`). CORS, Prometheus-`Instrumentator` (`/metrics`), `CustomMiddleware`, vier Router, `/` als Healthcheck-Ziel, `/scalar` als API-Referenz. `lifespan` ruft `create_db_and_tables()` und dann `seed_db_if_empty()`.
- `app/routers/` — dünne HTTP-Schicht, eine Domain pro Router: `auth_routes` (`/auth`), `seller_router` (`/sellers`), `order_routes` (`/order`), `shipment` (`/shipments`).
- `app/services/` — plain Klassen, die eine `AsyncSession` im Konstruktor bekommen. **Hier gehört die gesamte DB-Logik hin**; keine Queries direkt im Router-Body.
- `app/models/` — SQLModel `table=True`. `app/schemas/` — Pydantic In/Out. Beides nötig; Models nicht direkt aus Routes zurückgeben.
- `app/core/dependencies.py` — Service-DI über `@lru_cache`-dekorierte `get_*_service()` mit `Depends(get_async_session)`, exportiert als `Annotated`-Aliase (`SellerServiceDep`, `OrderServiceDep`, `ShipmentServiceDep`). Neue Services hier registrieren.
- `app/core/db.py` — Engine, `async_session_maker`, `get_async_session` (der Override-Punkt für Tests).

`seed_db_if_empty()` legt den `FIRST_SUPERUSER`-Seller an, falls dessen E-Mail in `seller` fehlt.

### Neue Route: Checkliste

1. Model in `app/models/` (bei `table=True` — siehe Registrierung unten).
2. Pydantic In/Out-Schema in `app/schemas/`.
3. Methode auf dem Service in `app/services/` — Queries gehören **nicht** in den Router.
4. Neuen Service in `app/core/dependencies.py` als `Annotated`-Alias registrieren.
5. Route in `app/routers/`, Router in `app/main.py` per `include_router` mounten.
6. `pytest tests/ -v` und `ruff format .` laufen lassen.

### Primary Keys sind `UUID`, nicht `int`

`Seller`, `Product`, `Order`, `Shipment` nutzen alle `id: UUID = Field(default_factory=uuid4, primary_key=True)`. Drei Stellen widersprechen dem und sind latent kaputt: `seller_service.py:115` (`get_seller_by_id(self, id: int)`), `shipment_service.py:97` (`get_customer_by_id(self, id: int)`), `routers/order_routes.py:19` (`id: int` im Pfad `/order/user/order/{id}/`). `session.get(Model, id)` mit `int` gegen UUID-PK liefert `None`.

Tabellenname stammt vom Klassennamen, außer ein `__tablename__` ist explizit gesetzt: `Order` → `order`, `Product` → `product`; `Seller` und `Shipment` setzen ihn explizit.

`OrderBase.created_at` / `updated_at` sind **Pflichtfelder ohne `default_factory`** — anders als `Seller.created_at`, das `get_datetime_utc()` nutzt. Ein `Order` ohne beide Werte schlägt bei der Validierung fehl.

### Neue Tabelle: Registrierung ist Pflicht

`create_all` kennt nur Tabellen in `SQLModel.metadata`. `app/models/__init__.py` re-exportiert die vier Modelle — diese Importkette registriert die Tabellen. Eine neue Tabelle, die nirgends importiert wird, wird **nie** angelegt.

Belegter Fall: `app/models/shipment_event.py` definiert `ShipmentEvent(table=True)`, wird aber nirgends importiert — `import app.main` ergibt exakt `['order', 'product', 'seller', 'shipment']`. Die Tabelle `shipment_event` existiert nicht.

Prüfen mit: `uv run python -c "import app.main; from sqlmodel import SQLModel; print(sorted(SQLModel.metadata.tables))"`

### Keine Migrations

`create_db_and_tables()` läuft nur `SQLModel.metadata.create_all` beim Start. Ein umbenanntes Feld lässt die alte Spalte still stehen. Nach Schema-Änderungen `backend/fastship.db` löschen (`*.db` ist gitignored).

## Response-Formate

`GET /sellers/` liefert **nicht** eine nackte Liste, sondern ein Envelope: `SellersPublic` = `{ "data": SellerPublic[], "count": int }` mit `offset` / `limit` (`limit` per `Query(le=100)`). Der Token-Endpoint liefert `{access_token, type}` mit `type: "jwt"`.

## Auth

FastAPI-natives OAuth2-Password-Flow — kein `fastapi-jwt-auth`, trotz der Kommentare. `POST /auth/token` nimmt einen `OAuth2PasswordRequestForm`-Body (`username` = E-Mail, `password`) und gibt `{access_token, type}` zurück. Der PyJWT-HS256-Payload verschachtelt den User unter dem Schlüssel `"user"`.

- **JWT-Key ist hardcodiert.** `app/core/utils.py` signiert mit `_key = "ANY_KEY_GHISLAIN"` und ignoriert `settings.authjwt_secret_key`. `exp` ist auf 10 Minuten festgenagelt und ignoriert `authjwt_access_token_expires`. Beide Env-Vars tun nichts, bis `utils.py` auf `settings` umgestellt ist.
- Passwort-Hashing über `passlib` **argon2**, nicht bcrypt. Die `# passlib[bcrypt] must be installed`-Kommentare sind falsch.
- `order_routes.py` annotiert mit `OAuth2PasswordBearer` statt `Depends(oauth2_scheme)` zu benutzen — die Route ist dadurch **nicht** geschützt. Bisher erzwingt sonst nichts Auth.
- Doppelte E-Mail wirft `HTTPException(409)` aus `SellerService.add_seller`. Login-Fehler werfen **404**, nicht 401 — Frontend zeigt daher `response.statusText`.

## Bekannter toter/kaputter Code

Nicht ungefragt "fixen", aber nicht als funktionierend behandeln:

- `app/routers/order_routes.py::get_all_orders` — `response_model=list[OrderPublic]`, gibt aber `None` zurück (`await` ohne `return`).
- `app/routers/seller_router.py::read_sellers` — Rückgabe-Annotation `-> any` (Built-in, nicht `typing.Any`).
- `app/core/utils.py::decode_access_token` — Annotation `dict[str, any]`, `any` ist hier der Built-in.
- `app/models/__init__.py` — `__all__ = [Seller, Product, Order, Shipment]` enthält Klassen statt Strings; `from app.models import *` bricht.
- `SellerService.get_seller_by_email` / `ShipmentService.get_customer_by_email` — nicht-`async`, inkonsistente `self.session.exec(...).first()`-Aufrufe, `@TODO`.
- `Shipment` hat `email`/`username`/`password`-Feldzugriffe in `ShipmentService`, die das Modell nicht deklariert.
- `app/models/shipment.py` — die `Order`-Relationship ist dort auskommentiert; `Order` hält die FK.
- `backend/Dockerfile` hat ein `test`-Stage, die `pytest tests/` ausführt — die würde an den roten Tests scheitern. Niemand baut dieses Target.

## Dependencies: zwei Quellen, auseinandergelaufen

`pyproject.toml` + `uv.lock` = lokale Entwicklung. `requirements.txt` = die Dockerfiles. Sie divergieren bereits (`requirements.txt` pinnt `sqlmodel==0.0.38`, `pytest-asyncio==1.3.0`, `ruff==0.15.12`; `pyproject.toml` ist großzügiger).

`asyncpg`, `argon2-cffi` und `bcrypt` stehen **nur** in `requirements.txt`. Deshalb funktioniert `DATABASE_URL=postgresql+asyncpg://...` in Docker, lokal aber nicht — lokal fehlt der Treiber. (Auch inkonsistent: `pyproject.toml` deklariert `psycopg2-binary`, `docker-compose.yaml` verlangt `asyncpg`.)

Nach `uv add` synchronisieren: `uv export --format requirements-txt --no-hashes > requirements.txt`.

Python-Drift: `pyproject.toml` fordert `>=3.12`, `backend/Dockerfile` ist `python:3.11-slim`, `ci.yaml` nutzt 3.12, `ci_docker.yaml` nutzt 3.11. Docker installiert aus `requirements.txt` und ist davon nicht betroffen.

`.dockerignore` schließt u.a. `uv.lock`, `.venv`, `fastship.db` aus — die Image-Größe hängt also an `requirements.txt`, nicht am Lockfile.