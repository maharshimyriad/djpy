# Personal Project and Task Manager

A beginner-focused Django application for personal project and task management. Registered users can organize projects, track tasks, set priorities and due dates, and filter their work. The project is built with Django function-based views, templates, SQLite, and Bootstrap.

## Learning Objectives

By the end, you will be able to explain Django's project and app structure, define models and relationships, use migrations and the ORM, connect URLs to function-based views, render templates, validate forms, use authentication and ownership checks, and write basic tests.

## Current Progress

- Phase 0: environment inspection completed.
- Phase 1: initial architecture lessons written in `docs/01-project-overview.md` through `docs/04-project-structure.md`.
- Phase 2: Django project initialized with Python 3.13 and Django 6.1.3.
- Phase 3: `accounts`, `projects`, and `tasks` app skeletons created and registered with Django.
- Phase 4: project and task models defined, migrations generated and applied to SQLite.
- Phases 5-11: CRUD pages, authentication, ownership checks, Bootstrap UI, filtering, pagination, admin, environment settings, middleware, signals, and tests are implemented.
- Phase 12: learning documentation and the standalone local run guide are complete.

## Technology

- Python 3.13
- Django 6.1.3
- SQLite, Django's default for a new project
- Django Templates for server-rendered HTML
- Bootstrap 5.3 and Bootstrap Icons, loaded from CDNs in the shared base template

## Prerequisites

- Windows with Python 3.13 installed and available through the Python launcher (`py -3.13`).
- A terminal opened at the project root.
- Internet access when installing packages.

The system has other Python interpreters too. Use `py -3.13` for environment creation so the project does not accidentally use the MSYS2 Python selected by `python` in some terminals.

## Installation and Setup

Run these commands from the project root.

### Create and activate a virtual environment

A virtual environment is a project-specific Python installation area. It keeps this project's Django version separate from packages installed for other projects or system tools.

PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Command Prompt:

```bat
py -3.13 -m venv .venv
.venv\Scripts\activate.bat
```

Git Bash:

```bash
py -3.13 -m venv .venv
source .venv/Scripts/activate
```

When activated, the terminal usually shows `(.venv)`. You can also avoid activation and call `.venv/Scripts/python.exe` explicitly.

### Install Python dependencies

```powershell
python -m pip install -r requirements.txt
```

`requirements.txt` currently pins Django 6.1.3. Django installs its own required support packages as dependencies. We do not add packages until a project feature needs them.

### Check the project and create database tables

```powershell
python manage.py check
python manage.py migrate
```

`check` looks for common configuration problems. `migrate` applies the checked-in migrations for Django's built-in apps and our project/task models, creating the local `db.sqlite3` database file. When you change a model during development, first run `python manage.py makemigrations projects tasks` to create a migration file, then run `python manage.py migrate` to apply it.

### Create an administrator account (optional)

```powershell
python manage.py createsuperuser
```

Follow the prompts to create a local account for Django's admin site. Application users can also register from `/accounts/register/`; staff access to the admin is separate from ordinary application access.

### Start the development server

```powershell
python manage.py runserver
```

Open `http://127.0.0.1:8000/` for the dashboard. Anonymous visitors are redirected to the login page. The admin site is at `http://127.0.0.1:8000/admin/` after migrations; sign in there with a superuser account.

Stop the development server with `Ctrl+C` in its terminal.

## URLs Available Now

| URL | Purpose |
| --- | --- |
| `/admin/` | Django's built-in administration site |
| `/accounts/register/` | Create an application account |
| `/accounts/login/` | Sign in |
| `/accounts/logout/` | Sign out using a CSRF-protected POST form |
| `/` | Personal dashboard; requires sign-in |
| `/projects/` | Search and browse owned projects |
| `/projects/create/` | Create a project |
| `/projects/<id>/` | Project details and its tasks |
| `/projects/<id>/tasks/create/` | Add a task to an owned project |
| `/tasks/` | Search, filter, and paginate tasks |

## Configuration and Secrets

`config/settings.py` reads `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, and `DJANGO_ALLOWED_HOSTS` from the process environment. If they are not set, development defaults allow the local server to run. `DJANGO_DEBUG` accepts `True` or `False`; hosts are a comma-separated list.

`.env.example` documents the variable names, but Django does not read `.env` files automatically and this project intentionally has no dotenv package. In PowerShell, set temporary values for the current terminal like this:

```powershell
$env:DJANGO_SECRET_KEY = "your-private-random-value"
$env:DJANGO_DEBUG = "True"
$env:DJANGO_ALLOWED_HOSTS = "127.0.0.1,localhost"
```

Generate a private key locally with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`. Never commit a real key or password. Do not use the development fallback key or `DEBUG=True` in a public deployment; set a private key, `DEBUG=False`, and the correct host names.

The database is SQLite and lives in `db.sqlite3` at the project root. That local data file is ignored by Git.

## Learning Documents

- [Project overview](docs/01-project-overview.md)
- [Django architecture](docs/02-django-architecture.md)
- [Request lifecycle](docs/03-request-lifecycle.md)
- [Project structure](docs/04-project-structure.md)
- [Database design](docs/05-database-design.md)
- [Models and ORM](docs/06-models-and-orm.md)
- [Views and URLs](docs/07-views-and-urls.md)
- [Templates and static files](docs/08-templates-and-static-files.md)
- [Forms and validation](docs/09-forms-and-validation.md)
- [Authentication and permissions](docs/10-authentication-and-permissions.md)
- [Testing](docs/11-testing.md)
- [Django commands reference](docs/12-commands-reference.md)
- [Learning roadmap](docs/13-learning-roadmap.md)
- [Middleware and signals](docs/14-middleware-and-signals.md)
- [Run locally](RUN_LOCAL.md)

## Troubleshooting

**`No module named django`**: make sure the virtual environment is active, or run `.venv/Scripts/python.exe manage.py check` explicitly. Verify the interpreter with `python --version` and Django with `python -m django --version`.

**The wrong Python version is used**: create the environment with `py -3.13 -m venv .venv`. In this workspace, plain `python` may refer to a separate MSYS2 installation.

**Port 8000 is already in use**: choose another local port with `python manage.py runserver 8001` and open `http://127.0.0.1:8001/`.

**The admin page says tables are missing**: stop the server, run `python manage.py migrate`, then start it again.

**A page returns 404**: check the route table above. Detail/edit/delete pages deliberately return 404 when an object is not owned by the signed-in user.# djpy
