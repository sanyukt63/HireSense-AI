from django.urls import path

from .views import CompanyCreateView, CompanyUpdateView, JobCreateView, JobDeleteView, JobDetailView, JobListView, JobUpdateView

app_name = "jobs"

urlpatterns = [
    path("jobs/", JobListView.as_view(), name="list"),
    path("jobs/create/", JobCreateView.as_view(), name="job_create"),
    path("jobs/<int:pk>/", JobDetailView.as_view(), name="detail"),
    path("jobs/<int:pk>/edit/", JobUpdateView.as_view(), name="job_edit"),
    path("jobs/<int:pk>/delete/", JobDeleteView.as_view(), name="job_delete"),
    path("company/create/", CompanyCreateView.as_view(), name="company_create"),
    path("company/<int:pk>/edit/", CompanyUpdateView.as_view(), name="company_edit"),
]
