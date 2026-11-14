"""URL patterns for task lists and task CRUD/status actions."""

from django.urls import path

from . import views

app_name = "tasks"

urlpatterns = [
    path("tasks/", views.task_list, name="task_list"),
    path(
        "projects/<int:project_pk>/tasks/create/",
        views.task_create,
        name="task_create",
    ),
    path("tasks/<int:pk>/", views.task_detail, name="task_detail"),
    path("tasks/<int:pk>/edit/", views.task_update, name="task_update"),
    path("tasks/<int:pk>/delete/", views.task_delete, name="task_delete"),
    path(
        "tasks/<int:pk>/status/",
        views.task_update_status,
        name="task_update_status",
    ),
]