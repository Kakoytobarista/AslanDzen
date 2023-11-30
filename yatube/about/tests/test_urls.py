from django.test import TestCase, Client
from http import HTTPStatus
from typing import Dict

class AboutUrlTests(TestCase):
    def setUp(self) -> None:
        """Set up a guest client for testing."""
        self.guest_client: Client = Client()

    def test_about_author(self) -> None:
        """Test the status code of the static author page."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_technology(self) -> None:
        """Test the status code of the static technology page."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_use_correct_template(self) -> None:
        """Test that the correct templates are used for specific URLs."""
        templates_url_names: Dict[str, str] = {
            'about/author.html': '/about/author/',
            'about/tech.html': '/about/tech/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)
