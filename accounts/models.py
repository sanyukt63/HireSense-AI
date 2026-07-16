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
