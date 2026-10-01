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
    class Meta:
        model = RecruiterProfile
        fields = ("job_title", "phone_number")
