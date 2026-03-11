"""Tests for the appointments app."""
from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, time

from accounts.models import User
from lawyers.models import LawyerProfile
from categories.models import LegalCategory
from .models import Appointment


class AppointmentTest(TestCase):
    """Test appointment booking and management."""

    def setUp(self):
        self.client = Client()

        # Create citizen
        self.citizen = User.objects.create_user(
            username='citizen1',
            password='testpass123',
            email='citizen@test.com',
            first_name='John',
            last_name='Doe',
            role=User.Role.CITIZEN,
        )

        # Create lawyer user
        self.lawyer_user = User.objects.create_user(
            username='lawyer1',
            password='testpass123',
            email='lawyer@test.com',
            first_name='Jane',
            last_name='Smith',
            role=User.Role.LAWYER,
        )

        # Create category
        self.category = LegalCategory.objects.create(
            name='Family Law',
            slug='family-law',
            is_active=True,
        )

        # Create lawyer profile
        self.lawyer_profile = LawyerProfile.objects.create(
            user=self.lawyer_user,
            bar_council_id='BAR001',
            experience_years=5,
            is_verified=True,
            is_available=True,
        )

        # Create appointment
        self.appointment = Appointment.objects.create(
            citizen=self.citizen,
            lawyer=self.lawyer_profile,
            category=self.category,
            subject='Divorce Consultation',
            description='Need legal advice regarding divorce.',
            appointment_date=date(2026, 4, 15),
            appointment_time=time(10, 0),
        )

    def test_appointment_creation(self):
        self.assertEqual(self.appointment.status, 'PENDING')
        self.assertEqual(self.appointment.citizen, self.citizen)
        self.assertEqual(self.appointment.lawyer, self.lawyer_profile)

    def test_appointment_str(self):
        self.assertIn('APT-', str(self.appointment))

    def test_booking_page_requires_login(self):
        response = self.client.get(
            reverse('appointments:book', args=[self.lawyer_profile.pk])
        )
        self.assertEqual(response.status_code, 302)

    def test_citizen_can_view_appointment_list(self):
        self.client.login(username='citizen1', password='testpass123')
        response = self.client.get(reverse('appointments:list'))
        self.assertEqual(response.status_code, 200)

    def test_citizen_can_view_appointment_detail(self):
        self.client.login(username='citizen1', password='testpass123')
        response = self.client.get(
            reverse('appointments:detail', args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_citizen_can_cancel_appointment(self):
        self.client.login(username='citizen1', password='testpass123')
        response = self.client.get(
            reverse('appointments:cancel', args=[self.appointment.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'CANCELLED')

    def test_lawyer_can_accept_appointment(self):
        self.client.login(username='lawyer1', password='testpass123')
        response = self.client.get(
            reverse('lawyers:appointment_action', args=[self.appointment.pk, 'accept'])
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'ACCEPTED')

    def test_lawyer_can_reject_appointment(self):
        self.client.login(username='lawyer1', password='testpass123')
        response = self.client.get(
            reverse('lawyers:appointment_action', args=[self.appointment.pk, 'reject'])
        )
        self.assertEqual(response.status_code, 302)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, 'REJECTED')

    def test_booking_form_submission(self):
        self.client.login(username='citizen1', password='testpass123')
        response = self.client.post(
            reverse('appointments:book', args=[self.lawyer_profile.pk]),
            {
                'category': self.category.pk,
                'subject': 'Property Dispute',
                'description': 'Need help with property dispute.',
                'appointment_date': '2026-05-01',
                'appointment_time': '14:00',
                'priority': 'MEDIUM',
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Appointment.objects.filter(subject='Property Dispute').exists()
        )


class DashboardTest(TestCase):
    """Test dashboard views."""

    def setUp(self):
        self.client = Client()
        self.citizen = User.objects.create_user(
            username='citizen_dash',
            password='testpass123',
            role=User.Role.CITIZEN,
        )
        self.admin = User.objects.create_user(
            username='admin_dash',
            password='testpass123',
            role=User.Role.ADMIN,
            is_staff=True,
        )

    def test_dashboard_redirects_citizen(self):
        self.client.login(username='citizen_dash', password='testpass123')
        response = self.client.get(reverse('dashboard:home'))
        self.assertEqual(response.status_code, 302)

    def test_citizen_dashboard_loads(self):
        self.client.login(username='citizen_dash', password='testpass123')
        response = self.client.get(reverse('dashboard:citizen_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_loads(self):
        self.client.login(username='admin_dash', password='testpass123')
        response = self.client.get(reverse('dashboard:admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_dashboard_denied_for_citizen(self):
        self.client.login(username='citizen_dash', password='testpass123')
        response = self.client.get(reverse('dashboard:admin_dashboard'))
        self.assertEqual(response.status_code, 302)
