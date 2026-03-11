"""Forms for lawyer profile creation and management."""
from django import forms
from .models import LawyerProfile, LawyerAvailability
from categories.models import LegalCategory


class LawyerProfileForm(forms.ModelForm):
    """Form for creating/editing lawyer profile."""

    specializations = forms.ModelMultipleChoiceField(
        queryset=LegalCategory.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required=False,
    )

    class Meta:
        model = LawyerProfile
        fields = [
            'bar_council_id', 'specializations', 'experience_years',
            'qualification', 'bio', 'consultation_fee',
            'office_address', 'verification_document'
        ]
        widgets = {
            'bar_council_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Bar Council Registration No.'
            }),
            'experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., LLB, LLM'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Write a short professional biography...'
            }),
            'consultation_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'step': '0.01'
            }),
            'office_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'verification_document': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }


class LawyerAvailabilityForm(forms.ModelForm):
    """Form for managing lawyer availability slots."""

    class Meta:
        model = LawyerAvailability
        fields = ['day', 'start_time', 'end_time', 'is_active']
        widgets = {
            'day': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
