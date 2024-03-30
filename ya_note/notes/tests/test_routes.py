from http import HTTPStatus

from .conftest import NotesTestCase


class RoutesTestCase(NotesTestCase):
    """Тесты для проверки маршрутов и редиректов"""

    def test_page_access_for_different_users(self):
        urls_and_expected_status = [
            (self.ROUTE_FOR_THE_HOME_PAGE, HTTPStatus.OK),
            (self.ROUTE_FOR_THE_USER_LOGOUT_PAGE, HTTPStatus.OK),
            (self.ROUTE_FOR_THE_USER_SIGNUP_PAGE, HTTPStatus.OK),
            (self.ROUTE_FOR_THE_USER_LOGIN_PAGE, HTTPStatus.OK),
            (self.ROUTE_FOR_THE_LIST_PAGE, HTTPStatus.OK),
            (self.ROUTE_FOR_THE_ADD_NOTE_PAGE, HTTPStatus.OK),
            (self.ROUTE_FOR_THE_SUCCESS_PAGE, HTTPStatus.OK),
            (self.ROUTE_FOR_THE_DETAIL_NOTE_PAGE, HTTPStatus.NOT_FOUND),
            (self.ROUTE_FOR_THE_EDIT_NOTE_PAGE, HTTPStatus.NOT_FOUND),
            (self.ROUTE_FOR_THE_DELETE_NOTE_PAGE, HTTPStatus.NOT_FOUND)
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
                            response, f'{self.ROUTE_FOR_THE_USER_LOGIN_PAGE}'
                            f'?next={url}'
                        )

                    if url in [self.ROUTE_FOR_THE_DETAIL_NOTE_PAGE,
                               self.ROUTE_FOR_THE_EDIT_NOTE_PAGE,
                               self.ROUTE_FOR_THE_DELETE_NOTE_PAGE]:
                        response = user.get(url, follow=True, credentials=True)
                        self.assertEqual(response.status_code, expected_status)
