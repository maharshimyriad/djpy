"""Admin configuration for project records."""

from django.contrib import admin

from .models import Project


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
	"""Make projects searchable and scannable for trusted administrators."""

	list_display = ("name", "owner", "created_at", "updated_at")
	list_filter = ("created_at", "updated_at")
	search_fields = ("name", "description", "owner__username")
	list_select_related = ("owner",)
