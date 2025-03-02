from django import forms

from .models import CVDocument


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {"accept": ".pdf,.doc,.docx"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(attrs=default_attrs)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CVDocumentForm(forms.ModelForm):
    file = MultipleFileField(label="Select files", required=False)

    class Meta:
        model = CVDocument
        fields = ("file",)
