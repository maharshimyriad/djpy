"""ModelForm for validating project fields from browser submissions."""

from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    """Expose only editable project fields; the view assigns the owner."""

    class Meta:
        """Tell Django which model and fields this form represents."""

        model = Project
        fields = ("name", "description")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        """Add Bootstrap classes while retaining ModelForm validation."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"