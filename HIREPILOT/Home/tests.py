from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.signing import dumps
from unittest.mock import patch

class EmailVerificationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')

    @patch('Home.views.send_brevo_email')
    def test_signup_creates_inactive_user_and_sends_email(self, mock_send_email):
        mock_send_email.return_value = True

        # 1. Sign up a new user
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'password1': 'SecurePass123!',
            'password2': 'SecurePass123!',
        })
        # Check that we redirect to verification sent page
        self.assertRedirects(response, reverse('verification_sent'))
        
        # Verify the user is created and inactive
        user = User.objects.get(username='newuser')
        self.assertFalse(user.is_active)
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'john@example.com')

        # Verify that send_brevo_email was called correctly
        mock_send_email.assert_called_once()
        call_kwargs = mock_send_email.call_args[1]
        self.assertEqual(call_kwargs['to_email'], 'john@example.com')
        self.assertEqual(call_kwargs['to_name'], 'John')
        self.assertEqual(call_kwargs['subject'], 'Verify your HirePilot email')
        self.assertIn("verify-email", call_kwargs['html_content'])

    def test_login_fails_for_inactive_user(self):
        # Create an inactive user
        user = User.objects.create_user(username='inactiveuser', email='inactive@example.com', password='SecurePass123!')
        user.is_active = False
        user.save()

        # Try to log in
        response = self.client.post(self.login_url, {
            'username': 'inactiveuser',
            'password': 'SecurePass123!',
        })
        
        # Should render the accounts/login.html template again with error
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')
        
        # Check message output
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 
            "Please verify your email before logging in. Check your inbox (and spam folder)."
        )

    def test_verify_email_activates_user_and_logs_in(self):
        # Create inactive user
        user = User.objects.create_user(username='john', email='john@example.com', password='SecurePass123!')
        user.is_active = False
        user.save()

        # Generate a valid token
        token = dumps(user.pk, salt='email-verification')
        
        # Call verification view
        verify_url = reverse('verify_email', kwargs={'token': token})
        response = self.client.get(verify_url)
        
        # Check that it redirects to dashboard
        self.assertRedirects(response, '/dashboard/')
        
        # Verify user is now active
        user.refresh_from_db()
        self.assertTrue(user.is_active)

    def test_verify_email_invalid_token(self):
        # Call verification view with invalid token
        verify_url = reverse('verify_email', kwargs={'token': 'invalid-token-value'})
        response = self.client.get(verify_url)
        
        # Check that it renders verification failed template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/verification_failed.html')


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
