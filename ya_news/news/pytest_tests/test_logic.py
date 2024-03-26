from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment


def test_client_cannot_create_comment(client,
                                      news,
                                      form_data,
                                      get_url_news_detail
                                      ):
    """Тест: клиент не может комментировать новость."""
    url = reverse('news:detail', args=get_url_news_detail(news))
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    assert Comment.objects.count() == 0


def test_authorization_user_can_add_comment(not_author_client, news, form_data, get_url_news_detail):
    """Тест: авторизованный пользователь может комментировать новость."""
    url = reverse('news:detail', args=get_url_news_detail(news))
    response = not_author_client.post(url, data=form_data)
    assert Comment.objects.count() == 1


def test_bad_wards_in_comment(not_author_client,
                              news,
                              form_data,
                              get_url_news_detail
                              ):
    """Тест: нельзя комментировать новость с запрещёнными словами."""
    form_data['text'] = BAD_WORDS
    url = reverse('news:detail', args=get_url_news_detail(news))
    response = not_author_client.post(url, data=form_data)
    assertFormError(response, form='form', field='text', errors=WARNING)


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('get_url_news_detail')),
        ('news:delete', pytest.lazy_fixture('get_url_news_detail')),
    )
)
def test_author_client_can_edit_and_delete_comment(author_client,
                                                   name,
                                                   args,
                                                   comment,
                                                   get_url_news_detail
                                                   ):
    """
    Тест: авторизованный пользователь
    может редактировать и удалять комментарии.
    """
    url = reverse(name, args=args(comment))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'name, args',
    (
        ('news:edit', pytest.lazy_fixture('get_url_news_detail')),
        ('news:delete', pytest.lazy_fixture('get_url_news_detail')),
    )
)
def test_not_author_client_cannot_edit_and_delete_comment(not_author_client,
                                                          name,
                                                          args,
                                                          comment,
                                                          get_url_news_detail
                                                          ):
    """
    Тест: не авторизованный пользователь
    не может редактировать и удалять комментарии.
    """
    url = reverse(name, args=args(comment))
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
