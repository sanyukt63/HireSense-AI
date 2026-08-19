from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from django.urls import include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("accounts.urls")),
    path("", include("jobs.urls")),
    path("", include("resume.urls")),
    path("", include("recruitment.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#fixed 
