"""Tests for project models, forms, ownership, and project views."""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.tasks.models import Task

from .forms import ProjectForm
from .models import Project


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class ProjectModelTests(TestCase):
	"""Check project persistence and its reverse user relationship."""

	def test_user_can_own_multiple_projects(self):
		"""The owner foreign key can be followed in both directions."""
		user = get_user_model().objects.create_user(username="owner", password="test-pass")
		first = Project.objects.create(owner=user, name="First")
		second = Project.objects.create(owner=user, name="Second")

		self.assertEqual(user.projects.count(), 2)
		self.assertEqual(str(first), "First")
		self.assertEqual(second.owner, user)


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class ProjectFormTests(TestCase):
	"""Check ModelForm validation before data reaches the model."""

	def test_project_name_is_required(self):
		"""A blank required name is rejected by model-driven form validation."""
		form = ProjectForm({"name": "", "description": ""})

		self.assertFalse(form.is_valid())
		self.assertIn("name", form.errors)


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class ProjectViewTests(TestCase):
	"""Check project CRUD routes and isolation between users."""

	def setUp(self):
		"""Create an authenticated owner for each view test."""
		self.user = get_user_model().objects.create_user(
			username="owner", password="test-pass"
		)
		self.client.force_login(self.user)

	def test_project_creation_assigns_current_user_as_owner(self):
		"""The owner comes from request.user, not a submitted owner field."""
		response = self.client.post(
			reverse("projects:project_create"),
			{"name": "Learning app", "description": "Django practice"},
		)

		project = Project.objects.get(name="Learning app")
		self.assertEqual(project.owner, self.user)
		self.assertRedirects(
			response,
			reverse("projects:project_detail", args=[project.pk]),
		)

	def test_dashboard_only_counts_current_users_records(self):
		"""Dashboard statistics do not include another user's projects."""
		other_user = get_user_model().objects.create_user(
			username="other", password="test-pass"
		)
		Project.objects.create(owner=self.user, name="Mine")
		Project.objects.create(owner=other_user, name="Theirs")

		response = self.client.get(reverse("projects:dashboard"))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.context["total_projects"], 1)

	def test_project_search_is_scoped_to_owner(self):
		"""Search results are limited to the current user's records."""
		other_user = get_user_model().objects.create_user(
			username="other", password="test-pass"
		)
		owned_project = Project.objects.create(owner=self.user, name="My notes")
		Task.objects.create(project=owned_project, title="Searchable task")
		Project.objects.create(owner=other_user, name="My notes elsewhere")

		response = self.client.get(reverse("projects:project_list"), {"q": "notes"})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(list(response.context["page"].object_list), [
			owned_project
		])
		self.assertEqual(response.context["page"].object_list[0].task_count, 1)

	def test_another_users_project_is_not_visible_or_mutable(self):
		"""Foreign project IDs return 404 for detail, edit, and delete requests."""
		other_user = get_user_model().objects.create_user(
			username="other", password="test-pass"
		)
		project = Project.objects.create(owner=other_user, name="Private")
		paths = [
			reverse("projects:project_detail", args=[project.pk]),
			reverse("projects:project_update", args=[project.pk]),
			reverse("projects:project_delete", args=[project.pk]),
		]

		for path in paths:
			with self.subTest(path=path):
				self.assertEqual(self.client.get(path).status_code, 404)
		self.assertEqual(
			self.client.post(paths[-1]).status_code,
			404,
		)
		self.assertTrue(Project.objects.filter(pk=project.pk).exists())

	def test_deleting_project_cascades_to_its_tasks(self):
		"""The declared foreign-key cascade removes dependent tasks."""
		project = Project.objects.create(owner=self.user, name="Temporary")
		task = Task.objects.create(project=project, title="Child task")

		response = self.client.post(
			reverse("projects:project_delete", args=[project.pk])
		)

		self.assertRedirects(response, reverse("projects:project_list"))
		self.assertFalse(Task.objects.filter(pk=task.pk).exists())
