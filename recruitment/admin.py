from django.contrib import admin

from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("candidate", "job", "status", "applied_at")
    list_filter = ("status",)
    search_fields = ("candidate__username", "candidate__email", "job__title")
    readonly_fields = ("applied_at", "updated_at")
