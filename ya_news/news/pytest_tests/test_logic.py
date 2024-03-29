from http import HTTPStatus

import pytest
from django.urls import reverse
from news.forms import BAD_WORDS, WARNING
from news.models import Comment
from pytest_django.asserts import assertFormError

from .conftest import (FORM_DATA,
                       ROUTES_FOR_DELETE_PAGE,
                       ROUTES_FOR_DETAIL_PAGE,
                       ROUTES_FOR_EDIT_PAGE
                       )


def test_client_cannot_create_comment(client,
                                      news,
                                      get_url_news_detail
                                      ):
    """Тест: клиент не может комментировать новость."""
    url = reverse(ROUTES_FOR_DETAIL_PAGE, args=get_url_news_detail(news))
    response = client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_client_user_can_add_comment(not_author_client,
                                     news,
                                     get_url_news_detail
                                     ):
    """Тест: авторизованный пользователь может комментировать новость."""
    url = reverse(ROUTES_FOR_DETAIL_PAGE, args=get_url_news_detail(news))
    response = not_author_client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 1
    assert Comment.objects.first().text == FORM_DATA['text']


def test_bad_wards_in_comment(not_author_client,
                              news,
                              get_url_news_detail
                              ):
    """Тест: нельзя комментировать новость с запрещёнными словами."""
    FORM_DATA['text'] = BAD_WORDS
    url = reverse(ROUTES_FOR_DETAIL_PAGE, args=get_url_news_detail(news))
    response = not_author_client.post(url, data=FORM_DATA)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'name, args',
    (
        (ROUTES_FOR_EDIT_PAGE, pytest.lazy_fixture('get_url_news_detail')),
    )
)
def test_author_client_can_edit_comment(author_client,
                                        name,
                                        args,
                                        comment,
                                        get_url_news_detail
                                        ):
    """
    Тест: авторизованный пользователь
    может редактировать комментарии.
    """
    url = reverse(name, args=args(comment))
    response = author_client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args',
    (
        (ROUTES_FOR_DELETE_PAGE, pytest.lazy_fixture('get_url_news_detail')),
    )
)
def test_author_client_can_delete_comment(author_client,
                                          name,
                                          args,
                                          comment,
                                          get_url_news_detail
                                          ):
    """
    Тест: авторизованный пользователь
    может удалять комментарии.
    """
    url = reverse(name, args=args(comment))
    response = author_client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


@pytest.mark.parametrize(
    'name, args',
    (
        (ROUTES_FOR_DELETE_PAGE, pytest.lazy_fixture('get_url_news_detail')),
    )
)
def test_not_author_client_cannot_delete_comment(not_author_client,
                                                 name,
                                                 args,
                                                 comment,
                                                 get_url_news_detail
                                                 ):
    """
    Тест: не авторизованный пользователь
    не может удалять комментарии.
    """
    url = reverse(name, args=args(comment))
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1


@pytest.mark.parametrize(
    'name, args',
    (
        (ROUTES_FOR_EDIT_PAGE, pytest.lazy_fixture('get_url_news_detail')),
    )
)
def test_not_author_client_cannot_edit_comment(not_author_client,
                                               name,
                                               args,
                                               comment,
                                               get_url_news_detail
                                               ):
    """
    Тест: не авторизованный пользователь
    не может редактировать комментарии.
    """
    url = reverse(name, args=args(comment))
    response = not_author_client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
