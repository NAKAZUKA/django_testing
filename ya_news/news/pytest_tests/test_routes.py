from http import HTTPStatus

from django.urls import reverse
from pytest_django.asserts import assertRedirects

ROUTES_FOR_HOME_PAGE = reverse('news:home')
ROUTES_FOR_USER_LOGIN_PAGE = reverse('users:login')
ROUTES_FOR_USER_LOGOUT_PAGE = reverse('users:logout')
ROUTES_FOR_USER_SIGNUP_PAGE = reverse('users:signup')


def test_pages_availability_for_different_users(client,
                                                author_client,
                                                not_author_client,
                                                detail_page_url,
                                                delete_page_url,
                                                edit_page_url,
                                                news
                                                ):
    """Тест проверяет доступность страниц для различных пользователей"""
    routes_to_check = [
        (client, ROUTES_FOR_HOME_PAGE, HTTPStatus.OK),
        (client, ROUTES_FOR_USER_LOGIN_PAGE, HTTPStatus.OK),
        (client, ROUTES_FOR_USER_LOGOUT_PAGE, HTTPStatus.OK),
        (client, ROUTES_FOR_USER_SIGNUP_PAGE, HTTPStatus.OK),
        (client, detail_page_url, HTTPStatus.OK),
        (author_client, delete_page_url, HTTPStatus.OK),
        (author_client, edit_page_url, HTTPStatus.OK),
        (not_author_client, delete_page_url, HTTPStatus.NOT_FOUND),
        (not_author_client, edit_page_url, HTTPStatus.NOT_FOUND),
    ]

    for client_type, url, expected_status_code in routes_to_check:
        response = client_type.get(url)
        assert response.status_code == expected_status_code


def test_redirect_for_anonymous_user(client, delete_page_url, edit_page_url):
    """Тест проверяет перенаправление анонимного пользователя."""
    routes_to_check = [
        (delete_page_url),
        (edit_page_url),
    ]

    for url in routes_to_check:
        response = client.get(url)
        assertRedirects(
            response,
            ROUTES_FOR_USER_LOGIN_PAGE + '?next=' + url
        )
