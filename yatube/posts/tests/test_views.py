import shutil
import tempfile
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django import forms

from posts.models import Post, Group, Follow
from posts import factories

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostsViewsTests(TestCase):
    """
    Test cases for the views related to posts in the application.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test data for the test class.
        """
        super().setUpClass()
        cls.user = User.objects.create_user(username='tester')
        cls.group = Group.objects.create(title='google',
                                         slug='google',
                                         description='its google dude')
        cls.second_group = Group.objects.create(title='yandex',
                                                slug='yandex',
                                                description='its yandex dude')
        small_gif = (b'\x47\x49\x46\x38\x39\x61\x02\x00'
                     b'\x01\x00\x80\x00\x00\x00\x00\x00'
                     b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
                     b'\x00\x00\x00\x2C\x00\x00\x00\x00'
                     b'\x02\x00\x01\x00\x00\x02\x02\x0C'
                     b'\x0A\x00\x3B'
                     )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        cls.post = Post.objects.create(text='its_test_post',
                                       author=cls.user,
                                       group=cls.group,
                                       pub_date='21.02.2021',
                                       image=uploaded
                                       )

    @classmethod
    def tearDownClass(cls):
        """
        Clean up after the test class.
        """
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        """
        Set up test data for each test method.
        """
        self.guest_user = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_with_set_group_present_to_pages(self):
        """
        Test that a post with a set group is present on index, group_list, and profile pages.
        """
        templates_urls = {
            reverse('posts:index'): self.post,
            reverse('posts:group_list', args=[self.group.slug]): self.post,
            reverse('posts:profile', args=[self.user]): self.post
        }

        for address, template in templates_urls.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address).context.get('page_obj').object_list
                self.assertIn(template, response)

    def test_post_with_set_group_not_present_wrong_group_page(self):
        """
        Test that a post without a set group is not present on the wrong group_list page.
        """
        address = reverse('posts:group_list', args=[self.second_group.slug])
        response = self.authorized_client.get(address).context.get('page_obj').object_list

        self.assertNotIn(self.post, response)

    def test_views_use_correct_template_with_guest_user(self):
        """
        Test that views render the correct template for guest users.
        """
        templates_url_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse('posts:group_list', args=[self.group.slug]),
            'posts/profile.html': reverse('posts:profile', args=[self.user]),
            'posts/post_detail.html': reverse('posts:post_detail', args=[self.post.id]),
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.guest_user.get(address)
                self.assertTemplateUsed(response, template)

    def test_views_use_correct_template_with_auth_user(self):
        """Test that views use the correct template for authenticated users."""
        templates_url_names = {
            'posts/create_post.html': [reverse("posts:post_create"),
                                       reverse("posts:update_post",
                                               args=[self.post.id])]
        }

        response_create_post = self.authorized_client.get(
            templates_url_names['posts/create_post.html'][0])
        response_update_post = self.authorized_client.get(
            templates_url_names['posts/create_post.html'][1])
        self.assertTemplateUsed(response_create_post,
                                'posts/create_post.html')
        self.assertTemplateUsed(response_update_post,
                                'posts/create_post.html')

    def test_create_post_page_show_correct_context(self):
        """Test that the create_post template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_update_post_page_show_correct_context(self):
        """Test that the update_post template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:update_post',
                                                      args=[self.post.id]))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }

        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_posts_index_page_show_correct_context(self):
        """Test that the posts:index template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:index'))
        title = response.context['title']
        self.assertEqual(title, 'Главная страница')
        post_context = response.context['page_obj']

        for post in post_context:
            self.assertEqual(post.text, self.post.text)
            self.assertEqual(post.author.get_username(),
                             self.post.author.get_username())
            self.assertEqual(post.group.title, self.post.group.title)
            self.assertEqual(post.image, self.post.image)

    def test_group_page_show_correct_context(self):
        """Test that the posts:group_list template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:group_list',
                                                      args=[self.group.slug]))
        title = response.context['title']
        post_object = response.context['page_obj']
        self.assertEqual(title, self.group)
        self.assertEqual(title.description, self.group.description)

        for post in post_object:
            self.assertEqual(post.text, self.post.text)
            self.assertEqual(post.author.get_username(),
                             self.post.author.get_username())
            self.assertEqual(post.group.title, self.post.group.title)
            self.assertEqual(post.image, self.post.image)

    def test_profile_page_show_correct_context(self):
        """Test that the posts:profile template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:profile',
                                                      args=[self.user]))
        title = response.context['title']
        count_posts = response.context['count_posts']
        author = response.context['author']
        post_object = response.context['page_obj']

        self.assertEqual(title, f'Профайл пользователя {self.user}')
        self.assertEqual(count_posts, len(Post.objects.all()))
        self.assertEqual(author, self.user)

        for post in post_object:
            self.assertEqual(post.text, self.post.text)
            self.assertEqual(post.author.get_username(),
                             self.post.author.get_username())
            self.assertEqual(post.group.title, self.post.group.title)
            self.assertEqual(post.image, self.post.image)

    def test_post_detail_page_show_correct_context(self):
        """Test that the post_detail template is formed with the correct context."""
        response = self.authorized_client.get(reverse('posts:post_detail',
                                                      args=[self.post.id]))
        post_context = response.context['post']
        title_context = response.context['title']
        count_posts_context = response.context['count_posts']

        self.assertEqual(count_posts_context, len(Post.objects.all()))
        self.assertEqual(title_context, self.post.text[:30])
        self.assertEqual(post_context.text, self.post.text)
        self.assertEqual(post_context.author.username,
                         self.post.author.get_username())
        self.assertEqual(post_context.group.title, self.post.group.title)
        self.assertEqual(post_context.image, self.post.image)

    def test_post_detail_page_show_correct_form_context(self):
        """Test that the post_detail template correctly displays the form context."""
        response = self.authorized_client.get(reverse('posts:post_detail',
                                                      args=[self.post.id]))
        form_context = response.context['form']
        self.assertTrue(form_context)

class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up data for PaginatorViewsTest"""
        super().setUpClass()
        cls.user = User.objects.create_user('tester2')
        cls.group = Group.objects.create(title='google', slug='google', description='its google dude')
        factories.PostFactory.create_batch(13, author=cls.user, group=cls.group)

    def setUp(self) -> None:
        """Set up the authorized client for testing"""
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_views_contains_ten_records(self) -> None:
        """Test whether views contain ten records on the first page"""
        templates_urls = {
            self.client.get(reverse('posts:group_list', args=[self.group.slug])): 10,
            self.client.get(reverse('posts:index')): 10,
            self.client.get(reverse('posts:profile', args=[self.user])): 10
        }
        for value, expected in templates_urls.items():
            with self.subTest(value=value):
                form_field = value.context['page_obj']
                self.assertEqual(len(form_field), expected)

    def test_views_contains_three_records(self) -> None:
        """Test whether views contain three records on the second page"""
        templates_urls = {
            self.client.get(reverse('posts:group_list', args=[self.group.slug]) + '?page=2'): 3,
            self.client.get(reverse('posts:index') + '?page=2'): 3,
            self.client.get(reverse('posts:profile', args=[self.user]) + '?page=2'): 3
        }
        for value, expected in templates_urls.items():
            with self.subTest(value=value):
                form_field = value.context['page_obj']
                self.assertEqual(len(form_field), expected)


class FollowViewsTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        """Set up data for FollowViewsTest"""
        super().setUpClass()
        cls.user = User.objects.create_superuser(username='form_tester',
                                                 email='mail@mail.ru',
                                                 password='qwe123!@#')
        cls.another_user = User.objects.create_user(username='another_user',
                                                    email='another@mail.ru',
                                                    password='qwe123!@#')
        cls.group = Group.objects.create(title='mail', slug='mail', description='just a mail')
        cls.post = Post.objects.create(text='its test text in setup', author=cls.user, group=cls.group)

    @classmethod
    def tearDownClass(cls) -> None:
        """Clean up after FollowViewsTest"""
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        """Set up clients for testing"""
        self.guest_user = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.another_auth_client = Client()
        self.another_auth_client.force_login(self.another_user)

    def test_following_posts_present_at_follow_page(self) -> None:
        """Test whether posts from followed authors are present on the follow page"""
        response_content = self.another_auth_client.get(reverse('posts:follow_index')).content
        self.assertNotIn(self.post.text, str(response_content))
        self.another_auth_client.post(reverse('posts:profile_follow', args=[self.user]))
        posts_after_follow = self.another_auth_client.get(reverse('posts:follow_index')).content
        self.assertIn(self.post.text, str(posts_after_follow))

    def test_posts_not_present_for_unfollow_user(self) -> None:
        """Test whether posts from authors not followed by the user do not appear on the follow page"""
        self.another_auth_client.post(reverse('posts:profile_follow', args=[self.user]))
        response = self.authorized_client.get(reverse('posts:follow_index')).content
        self.assertNotIn(self.post.text, str(response))

    def test_auth_user_can_following(self) -> None:
        """Test whether an authenticated user can follow other users"""
        response_auth = self.another_auth_client.post(reverse('posts:profile_follow', args=[self.user]))
        self.assertEqual(response_auth.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response_auth, reverse('posts:profile', args=[self.user.username]))
        following = Follow.objects.filter(user=self.another_user)
        self.assertTrue(following.exists())

    def test_auth_user_can_unfollow(self) -> None:
        """Test whether an authenticated user can unfollow other users"""
        self.another_auth_client.post(reverse('posts:profile_follow', args=[self.user]))
        self.another_auth_client.post(reverse('posts:profile_unfollow', args=[self.user]))
        follow = Follow.objects.filter(user=self.another_user)
        self.assertNotIn(self.another_user, follow)
