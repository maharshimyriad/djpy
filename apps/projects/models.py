"""Database model for user-owned projects."""

from django.conf import settings
from django.db import models


class Project(models.Model):
	"""A project owned by one user and containing zero or more tasks."""

	# ForeignKey stores the owner's user ID; the reverse relation is user.projects.
	owner = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		related_name="projects",
	)
	# The required name is the short label shown in project lists and headings.
	name = models.CharField(max_length=150)
	# blank=True allows an empty description in forms while keeping a non-NULL database value.
	description = models.TextField(blank=True)
	# Django sets these timestamps when the row is first created and subsequently saved.
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		"""Set a predictable default order for project querysets."""

		ordering = ["-updated_at", "name"]

	def __str__(self):
		"""Return a readable project name in the admin and Django shell."""
		return self.name
