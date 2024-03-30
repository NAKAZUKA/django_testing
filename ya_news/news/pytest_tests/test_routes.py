from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from .conftest import (ROUTES_FOR_DELETE_PAGE,
                       ROUTES_FOR_EDIT_PAGE)


pytestmark = pytest.mark.django_db
ROUTES_FOR_HOME_PAGE = reverse('news:home')
ROUTES_FOR_USER_LOGIN_PAGE = reverse('users:login')
ROUTES_FOR_USER_LOGOUT_PAGE = reverse('users:logout')
ROUTES_FOR_USER_SIGNUP_PAGE = reverse('users:signup')


@pytest.mark.parametrize(
    'name',
    (ROUTES_FOR_HOME_PAGE,
     ROUTES_FOR_USER_LOGIN_PAGE,
     ROUTES_FOR_USER_LOGOUT_PAGE,
     ROUTES_FOR_USER_SIGNUP_PAGE)
)
def test_pages_availability_for_anonymous_user(client, name):
    """
    Тест проверяет доступность определенных
    страниц для анонимных пользователей
    """
    url = name
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_pages_detail(client, detail_page_url):
    """
    Тест проверяет доступность страницы
    с подробной информацией о новостях.
    """
    url = detail_page_url
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    (ROUTES_FOR_DELETE_PAGE, ROUTES_FOR_EDIT_PAGE),
)
def test_pages_availability_for_author(author_client,
                                       name,
                                       delete_page_url,
                                       edit_page_url
                                       ):
    """
    Тест проверяет доступность страниц
    для аутентифицированных авторов.
    """
    url = delete_page_url if name == ROUTES_FOR_DELETE_PAGE else edit_page_url
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    (ROUTES_FOR_DELETE_PAGE, ROUTES_FOR_EDIT_PAGE),
)
def test_redirects_for_client(client, name, delete_page_url, edit_page_url):
    """
    Тест проверяет перенаправление для неавторизованных
    пользователей, пытающихся получить доступ к страницам
    редактирования или удаления комментариев.
    """
    url = delete_page_url if name == ROUTES_FOR_DELETE_PAGE else edit_page_url
    response = client.get(url)
    assertRedirects(
        response,
        ROUTES_FOR_USER_LOGIN_PAGE + '?next=' + url
    )


@pytest.mark.parametrize(
    'name',
    (ROUTES_FOR_DELETE_PAGE, ROUTES_FOR_EDIT_PAGE),
)
def test_pages_availability_for_not_author_client(not_author_client,
                                                  name,
                                                  delete_page_url,
                                                  edit_page_url
                                                  ):
    """
    Тест проверяет не доступность страниц для
    авторизованных пользователей не имеющих авторство
    """
    url = delete_page_url if name == ROUTES_FOR_DELETE_PAGE else edit_page_url
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
