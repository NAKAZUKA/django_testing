from http import HTTPStatus

from django.urls import reverse
import pytest
from pytest_django.asserts import assertRedirects

ROUTES_FOR_HOME_PAGE = reverse('news:home')
ROUTES_FOR_USER_LOGIN_PAGE = reverse('users:login')
ROUTES_FOR_USER_LOGOUT_PAGE = reverse('users:logout')
ROUTES_FOR_USER_SIGNUP_PAGE = reverse('users:signup')


@pytest.mark.parametrize(
    "client_type, url, expected_status_code",
    [
        ("client", ROUTES_FOR_HOME_PAGE, HTTPStatus.OK),
        ("client", ROUTES_FOR_USER_LOGIN_PAGE, HTTPStatus.OK),
        ("client", ROUTES_FOR_USER_LOGOUT_PAGE, HTTPStatus.OK),
        ("client", ROUTES_FOR_USER_SIGNUP_PAGE, HTTPStatus.OK),
        ("client", pytest.lazy_fixture("detail_page_url"), HTTPStatus.OK),
        ("author_client", pytest.lazy_fixture("delete_page_url"),
         HTTPStatus.OK),
        ("author_client", pytest.lazy_fixture("edit_page_url"), HTTPStatus.OK),
        ("not_author_client", pytest.lazy_fixture("delete_page_url"),
         HTTPStatus.NOT_FOUND),
        ("not_author_client", pytest.lazy_fixture("edit_page_url"),
         HTTPStatus.NOT_FOUND),
    ]
)
def test_pages_availability_for_different_users(client,
                                                author_client,
                                                not_author_client,
                                                news,
                                                client_type,
                                                url,
                                                expected_status_code
                                                ):
    """Тест проверяет доступность страниц для различных пользователей"""
    response = locals()[client_type].get(url)
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "url",
    [
        pytest.lazy_fixture('delete_page_url'),
        pytest.lazy_fixture('edit_page_url')
    ]
)
def test_redirect_for_anonymous_user(client, url):
    """Тест проверяет перенаправление анонимного пользователя."""
    response = client.get(url)
    assertRedirects(response, reverse("users:login") + "?next=" + url)
