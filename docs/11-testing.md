# Testing

## Django Test Framework

Django's test runner discovers `test*.py` modules and `TestCase` subclasses. A `TestCase` creates an isolated test database, runs its tests, and discards that database afterward. Tests can use Django's test client to make requests without starting a web server.

Run the suite from the project root:

```powershell
python manage.py test
```

The current tests live beside their feature code in `apps/accounts/tests.py`, `apps/projects/tests.py`, and `apps/tasks/tests.py`.

## What We Test

- Registration creates a user, rejects mismatched passwords, and signs the user in.
- Login establishes a session; unsafe external `next` URLs are rejected; logout requires POST.
- Project and task models create rows and expose their reverse relationships and defaults.
- Forms reject missing project names and invalid task status choices.
- Project/task creation assigns the current user or verified project on the server.
- Dashboard counts, project search, task filters, pagination, and task-detail templates work.
- A user cannot read, edit, delete, or add tasks to another user's records.
- The development middleware adds its response header only when DEBUG is enabled.
- The task `post_save` receiver logs a saved task.

The test classes temporarily use Django's fast MD5 password hasher to avoid the intentionally expensive production password hashing cost. This override exists only inside tests; application settings keep Django's normal password hasher.

## Understanding Failures

The test output names the failing test and assertion. Read the traceback from the bottom up to the test assertion, then check whether the failure is in the view, form, model, template, or test setup. A 404 in an ownership test is expected; a 500 indicates an unhandled error. Run one failing test by its dotted path while debugging, then rerun the full suite before finishing.