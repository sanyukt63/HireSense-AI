 from django import forms

from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("resume", "cover_letter")
        widgets = {"cover_letter": forms.Textarea(attrs={"rows": 6, "placeholder": "Optional note to the hiring team"})}

    def clean_cover_letter(self):
        return self.cleaned_data.get("cover_letter", "").strip()


class ApplicationReviewForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ("status", "recruiter_notes")
        widgets = {"recruiter_notes": forms.Textarea(attrs={"rows": 6, "placeholder": "Internal notes — not visible to the candidate"})}

    def clean_recruiter_notes(self):
        return self.cleaned_data.get("recruiter_notes", "").strip()
