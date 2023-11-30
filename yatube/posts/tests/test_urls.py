from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client
from http import HTTPStatus

from posts.models import Post, Group

User = get_user_model()


class PostsUrlTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='tester')
        cls.post = Post.objects.create(author=cls.user)
        cls.group = Group.objects.create(title='google',
                                         slug='google')

    def setUp(self) -> None:
        self.guest_user = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_use_correct_template(self) -> None:
        """Test whether URLs use the correct templates for unauthorized users."""

        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.user}/',
            'posts/post_detail.html': f'/posts/{self.post.id}/'
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_user.get(address)
                self.assertTemplateUsed(response, template)

    def test_user_can_open_page_for_auth_user(self) -> None:
        """Test whether authorized users can access the create post page."""

        response = self.authorized_client.get('/create/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_author_can_see_edit_post_page(self) -> None:
        """Test whether the edit post page is rendered correctly
        only for authorized users who are also the author of the post."""

        response = self.authorized_client.get(f'/posts/{self.post.id}/edit/')
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_is_page_302(self) -> None:
        """Test whether the page returns a 302 status code."""
        response = self.guest_user.get(reverse('posts:post_create'))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
