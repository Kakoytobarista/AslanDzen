from django.test import TestCase, Client
from http import HTTPStatus


class AboutUrlTests(TestCase):
    def setUp(self):
        self.guest_client: Client = Client()

    def test_about_author(self):
        """Проверка на статус код 200
        статичной страницы author"""

        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_technology(self):
        """Проверка на статус код 200
        статичной страницы technology"""

        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_use_correct_template(self):
        templates_url_names = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertTemplateUsed(response, template)
