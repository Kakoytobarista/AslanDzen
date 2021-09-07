from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый объект модели Post',
        )

    def test_post_have_correct_object_name(self):
        """Проверяем, что у модели Post строка возвращаемая
         методом __str__ берется из поля text."""

        self.assertIn(self.post.__str__(), self.post.text)

    def test_post_have_length_str_method_with_15_symbols(self):
        """Проверяем, что у модели Post длина строки
         возвращаемая методом __str__ не более 15 символов."""

        self.assertLess(len(self.post.__str__()), 16)

    def test_post_have_empty_group_without_set_field_group(self):
        """Проверяем что при создании поста без указания группы,
        группа к посту не прикрепляется."""

        self.assertIsNone(self.post.group)

    def test_post_have_auto_correct_pub_date(self):
        """Проверяем что дата присуждающаяся посту, добавляется
        корректно."""

        current_time = dt.now().strftime("%d/%m/%y %H:%M")
        pub_date_field = self.post.pub_date.strftime("%d/%m/%y %H:%M")
        self.assertEqual(pub_date_field, current_time)

    def test_post_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""

        task = PostModelTest.post
        verbose_fields = {
            'author': 'Автор поста',
            'text': 'Текст поста',
            'pub_date': 'Дата создания',
            'group': 'Группа',
        }
        for field, expected_value in verbose_fields.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)


class PostGroupTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_group_have_correct_object_name(self):
        """Проверяем, что у модели Group корректно строка возвращаемая
        методом __str__ равна значению поля title."""

        self.assertEqual(self.group.__str__(), self.group.title)

    def test_group_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""

        task = PostGroupTest.group
        fields_verbose_name_text = {
            'title': 'Имя',
            'slug': 'Адрес',
            'description': 'Описание',
        }
        for field, expected_value in fields_verbose_name_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)
