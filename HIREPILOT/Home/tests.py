from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from unittest.mock import patch

class SignupAndLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')

    def test_signup_creates_active_user_and_redirects_to_dashboard(self):
        # 1. Sign up a new user
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        # Check that we redirect to dashboard
        self.assertRedirects(response, reverse('dashboard'))
        
        # Verify the user is created and active
        user = User.objects.get(username='newuser')
        self.assertTrue(user.is_active)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john@example.com')


class PasswordResetTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.reset_url = reverse('password_reset')
        # Create an active user
        self.user = User.objects.create_user(
            username='activeuser', 
            email='active@example.com', 
            password='SecurePass123!',
            first_name='Active'
        )

    @patch('Home.views.send_brevo_email')
    def test_password_reset_sends_email_and_does_not_reveal_non_existent(self, mock_send_email):
        mock_send_email.return_value = True

        # 1. Reset for existing user
        response = self.client.post(self.reset_url, {'email': 'active@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))
        
        # Verify that send_brevo_email was called
        mock_send_email.assert_called_once()
        call_kwargs = mock_send_email.call_args[1]
        self.assertEqual(call_kwargs['to_email'], 'active@example.com')
        self.assertEqual(call_kwargs['to_name'], 'Active')
        self.assertEqual(call_kwargs['subject'], 'Reset your HirePilot password')
        self.assertIn("password-reset-confirm", call_kwargs['html_content'])
        
        # Reset mock
        mock_send_email.reset_mock()

        # 2. Reset for non-existent user
        response = self.client.post(self.reset_url, {'email': 'nonexistent@example.com'})
        self.assertRedirects(response, reverse('password_reset_done'))
        # Should not send email
        mock_send_email.assert_not_called()
