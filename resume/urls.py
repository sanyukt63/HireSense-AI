from django.urls import path

from .views import ResumeDeleteView, ResumeDocumentView, ResumeListView, ResumeUploadView

app_name = "resume"

urlpatterns = [
    path("resumes/", ResumeListView.as_view(), name="list"),
    path("resumes/upload/", ResumeUploadView.as_view(), name="upload"),
    path("resumes/<int:pk>/document/", ResumeDocumentView.as_view(), name="document"),
    path("resumes/<int:pk>/delete/", ResumeDeleteView.as_view(), name="delete"),
]
