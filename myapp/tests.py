from django.test import TestCase
from django.urls import reverse
from .models import UserInput

class UserInputTests(TestCase):
    
    # ----- Registration Tests -----
    def test_input_page_loads(self):
        """Check that registration page loads successfully (GET request)"""
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'input.html')

    def test_user_registration_success(self):
        """Test POST request for successful registration"""
        user_data = {'name': 'Test User', 'email': 'test@example.com'}
        response = self.client.post(reverse('register'), data=user_data)
        
        user = UserInput.objects.first()
        self.assertRedirects(response, reverse('success', args=[user.id]))
        self.assertEqual(UserInput.objects.count(), 1)
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')

    def test_empty_registration_fails(self):
        """Test POST request with empty fields"""
        response = self.client.post(reverse('register'), data={'name': '', 'email': ''})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')
        self.assertEqual(UserInput.objects.count(), 0)

    def test_duplicate_email_registration(self):
        """Ensure duplicate email cannot register"""
        UserInput.objects.create(name='Existing User', email='exist@example.com')
        response = self.client.post(reverse('register'), data={'name': 'New User', 'email': 'exist@example.com'})
        self.assertRedirects(response, reverse('failed_page'))
        self.assertEqual(UserInput.objects.count(), 1)

    # ----- Login Tests -----
    def test_login_page_loads(self):
        """Check login page loads successfully"""
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_success(self):
        """Test login with valid email"""
        user = UserInput.objects.create(name='Login User', email='login@example.com')
        response = self.client.post(reverse('login'), data={'email': 'login@example.com', 'password': 'dummy'})
        self.assertContains(response, f'WELCOME BACK {user.name}')

    def test_login_invalid_email(self):
        """Test login with email that doesn't exist"""
        response = self.client.post(reverse('login'), data={'email': 'wrong@example.com', 'password': 'dummy'})
        self.assertRedirects(response, reverse('Fail'))

    # ----- Success / Failure Page Tests -----
    def test_success_page_loads(self):
        """Check that success page loads for registered user"""
        user = UserInput.objects.create(name='Another User', email='another@example.com')
        response = self.client.get(reverse('success', args=[user.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Another User')
        self.assertTemplateUsed(response, 'success.html')

    def test_fail_registration_page_loads(self):
        """Check fail page for registration"""
        response = self.client.get(reverse('failed_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'failregistration.html')

    def test_fail_login_page_loads(self):
        """Check fail page for login"""
        response = self.client.get(reverse('Fail'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'faillogin.html')
