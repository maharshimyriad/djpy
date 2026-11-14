# Forms and Validation

## Django Forms and ModelForms

A Django `Form` describes accepted input and validation. A `ModelForm` derives fields and basic validation from a model, reducing duplicated rules. `ProjectForm` exposes only a project's name and description. `TaskForm` exposes task fields but deliberately omits `project`; the view assigns a project only after checking that the signed-in user owns it.

The account registration form extends Django's `UserCreationForm`. Django checks that passwords match, runs the configured password validators, and hashes the password when saving. Login uses Django's `AuthenticationForm`, which validates credentials without exposing whether a username or password was incorrect.

## GET, POST, and Errors

On GET, a view creates an unbound form and renders it. On POST, it binds `request.POST`, calls `is_valid()`, and either saves/redirects or renders the same page with errors. Validated values are in `cleaned_data`; a `ModelForm` can save them after validation.

Field validation checks such as required values and choices are supplied by the fields. A form can implement `clean_<field>()` for a rule about one field, or `clean()` for a rule involving multiple fields. This project has no extra cross-field rule that needs a custom `clean()` method.

`templates/includes/form_fields.html` renders labels, widgets, help text, field errors, and non-field errors. Errors are displayed near the form that needs correction.

## CSRF Protection

Cross-Site Request Forgery (CSRF) is an attack that tricks a browser into submitting a request using a user's existing session. Django's CSRF middleware checks a secret token on unsafe requests. Every POST form in these templates includes `{% csrf_token %}`. GET forms are used for read-only search and filters and do not change data.

The model's `choices` help forms validate status and priority. Calling `model.save()` directly does not run `full_clean()`, so application code must validate browser input through a form before saving it.