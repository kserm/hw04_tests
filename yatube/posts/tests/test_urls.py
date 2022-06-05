from http import HTTPStatus
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from posts.models import Post, Group


User = get_user_model()


POST_URL_DICT_GUEST = {
    '/': 'posts/index.html',
    '/group/test-slug/': 'posts/group_list.html',
    '/profile/auth/': 'posts/profile.html',
    '/posts/1/': 'posts/post_detail.html',
}

POST_URL_DICT_AUTH = {
    '/create/': 'posts/create_post.html',
    '/posts/1/edit/': 'posts/create_post.html',
}


class PostsURLTests(TestCase):
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
        )

    def setUp(self) -> None:
        super().setUp()
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_url_exists_for_guest(self):
        for address in POST_URL_DICT_GUEST.keys():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.guest_client.get('unexisting_page')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_url_exists_for_authorized(self):
        for address in POST_URL_DICT_GUEST.keys():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        for address in POST_URL_DICT_AUTH.keys():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.authorized_client.get('unexisting_page')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template_for_guest(self):
        for address, template in POST_URL_DICT_GUEST.items():
            with self.subTest(address=address):
                response = self.guest_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_urls_uses_correct_template_for_authorized(self):
        for address, template in POST_URL_DICT_GUEST.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
        for address, template in POST_URL_DICT_AUTH.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)
