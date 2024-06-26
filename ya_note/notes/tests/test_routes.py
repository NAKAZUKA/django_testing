from http import HTTPStatus

from .conftest import NotesTestCase


class RoutesTestCase(NotesTestCase):
    """Тесты для проверки маршрутов и редиректов"""

    def test_page_access_for_different_users(self):
        urls_and_expected_status = [
            (self.HOME_URL, self.client, HTTPStatus.OK),
            (self.USER_LOGIN_URL, self.client, HTTPStatus.OK),
            (self.USER_LOGIN_URL, self.client, HTTPStatus.OK),
            (self.USER_LOGOUT_URL, self.client, HTTPStatus.OK),
            (self.LIST_URL, self.client, HTTPStatus.FOUND),
            (self.ADD_URL, self.author_client, HTTPStatus.OK),
            (self.SUCCES_URL, self.author_client, HTTPStatus.OK),
            (self.DETAIL_URL, self.user_client, HTTPStatus.NOT_FOUND),
            (self.EDIT_URL, self.user_client, HTTPStatus.NOT_FOUND),
            (self.DELETE_URL, self.user_client, HTTPStatus.NOT_FOUND),
            (self.DETAIL_URL, self.author_client, HTTPStatus.OK),
            (self.EDIT_URL, self.author_client, HTTPStatus.OK),
            (self.DELETE_URL, self.author_client, HTTPStatus.OK)
        ]

        for url, client, expected_status_code in urls_and_expected_status:
            assert client.get(url).status_code == expected_status_code

    def test_redirect_for_anonymous_user(self):
        """Тест проверяет перенаправление анонимного пользователя."""
        routes_to_check = [
            (self.DETAIL_URL),
            (self.EDIT_URL),
            (self.DELETE_URL),
        ]
        for url in routes_to_check:
            response = self.client.get(url)
            self.assertRedirects(
                response, f'{self.USER_LOGIN_URL}?next={url}'
            )
