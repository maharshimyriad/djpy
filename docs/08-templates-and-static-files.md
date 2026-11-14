# Templates and Static Files

## Django Templates

Django templates turn view context into HTML. Project-wide templates are in `templates/`, configured by `TEMPLATES[0]['DIRS']` in `config/settings.py`. App pages are grouped into `templates/accounts/`, `templates/projects/`, and `templates/tasks/`; shared parts live in `templates/includes/`.

`templates/base.html` is the shared page frame. A page uses `{% extends "base.html" %}` and fills named `{% block %}` sections. `{% include %}` reuses a fragment such as the sidebar, message list, task table, or form fields. This keeps navigation and repeated markup consistent.

Views pass a context dictionary. For example, `project_detail` supplies `project` and `task_page`; the template reads them with `{{ project.name }}`. The built-in `date`, `truncatewords`, and `default` filters format values. `{% url %}` reverses a named route, and `{% csrf_token %}` protects POST forms.

## Shared Layout and Components

The base template checks the authenticated user and displays the responsive sidebar and profile menu for signed-in users; login and registration use a centered public layout. Reusable includes render messages, form fields, projects, tasks, and pagination. Django's messages context processor makes queued feedback available to templates.

## Static Files

Static files are assets that do not change per request, such as CSS, JavaScript, and images. `STATIC_URL` is their browser URL prefix. `STATICFILES_DIRS` tells Django where this project's source assets live: `static/css/app.css` and `static/js/app.js`. Templates use `{% load static %}` and `{% static 'css/app.css' %}` so the correct URL is generated.

Bootstrap 5.3 and Bootstrap Icons are included from a CDN in `base.html`; the project keeps its additional design rules in `app.css`. `app.js` uses Bootstrap's alert API to dismiss success/error messages after five seconds. The Bootstrap bundle also handles the responsive offcanvas navigation and dropdown.

During development, `runserver` serves static files when `DEBUG=True`. A production deployment must collect and serve static files through an appropriate static-file server; `collectstatic` is documented in the command reference.