from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [("jobs", "0001_initial"), ("resume", "0001_initial"), ("recruitment", "0001_initial")]
 
    operations = [
        migrations.CreateModel(name="Skill", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("name", models.CharField(max_length=100, unique=True)), ("normalized_name", models.CharField(editable=False, max_length=100, unique=True)),
        ], options={"ordering": ("name",)}),
        migrations.CreateModel(name="ResumeParseResult", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("raw_text", models.TextField()), ("extracted_data", models.JSONField(default=dict)),
            ("parser_version", models.CharField(default="rule-based-v1", max_length=40)), ("processed_at", models.DateTimeField(auto_now=True)),
            ("resume", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="parse_result", to="resume.resume")),
        ]),
        migrations.CreateModel(name="ResumeSkill", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("confidence", models.DecimalField(decimal_places=3, default=1, max_digits=4)),
            ("resume", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="skill_matches", to="resume.resume")),
            ("skill", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="resume_matches", to="ai_engine.skill")),
        ]),
        migrations.CreateModel(name="JobSkillRequirement", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("is_required", models.BooleanField(default=True)), ("weight", models.PositiveSmallIntegerField(default=1)),
            ("job", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="skill_requirements", to="jobs.job")),
            ("skill", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="job_requirements", to="ai_engine.skill")),
        ]),
        migrations.CreateModel(name="ATSAssessment", fields=[
            ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
            ("skill_score", models.DecimalField(decimal_places=2, max_digits=5)), ("experience_score", models.DecimalField(decimal_places=2, max_digits=5)),
            ("education_score", models.DecimalField(decimal_places=2, max_digits=5)), ("keyword_score", models.DecimalField(decimal_places=2, max_digits=5)),
            ("semantic_score", models.DecimalField(decimal_places=2, max_digits=5)), ("final_score", models.DecimalField(decimal_places=2, max_digits=5)),
            ("score_details", models.JSONField(default=dict)), ("scoring_version", models.CharField(default="ats-v1", max_length=40)),
            ("calculated_at", models.DateTimeField(auto_now=True)),
            ("application", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="ats_assessment", to="recruitment.application")),
        ], options={"ordering": ("-final_score", "-calculated_at")}),
        migrations.AddConstraint(model_name="resumeskill", constraint=models.UniqueConstraint(fields=("resume", "skill"), name="one_skill_per_resume")),
        migrations.AddConstraint(model_name="jobskillrequirement", constraint=models.UniqueConstraint(fields=("job", "skill"), name="one_skill_per_job")),
    ]
