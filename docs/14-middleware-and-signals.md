# Middleware and Signals

## Middleware

Middleware is a chain of request/response hooks. Each middleware can inspect or change a request before the view, then inspect or change the response after the view returns. In `config/settings.py`, `MIDDLEWARE` order is significant: the request travels from top to bottom and the response unwinds in reverse order.

`config/middleware.py` contains `RequestTimingMiddleware`. Its `__call__()` records a start time, calls the next middleware or view, and adds an `X-Request-Duration-ms` response header when `DEBUG=True`. This makes the request/response cycle visible without changing page content. It is an educational example, not production monitoring; the header is deliberately omitted when debug mode is off.

Middleware is suitable for behavior that should apply broadly to many requests. It should not become a home for project-specific business rules that belong in views or models.

## Signals

A signal lets one part of Django announce that an event happened while another part listens for it. Django emits `post_save` after a model's `save()` method completes. `apps/tasks/signals.py` listens for saves of `Task` and logs whether the row was created or updated.

`TasksConfig.ready()` imports the receiver module after Django's app registry is ready. The `@receiver` decorator connects the function to `post_save` for `Task`; the `created` argument distinguishes inserts from updates. The automated test checks that creating a task emits the log entry.

Signals can hide control flow and make behavior harder to follow, and bulk operations such as `QuerySet.update()` do not emit `post_save`. Keep them for decoupled cross-cutting reactions. If a normal view is the only place that needs to perform an action, calling that action directly is usually clearer.