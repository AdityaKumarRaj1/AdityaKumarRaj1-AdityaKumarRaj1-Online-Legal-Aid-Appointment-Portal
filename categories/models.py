"""Models for legal categories."""
from django.db import models
from django.utils.text import slugify


class LegalCategory(models.Model):
    """Legal service categories (e.g., Family Law, Criminal Law, etc.)."""

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Bootstrap icon class (e.g., bi-briefcase)'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'legal_categories'
        verbose_name = 'Legal Category'
        verbose_name_plural = 'Legal Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def lawyer_count(self):
        return self.lawyers.filter(is_verified=True).count()

    @property
    def appointment_count(self):
        return self.appointments.count()
