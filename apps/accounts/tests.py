"""Tests for registration, authentication, logout, and middleware behavior."""

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.test import TestCase, override_settings
from django.urls import reverse


@override_settings(PASSWORD_HASHERS=["django.contrib.auth.hashers.MD5PasswordHasher"])
class AccountViewTests(TestCase):
	"""Check that account forms use Django authentication safely."""

	def test_registration_creates_user_and_starts_session(self):
		"""A valid registration stores a user and logs that user in."""
		response = self.client.post(
			reverse("accounts:register"),
			{
				"username": "newlearner",
				"email": "learner@example.com",
				"password1": "correct-horse-battery-41",
				"password2": "correct-horse-battery-41",
			},
		)

		self.assertRedirects(response, reverse("projects:dashboard"))
		user = get_user_model().objects.get(username="newlearner")
		self.assertEqual(user.email, "learner@example.com")
		self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

	def test_registration_rejects_mismatched_passwords(self):
		"""Invalid passwords redisplay errors and do not create an account."""
		response = self.client.post(
			reverse("accounts:register"),
			{
				"username": "newlearner",
				"password1": "correct-horse-battery-41",
				"password2": "different-password-42",
			},
		)

		self.assertEqual(response.status_code, 200)
		self.assertFalse(get_user_model().objects.filter(username="newlearner").exists())
		self.assertContains(response, "The two password fields didn’t match")

	def test_login_accepts_valid_credentials(self):
		"""AuthenticationForm verifies credentials before login creates a session."""
		user = get_user_model().objects.create_user(
			username="returning", password="correct-horse-battery-41"
		)

		response = self.client.post(
			reverse("accounts:login"),
			{"username": "returning", "password": "correct-horse-battery-41"},
		)

		self.assertRedirects(response, reverse("projects:dashboard"))
		self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

	def test_login_rejects_external_next_url(self):
		"""A supplied redirect target cannot send a user to an untrusted host."""
		get_user_model().objects.create_user(
			username="returning", password="correct-horse-battery-41"
		)

		response = self.client.post(
			reverse("accounts:login"),
			{
				"username": "returning",
				"password": "correct-horse-battery-41",
				"next": "https://example.invalid/",
			},
		)

		self.assertRedirects(response, reverse("projects:dashboard"))

	def test_logout_requires_post_and_ends_session(self):
		"""Logout uses POST and removes the authenticated session."""
		user = get_user_model().objects.create_user(
			username="returning", password="correct-horse-battery-41"
		)
		self.client.force_login(user)

		self.assertEqual(self.client.get(reverse("accounts:logout")).status_code, 405)
		response = self.client.post(reverse("accounts:logout"))

		self.assertRedirects(response, reverse("accounts:login"))
		self.assertNotIn("_auth_user_id", self.client.session)

	@override_settings(DEBUG=True)
	def test_auth_page_includes_development_timing_header(self):
		"""The educational middleware adds timing metadata while DEBUG is on."""
		response = self.client.get(reverse("accounts:login"), HTTP_HOST="localhost")

		self.assertEqual(response.status_code, 200)
		self.assertIn("X-Request-Duration-ms", response.headers)
