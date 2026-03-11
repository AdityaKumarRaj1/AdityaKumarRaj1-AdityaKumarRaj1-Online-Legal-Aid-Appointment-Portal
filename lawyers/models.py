"""Models for lawyer profiles and specializations."""
from django.db import models
from django.conf import settings
from categories.models import LegalCategory


class LawyerProfile(models.Model):
    """Extended profile for lawyer users."""

    class VerificationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        VERIFIED = 'VERIFIED', 'Verified'
        REJECTED = 'REJECTED', 'Rejected'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lawyer_profile'
    )
    bar_council_id = models.CharField(
        max_length=50,
        unique=True,
        help_text='Bar Council Registration Number'
    )
    specializations = models.ManyToManyField(
        LegalCategory,
        related_name='lawyers',
        blank=True
    )
    experience_years = models.PositiveIntegerField(default=0)
    qualification = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True, help_text='Professional biography')
    consultation_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text='Consultation fee in INR'
    )
    office_address = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    verification_status = models.CharField(
        max_length=10,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
    )
    is_available = models.BooleanField(
        default=True,
        help_text='Is the lawyer currently accepting appointments?'
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    total_cases = models.PositiveIntegerField(default=0)
    verification_document = models.FileField(
        upload_to='lawyer_docs/',
        blank=True,
        null=True,
        help_text='Upload bar council certificate or ID'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'lawyer_profiles'
        verbose_name = 'Lawyer Profile'
        verbose_name_plural = 'Lawyer Profiles'
        ordering = ['-rating', '-experience_years']

    def __str__(self):
        return f"Adv. {self.user.get_full_name()} - {self.bar_council_id}"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def pending_appointments(self):
        return self.appointments.filter(status='PENDING').count()

    @property
    def completed_appointments(self):
        return self.appointments.filter(status='COMPLETED').count()


class LawyerAvailability(models.Model):
    """Track lawyer availability slots."""

    class DayChoices(models.TextChoices):
        MONDAY = 'MON', 'Monday'
        TUESDAY = 'TUE', 'Tuesday'
        WEDNESDAY = 'WED', 'Wednesday'
        THURSDAY = 'THU', 'Thursday'
        FRIDAY = 'FRI', 'Friday'
        SATURDAY = 'SAT', 'Saturday'
        SUNDAY = 'SUN', 'Sunday'

    lawyer = models.ForeignKey(
        LawyerProfile,
        on_delete=models.CASCADE,
        related_name='availability_slots'
    )
    day = models.CharField(max_length=3, choices=DayChoices.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'lawyer_availability'
        verbose_name = 'Availability Slot'
        verbose_name_plural = 'Availability Slots'
        ordering = ['day', 'start_time']
        unique_together = ['lawyer', 'day', 'start_time']

    def __str__(self):
        return f"{self.lawyer.full_name} - {self.get_day_display()} {self.start_time}-{self.end_time}"
