"""Function-based views for registration and session authentication."""

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import AccountLoginForm, AccountRegistrationForm


def register(request):
	"""Validate a registration POST, create the user, and sign them in."""
	if request.user.is_authenticated:
		return redirect("projects:dashboard")

	form = AccountRegistrationForm(
		request.POST if request.method == "POST" else None
	)
	if request.method == "POST" and form.is_valid():
		user = form.save()
		login(request, user)
		messages.success(request, "Your account is ready.")
		return redirect("projects:dashboard")

	return render(request, "accounts/register.html", {"form": form})


def sign_in(request):
	"""Authenticate submitted credentials and start a Django session."""
	if request.user.is_authenticated:
		return redirect("projects:dashboard")

	form = AccountLoginForm(
		request,
		data=request.POST if request.method == "POST" else None,
	)
	if request.method == "POST" and form.is_valid():
		login(request, form.get_user())
		messages.success(request, "Welcome back.")
		next_url = request.POST.get("next") or request.GET.get("next", "")
		if next_url and url_has_allowed_host_and_scheme(
			next_url,
			allowed_hosts={request.get_host()},
			require_https=request.is_secure(),
		):
			return redirect(next_url)
		return redirect("projects:dashboard")

	return render(
		request,
		"accounts/login.html",
		{"form": form, "next": request.GET.get("next", "")},
	)


@login_required
@require_POST
def sign_out(request):
	"""End the current session; POST prevents logout through a simple link."""
	logout(request)
	messages.info(request, "You have been signed out.")
	return redirect("accounts:login")
