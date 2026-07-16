from django.urls import path

from .views import ApplicationCreateView, ApplicationScoreView, CandidateApplicationHistoryView, RecruiterApplicantListView, RecruiterApplicationReviewView, RecruiterApplicationResumeView

app_name = "recruitment"

urlpatterns = [
    path("jobs/<int:job_pk>/apply/", ApplicationCreateView.as_view(), name="apply"),
    path("applications/", CandidateApplicationHistoryView.as_view(), name="history"),
    path("jobs/<int:job_pk>/applicants/", RecruiterApplicantListView.as_view(), name="applicants"),
    path("applications/<int:pk>/review/", RecruiterApplicationReviewView.as_view(), name="review"),
    path("applications/<int:pk>/resume/", RecruiterApplicationResumeView.as_view(), name="resume_document"),
    path("applications/<int:pk>/score/", ApplicationScoreView.as_view(), name="score"),
]
