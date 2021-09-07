from django.contrib.auth import get_user_model
from django.test import TestCase, Client

User = get_user_model()


class UsersUrlsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self) -> None:
        self.guest_user = Client()
        self.user = User.objects.create_user(username='test')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_guest_can_open_accounts_pages_for_un_auth_client(self):
        """Проверка на возможность открытия страниц
        доступных неавторизованному пользователю"""
        templates_url_names = {
            'users/login.html': '/auth/login/',
            'users/signup.html': '/auth/signup/',
            'users/password_reset_form.html':
                '/auth/password_reset_form/',
            'users/password_reset_done.html':
                '/auth/password_reset/done/',
            'users/password_reset_complete.html':
                '/auth/password_reset/complete/'
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_user.get(adress)
                self.assertTemplateUsed(response, template)

    def test_auth_user_can_open_pages_with_auth_client(self):
        """Проверка на возможность открытия страниц
        для авторизованного пользователя"""
        templates_url_names = {
            'users/password_change_form.html':
                '/auth/password_change_form/',
            'users/password_change_done.html':
                '/auth/password_change/done/',
            'users/logged_out.html': '/auth/logout/'
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.authorized_client.get(adress)
                self.assertTemplateUsed(response, template)

    def test_page_password_change_doesnt_work_with_guest(self):
        """Проверка на возможность корректной смены
        пароля"""
        response = self.guest_user.get('/auth/password_change_form/')
        self.assertTemplateNotUsed(response, 'users/password_change_form.html')
