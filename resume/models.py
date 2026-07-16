from pathlib import Path
from uuid import uuid4

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

MAX_RESUME_SIZE_BYTES = 5 * 1024 * 1024
ALLOWED_RESUME_EXTENSIONS = ("pdf", "doc", "docx")


def resume_upload_path(instance, filename):
    """Use generated names so user-supplied filenames never become storage paths."""
    extension = Path(filename).suffix.lower()
    return f"resumes/{instance.candidate_id}/{uuid4().hex}{extension}"


def validate_resume_size(uploaded_file):
    if uploaded_file.size > MAX_RESUME_SIZE_BYTES:
        raise ValidationError("Resume files must be 5 MB or smaller.")


class Resume(models.Model):
    """A versioned candidate-owned resume document."""

    candidate = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="resumes")
    title = models.CharField(max_length=120)
    original_filename = models.CharField(max_length=255)
    document = models.FileField(
        upload_to=resume_upload_path,
        validators=[
            FileExtensionValidator(allowed_extensions=ALLOWED_RESUME_EXTENSIONS),
            validate_resume_size,
        ],
    )
    file_size = models.PositiveBigIntegerField()
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-is_primary", "-uploaded_at")
        constraints = [
            models.UniqueConstraint(
                fields=("candidate",),
                condition=models.Q(is_primary=True),
                name="one_primary_resume_per_candidate",
            )
        ]

    def save(self, *args, **kwargs):
        if self.document:
            self.original_filename = Path(self.document.name).name
            self.file_size = self.document.size
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Remove the stored document when its database record is deleted."""
        storage, name = self.document.storage, self.document.name
        super().delete(*args, **kwargs)
        if name:
            storage.delete(name)

    def __str__(self):
        return f"{self.title} ({self.candidate})"
