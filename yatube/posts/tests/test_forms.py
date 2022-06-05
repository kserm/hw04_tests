from django.contrib.auth import get_user_model
from posts.forms import PostForm
from posts.models import Post, Group
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
            group=cls.group
        )
        cls.form = PostForm()

    def setUp(self) -> None:
        super().setUp()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        posts_count = Post.objects.count()
        context = {
            'author': 'auth',
            'text': 'Новый тестовый пост',
            'group': (self.group, 1),
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=context,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile',
            kwargs={'username': 'auth'})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Новый тестовый пост',
                group=1
            ).exists()
        )

    def test_edit_post(self):
        posts_count = Post.objects.count()
        context = {
            'text': 'Новый тестовый пост изменен',
            'group': (self.group, 1),
            # 'group': '',
        }
        response = self.authorized_client.post(
            reverse(
                'posts:post_edit', kwargs={'post_id': 1}
            ),
            data=context,
            follow=True
        )
        self.assertRedirects(
            response,
            reverse('posts:post_detail', kwargs={'post_id': 1})
        )
        self.assertEqual(Post.objects.count(), posts_count)
        self.assertTrue(
            Post.objects.filter(
                text='Новый тестовый пост изменен',
                group=1
            ).exists()
        )
