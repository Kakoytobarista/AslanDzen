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
            text='Test model object Post',
        )

    def test_post_have_correct_object_name(self) -> None:
        """Test that the Post model's __str__ method returns the value of the 'text' field."""
        self.assertIn(self.post.__str__(), self.post.text)

    def test_post_have_length_str_method_with_15_symbols(self) -> None:
        """Test that the length of the string returned by the Post model's __str__ method is less than 16 characters."""
        self.assertLess(len(self.post.__str__()), 16)

    def test_post_have_empty_group_without_set_field_group(self) -> None:
        """Test that when creating a post without specifying a group, the post is not attached to any group."""
        self.assertIsNone(self.post.group)

    def test_post_have_auto_correct_pub_date(self) -> None:
        """Test that the date assigned to the post is added correctly."""
        current_time = dt.now().strftime("%d/%m/%y %H:%M")
        pub_date_field = self.post.pub_date.strftime("%d/%m/%y %H:%M")
        self.assertEqual(pub_date_field, current_time)

    def test_post_verbose_name(self) -> None:
        """Test that the verbose_name in the fields matches the expected values."""
        task = PostModelTest.post
        verbose_fields = {
            'author': 'Author of the post',
            'text': 'Post text',
            'pub_date': 'Creation date',
            'group': 'Group',
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
            title='Test group',
            slug='Test slug',
            description='Test description',
        )

    def test_group_have_correct_object_name(self) -> None:
        """Test that the Group model's __str__ method returns the value of the 'title' field."""
        self.assertEqual(self.group.__str__(), self.group.title)

    def test_group_verbose_name(self) -> None:
        """Test that the verbose_name in the fields matches the expected values."""
        task = PostGroupTest.group
        fields_verbose_name_text = {
            'title': 'Name',
            'slug': 'Address',
            'description': 'Description',
        }
        for field, expected_value in fields_verbose_name_text.items():
            with self.subTest(field=field):
                self.assertEqual(
                    task._meta.get_field(field).verbose_name, expected_value)
