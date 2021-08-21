from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
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

    def setUp(self):
        self.guest_user = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_use_correct_template(self):
        """Проверка на корректный рендеринг страниц
        для неавторизованных пользователей."""

        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.user}/',
            'posts/post_detail.html': f'/posts/{self.post.id}/'
        }
        for template, adress in templates_url_names.items():
            with self.subTest(adress=adress):
                response = self.guest_user.get(adress)
                self.assertTemplateUsed(response, template)

    def test_user_can_open_page_for_auth_user(self):
        """Проверка на корректный рендеринг страниц только
        авторизованных пользователей."""

        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_author_can_see_edit_post_page(self):
        """Проверка на корректный рендеринг страницы редактирования
        поста только у авторизованного пользователя + Автора этого поста."""

        response = self.authorized_client.get(reverse('posts:update_post',
                                                      args=[self.post.id]))
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_is_page_404(self):
        """Проверка на возврат 404 ошибки"""
        response = self.authorized_client.get('posts/tests/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
