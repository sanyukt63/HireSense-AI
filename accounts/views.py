from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from analytics.services import get_dashboard_metrics

from .forms import CandidateProfileForm, RecruiterProfileForm, RegistrationForm
from .models import CandidateProfile, RecruiterProfile, User


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("accounts:dashboard")

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.object.role == User.Role.CANDIDATE:
            CandidateProfile.objects.create(user=self.object)
        else:
            RecruiterProfile.objects.create(user=self.object)
        login(self.request, self.object)
        messages.success(self.request, "Your HireSense AI account is ready.")
        return response


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == User.Role.RECRUITER:
            context["metrics"] = get_dashboard_metrics(self.request.user)
        return context


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect("accounts:login")
    if request.user.role == User.Role.CANDIDATE:
        profile, _ = CandidateProfile.objects.get_or_create(user=request.user)
        form_class = CandidateProfileForm
    elif request.user.role == User.Role.RECRUITER:
        profile, _ = RecruiterProfile.objects.get_or_create(user=request.user)
        form_class = RecruiterProfileForm
    else:
        messages.info(request, "Administrator profiles are managed in Django admin.")
        return redirect("accounts:dashboard")
    form = form_class(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile")
    return render(request, "accounts/profile.html", {"form": form})
