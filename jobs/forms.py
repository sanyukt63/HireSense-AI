from django import forms
from django.utils import timezone

from .models import Company, Job


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ("name", "website", "description", "location")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = (
            "title",
            "description",
            "location",
            "work_mode",
            "employment_type",
            "minimum_experience_years",
            "education_requirement",
            "status",
            "application_deadline",
        )
        widgets = {
            "description": forms.Textarea(attrs={"rows": 8}),
            "application_deadline": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_application_deadline(self):
        deadline = self.cleaned_data.get("application_deadline")
        status = self.cleaned_data.get("status")
        if (
            deadline
            and status == Job.Status.OPEN
            and deadline < timezone.localdate()
        ):
            raise forms.ValidationError(
                "An open job must have today or a future application deadline."
            )
        return deadline
