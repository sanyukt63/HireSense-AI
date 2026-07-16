from django.conf import settings
from django.db import models


class Application(models.Model):
    """A candidate's single application to a specific job opening."""

    class Status(models.TextChoices):
        SUBMITTED = "submitted", "Submitted"
        REVIEWED = "reviewed", "Reviewed"
        SHORTLISTED = "shortlisted", "Shortlisted"
        REJECTED = "rejected", "Rejected"

    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE, related_name="applications")
    resume = models.ForeignKey("resume.Resume", on_delete=models.SET_NULL, null=True, related_name="applications")
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SUBMITTED)
    recruiter_notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-applied_at",)
        constraints = [
            models.UniqueConstraint(fields=("candidate", "job"), name="one_application_per_candidate_job")
        ]
        indexes = [models.Index(fields=("job", "status")), models.Index(fields=("candidate", "-applied_at"))]

    def __str__(self):
        return f"{self.candidate} → {self.job}"
