from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

User = get_user_model()


class FormUsersTest(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def setUp(self) -> None:
        self.guest_user = Client()

    def test_can_create_user(self):
        """Проверка на корректное создание пользователя
        через reverse('users:signup')"""
        form_data = {
            'username': 'tester',
            'password1': 'qwe123!@#',
            'password2': 'qwe123!@#'
        }
        response = self.guest_user.post(reverse('users:signup'),
                                        data=form_data,
                                        follow=True)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(response)
        self.assertEqual(User.objects.get(
                         username=form_data['username']).get_username(),
                         form_data['username'])
