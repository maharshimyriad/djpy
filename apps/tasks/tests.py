"""Tests for task persistence, forms, filters, status updates, and ownership."""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.projects.models import Project

from .forms import TaskForm
from .models import Task


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class TaskModelTests(TestCase):
	"""Check task fields, choices, and project reverse relationships."""

	def setUp(self):
		"""Create a project to use as the required task parent."""
		user = get_user_model().objects.create_user(username="owner", password="test-pass")
		self.project = Project.objects.create(owner=user, name="Plan")

	def test_task_uses_defaults_and_belongs_to_project(self):
		"""A new task receives its default status and priority."""
		task = Task.objects.create(project=self.project, title="Write outline")

		self.assertEqual(task.status, Task.Status.PENDING)
		self.assertEqual(task.priority, Task.Priority.MEDIUM)
		self.assertEqual(self.project.tasks.get(), task)
		self.assertEqual(str(task), "Write outline")


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class TaskFormTests(TestCase):
	"""Check task choice validation before saving user input."""

	def test_invalid_status_is_rejected(self):
		"""A value outside Task.Status choices is invalid form data."""
		form = TaskForm(
			{
				"title": "Write outline",
				"description": "",
				"status": "not-a-status",
				"priority": Task.Priority.MEDIUM,
				"due_date": "",
			}
		)

		self.assertFalse(form.is_valid())
		self.assertIn("status", form.errors)


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class TaskViewTests(TestCase):
	"""Check task CRUD, filtering, pagination, and parent ownership rules."""

	def setUp(self):
		"""Create an authenticated user and an owned project."""
		self.user = get_user_model().objects.create_user(
			username="owner", password="test-pass"
		)
		self.project = Project.objects.create(owner=self.user, name="Plan")
		self.client.force_login(self.user)

	def test_task_creation_uses_owned_project_from_url(self):
		"""The route's verified project is used even if POST includes another ID."""
		other_user = get_user_model().objects.create_user(
			username="other", password="test-pass"
		)
		other_project = Project.objects.create(owner=other_user, name="Other")
		response = self.client.post(
			reverse("tasks:task_create", args=[self.project.pk]),
			{
				"title": "Make checklist",
				"description": "",
				"status": Task.Status.PENDING,
				"priority": Task.Priority.HIGH,
				"due_date": "",
				"project": other_project.pk,
			},
		)

		task = Task.objects.get(title="Make checklist")
		self.assertEqual(task.project, self.project)
		self.assertRedirects(response, reverse("tasks:task_detail", args=[task.pk]))

	def test_task_creation_rejects_another_users_project(self):
		"""A guessed project ID cannot be used to add a task to someone else's project."""
		other_user = get_user_model().objects.create_user(
			username="other", password="test-pass"
		)
		other_project = Project.objects.create(owner=other_user, name="Other")

		response = self.client.get(
			reverse("tasks:task_create", args=[other_project.pk])
		)

		self.assertEqual(response.status_code, 404)

	def test_task_status_update_validates_posted_choice(self):
		"""Only a declared status can be saved through the status endpoint."""
		task = Task.objects.create(project=self.project, title="Write outline")
		response = self.client.post(
			reverse("tasks:task_update_status", args=[task.pk]),
			{"status": Task.Status.COMPLETED},
		)

		task.refresh_from_db()
		self.assertEqual(task.status, Task.Status.COMPLETED)
		self.assertRedirects(response, reverse("tasks:task_detail", args=[task.pk]))

		self.client.post(
			reverse("tasks:task_update_status", args=[task.pk]),
			{"status": "invalid"},
		)
		task.refresh_from_db()
		self.assertEqual(task.status, Task.Status.COMPLETED)

	def test_task_list_filters_and_paginates_owned_tasks(self):
		"""Status and priority filters work and pagination returns bounded pages."""
		for index in range(12):
			Task.objects.create(
				project=self.project,
				title=f"Task {index}",
				status=Task.Status.COMPLETED if index == 0 else Task.Status.PENDING,
				priority=Task.Priority.HIGH if index == 0 else Task.Priority.LOW,
			)

		first_page = self.client.get(reverse("tasks:task_list"))
		filtered = self.client.get(
			reverse("tasks:task_list"),
			{"status": Task.Status.COMPLETED, "priority": Task.Priority.HIGH},
		)
		second_page = self.client.get(reverse("tasks:task_list"), {"page": "2"})

		self.assertEqual(first_page.context["page"].paginator.count, 12)
		self.assertEqual(len(first_page.context["page"].object_list), 10)
		self.assertEqual(filtered.context["page"].paginator.count, 1)
		self.assertEqual(len(second_page.context["page"].object_list), 2)

	def test_task_search_matches_description(self):
		"""The task search box finds a phrase in either the title or description."""
		Task.objects.create(
			project=self.project,
			title="Write outline",
			description="Include the research summary",
		)

		response = self.client.get(
			reverse("tasks:task_list"), {"q": "research summary"}
		)

		self.assertEqual(response.context["page"].paginator.count, 1)

	def test_task_detail_edit_and_delete_are_owner_scoped(self):
		"""A task under another user's project cannot be read or changed by this user."""
		other_user = get_user_model().objects.create_user(
			username="other", password="test-pass"
		)
		other_project = Project.objects.create(owner=other_user, name="Other")
		task = Task.objects.create(project=other_project, title="Private task")
		paths = [
			reverse("tasks:task_detail", args=[task.pk]),
			reverse("tasks:task_update", args=[task.pk]),
			reverse("tasks:task_delete", args=[task.pk]),
		]

		for path in paths:
			with self.subTest(path=path):
				self.assertEqual(self.client.get(path).status_code, 404)
		self.assertEqual(self.client.post(paths[2]).status_code, 404)
		self.assertTrue(Task.objects.filter(pk=task.pk).exists())

	def test_task_detail_template_renders_status_choices(self):
		"""The detail template can render choices from the model's TextChoices class."""
		task = Task.objects.create(project=self.project, title="Visible task")

		response = self.client.get(reverse("tasks:task_detail", args=[task.pk]))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Pending")


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class TaskSignalTests(TestCase):
	"""Check that the post_save receiver logs task creation."""

	def test_task_save_emits_activity_log(self):
		"""The registered receiver receives Django's post_save signal."""
		user = get_user_model().objects.create_user(username="signal-owner", password="test-pass")
		project = Project.objects.create(owner=user, name="Signal test")

		with self.assertLogs("apps.tasks.signals", level="INFO") as captured:
			Task.objects.create(project=project, title="Logged task")

		self.assertIn("created", captured.output[0])
