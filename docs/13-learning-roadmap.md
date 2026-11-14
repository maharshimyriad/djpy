# Learning Roadmap

Concepts are checked only after both an implementation and an explanation exist in this project.

## Beginner Concepts

- [x] Python virtual environment and pinned project dependency
- [x] Django project versus Django app
- [x] MVT architecture and request lifecycle
- [x] Settings, root/app URL maps, ASGI, WSGI, and `manage.py`
- [x] Models, fields, primary keys, foreign keys, and migrations
- [x] SQLite and basic ORM create/read/update/delete queries
- [x] Function-based views, request methods, render, redirects, and responses
- [x] Templates, inheritance, includes, tags, filters, CSS, and static files
- [x] Forms, ModelForms, validation errors, and CSRF protection
- [x] Registration, login, logout, and sessions
- [x] Authentication versus authorization and object ownership checks
- [x] Django Admin registration and list configuration
- [x] Automated tests with Django `TestCase` and test client

## Intermediate Concepts

- [x] Searching, filtering, and paginating QuerySets
- [x] `select_related` and `prefetch_related` fundamentals in the ORM guide
- [x] Django messages and reusable template partials
- [x] Environment-based secret/debug/host configuration
- [x] Custom request/response middleware
- [x] `post_save` signals and receiver registration
- [x] Regression tests for user data isolation
- [ ] Production deployment, HTTPS, and production database configuration
- [ ] More advanced query optimization based on measured workloads
- [ ] Custom user model, only if future identity requirements justify it

## Explore Later

- [ ] Class-based views after becoming comfortable with function-based views
- [ ] Django REST Framework and API design
- [ ] Background jobs and task queues
- [ ] PostgreSQL deployment and backups
- [ ] Accessibility and browser automation beyond the current Django tests