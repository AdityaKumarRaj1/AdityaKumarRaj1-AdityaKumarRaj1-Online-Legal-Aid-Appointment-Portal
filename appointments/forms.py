"""Forms for appointment booking and document upload."""
from django import forms
from .models import Appointment, Document
from lawyers.models import LawyerProfile
from categories.models import LegalCategory


class AppointmentBookingForm(forms.ModelForm):
    """Form for citizens to book appointments."""

    category = forms.ModelChoiceField(
        queryset=LegalCategory.objects.filter(is_active=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label='Select Legal Category',
    )

    class Meta:
        model = Appointment
        fields = [
            'category', 'subject', 'description',
            'appointment_date', 'appointment_time',
            'priority', 'citizen_notes'
        ]
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief subject of your legal matter'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your legal issue in detail...'
            }),
            'appointment_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'appointment_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'priority': forms.Select(attrs={'class': 'form-select'}),
            'citizen_notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Any additional notes...'
            }),
        }


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents."""

    class Meta:
        model = Document
        fields = ['title', 'document_type', 'file', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Document Title'
            }),
            'document_type': forms.Select(attrs={'class': 'form-select'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Brief description of the document'
            }),
        }

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file size (10 MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError('File size must be less than 10 MB.')
            # Check file type
            allowed_types = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'image/jpeg',
                'image/png',
            ]
            if file.content_type not in allowed_types:
                raise forms.ValidationError(
                    'Only PDF, DOC, DOCX, JPEG, and PNG files are allowed.'
                )
        return file
