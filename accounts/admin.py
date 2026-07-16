from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CandidateProfile, RecruiterProfile, User


@admin.register(User)
class HireSenseUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("HireSense", {"fields": ("role",)}),)
    list_display = ("username", "email", "first_name", "last_name", "role", "is_staff")
    list_filter = ("role", "is_staff", "is_active")


admin.site.register(CandidateProfile)
admin.site.register(RecruiterProfile)
