# Django Architecture

## What Django Is

Django is a Python web framework: a collection of conventions and tools for receiving web requests, validating data, reading and writing a database, and returning pages. It includes an ORM, URL routing, templates, forms, authentication, security protections, and an administration site.

## The MVT Pattern

Django commonly describes its design as **MVT**:

- **Model** describes stored data and relationships. Django uses model classes to build database queries and, through migrations, database tables.
- **View** handles a request. It decides what data or action is needed and returns a response, often by asking Django to render a template.
- **Template** describes the presentation, usually HTML with placeholders for data and Django template tags.

For example, the `/projects/` page uses the `Project` model, a view that selects only projects belonging to the signed-in user, and a template that displays those projects.

## MVC Compared with MVT

MVC means **Model-View-Controller**. The names are not perfectly interchangeable across frameworks, but a useful comparison is:

| Common MVC term | Closest Django concept | Responsibility |
| --- | --- | --- |
| Model | Model | Data and database operations |
| Controller | View plus URL dispatcher | Route a request and coordinate work |
| View | Template | Present the result to the user |

Django calls the request-handling code a *view*, even though it performs work that another MVC framework might put in a controller. Django's template is closer to MVC's view. The important idea is separation of responsibility, not memorizing a one-to-one naming translation.

## Project Versus App

A **Django project** is the configuration and entry point for one website. Here the `config` package contains settings, the root URL map, middleware, and server entry points.

A **Django app** is a Python package for one area of functionality. Apps can be combined in a project. Our `accounts`, `projects`, and `tasks` apps own related forms, views, URL patterns, and tests. The `projects` and `tasks` apps own the two application models; accounts uses Django's built-in user model. Page templates are grouped in the shared project-level `templates/` directory.

An app does not run by itself. The project enables an app in `INSTALLED_APPS` and can connect that app's URL patterns to the site's URL map.

## Main Components and How They Connect

1. The web server passes an HTTP request to Django.
2. Middleware runs common request and response processing, such as session and authentication support.
3. The URL dispatcher matches the requested path and selects a view.
4. The view reads the request, checks permissions, and may use a form to validate submitted data.
5. A model's ORM interface asks the database for data or saves validated changes.
6. The view supplies data to a template, or redirects to another page.
7. Django returns an HTTP response to the browser.

The actual `/projects/` example is traced in [Request Lifecycle](03-request-lifecycle.md). That walkthrough shows how the pieces connect for a real request.

## App Boundaries

- `accounts`: registration and account-facing forms and views. Django's built-in authentication system supplies the user model, password handling, sessions, login, and logout mechanisms.
- `projects`: project data, project forms, project pages, and checks that a project belongs to the current user.
- `tasks`: task data, task forms and pages, status and priority filtering, and pagination.

Tasks refer to projects, and projects refer to their owner. This gives the application a chain it can check before showing or changing data: the task's project must belong to the signed-in user.