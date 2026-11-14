# Views and URLs

## URL Patterns

Django starts with `config/urls.py`. Its `path()` entries include the three app URL files and the admin site. Each app sets an `app_name`, so templates and views can reverse a route by a stable name, for example `projects:project_detail`, instead of hard-coding `/projects/12/`.

The `<int:pk>` part of a pattern captures an integer from the path and passes it to the view as `pk`. The project detail route then calls `project_detail(request, pk)`. `include()` delegates a group of paths to an app, which keeps the root URL map short.

## Function-Based Views

A function-based view receives a Django `HttpRequest` and returns an `HttpResponse`. Our `dashboard()` view in `apps/projects/views.py` reads `request.user`, queries that user's projects and tasks, prepares a context dictionary, and calls `render()` to produce HTML.

`render(request, template_name, context)` finds and renders a template, then returns an HTTP response. `redirect()` returns an HTTP redirect response, asking the browser to request another named route. After a successful form POST, redirecting avoids accidentally submitting the same form again when the page is refreshed.

## GET and POST

`GET` requests display pages, read filters, or request details. `POST` requests submit changes. Project creation illustrates the pattern: a `GET /projects/create/` renders an empty form; a `POST` validates it; valid data is saved and redirected to the new project's detail page. Destructive changes and logout also require POST.

`request.GET` and `request.POST` are mappings of submitted values. Treat both as untrusted input. Views pass POST data into a Django form, then use `form.cleaned_data` or `form.save()` only after `form.is_valid()` succeeds.

## Responses, Redirects, and Access

The app's views return a rendered page, redirect, or a 404 response when an object does not belong to the signed-in user. `login_required` redirects anonymous users to the configured login URL. Ownership is checked in ORM lookups such as `get_object_or_404(Project, pk=pk, owner=request.user)`, not merely by hiding a link in a template.

Example request path:

```text
GET /projects/12/
  -> config/urls.py includes apps.projects.urls
  -> project_detail(request, pk=12)
  -> get_object_or_404 filters by pk AND request.user
  -> render projects/project_detail.html with project and task_page
```