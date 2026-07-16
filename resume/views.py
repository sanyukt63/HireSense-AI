from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import transaction
from django.http import FileResponse, Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView

from accounts.models import User
from ai_engine.services import build_resume_suggestions, parse_resume

from .forms import ResumeUploadForm
from .models import Resume


class CandidateRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == User.Role.CANDIDATE

    def handle_no_permission(self):
        messages.error(self.request, "Candidate access is required for this action.")
        return redirect("accounts:dashboard")


class ResumeListView(CandidateRequiredMixin, ListView):
    model = Resume
    template_name = "resume/resume_list.html"
    context_object_name = "resumes"

    def get_queryset(self):
        return Resume.objects.filter(candidate=self.request.user).order_by("-is_primary", "-uploaded_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resume_cards = []
        for resume in context.get("resumes", []):
            suggestions = {}
            try:
                parsed_resume = parse_resume(resume)
            except (FileNotFoundError, OSError, ValueError):
                parsed_resume = None
            if parsed_resume is not None:
                suggestions = build_resume_suggestions(parsed_resume.extracted_data)
            resume_cards.append({"resume": resume, "suggestions": suggestions})
        context["resume_cards"] = resume_cards
        return context


class ResumeUploadView(CandidateRequiredMixin, CreateView):
    model = Resume
    form_class = ResumeUploadForm
    template_name = "resume/resume_upload.html"
    success_url = reverse_lazy("resume:list")

    @transaction.atomic
    def form_valid(self, form):
        form.instance.candidate = self.request.user
        if form.cleaned_data["is_primary"]:
            Resume.objects.filter(candidate=self.request.user, is_primary=True).update(is_primary=False)
        elif not Resume.objects.filter(candidate=self.request.user).exists():
            form.instance.is_primary = True
        messages.success(self.request, "Resume uploaded successfully.")
        return super().form_valid(form)


class ResumeDocumentView(CandidateRequiredMixin, View):
    def get(self, request, pk):
        resume = Resume.objects.filter(pk=pk, candidate=request.user).first()
        if not resume:
            raise Http404("Resume not found.")
        return FileResponse(resume.document.open("rb"), as_attachment=True, filename=resume.original_filename)


class ResumeDeleteView(CandidateRequiredMixin, DeleteView):
    model = Resume
    template_name = "resume/resume_confirm_delete.html"
    success_url = reverse_lazy("resume:list")

    def get_queryset(self):
        return Resume.objects.filter(candidate=self.request.user)

    @transaction.atomic
    def form_valid(self, form):
        resume = self.get_object()
        was_primary = resume.is_primary
        response = super().form_valid(form)
        if was_primary:
            replacement = Resume.objects.filter(candidate=self.request.user).order_by("-uploaded_at").first()
            if replacement:
                replacement.is_primary = True
                replacement.save(update_fields=("is_primary", "updated_at"))
        messages.success(self.request, "Resume deleted successfully.")
        return response
