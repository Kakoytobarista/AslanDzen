from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.forms import PostForm
from posts.models import Post, Group

User = get_user_model()


class PostFieldsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()

    def test_fields_present(self):
        """Проверка на наличие полей формы PostForm"""
        fields = PostFieldsTest.form.fields
        self.assertTrue(fields, ('text', 'group'))

    def test_title_help_text(self):
        """Проверка на корректные help_text полей"""
        help_text_group = PostFieldsTest.form.fields['group'].help_text
        help_text_for_text = PostFieldsTest.form.fields['text'].help_text
        self.assertEqual(help_text_group, ('Это поле выбора группы поста, '
                                           'оно необязательное.'))
        self.assertEqual(help_text_for_text,
                         ('Это поле для текста '
                          'поста, оно не имеет ограничений '
                          'на количество символов.'))


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_superuser(username='form_tester',
                                                 email='mail@mail.ru',
                                                 password='qwe123!@#')
        cls.group = Group.objects.create(title='mail',
                                         slug='mail',
                                         description='just a mail')
        cls.post = Post.objects.create(text='its test text',
                                       author=cls.user,
                                       group=cls.group
                                       )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Проверка на корректное создание Post объекта"""
        post_count = Post.objects.count()
        form_data = {
            'text': 'its test text',
            'author': self.user,
        }
        response = self.authorized_client.post(reverse('posts:post_create'),
                                               data=form_data,
                                               follow=True)
        self.assertRedirects(response, reverse('posts:profile',
                                               args=[self.user]))
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertTrue(Post.objects.filter(text='its test text',
                                            author=self.user,
                                            group=self.group).exists())

    def test_cant_create_group_with_existing_slug(self):
        """Проверка на невозможность создания объекта
        Group с неуникальным значением slug поля"""
        form_data = {
            'title': 'mail',
            'slug': 'mail',
            'description': 'just a mail'
        }
        response = self.authorized_client.post('/admin/posts/group/add/',
                                               data=form_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_post(self):
        """Проверка на возможность изменение поста через
        форму PostForm у reverse('posts:update_pos')"""
        form_data = {
            'text': 'its new test text',
            'author': self.user,
        }
        response = self.authorized_client.post(reverse('posts:update_post',
                                                       args=[self.post.id]),
                                               data=form_data,
                                               follow=True)
        self.assertRedirects(response, reverse('posts:post_detail',
                                               args=[self.user.id]))
        self.assertEqual(Post.objects.get(id=self.post.id).text,
                         'its new test text')
