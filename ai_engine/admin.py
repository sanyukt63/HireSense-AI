from django.contrib import admin

from .models import ATSAssessment, JobSkillRequirement, ResumeParseResult, ResumeSkill, Skill


admin.site.register(Skill)
admin.site.register(ResumeParseResult)
admin.site.register(ResumeSkill)
admin.site.register(JobSkillRequirement)


@admin.register(ATSAssessment)
class ATSAssessmentAdmin(admin.ModelAdmin):
    list_display = ("application", "final_score", "scoring_version", "calculated_at")
    readonly_fields = ("calculated_at",)
