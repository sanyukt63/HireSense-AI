from django.db import models


class Skill(models.Model):
    """Canonical skill vocabulary shared by resumes and job requirements."""

    name = models.CharField(max_length=100, unique=True)
    normalized_name = models.CharField(max_length=100, unique=True, editable=False)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        self.normalized_name = self.name.strip().lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ResumeParseResult(models.Model):
    resume = models.OneToOneField("resume.Resume", on_delete=models.CASCADE, related_name="parse_result")
    raw_text = models.TextField()
    extracted_data = models.JSONField(default=dict)
    parser_version = models.CharField(max_length=40, default="rule-based-v1")
    processed_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parsed {self.resume}"


class ResumeSkill(models.Model):
    resume = models.ForeignKey("resume.Resume", on_delete=models.CASCADE, related_name="skill_matches")
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT, related_name="resume_matches")
    confidence = models.DecimalField(max_digits=4, decimal_places=3, default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("resume", "skill"), name="one_skill_per_resume")]


class JobSkillRequirement(models.Model):
    job = models.ForeignKey("jobs.Job", on_delete=models.CASCADE, related_name="skill_requirements")
    skill = models.ForeignKey(Skill, on_delete=models.PROTECT, related_name="job_requirements")
    is_required = models.BooleanField(default=True)
    weight = models.PositiveSmallIntegerField(default=1)

    class Meta:
        constraints = [models.UniqueConstraint(fields=("job", "skill"), name="one_skill_per_job")]


class ATSAssessment(models.Model):
    """Reproducible ATS scores for a specific application and scoring version."""

    application = models.OneToOneField("recruitment.Application", on_delete=models.CASCADE, related_name="ats_assessment")
    skill_score = models.DecimalField(max_digits=5, decimal_places=2)
    experience_score = models.DecimalField(max_digits=5, decimal_places=2)
    education_score = models.DecimalField(max_digits=5, decimal_places=2)
    keyword_score = models.DecimalField(max_digits=5, decimal_places=2)
    semantic_score = models.DecimalField(max_digits=5, decimal_places=2)
    final_score = models.DecimalField(max_digits=5, decimal_places=2)
    score_details = models.JSONField(default=dict)
    scoring_version = models.CharField(max_length=40, default="ats-v1")
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-final_score", "-calculated_at")

    def __str__(self):
        return f"ATS {self.final_score}: {self.application}"
