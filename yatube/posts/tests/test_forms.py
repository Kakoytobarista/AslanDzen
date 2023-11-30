from http import HTTPStatus
import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.shortcuts import get_object_or_404

from posts.forms import PostForm
from posts.models import Post, Group, Comment

User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class PostFieldsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()

    def test_fields_present(self) -> None:
        """Test whether the fields 'text' and 'group' are present in PostForm."""
        fields = PostFieldsTest.form.fields
        self.assertTrue(fields, ('text', 'group'))

    def test_title_help_text(self) -> None:
        """Test whether the help_text for fields is correct."""
        help_text_group = PostFieldsTest.form.fields['group'].help_text
        help_text_for_text = PostFieldsTest.form.fields['text'].help_text
        self.assertEqual(help_text_group, ('This is the field for choosing the post group, '
                                           'it is optional.'))
        self.assertEqual(help_text_for_text,
                         ('This is the field for the text '
                          'of the post, it has no restrictions '
                          'on the number of characters.'))


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_superuser(username='form_tester',
                                                 email='mail@mail.ru',
                                                 password='qwe123!@#')
        cls.another_user = User.objects.create_user(username='another_user',
                                                    email='another@mail.ru',
                                                    password='qwe123!@#')
        cls.group = Group.objects.create(title='mail',
                                         slug='mail',
                                         description='just a mail')
        cls.post = Post.objects.create(text='its test text in setup',
                                       author=cls.user,
                                       group=cls.group
                                       )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self) -> None:
        self.guest_user = Client()

        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

        self.another_auth_client = Client()
        self.another_auth_client.force_login(self.another_user)

    def test_create_post(self) -> None:
        """Test the correct creation of a Post object."""
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
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
        post_count = Post.objects.count()
        form_data = {
            'text': 'its test text',
            'author': self.user,
            'image': uploaded
        }
        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data,
                                               follow=True)
        created_post = get_object_or_404(Post, text=form_data['text'])

        self.assertRedirects(response, reverse('posts:profile',
                                               args=[self.user]))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertEqual(created_post.text, form_data['text'])
        self.assertEqual(created_post.author.get_username(),
                         form_data['author'].get_username())
        self.assertTrue(created_post.image, form_data['image'])

    def test_edit_post(self) -> None:
        """Test the ability to edit a post using the PostForm at reverse('posts:update_pos')."""
        form_data = {
            'text': 'its new test text',
        }
        response = self.authorized_client.post(reverse('posts:update_post',
                                                       args=[self.post.id]),
                                               data=form_data,
                                               follow=True)
        post = get_object_or_404(Post, text=form_data['text'])
        self.assertRedirects(response, reverse('posts:post_detail',
                                               args=[self.user.id]))
        self.assertEqual(post.text,
                         form_data['text'])
        self.assertEqual(post.author.get_username(),
                         self.user.get_username())

    def test_un_auth_user_cant_create_post(self) -> None:
        """Test that an unauthorized user cannot create a post."""
        form_data = {
            'text': 'its test text',
            'author': self.user,
        }
        response_guest = self.guest_user.post(reverse('posts:post_create'),
                                              data=form_data,
                                              follow=True)
        self.assertTrue(response_guest.status_code, HTTPStatus.NOT_FOUND)
        self.assertRedirects(
            response_guest,
            reverse('users:login') + '?next=' + reverse('posts:post_create'))

    def test_add_comment_can_only_auth_user(self) -> None:
        """Test that only an authorized user can leave comments."""
        form_data = {
            'text': 'test mongol',
            'author': self.user
        }
        response_auth = self.authorized_client.post(
            reverse('posts:add_comment',
                    args=[self.post.id]),
            data=form_data,
            follow=True)
        comment = get_object_or_404(Comment, text=form_data['text'])
        self.assertEqual(response_auth.status_code, HTTPStatus.OK)
        self.assertRedirects(response_auth,
                             reverse('posts:post_detail',
                                     args=[self.post.id]))
        self.assertEqual(comment.text, form_data['text'])

    def test_cash_on_index_page_working(self) -> None:
        """Test whether the cache of posts on the index page is working."""
        form_data = {
            'text': 'cash_text',
            'author': self.user
        }

        self.authorized_client.post(reverse('posts:post_create'),
                                    data=form_data,
                                    follow=True
                                    )
        content = self.authorized_client.get(reverse('posts:index')).content
        get_object_or_404(Post, text=form_data['text']).delete()
        self.assertIn(form_data['text'], str(content))
