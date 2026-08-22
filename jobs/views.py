from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from accounts.models import User

from .forms import CompanyForm, JobForm
from .models import Company, Job


class RecruiterRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.Role.RECRUITER

    def handle_no_permission(self):
        messages.error(self.request, "Recruiter access is required for this action.")
        return redirect("accounts:dashboard")
 

class JobListView(ListView):
    model = Job
    template_name = "jobs/job_list.html"
    context_object_name = "jobs"
    paginate_by = 12

    def get_queryset(self):
        return Job.objects.filter(status=Job.Status.OPEN).select_related("company")


class JobDetailView(DetailView):
    model = Job
    template_name = "jobs/job_detail.html"
    context_object_name = "job"


class CompanyCreateView(RecruiterRequiredMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "jobs/company_form.html"

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        self.request.user.recruiter_profile.company = self.object
        self.request.user.recruiter_profile.save(update_fields=("company", "updated_at"))
        messages.success(self.request, "Company profile created.")
        return response

    def get_success_url(self):
        return reverse_lazy("jobs:job_create")


class CompanyUpdateView(RecruiterRequiredMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "jobs/company_form.html"

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)

    def get_success_url(self):
        messages.success(self.request, "Company profile updated.")
        return reverse_lazy("accounts:dashboard")


class JobCreateView(RecruiterRequiredMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"

    def dispatch(self, request, *args, **kwargs):
        if not hasattr(request.user, "recruiter_profile") or not request.user.recruiter_profile.company_id:
            messages.info(request, "Create your company profile before posting a job.")
            return redirect("jobs:company_create")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.company = self.request.user.recruiter_profile.company
        form.instance.created_by = self.request.user
        messages.success(self.request, "Job saved successfully.")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("jobs:detail", kwargs={"pk": self.object.pk})


class RecruiterJobMixin(RecruiterRequiredMixin):
    def get_queryset(self):
        return Job.objects.filter(created_by=self.request.user).select_related("company")


class JobUpdateView(RecruiterJobMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = "jobs/job_form.html"

    def get_success_url(self):
        messages.success(self.request, "Job updated successfully.")
        return reverse_lazy("jobs:detail", kwargs={"pk": self.object.pk})


class JobDeleteView(RecruiterJobMixin, DeleteView):
    model = Job
    template_name = "jobs/job_confirm_delete.html"
    success_url = reverse_lazy("jobs:list")

    def form_valid(self, form):
        messages.success(self.request, "Job deleted successfully.")
        return super().form_valid(form)
