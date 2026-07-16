from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models


class User(AbstractUser):
    """Platform identity with one primary HireSense role."""

    class Role(models.TextChoices):
        CANDIDATE = "candidate", "Candidate"
        RECRUITER = "recruiter", "Recruiter"
        ADMIN = "admin", "Administrator"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CANDIDATE)

    def __str__(self):
        return self.get_full_name() or self.username


class CandidateProfile(models.Model):
    """Candidate-specific information, separated from authentication data."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="candidate_profile")
    phone_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=120, blank=True)
    headline = models.CharField(max_length=180, blank=True)
    bio = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    portfolio_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Candidate profile: {self.user}"


class RecruiterProfile(models.Model):
    """Recruiter-specific information and optional company membership."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="recruiter_profile")
    company = models.ForeignKey("jobs.Company", on_delete=models.SET_NULL, null=True, blank=True, related_name="recruiters")
    job_title = models.CharField(max_length=120, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Recruiter profile: {self.user}"
