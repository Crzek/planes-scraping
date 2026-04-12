# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project does

Web scraper for Sabadell Airport flight schedules. It uses Selenium to log into `https://acbs.private-radar.com/`, navigate the schedule UI, extract booking data via BeautifulSoup, and serves the results through a Flask web app. Data is stored locally (SQLite by default) and exported to Excel.

## Required setup

Before running, create `src/config/default.py` (already present, generated from `src/config/default.py` template) and a `.env` file based on `.env.example`:

```env
FLASK_APP=main:app
FLASK_ENV=development      # or production
SECRET_KEY=your-secret
PATH_BROWSER=/usr/bin/google-chrome   # or chromium path
PATH_DRIVER=/usr/local/bin/chromedriver   # ARM64 only
SQLALCHEMY_DATABASE_URI=sqlite:///midb.db
user=<private-radar-username>
password=<private-radar-password>
base_url=https://acbs.private-radar.com/
```

The `ENV_FILE` env var can point to a specific env file (e.g. `.env.chrome`, `.env.chromium`). If unset, system environment variables are used.

## Running the app

```shell
# Local development
export ENV_FILE=.env.chrome
flask run --debug --reload

# Via uv run
uv run flask run --reload
uv run flask db migrate
uv run flask db upgrade

# Production (gunicorn)
gunicorn -w 2 -b '0.0.0.0:5000' --timeout 120 'main:app'

# Run scraper directly (without web server)
python main.py
```

## Docker

```shell
# Production AMD64 (uses root docker-compose.yml or docker/docker-compose.pro.yml)
docker compose up --build
docker compose -f docker/docker-compose.pro.yml up --build

# Production ARM64
docker compose -f docker/docker-compose-arm.pro.yml up --build

# Development (mounts source, uses flask dev server)
docker compose -f docker/docker-compose.dev.yml up --build

# Run and attach interactively
docker compose -f docker/docker-compose.dev.yml run --rm vuelos-app bash
# Then inside container:
flask run --host 0.0.0.0 --debug --reload
```

## Architecture

**Entry point:** `main.py` → calls `create_app()` from `src/__init__.py`

**Flask app factory (`src/__init__.py`):**
- Loads env via `extencions.load_env()`
- Selects config from `FLASK_ENV` / `CONFIG_ENV` → `src/config/default.py`
- Initializes Flask-Login and Flask-SQLAlchemy
- Registers three blueprints: `authBP` (`/`), `scrapBP` (`/scrapy`), `health` (`/status/health`)

**Globals (`globals.py`):** Loaded at import time. Reads env file specified by `ENV_FILE`, falls back to system env. Exports `URL`, `USER`, `PAS`, `PATH_BROWSER`, `PATH_DRIVER`, and path constants used throughout.

**Blueprints:**
- `src/auth/` — login/logout routes using Flask-Login; `User` model in `src/auth/models/users.py`
- `src/app/` (`scrapBP`) — main scraping UI; routes in `src/app/routes/routes.py`
- `src/health/` — health check at `/status/health` and `/check/health`

**Scraping pipeline (`src/app/`):**
1. `utils/wdriver.py` — `CustomChromeDriver` wraps `selenium.webdriver.Chrome`; auto-detects ARM64 (`aarch64`) to use a `Service` with explicit chromedriver path; headless on ARM or when `hidden_windows=True`
2. `utils/page.py` — helpers for Selenium interactions (`login_page`, `get_element_click_newPage`, `find_element`)
3. `main.py` — orchestrates navigation: login → navigate to schedule → apply filters (deselects Canceled/Maintenance/Not Available/Type Rating statuses) → parse HTML with BeautifulSoup → extract booking `title` attributes → call `save_Book_by_tag`
4. `utils/utils.py` — `save_Book_by_tag` parses booking strings, creates `Book`/`Aircraft` model instances; `clas_to_series` converts DB records to pandas Series and generates HTML table
5. `utils/export.py` — exports data to Excel (`.xlsx`) via openpyxl
6. `utils/styles.py` — applies Excel cell styles

**Models (`src/app/models/`):** `Book` (a flight booking) and `Aircraft`. `src/auth/models/users.py` has the `User` model for authentication.

**Architecture note:** `CONFIG_ENV=production` or `production-amd` activates `ProductionConfig`; anything else uses `DevelopmentConfig`. ARM64 detection is runtime via `platform.machine()` — no build-time flag needed.
