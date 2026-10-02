from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import CandidateProfile, RecruiterProfile, User


class RegistrationForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=[
            (User.Role.CANDIDATE, "Candidate"),
            (User.Role.RECRUITER, "Recruiter"),
        ]
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email", "role")

    def clean_first_name(self):
        return self.cleaned_data.get("first_name", "").strip()

    def clean_last_name(self):
        return self.cleaned_data.get("last_name", "").strip()

    def clean_username(self):
        username = self.cleaned_data.get("username", "").strip()
        if not username:
            raise forms.ValidationError("Username is required.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if not email:
            raise forms.ValidationError("Email is required.")
        return email


class CandidateProfileForm(forms.ModelForm):
    def clean_headline(self):
        return self.cleaned_data.get("headline", "").strip()

    def clean_bio(self):
        return self.cleaned_data.get("bio", "").strip()

    def clean_location(self):
        return self.cleaned_data.get("location", "").strip()

    class Meta:
        model = CandidateProfile
        fields = (
            "phone_number",
            "location",
            "headline",
            "bio",
            "linkedin_url",
            "portfolio_url",
        )
        widgets = {"bio": forms.Textarea(attrs={"rows": 4})}


class RecruiterProfileForm(forms.ModelForm):
    def clean_job_title(self):
        return self.cleaned_data.get("job_title", "").strip()

    def clean_phone_number(self):
        return self.cleaned_data.get("phone_number", "").strip()

    class Meta:
        model = RecruiterProfile
        fields = ("job_title", "phone_number")
