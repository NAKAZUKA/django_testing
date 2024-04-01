from http import HTTPStatus

from .conftest import NotesTestCase


class RoutesTestCase(NotesTestCase):
    """Тесты для проверки маршрутов и редиректов"""

    def test_page_access_for_different_users(self):
        urls_and_expected_status = [
            (self.HOME_URL, HTTPStatus.OK),
            (self.USER_LOGOUT_URL, HTTPStatus.OK),
            (self.USER_SIGNUP_URL, HTTPStatus.OK),
            (self.USER_LOGIN_URL, HTTPStatus.OK),
            (self.LIST_URL, HTTPStatus.OK),
            (self.ADD_URL, HTTPStatus.OK),
            (self.SUCCES_URL, HTTPStatus.OK),
            (self.DETAIL_URL, HTTPStatus.NOT_FOUND),
            (self.EDIT_URL, HTTPStatus.NOT_FOUND),
            (self.DELETE_URL, HTTPStatus.NOT_FOUND)
        ]

        users_and_clients = [
            (self.user_client, HTTPStatus.OK),
            (self.author_client, HTTPStatus.OK)
        ]

        for user, expected_status in users_and_clients:
            for url, _ in urls_and_expected_status:
                with self.subTest(url=url):
                    response = user.get(url, follow=True)
                    self.assertEqual(response.status_code, expected_status)

                    if expected_status != HTTPStatus.OK:
                        self.assertRedirects(
                            response, f'{self.USER_LOGIN_URL}'
                            f'?next={url}'
                        )
