from django.contrib.auth import get_user_model
from django.test import TestCase

from posts.models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        group = PostModelTest.group

        self.assertEqual(str(post), 'Тестовый пост')
        self.assertEqual(str(group), 'Тестовая группа')

    def test_post_verbose_name(self):
        """verbose_name в полях модели post совпадает с ожидаемым."""
        post = PostModelTest.post
        field_verboses = {
            'text': 'Текст поста',
            'pub_date': 'Дата публикации',
            'author': 'Автор',
            'group': 'Группа',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).verbose_name, expected_value)

    def test_group_verbose_name(self):
        """verbose_name в полях модели group совпадает с ожидаемым."""
        group = PostModelTest.group
        field_verboses = {
            'title': 'Группа',
            'slug': 'URL',
            'description': 'Описание группы',
        }
        for field, expected_value in field_verboses.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).verbose_name, expected_value)

    def test_group_help_text(self):
        """help_text в полях модели group совпадает с ожидаемым."""
        group = PostModelTest.group
        field_help_texts = {
            'title': 'Группа, к которой будет относиться пост',
            'slug': 'Название группы для URL',
            'description': 'Подробное описание группы',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    group._meta.get_field(field).help_text, expected_value)

    def test_post_help_text(self):
        """help_text в полях модели group совпадает с ожидаемым."""
        post = PostModelTest.post
        field_help_texts = {
            'text': 'Текст нового поста',
            'pub_date': 'Дата публикации поста',
            'author': 'Автор поста',
            'group': 'Группа, к которой относится пост',
        }
        for field, expected_value in field_help_texts.items():
            with self.subTest(field=field):
                self.assertEqual(
                    post._meta.get_field(field).help_text, expected_value)
