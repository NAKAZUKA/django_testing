from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects

from .conftest import (ROUTES_FOR_HOME_PAGE,
                       ROUTES_FOR_USER_LOGIN_PAGE,
                       ROUTES_FOR_USER_LOGOUT_PAGE,
                       ROUTES_FOR_USER_SIGNUP_PAGE,
                       ROUTES_FOR_DELETE_PAGE,
                       ROUTES_FOR_EDIT_PAGE
                       )

pytestmark = pytest.mark.django_db


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
    url = reverse(name)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


def test_pages_detail(client, news, get_url_news_detail):
    """
    Тест проверяет доступность страницы
    с подробной информацией о новостях.
    """
    url = reverse('news:detail', args=get_url_news_detail(news))
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name',
    (ROUTES_FOR_DELETE_PAGE, ROUTES_FOR_EDIT_PAGE),
)
def test_pages_availability_for_author(author_client,
                                       name,
                                       comment,
                                       get_url_news_detail
                                       ):
    """
    Тест проверяет доступность страниц
    для аутентифицированных авторов.
    """
    url = reverse(name, args=get_url_news_detail(comment))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args',
    (
        (ROUTES_FOR_EDIT_PAGE, pytest.lazy_fixture('get_url_news_detail')),
        (ROUTES_FOR_DELETE_PAGE, pytest.lazy_fixture('get_url_news_detail')),
    ),
)
def test_redirects_for_client(client, name, args, comment):
    """
    Тест проверяет перенаправление для неавторизованных
    пользователей, пытающихся получить доступ к страницам
    редактирования или удаления комментариев.
    """
    url = reverse(name, args=args(comment))
    response = client.get(url)
    assertRedirects(
        response,
        reverse(ROUTES_FOR_USER_LOGIN_PAGE) + '?next=' + url
    )


@pytest.mark.parametrize(
    'name',
    (ROUTES_FOR_DELETE_PAGE, ROUTES_FOR_EDIT_PAGE),
)
def test_pages_availability_for_not_author_client(not_author_client,
                                                  name,
                                                  comment,
                                                  get_url_news_detail
                                                  ):
    """
    Тест проверяет не доступность страниц для
    авторизованных пользователей не имеющих авторство
    """
    url = reverse(name, args=get_url_news_detail(comment))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
