"""Models for the appointments and documents."""
from django.db import models
from django.conf import settings
from lawyers.models import LawyerProfile
from categories.models import LegalCategory


class Appointment(models.Model):
    """Appointment between a citizen and a lawyer."""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
        NO_SHOW = 'NO_SHOW', 'No Show'

    class Priority(models.TextChoices):
        LOW = 'LOW', 'Low'
        MEDIUM = 'MEDIUM', 'Medium'
        HIGH = 'HIGH', 'High'
        URGENT = 'URGENT', 'Urgent'

    citizen = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='citizen_appointments',
        limit_choices_to={'role': 'CITIZEN'}
    )
    lawyer = models.ForeignKey(
        LawyerProfile,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    category = models.ForeignKey(
        LegalCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name='appointments'
    )
    subject = models.CharField(max_length=300)
    description = models.TextField(
        help_text='Describe your legal issue briefly'
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    duration_minutes = models.PositiveIntegerField(
        default=30,
        help_text='Expected duration in minutes'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True,
    )
    priority = models.CharField(
        max_length=6,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    lawyer_notes = models.TextField(
        blank=True,
        help_text='Notes from the lawyer'
    )
    citizen_notes = models.TextField(
        blank=True,
        help_text='Additional notes from the citizen'
    )
    rejection_reason = models.TextField(blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'appointments'
        verbose_name = 'Appointment'
        verbose_name_plural = 'Appointments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'appointment_date']),
            models.Index(fields=['citizen', 'status']),
            models.Index(fields=['lawyer', 'status']),
        ]

    def __str__(self):
        return f"APT-{self.id}: {self.citizen.get_full_name()} → {self.lawyer.full_name} ({self.status})"

    @property
    def is_upcoming(self):
        from django.utils import timezone
        import datetime
        now = timezone.now()
        apt_datetime = datetime.datetime.combine(
            self.appointment_date, self.appointment_time
        )
        return apt_datetime > now.replace(tzinfo=None)

    @property
    def status_badge_class(self):
        """Return Bootstrap badge class for status."""
        mapping = {
            'PENDING': 'bg-warning text-dark',
            'ACCEPTED': 'bg-success',
            'REJECTED': 'bg-danger',
            'COMPLETED': 'bg-info',
            'CANCELLED': 'bg-secondary',
            'NO_SHOW': 'bg-dark',
        }
        return mapping.get(self.status, 'bg-secondary')


class Document(models.Model):
    """Documents uploaded by citizens for appointments."""

    class DocumentType(models.TextChoices):
        IDENTITY = 'IDENTITY', 'Identity Proof'
        LEGAL = 'LEGAL', 'Legal Document'
        EVIDENCE = 'EVIDENCE', 'Evidence'
        OTHER = 'OTHER', 'Other'

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
        related_name='documents'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='uploaded_documents'
    )
    title = models.CharField(max_length=255)
    document_type = models.CharField(
        max_length=10,
        choices=DocumentType.choices,
        default=DocumentType.OTHER,
    )
    file = models.FileField(upload_to='documents/%Y/%m/')
    file_size = models.PositiveIntegerField(
        default=0,
        help_text='File size in bytes'
    )
    description = models.TextField(blank=True)
    is_confidential = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'documents'
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'
        ordering = ['-uploaded_at']

    def __str__(self):
        return f"{self.title} - {self.get_document_type_display()}"

    @property
    def file_size_display(self):
        """Human-readable file size."""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"

    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)
