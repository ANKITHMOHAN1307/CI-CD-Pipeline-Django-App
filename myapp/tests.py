from django.test import TestCase
from django.urls import reverse
from .models import UserInput

class UserInputTests(TestCase):
    
    def test_input_page_loads(self):
        """
        Test that the input page loads successfully (GET request)
        """
        response = self.client.get(reverse('input'))  # Changed from 'input_view' to 'input'
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'input.html')

    def test_user_input_creation(self):
        """
        Test POST request to submit user data and save to database
        """
        user_data = {
            'name': 'Test User',
            'email': 'test@example.com'
        }
        response = self.client.post(reverse('input'), data=user_data)  # Changed from 'input_view' to 'input'
        
        # Check redirect to success page
        user = UserInput.objects.first()
        self.assertRedirects(response, reverse('success', args=[user.id]))  # This should work with user_id parameter
        
        # Check if data is saved correctly
        self.assertEqual(UserInput.objects.count(), 1)
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.email, 'test@example.com')

    def test_success_page_loads(self):
        """
        Test that the success page loads and displays the correct user
        """
        user = UserInput.objects.create(name='Another User', email='another@example.com')
        response = self.client.get(reverse('success', args=[user.id]))  # Django will map this to user_id
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Another User')
        self.assertTemplateUsed(response, 'success.html')