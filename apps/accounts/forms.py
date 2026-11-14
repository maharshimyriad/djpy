"""Forms for creating accounts with Django's built-in user model."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class AccountRegistrationForm(UserCreationForm):
    """Collect a username, optional email, and validated password pair."""

    email = forms.EmailField(required=False)

    class Meta:
        """Connect this form to Django's configured user model."""

        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        """Add Bootstrap-compatible classes without changing validation."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"


class AccountLoginForm(AuthenticationForm):
    """Use Django's credential validation with Bootstrap-compatible widgets."""

    def __init__(self, *args, **kwargs):
        """Add presentation classes without changing authentication validation."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"