# Request Lifecycle

This walkthrough follows a real feature: a signed-in user opens `/projects/` to see their projects. The route is implemented, and the same sequence applies to task and dashboard pages.

## Browser to Response

```text
Browser
  -> HTTP request: GET /projects/
  -> Django middleware
  -> root URL dispatcher: config/urls.py
  -> projects URL patterns
  -> project-list view
  -> Project model / Django ORM
  -> SQLite database
  -> project-list template + base template
  -> HTTP response containing HTML
  -> Browser
```

## Step by Step

1. **Browser and HTTP request.** The browser asks for `/projects/` using HTTP `GET`, which conventionally requests a page without changing stored data. The browser also sends its session cookie if the user has signed in.
2. **Middleware.** Built-in session and authentication middleware restore the signed-in user as `request.user`. Our `RequestTimingMiddleware` measures the request and adds a development-only response header. Middleware runs before and after the view as the response returns.
3. **URL dispatcher.** Django checks `config/urls.py`, which includes the app maps. `apps/projects/urls.py` matches `/projects/` and selects `project_list` in `apps/projects/views.py`.
4. **View.** `project_list(request)` receives an `HttpRequest`. `login_required` redirects anonymous users; the view scopes its query to `owner=request.user`, applies search and pagination, then calls `render()` to return an `HttpResponse`.
5. **Model and ORM.** `Project.objects.filter(owner=request.user)` becomes a database query. The ORM turns Python model operations into SQL. Filtering by owner is an access-control boundary; a URL or hidden button is never proof that a record belongs to the user.
6. **Database.** SQLite reads rows from `projects_project` and, for task pages, `tasks_task`. A GET list request reads data and does not change project rows.
7. **Template.** The view passes the page of projects and search term as context. `templates/projects/project_list.html` extends `templates/base.html`; shared partials render the navigation and project cards. The base template loads Bootstrap and `static/css/app.css`.
8. **HTTP response.** Django renders HTML and returns it to the browser. The browser then requests CSS, JavaScript, Bootstrap, icons, and fonts separately.

## A Form Submission Is Different

Creating a project starts with a `GET` to `/projects/create/`, which displays an empty `ProjectForm`. Submitting it sends `POST`; the CSRF middleware checks the token, the form validates fields, and the view assigns `request.user` as owner before saving. The view redirects to the new project's detail page, causing a fresh GET. Invalid data is not saved; the same form is rendered with errors.