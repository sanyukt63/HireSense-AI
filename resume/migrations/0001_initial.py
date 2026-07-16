import django.core.validators
from django.conf import settings
from django.db import migrations, models
import resume.models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Resume",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=120)), ("original_filename", models.CharField(max_length=255)),
                ("document", models.FileField(upload_to=resume.models.resume_upload_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=("pdf", "doc", "docx")), resume.models.validate_resume_size])),
                ("file_size", models.PositiveBigIntegerField()), ("is_primary", models.BooleanField(default=False)),
                ("uploaded_at", models.DateTimeField(auto_now_add=True)), ("updated_at", models.DateTimeField(auto_now=True)),
                ("candidate", models.ForeignKey(on_delete=models.deletion.CASCADE, related_name="resumes", to=settings.AUTH_USER_MODEL)),
            ], options={"ordering": ("-is_primary", "-uploaded_at")},
        ),
        migrations.AddConstraint(model_name="resume", constraint=models.UniqueConstraint(condition=models.Q(("is_primary", True)), fields=("candidate",), name="one_primary_resume_per_candidate")),
    ]
