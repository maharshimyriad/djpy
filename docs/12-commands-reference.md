# Django Commands Reference

Run commands from the project root with the project's virtual environment active. In this Windows workspace, prefixing commands with `.venv/Scripts/python.exe` avoids accidentally using another installed Python.

| Command | Purpose and example |
| --- | --- |
| `django-admin startproject` | Create project configuration. Here the equivalent initial command was `python -m django startproject config .`; the final dot means “use this directory.” |
| `python manage.py startapp` | Create a feature app. For this layout, first create the `apps` package, then use `python manage.py startapp projects apps/projects`. |
| `python manage.py runserver` | Start Django's local development server: `python manage.py runserver 127.0.0.1:8000`. It is not a production server. |
| `python manage.py makemigrations` | Create migration instructions after model changes: `python manage.py makemigrations projects tasks`. |
| `python manage.py migrate` | Apply unapplied migrations to the configured database: `python manage.py migrate`. |
| `python manage.py createsuperuser` | Interactively create an administrator account for `/admin/`; enter credentials directly in the terminal. |
| `python manage.py shell` | Open Python with Django settings loaded. Example: `from apps.projects.models import Project`, then `Project.objects.count()`. |
| `python manage.py showmigrations` | Show migration files and whether each is applied. Example: `python manage.py showmigrations projects tasks`. |
| `python manage.py check` | Run Django's configuration and model checks without changing the database. |
| `python manage.py test` | Run the automated suite using a temporary test database. Example: `python manage.py test apps.tasks`. |
| `python manage.py collectstatic` | Copy static assets into `STATIC_ROOT` for deployment. It is not needed for local `runserver`; this project does not configure a production `STATIC_ROOT` yet. |

`makemigrations` writes Python migration files; `migrate` executes them against the database. They are separate steps so a developer can inspect a proposed schema change before applying it.