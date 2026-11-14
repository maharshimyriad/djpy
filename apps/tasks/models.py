"""Database model for tasks that belong to projects."""

from django.db import models

from apps.projects.models import Project


class Task(models.Model):
	"""A piece of work that must belong to a project."""

	class Status(models.TextChoices):
		"""Stable status values stored in the database and human-readable labels."""

		PENDING = "pending", "Pending"
		IN_PROGRESS = "in_progress", "In progress"
		COMPLETED = "completed", "Completed"

	class Priority(models.TextChoices):
		"""Stable priority values stored in the database and human-readable labels."""

		LOW = "low", "Low"
		MEDIUM = "medium", "Medium"
		HIGH = "high", "High"

	# ForeignKey stores the parent project's ID; the reverse relation is project.tasks.
	project = models.ForeignKey(
		Project,
		on_delete=models.CASCADE,
		related_name="tasks",
	)
	# A concise required label that identifies the work item.
	title = models.CharField(max_length=200)
	# Optional extra detail for the task.
	description = models.TextField(blank=True)
	# choices provide form/model-validation options and human-readable labels; they are not a database constraint.
	status = models.CharField(
		max_length=20,
		choices=Status.choices,
		default=Status.PENDING,
	)
	priority = models.CharField(
		max_length=10,
		choices=Priority.choices,
		default=Priority.MEDIUM,
	)
	# A task may have no deadline; null=True stores SQL NULL and blank=True permits empty form input.
	due_date = models.DateField(blank=True, null=True)
	# Django sets these timestamps when the row is first created and subsequently saved.
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		"""Set a predictable newest-first order for task querysets."""

		ordering = ["-created_at"]

	def __str__(self):
		"""Return a readable task title in the admin and Django shell."""
		return self.title
