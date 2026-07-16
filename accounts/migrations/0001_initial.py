from django.conf import settings
from django.contrib.auth.models import UserManager
from django.db import migrations, models
import django.contrib.auth.models
import django.contrib.auth.validators


class Migration(migrations.Migration):
    initial = True
    dependencies = [("auth", "0012_alter_user_first_name_max_length")]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                ("last_login", models.DateTimeField(blank=True, null=True, verbose_name="last login")),
                ("is_superuser", models.BooleanField(default=False, help_text="Designates that this user has all permissions without explicitly assigning them.", verbose_name="superuser status")),
                ("username", models.CharField(error_messages={"unique": "A user with that username already exists."}, help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.", max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name="username")),
                ("first_name", models.CharField(blank=True, max_length=150, verbose_name="first name")),
                ("last_name", models.CharField(blank=True, max_length=150, verbose_name="last name")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("is_staff", models.BooleanField(default=False, help_text="Designates whether the user can log into this admin site.", verbose_name="staff status")),
                ("is_active", models.BooleanField(default=True, help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.", verbose_name="active")),
                ("date_joined", models.DateTimeField(auto_now_add=True, verbose_name="date joined")),
                ("role", models.CharField(choices=[("candidate", "Candidate"), ("recruiter", "Recruiter"), ("admin", "Administrator")], default="candidate", max_length=20)),
                ("groups", models.ManyToManyField(blank=True, help_text="The groups this user belongs to.", related_name="user_set", related_query_name="user", to="auth.group", verbose_name="groups")),
                ("user_permissions", models.ManyToManyField(blank=True, help_text="Specific permissions for this user.", related_name="user_set", related_query_name="user", to="auth.permission", verbose_name="user permissions")),
            ],
            options={"verbose_name": "user", "verbose_name_plural": "users", "abstract": False},
            managers=[("objects", UserManager())],
        ),
        migrations.CreateModel(name="CandidateProfile", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("phone_number", models.CharField(blank=True, max_length=20)), ("location", models.CharField(blank=True, max_length=120)),
            ("headline", models.CharField(blank=True, max_length=180)), ("bio", models.TextField(blank=True)),
            ("linkedin_url", models.URLField(blank=True)), ("portfolio_url", models.URLField(blank=True)),
            ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
            ("user", models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="candidate_profile", to=settings.AUTH_USER_MODEL)),
        ]),
        migrations.CreateModel(name="RecruiterProfile", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("company_name", models.CharField(blank=True, max_length=160)), ("job_title", models.CharField(blank=True, max_length=120)),
            ("phone_number", models.CharField(blank=True, max_length=20)), ("company_website", models.URLField(blank=True)),
            ("company_description", models.TextField(blank=True)), ("created_at", models.DateTimeField(auto_now_add=True)),
            ("updated_at", models.DateTimeField(auto_now=True)),
            ("user", models.OneToOneField(on_delete=models.deletion.CASCADE, related_name="recruiter_profile", to=settings.AUTH_USER_MODEL)),
        ]),
    ]
