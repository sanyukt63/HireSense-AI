from pathlib import Path

from django import forms

from .models import Resume


class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ("title", "document", "is_primary")

    def clean_document(self):
        document = self.cleaned_data["document"]
        extension = Path(document.name).suffix.lower()
        content_type = getattr(document, "content_type", "")
        expected_types = { 
            ".pdf": {"application/pdf", "application/octet-stream"},
            ".doc": {"application/msword", "application/octet-stream"},
            ".docx": {
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                "application/octet-stream",
            },
        }
        if content_type and content_type not in expected_types.get(extension, set()):
            raise forms.ValidationError("The uploaded file type does not match its extension.")
        return document
