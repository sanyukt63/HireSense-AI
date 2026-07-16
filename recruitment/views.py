from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import IntegrityError, transaction
from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from accounts.models import User
from jobs.models import Job
from resume.models import Resume
from ai_engine.services import score_application

from .forms import ApplicationForm, ApplicationReviewForm
from .models import Application


class CandidateRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.Role.CANDIDATE

    def handle_no_permission(self):
        messages.error(self.request, "Candidate access is required for this action.")
        return redirect("accounts:dashboard")


class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.Role.RECRUITER

    def handle_no_permission(self):
        messages.error(self.request, "Recruiter access is required for this action.")
        return redirect("accounts:dashboard")


class ApplicationCreateView(CandidateRequiredMixin, CreateView):
    model = Application
    form_class = ApplicationForm
    template_name = "recruitment/application_form.html"

    def dispatch(self, request, *args, **kwargs):
        self.job = Job.objects.filter(pk=kwargs["job_pk"], status=Job.Status.OPEN).first()
        if not self.job:
            raise Http404("This job is not available for applications.")
        if Application.objects.filter(candidate=request.user, job=self.job).exists():
            messages.info(request, "You have already applied for this job.")
            return redirect("recruitment:history")
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["resume"].queryset = Resume.objects.filter(candidate=self.request.user)
        form.fields["resume"].required = True
        return form

    def get_initial(self):
        initial = super().get_initial()
        initial["resume"] = Resume.objects.filter(candidate=self.request.user, is_primary=True).first()
        return initial

    @transaction.atomic
    def form_valid(self, form):
        form.instance.candidate = self.request.user
        form.instance.job = self.job
        try:
            response = super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "You have already applied for this job.")
            return self.form_invalid(form)
        messages.success(self.request, "Application submitted successfully.")
        return response

    def get_success_url(self):
        return reverse_lazy("recruitment:history")


class CandidateApplicationHistoryView(CandidateRequiredMixin, ListView):
    model = Application
    template_name = "recruitment/application_history.html"
    context_object_name = "applications"

    def get_queryset(self):
        return Application.objects.filter(candidate=self.request.user).select_related("job__company", "resume")


class RecruiterApplicantListView(RecruiterRequiredMixin, ListView):
    model = Application
    template_name = "recruitment/applicant_list.html"
    context_object_name = "applications"

    def dispatch(self, request, *args, **kwargs):
        self.job = Job.objects.filter(pk=kwargs["job_pk"], created_by=request.user).first()
        if not self.job:
            raise Http404("Job not found.")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Application.objects.filter(job=self.job).select_related("candidate", "resume")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = self.job
        return context


class RecruiterApplicationReviewView(RecruiterRequiredMixin, UpdateView):
    model = Application
    form_class = ApplicationReviewForm
    template_name = "recruitment/application_review.html"
    context_object_name = "application"

    def get_queryset(self):
        return Application.objects.filter(job__created_by=self.request.user).select_related("candidate", "job", "resume")

    def get_success_url(self):
        messages.success(self.request, "Application review updated.")
        return reverse_lazy("recruitment:applicants", kwargs={"job_pk": self.object.job_id})


class ApplicationScoreView(RecruiterRequiredMixin, View):
    """Calculate an ATS assessment for an application owned by this recruiter."""

    def post(self, request, pk):
        application = Application.objects.filter(pk=pk, job__created_by=request.user).select_related("resume", "job").first()
        if not application:
            raise Http404("Application not found.")
        try:
            score_application(application)
            messages.success(request, "ATS assessment calculated successfully.")
        except (ImportError, OSError, ValueError) as exc:
            messages.error(request, f"ATS assessment could not be calculated: {exc}")
        return redirect("recruitment:review", pk=application.pk)


class RecruiterApplicationResumeView(RecruiterRequiredMixin, View):
    """Serve a submitted file only to the recruiter who owns the job."""

    def get(self, request, pk):
        application = Application.objects.filter(pk=pk, job__created_by=request.user).select_related("resume").first()
        if not application or not application.resume:
            raise Http404("Submitted resume not found.")
        resume = application.resume
        return FileResponse(resume.document.open("rb"), as_attachment=True, filename=resume.original_filename)
