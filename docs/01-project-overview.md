# Project Overview

## What We Are Building

This is a personal project and task manager. Registered people can create projects and organize tasks within them. Each person must only see and change their own data, enforced by ownership-scoped views and queries.

## Why This Project

A project manager gives us realistic examples of the most important parts of Django without needing a complicated domain. It has users, related database records, forms, pages, and permissions:

- One user can own many projects.
- One project can contain many tasks.
- Pages can create, display, update, and delete those records.
- Authentication identifies the signed-in user, and ownership checks protect that user's records.

## Features

- Register, sign in, and sign out.
- View a dashboard with project and task counts.
- Create, list, view, edit, and delete projects.
- Create, list, view, edit, and delete tasks within projects.
- Set task status, priority, and due date.
- Search and filter tasks, then browse results using pagination.
- Use Django's built-in administration site for development and data inspection.

## Architecture

## Architecture
The site uses Django's server-rendered templates. A browser requests a URL, Django selects a view, the view uses models and the ORM to work with SQLite, and a template turns the result into HTML. Bootstrap 5.3 provides responsive layout and common interface components; the project's CSS and small JavaScript file live under `static/`.

The project is divided by responsibility:

- `config` holds project-wide settings and the root URL map.
- `accounts` handles registration and authentication pages.
- `projects` handles projects and their ownership.
- `tasks` handles tasks, task filters, and task-specific pages.

The application uses Django's built-in `User` model. A custom user model is useful when an application needs a different login identifier or identity fields that belong to every user; this application does not have that requirement. The built-in model keeps the design simpler. Changing user models after migrations can be difficult, so choose a custom model before the first migration if future requirements need one.

## Learning Goals

## Concepts Covered

The project demonstrates Django projects and apps, models and relationships, migrations and ORM queries, function-based views and URL routing, templates and static files, forms and CSRF, authentication and authorization, ownership checks, tests, admin, messages, pagination, environment settings, middleware, and signals.

Start with [Django Architecture](02-django-architecture.md), follow the actual request in [Request Lifecycle](03-request-lifecycle.md), and use [Project Structure](04-project-structure.md) as a file map. The [Learning Roadmap](13-learning-roadmap.md) distinguishes completed concepts from topics left for later exploration.