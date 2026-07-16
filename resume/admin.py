from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "candidate", "is_primary", "file_size", "uploaded_at")
    list_filter = ("is_primary",)
    search_fields = ("title", "candidate__username", "candidate__email")
    readonly_fields = ("original_filename", "file_size", "uploaded_at", "updated_at")
