from http import HTTPStatus

from django.urls import reverse

from .conftest import NotesTestCase
from .set_of_routes import (ROUTE_FOR_THE_ADD_NOTE_PAGE,
                            ROUTE_FOR_THE_DELETE_NOTE_PAGE,
                            ROUTE_FOR_THE_DETAIL_NOTE_PAGE,
                            ROUTE_FOR_THE_EDIT_NOTE_PAGE,
                            ROUTE_FOR_THE_HOME_PAGE,
                            ROUTE_FOR_THE_LIST_PAGE,
                            ROUTE_FOR_THE_SUCCESS_PAGE,
                            ROUTE_FOR_THE_USER_LOGIN_PAGE,
                            ROUTE_FOR_THE_USER_LOGOUT_PAGE,
                            ROUTE_FOR_THE_USER_SIGNUP_PAGE)


class RoutesTestCase(NotesTestCase):
    """Тесты для проверки маршрутов."""

    def test_home_page_for_anonymous_user(self):
        """
        Проверяем доступность страниц
        для анонимных пользователей.
        """
        urls = (
            ROUTE_FOR_THE_HOME_PAGE,
            ROUTE_FOR_THE_USER_LOGOUT_PAGE,
            ROUTE_FOR_THE_USER_SIGNUP_PAGE,
            ROUTE_FOR_THE_USER_LOGIN_PAGE
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(self.reverse_method(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_different_pages_for_auth_user(self):
        """
        Проверяем доступность страниц
        для авторизированных пользователей.
        """
        urls = (
            ROUTE_FOR_THE_LIST_PAGE,
            ROUTE_FOR_THE_ADD_NOTE_PAGE,
            ROUTE_FOR_THE_SUCCESS_PAGE,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.user_client.get(self.reverse_method(url))
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_availability_detail_delete_edit_page_for_only_author(self):
        """
        Проверяем доступность страниц
        для авторизированных пользователей
        только для автора заметки.
        """
        urls = (
            (ROUTE_FOR_THE_DETAIL_NOTE_PAGE, self.note.slug),
            (ROUTE_FOR_THE_EDIT_NOTE_PAGE, self.note.slug),
            (ROUTE_FOR_THE_DELETE_NOTE_PAGE, self.note.slug),
        )
        users_ststus = (
            (self.user_client, HTTPStatus.NOT_FOUND),
            (self.author_client, HTTPStatus.OK),
        )
        for user, status in users_ststus:
            for url, args in urls:
                with self.subTest(url=url, user=user):
                    response = user.get(self.reverse_method(url, (args,)))
                    self.assertEqual(response.status_code, status)

    def test_redirect_to_page_auth0rizetion_for_anonymous_user(self):
        """Проверяем редиректы для анонимных пользователей."""
        urls = (ROUTE_FOR_THE_LIST_PAGE,
                ROUTE_FOR_THE_ADD_NOTE_PAGE,
                ROUTE_FOR_THE_SUCCESS_PAGE
                )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(self.reverse_method(url))
                self.assertRedirects(
                    response,
                    f'{reverse(ROUTE_FOR_THE_USER_LOGIN_PAGE)}'
                    f'?next={reverse(url)}'
                )
