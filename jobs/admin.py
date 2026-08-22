from django.contrib import admin

from .models import Company, Job


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "location", "owner", "created_at")
    search_fields = ("name", "location")

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company", "status", "work_mode", "created_at")
    list_filter = ("status", "work_mode", "employment_type")
    search_fields = ("title", "company__name")
