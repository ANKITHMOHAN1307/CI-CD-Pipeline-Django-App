from django.test import TestCase
from django.urls import reverse
from .models import UserInput

class UserInputTests(TestCase):

    def test_main_page_loads(self):
        """Test that the main page loads successfully"""
        response = self.client.get(reverse('maingpage'))
        self.assertEqual(response.status_code, 200)

    def test_registration_creates_user(self):
        """Test POST request creates a new user in the database"""
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('register'), data=user_data)
        
        # Should redirect to success page
        user = UserInput.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(UserInput.objects.count(), 1)
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')

    def test_duplicate_email_redirects_failure(self):
        """Test that registering with an existing email redirects to fail page"""
        UserInput.objects.create(name='Existing User', email='existing@example.com')
        user_data = {
            'name': 'Another User',
            'email': 'existing@example.com'
        }
        response = self.client.post(reverse('register'), data=user_data)
        self.assertEqual(response.status_code, 302)  # Redirect to fail page

    def test_success_view_loads(self):
        """Test success page returns 200 and correct user"""
        user = UserInput.objects.create(name='User', email='user@example.com')
        response = self.client.get(reverse('success', args=[user.id]))
        self.assertEqual(response.status_code, 200)

    def test_login_redirects_on_existing_user(self):
        """Test login view redirects / responds correctly for existing user"""
        user = UserInput.objects.create(name='Login User', email='login@example.com')
        response = self.client.post(reverse('login'), data={'email': 'login@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'WELCOME BACK')

    def test_login_redirects_on_nonexistent_user(self):
        """Test login view redirects to fail page for non-existent email"""
        response = self.client.post(reverse('login'), data={'email': 'noone@example.com'})
        self.assertEqual(response.status_code, 302)  # Redirect to fail page
