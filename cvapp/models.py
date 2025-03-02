from django.db import models


class CVDocument(models.Model):
    file = models.FileField(upload_to="cv_documents/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    extracted_text = models.TextField(blank=True, null=True)
    parsed_data = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"CV Document uploaded at {self.uploaded_at}"
