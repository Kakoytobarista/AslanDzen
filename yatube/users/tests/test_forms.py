from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()

class FormUsersTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class."""
        super().setUpClass()

    def setUp(self) -> None:
        """Set up the test data."""
        self.guest_user = Client()

    def test_can_create_user(self):
        """Test the correct creation of a user using reverse('users:signup')."""
        form_data = {
            'username': 'tester',
            'password1': 'qwe123!@#',
            'password2': 'qwe123!@#'
        }
        response = self.guest_user.post(reverse('users:signup'),
                                        data=form_data,
                                        follow=True)
        # Check if the response redirects to the login page
        self.assertRedirects(response, reverse('users:login'))
        # Check if the response is successful
        self.assertTrue(response)
        # Check if the user with the given username is created
        created_user = User.objects.get(username=form_data['username'])
        self.assertEqual(created_user.get_username(), form_data['username'])
