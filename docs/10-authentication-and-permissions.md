# Authentication and Permissions

## User and Authentication

Authentication answers “who is signed in?” Django's built-in `User` model stores credentials and identity fields. We use it because the project needs ordinary username/password accounts and does not require a different identity model. `settings.AUTH_USER_MODEL` is used in the project owner relationship so the model reference follows Django's configuration convention.

Registration uses `UserCreationForm`, including Django's password hashing and password validators. Login checks the credentials and calls Django's `login()` function. Django stores the signed-in user's ID in the session; the browser sends a session cookie on later requests. `AuthenticationMiddleware` reads that session and exposes the user as `request.user`.

Logout is a POST-only view. A POST form with a CSRF token is used because signing out changes session state; a plain GET link should not perform that action.

## Authorization and Ownership

Authorization answers “what may this user access?” `login_required` restricts the dashboard, projects, and task views to signed-in users. It does not by itself protect one user's objects from another user, so each data query also scopes records by ownership.

Projects are selected with `owner=request.user`. Tasks are selected with `project__owner=request.user`, following the task-to-project foreign key. Detail, update, and delete views use these ownership conditions in `get_object_or_404`. A guessed ID therefore returns 404. Task creation first fetches an owned project, and the form does not accept a project ID from the browser.

This is application-level object permission enforcement. Hiding a link or button is not a security check; the view and query must enforce the rule for every request. Automated tests verify that another user's project and task cannot be read or changed.

## Sessions and Messages

Sessions let Django remember a user between requests without storing the password in the browser. The messages framework stores short feedback such as “Project updated” across a redirect and then displays it in the next template response.

## User Model Decision

A custom user model is appropriate when a project needs different authentication fields or identity behavior. It must be selected before the first migrations because authentication tables and foreign keys depend on it. This project already uses Django's default model, so we keep that simple and do not switch models midway through the database history.