import json

from django.contrib.messages import get_messages
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse

from .forms import CVDocumentForm
from .models import CVDocument


class TestCVViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_upload_cv_get(self):
        """GET request should render the upload form."""
        response = self.client.get(reverse("upload_cv"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cvapp/upload_cv.html")

    def test_upload_cv_no_files(self):
        """POST with no files should redirect and add an error message."""
        response = self.client.post(reverse("upload_cv"), {})
        self.assertRedirects(response, reverse("upload_cv"))
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("No files were selected" in m.message for m in messages))

    def test_chatbot_view_get(self):
        """GET request to chatbot view should render the chatbot template."""
        response = self.client.get(reverse("chatbot"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cvapp/chatbot.html")

    def test_cv_summary(self):
        """
        The cv_summary view should retrieve the parsed CV data from the session,
        process it (pretty-print JSON), and pass it to the template.
        """
        dummy_parsed_data = [{"dummy": "data"}]
        session = self.client.session
        session["cv_parsed_data"] = dummy_parsed_data
        session.save()

        response = self.client.get(reverse("cv_summary"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cvapp/cv_summary.html")
        self.assertIn("cv_parsed_data", response.context)
        for entry in response.context["cv_parsed_data"]:
            self.assertIn("raw", entry)
            self.assertIn("pretty_json", entry)
            # Also verify that pretty_json is valid JSON
            parsed = json.loads(entry["pretty_json"])
            self.assertEqual(parsed, entry["raw"])

    def test_clear_chat(self):
        """Calling clear_chat should empty the conversation history and redirect to the chatbot."""
        session = self.client.session
        session["conversation_history"] = [{"role": "user", "content": "hello"}]
        session.save()
        response = self.client.get(reverse("clear_chat"))
        self.assertRedirects(response, reverse("chatbot"))
        session = self.client.session
        self.assertEqual(session.get("conversation_history"), [])

    def test_upload_success(self):
        """The upload_success view should render its template."""
        response = self.client.get(reverse("cv_upload_success"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cvapp/upload_success.html")


class TestCVDocumentModel(TestCase):
    def test_str_method(self):
        """Test that the model's __str__ returns the expected string."""
        # Create a document with a dummy file path; uploaded_at is auto-set.
        cv_doc = CVDocument.objects.create(file="dummy.pdf")
        expected_str = f"CV Document uploaded at {cv_doc.uploaded_at}"
        self.assertEqual(str(cv_doc), expected_str)


class TestCVDocumentForm(TestCase):
    def test_form_valid_single_file(self):
        """The form should be valid with a single file."""
        file_data = SimpleUploadedFile(
            "test.pdf", b"dummy content", content_type="application/pdf"
        )
        form = CVDocumentForm(data={}, files={"file": file_data})
        self.assertTrue(form.is_valid())

    def test_form_valid_multiple_files(self):
        """The form should be valid with multiple files."""
        file1 = SimpleUploadedFile(
            "test1.pdf", b"dummy content 1", content_type="application/pdf"
        )
        file2 = SimpleUploadedFile(
            "test2.pdf", b"dummy content 2", content_type="application/pdf"
        )
        form = CVDocumentForm(data={}, files={"file": [file1, file2]})
        self.assertTrue(form.is_valid())
