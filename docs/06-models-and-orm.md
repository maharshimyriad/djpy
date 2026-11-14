# Models and ORM

## Models and Fields

A Django model is a Python class that describes a kind of database row. Django uses the class both to build database schema migrations and to provide Python methods for querying and changing rows.

`Project` in `apps/projects/models.py` has an owner foreign key, a required name, an optional description, and creation/update timestamps. `Task` in `apps/tasks/models.py` has a required project foreign key and title, optional description and due date, status and priority choices, and timestamps. Django supplies each model's `id` primary key automatically.

`CharField` stores bounded-length text and requires `max_length`. `TextField` stores longer text. `DateField` stores a date without a time. `DateTimeField(auto_now_add=True)` records the creation time; `auto_now=True` refreshes the update time on each save. `blank=True` allows empty form input. `null=True` allows SQL `NULL`; the optional task due date uses both because it can be omitted from a form and has no date in the database.

## Choices

`Task.Status` and `Task.Priority` use `models.TextChoices`. The database stores stable short values such as `in_progress` and `high`; Django forms and templates can use their human-readable labels. Defaults mean a new task starts as pending with medium priority. Choices support form and model validation, but they do not create a database constraint, and calling `save()` directly does not automatically run `full_clean()`. Code should use the declared constants and validate user input through a form.

## Relationships

`Project.owner` points to `settings.AUTH_USER_MODEL`, Django's configured user model. Using this setting is more flexible and is the recommended relationship pattern, even though this learning project currently uses Django's built-in `User` model.

`Task.project` points to `Project`. The `related_name` values let Python follow the relationship in reverse: `user.projects.all()` and `project.tasks.all()`. `on_delete=models.CASCADE` tells Django to remove dependent rows when their parent is deleted.

## Migrations

A migration is a versioned set of database changes. It lets Django compare the model description in Python with the schema already recorded for the database.

```powershell
python manage.py makemigrations projects tasks
python manage.py migrate
```

`makemigrations` created `0001_initial.py` for each app. The task migration depends on the project migration, since its table has a foreign key to the project table. `migrate` applied both and recorded them as applied. `makemigrations` does not itself edit the database; `migrate` does not rewrite the model source.

## QuerySets and CRUD

The ORM (object-relational mapper) translates Python operations on models into SQL. A `QuerySet` represents a database query. QuerySets are generally lazy: Django waits to run the query until results are needed.

Examples below assume `user` is a `User` object that has already been retrieved or supplied by a signed-in request:

```python
from apps.projects.models import Project
from apps.tasks.models import Task

# Create rows. Each task must be connected to a saved project.
project = Project.objects.create(owner=user, name="Website refresh")
task = Task.objects.create(project=project, title="Draft the home page")

# Read a user's projects and their pending tasks.
projects = Project.objects.filter(owner=user)
pending_tasks = Task.objects.filter(
    project__owner=user,
    status=Task.Status.PENDING,
)

# Update a task, then save the change.
task.status = Task.Status.IN_PROGRESS
task.save()

# Delete a row. Deleting a project also cascades to its tasks.
project.delete()
```

`filter()` narrows a QuerySet and `order_by()` changes its ordering. The `project__owner` lookup follows foreign keys from task to project to owner. For a security-sensitive page, filtering by the current user is important; never fetch a user-owned object by an unverified URL ID alone.

## Avoiding Extra Queries

`select_related()` follows foreign keys in one SQL query. For example, `Task.objects.select_related("project", "project__owner")` is useful when a page displays each task's project and owner.

`prefetch_related()` loads related rows in a separate query and joins them in Python. For example, `Project.objects.filter(owner=user).prefetch_related("tasks")` is useful when a page displays many projects and each project's tasks. These optimizations are useful when the page needs the related objects; they are not required for every query.