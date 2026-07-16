from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160, unique=True)),
                ("website", models.URLField(blank=True)), ("description", models.TextField(blank=True)),
                ("location", models.CharField(blank=True, max_length=120)),
                ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("owner", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="companies_created", to=settings.AUTH_USER_MODEL)),
            ], options={"ordering": ("name",), "verbose_name_plural": "companies"},
        ),
        migrations.CreateModel(
            name="Job",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180)), ("description", models.TextField()),
                ("location", models.CharField(blank=True, max_length=120)),
                ("work_mode", models.CharField(choices=[("onsite", "On-site"), ("hybrid", "Hybrid"), ("remote", "Remote")], default="onsite", max_length=20)),
                ("employment_type", models.CharField(choices=[("full_time", "Full-time"), ("part_time", "Part-time"), ("contract", "Contract"), ("internship", "Internship")], default="full_time", max_length=20)),
                ("minimum_experience_years", models.DecimalField(decimal_places=1, default=0, max_digits=4)),
                ("education_requirement", models.CharField(blank=True, max_length=180)),
                ("status", models.CharField(choices=[("draft", "Draft"), ("open", "Open"), ("closed", "Closed")], default="draft", max_length=20)),
                ("application_deadline", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("company", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="jobs", to="jobs.company")),
                ("created_by", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="jobs_created", to=settings.AUTH_USER_MODEL)),
            ], options={"ordering": ("-created_at",)},
        ),
        migrations.AddIndex(model_name="job", index=models.Index(fields=["status", "-created_at"], name="jobs_job_status_95ebbb_idx")),
        migrations.AddIndex(model_name="job", index=models.Index(fields=["company", "status"], name="jobs_job_company_eaee7e_idx")),
    ]
