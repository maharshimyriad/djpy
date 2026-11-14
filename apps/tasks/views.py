"""Request handlers for user-owned tasks and task filtering."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from apps.projects.models import Project

from .forms import TaskForm, TaskStatusForm
from .models import Task


def _owned_task_or_404(user, pk):
	"""Find a task only when its parent project belongs to the given user."""
	return get_object_or_404(
		Task.objects.select_related("project"),
		pk=pk,
		project__owner=user,
	)


@login_required
def task_list(request):
	"""Filter and paginate tasks across the signed-in user's projects."""
	tasks = Task.objects.filter(project__owner=request.user).select_related("project")
	selected_status = request.GET.get("status", "")
	selected_priority = request.GET.get("priority", "")
	search_query = request.GET.get("q", "").strip()

	if selected_status in Task.Status.values:
		tasks = tasks.filter(status=selected_status)
	if selected_priority in Task.Priority.values:
		tasks = tasks.filter(priority=selected_priority)
	if search_query:
		tasks = tasks.filter(
			Q(title__icontains=search_query)
			| Q(description__icontains=search_query)
		)

	page = Paginator(tasks, 10).get_page(request.GET.get("page"))
	return render(
		request,
		"tasks/task_list.html",
		{
			"page": page,
			"selected_status": selected_status,
			"selected_priority": selected_priority,
			"search_query": search_query,
			"status_choices": Task.Status.choices,
			"priority_choices": Task.Priority.choices,
		},
	)


@login_required
@require_http_methods(["GET", "POST"])
def task_create(request, project_pk):
	"""Create a task only inside a project owned by the signed-in user."""
	project = get_object_or_404(Project, pk=project_pk, owner=request.user)
	form = TaskForm(request.POST if request.method == "POST" else None)
	if request.method == "POST" and form.is_valid():
		task = form.save(commit=False)
		task.project = project
		task.save()
		messages.success(request, "Task created.")
		return redirect("tasks:task_detail", pk=task.pk)

	return render(
		request,
		"tasks/task_form.html",
		{"form": form, "project": project},
	)


@login_required
def task_detail(request, pk):
	"""Show task details after checking the parent project's owner."""
	task = _owned_task_or_404(request.user, pk)
	return render(request, "tasks/task_detail.html", {"task": task})


@login_required
@require_http_methods(["GET", "POST"])
def task_update(request, pk):
	"""Validate and save editable fields for an owned task."""
	task = _owned_task_or_404(request.user, pk)
	form = TaskForm(
		request.POST if request.method == "POST" else None,
		instance=task,
	)
	if request.method == "POST" and form.is_valid():
		task = form.save()
		messages.success(request, "Task updated.")
		return redirect("tasks:task_detail", pk=task.pk)

	return render(
		request,
		"tasks/task_form.html",
		{"form": form, "project": task.project, "task": task},
	)


@login_required
@require_http_methods(["GET", "POST"])
def task_delete(request, pk):
	"""Confirm deletion of an owned task."""
	task = _owned_task_or_404(request.user, pk)
	if request.method == "POST":
		task.delete()
		messages.success(request, "Task deleted.")
		return redirect("tasks:task_list")

	return render(request, "tasks/task_confirm_delete.html", {"task": task})


@login_required
@require_POST
def task_update_status(request, pk):
	"""Validate a status-only POST and save it without accepting other fields."""
	task = _owned_task_or_404(request.user, pk)
	form = TaskStatusForm(request.POST)
	if form.is_valid():
		task.status = form.cleaned_data["status"]
		task.save(update_fields=["status", "updated_at"])
		messages.success(request, "Task status updated.")
	else:
		messages.error(request, "Choose a valid task status.")
	return redirect("tasks:task_detail", pk=task.pk)
