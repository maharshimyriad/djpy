"""Forms for task data and status-only updates."""

from django import forms

from .models import Task


class TaskForm(forms.ModelForm):
    """Validate editable task fields without accepting a project ID from the browser."""

    class Meta:
        """Connect this form to Task and list only fields users may edit."""

        model = Task
        fields = ("title", "description", "status", "priority", "due_date")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "due_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        """Add Bootstrap classes while keeping model-driven field validation."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-select" if isinstance(
                field.widget, forms.Select
            ) else "form-control"


class TaskStatusForm(forms.Form):
    """Allow a task status to change without accepting other task fields."""

    status = forms.ChoiceField(choices=Task.Status.choices)