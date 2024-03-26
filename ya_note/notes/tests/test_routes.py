from http import HTTPStatus

from django.urls import reverse

from .conftest import NotesTestCase


class RoutesTestCase(NotesTestCase):
    """Тесты для проверки маршрутов."""

    def test_home_page_for_anonymous_user(self):
        """
        Проверяем доступность страниц
        для анонимных пользователей.
        """
        urls = (
            'notes:home',
            'users:logout',
            'users:login',
            'users:signup'
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(reverse(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_different_pages_for_auth_user(self):
        """
        Проверяем доступность страниц
        для авторизированных пользователей.
        """
        urls = (
            'notes:list',
            'notes:add',
            'notes:success',
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(reverse(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_detail_delete_edit_page_for_only_author(self):
        """
        Проверяем доступность страниц
        для авторизированных пользователей
        только для автора заметки.
        """
        urls = (
            ('notes:detail', self.note.slug),
            ('notes:edit', self.note.slug),
            ('notes:delete', self.note.slug),
        )
        users_ststus = (
            (self.user_client, HTTPStatus.NOT_FOUND),
            (self.author_client, HTTPStatus.OK),
        )
        for user, status in users_ststus:
            for url, args in urls:
                with self.subTest(url=url, user=user):
                    response = user.get(reverse(url, args=(args,)))
                    self.assertEqual(response.status_code, status)

    def test_redirect_to_page_auth0rizetion_for_anonymous_user(self):
        """Проверяем редиректы для анонимных пользователей."""
        urls = ('notes:list', 'notes:add', 'notes:success')
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(reverse(url))
                self.assertRedirects(
                    response,
                    f'{reverse("users:login")}?next={reverse(url)}'
                )
