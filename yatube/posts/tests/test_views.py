from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from django import forms
from http import HTTPStatus
from posts.models import Post, Group


User = get_user_model()


class PostsPagesTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group1 = Group.objects.create(
            title='Тестовая группа 1',
            slug='test-slug1',
            description='Тестовое описание',
        )
        cls.group2 = Group.objects.create(
            title='Тестовая группа 2',
            slug='test-slug2',
            description='Тестовое описание',
        )
        for i in range(1, 11):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Тестовый пост {i}',
                group=cls.group1
            )
        for i in range(11, 16):
            cls.post = Post.objects.create(
                author=cls.user,
                text=f'Тестовый пост {i}',
                group=cls.group2
            )

    def setUp(self) -> None:
        super().setUp()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_posts_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        posts_pages_dict = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': 'test-slug1'}):
                'posts/group_list.html',
            reverse('posts:profile', kwargs={'username': 'auth'}):
                'posts/profile.html',
                reverse('posts:post_detail', kwargs={'post_id': 1}):
                'posts/post_detail.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edit', kwargs={'post_id': 1}):
                'posts/create_post.html',
        }
        for name, template in posts_pages_dict.items():
            with self.subTest(name=name):
                response = self.authorized_client.get(name)
                self.assertTemplateUsed(response, template)

    def test_index_page_1_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом и содержит нужное
         количество постов."""
        response = self.authorized_client.get(reverse('posts:index'))
        for post in response.context['page_obj']:
            self.assertIsInstance(post, Post)
            self.assertIsNotNone(post.group.title)
        posts_count = len(response.context['page_obj'])
        self.assertEqual(posts_count, settings.POSTS_NUM)

    def test_index_page_2_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом и содержит
         нужное количество постов (стр.2)."""
        response = self.authorized_client.get(reverse('posts:index') +
                                              '?page=2')
        for post in response.context['page_obj']:
            self.assertIsInstance(post, Post)
            self.assertIsNotNone(post.group.title)
        posts_count = len(response.context['page_obj'])
        self.assertEqual(posts_count, 5)

    def test_group_page_1_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом и содержит
         нужное количество постов."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'test-slug1'}
            ))
        for post in response.context['page_obj']:
            self.assertIsInstance(post, Post)
            self.assertEqual(post.group.title, 'Тестовая группа 1')
        self.assertIsInstance(response.context['group'], Group)
        posts_count = len(response.context['page_obj'])
        self.assertEqual(posts_count, settings.POSTS_NUM)

    def test_group_page_2_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом и содержит
         нужное количество постов (стр.2)."""
        response = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'test-slug2'}
            ))
        for post in response.context['page_obj']:
            self.assertIsInstance(post, Post)
            self.assertEqual(post.group.title, 'Тестовая группа 2')
        self.assertIsInstance(response.context['group'], Group)
        posts_count = len(response.context['page_obj'])
        self.assertEqual(posts_count, 5)
        diff_group_posts = self.authorized_client.get(reverse(
            'posts:group_list', kwargs={'slug': 'test-slug1'}
            ))
        self.assertNotEqual(diff_group_posts.context['group'].title,
                            response.context['group'].title)

    def test_profile_page_1_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом и содержит
         нужное количество постов."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'auth'}
            ))
        for post in response.context['page_obj']:
            self.assertIsInstance(post, Post)
            self.assertIsNotNone(post.group.title)
        self.assertIsInstance(response.context['username'], User)
        posts_count = len(response.context['page_obj'])
        self.assertEqual(posts_count, settings.POSTS_NUM)

    def test_profile_page_2_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом и содержит
         нужное количество постов (стр.2)."""
        response = self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'auth'}
            ) + '?page=2')
        for post in response.context['page_obj']:
            self.assertIsInstance(post, Post)
            self.assertIsNotNone(post.group.title)
        self.assertIsInstance(response.context['username'], User)
        posts_count = len(response.context['page_obj'])
        self.assertEqual(posts_count, 5)

    def test_post_detail_page_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом"""
        id = 7
        response = self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': id}
            ))
        post = response.context['post']
        self.assertIsInstance(post, Post)
        self.assertEqual(post.id, id)

    def test_post_create_page_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse('posts:post_create'))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_create_page_not_available_for_guest(self):
        """Шаблон post_create недоступен для неавторизованного пользователя"""
        response = self.guest_client.get(reverse('posts:post_create'))
        self.assertTemplateNotUsed(response, 'posts/create_post.html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_post_edit_page_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом"""
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': 1}
            ))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_not_available_for_guest(self):
        """Шаблон post_edit недоступен для неавторизованного пользователя"""
        response = self.guest_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': 1}
            ))
        self.assertTemplateNotUsed(response, 'posts/create_post.html')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
