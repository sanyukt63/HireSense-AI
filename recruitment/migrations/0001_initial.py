from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("jobs", "0001_initial"),
        ("resume", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Application",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("cover_letter", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("submitted", "Submitted"), ("reviewed", "Reviewed"), ("shortlisted", "Shortlisted"), ("rejected", "Rejected")], default="submitted", max_length=20)),
                ("recruiter_notes", models.TextField(blank=True)),
                ("applied_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("candidate", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to=settings.AUTH_USER_MODEL)),
                ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="applications", to="jobs.job")),
                ("resume", models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="applications", to="resume.resume")),
            ], options={"ordering": ("-applied_at",)},
        ),
        migrations.AddConstraint(model_name="application", constraint=models.UniqueConstraint(fields=("candidate", "job"), name="one_application_per_candidate_job")),
        migrations.AddIndex(model_name="application", index=models.Index(fields=["job", "status"], name="recruitment_job_status_idx")),
        migrations.AddIndex(model_name="application", index=models.Index(fields=["candidate", "-applied_at"], name="recruitment_candidate_date_idx")),
    ]
