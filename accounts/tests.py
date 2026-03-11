"""Tests for the accounts app."""
from django.test import TestCase, Client
from django.urls import reverse
from .models import User


class UserModelTest(TestCase):
    """Test the custom User model."""

    def setUp(self):
        self.citizen = User.objects.create_user(
            username='testcitizen',
            password='testpass123',
            email='citizen@test.com',
            first_name='John',
            last_name='Doe',
            role=User.Role.CITIZEN,
        )
        self.lawyer = User.objects.create_user(
            username='testlawyer',
            password='testpass123',
            email='lawyer@test.com',
            first_name='Jane',
            last_name='Smith',
            role=User.Role.LAWYER,
        )

    def test_user_creation(self):
        self.assertEqual(self.citizen.role, 'CITIZEN')
        self.assertTrue(self.citizen.is_citizen)
        self.assertFalse(self.citizen.is_lawyer)

    def test_lawyer_role(self):
        self.assertEqual(self.lawyer.role, 'LAWYER')
        self.assertTrue(self.lawyer.is_lawyer)
        self.assertFalse(self.lawyer.is_citizen)

    def test_user_str(self):
        self.assertIn('John Doe', str(self.citizen))
        self.assertIn('CITIZEN', str(self.citizen))


class AuthenticationTest(TestCase):
    """Test authentication views."""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com',
            role=User.Role.CITIZEN,
        )

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse('accounts:register_citizen'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)  # Redirect on success

    def test_login_failure(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 200)  # Re-renders form

    def test_register_citizen(self):
        response = self.client.post(reverse('accounts:register_citizen'), {
            'first_name': 'New',
            'last_name': 'User',
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'securepass123!',
            'password2': 'securepass123!',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_profile_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_loads_when_logged_in(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)
