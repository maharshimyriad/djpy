"""Request handlers for the dashboard and user-owned projects."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from apps.tasks.models import Task

from .forms import ProjectForm
from .models import Project


@login_required
def dashboard(request):
	"""Show statistics and recent records belonging to the signed-in user."""
	projects = Project.objects.filter(owner=request.user)
	tasks = Task.objects.filter(project__owner=request.user)
	context = {
		"total_projects": projects.count(),
		"total_tasks": tasks.count(),
		"pending_tasks": tasks.filter(status=Task.Status.PENDING).count(),
		"completed_tasks": tasks.filter(status=Task.Status.COMPLETED).count(),
		"recent_tasks": tasks.select_related("project").order_by("-created_at")[:5],
		"recent_projects": projects.annotate(task_count=Count("tasks")).order_by(
			"-updated_at"
		)[:5],
	}
	return render(request, "projects/dashboard.html", context)


@login_required
def project_list(request):
	"""List and search only projects owned by the current user."""
	projects = Project.objects.filter(owner=request.user).annotate(
		task_count=Count("tasks")
	)
	search_query = request.GET.get("q", "").strip()
	if search_query:
		projects = projects.filter(
			Q(name__icontains=search_query)
			| Q(description__icontains=search_query)
		)

	projects = projects.order_by("-updated_at", "name")
	page = Paginator(projects, 8).get_page(request.GET.get("page"))
	return render(
		request,
		"projects/project_list.html",
		{"page": page, "search_query": search_query},
	)


@login_required
def project_detail(request, pk):
	"""Show one owned project and a page of its tasks; unknown ownership is a 404."""
	project = get_object_or_404(Project, pk=pk, owner=request.user)
	task_page = Paginator(
		project.tasks.select_related("project"), 8
	).get_page(request.GET.get("page"))
	return render(
		request,
		"projects/project_detail.html",
		{"project": project, "task_page": task_page},
	)


@login_required
@require_http_methods(["GET", "POST"])
def project_create(request):
	"""Validate a project form and assign ownership on the server, not from POST data."""
	form = ProjectForm(request.POST if request.method == "POST" else None)
	if request.method == "POST" and form.is_valid():
		project = form.save(commit=False)
		project.owner = request.user
		project.save()
		messages.success(request, "Project created.")
		return redirect("projects:project_detail", pk=project.pk)

	return render(request, "projects/project_form.html", {"form": form})


@login_required
@require_http_methods(["GET", "POST"])
def project_update(request, pk):
	"""Edit an owned project after validating submitted fields."""
	project = get_object_or_404(Project, pk=pk, owner=request.user)
	form = ProjectForm(
		request.POST if request.method == "POST" else None,
		instance=project,
	)
	if request.method == "POST" and form.is_valid():
		project = form.save()
		messages.success(request, "Project updated.")
		return redirect("projects:project_detail", pk=project.pk)

	return render(
		request,
		"projects/project_form.html",
		{"form": form, "project": project},
	)


@login_required
@require_http_methods(["GET", "POST"])
def project_delete(request, pk):
	"""Confirm deletion of an owned project and its related tasks."""
	project = get_object_or_404(Project, pk=pk, owner=request.user)
	if request.method == "POST":
		project.delete()
		messages.success(request, "Project and its tasks were deleted.")
		return redirect("projects:project_list")

	return render(request, "projects/project_confirm_delete.html", {"project": project})
