"""
Custom User model and profile models for the accounts app.
Supports three roles: Citizen, Lawyer, Admin.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Extended User model with role-based access control.
    """

    class Role(models.TextChoices):
        CITIZEN = 'CITIZEN', _('Citizen')
        LAWYER = 'LAWYER', _('Lawyer')
        ADMIN = 'ADMIN', _('Admin')

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CITIZEN,
        db_index=True,
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        blank=True,
        null=True
    )
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"

    @property
    def is_citizen(self):
        return self.role == self.Role.CITIZEN

    @property
    def is_lawyer(self):
        return self.role == self.Role.LAWYER

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN
