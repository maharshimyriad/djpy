"""Django app configuration for task management functionality."""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """Tell Django how to identify and import the tasks app."""

    name = 'apps.tasks'

    def ready(self):
        """Import signal receivers after Django's app registry is ready."""
        from . import signals  # noqa: F401
