"""Admin configuration for task records."""

from django.contrib import admin

from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
	"""Make tasks searchable and filterable for trusted administrators."""

	list_display = ("title", "project", "status", "priority", "due_date")
	list_filter = ("status", "priority", "due_date")
	search_fields = ("title", "description", "project__name", "project__owner__username")
	list_select_related = ("project", "project__owner")
