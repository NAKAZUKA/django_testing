from http import HTTPStatus

import pytest
from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Текст комментария'}
NEW_TEXT_DATA = {'text': 'Новый текст комментария'}
comment_form_data = {
    'text': 'Новый текст комментария'
}


def test_client_cannot_create_comment(client,
                                      detail_page_url
                                      ):
    """Тест: клиент не может комментировать новость."""
    response = client.post(detail_page_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_client_user_can_add_comment(author_client,
                                     author,
                                     detail_page_url,
                                     news
                                     ):
    """Тест: авторизованный пользователь может комментировать новость."""
    response = author_client.post(detail_page_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 1
    comment = Comment.objects.get()
    assert comment.text == FORM_DATA['text']
    assert comment.news == news
    assert comment.author == author


@pytest.mark.parametrize(
    "word",
    BAD_WORDS
)
def test_bad_words_in_comment(not_author_client, detail_page_url, word):
    """Тест: нельзя комментировать новость с запрещёнными словами."""
    response = not_author_client.post(detail_page_url, data={'text': word})
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_client_can_edit_comment(author_client,
                                        edit_page_url,
                                        comment,
                                        ):
    """
    Тест: авторизованный пользователь
    может редактировать комментарии.
    """
    response = author_client.post(edit_page_url,
                                  data=NEW_TEXT_DATA
                                  )
    new_comment = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.FOUND
    assert new_comment.text == comment_form_data['text']
    assert new_comment.author == comment.author
    assert new_comment.news == comment.news


def test_author_client_can_delete_comment(author_client,
                                          delete_page_url,
                                          ):
    """
    Тест: авторизованный пользователь
    может удалять комментарии.
    """
    response = author_client.post(delete_page_url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_not_author_client_cannot_delete_comment(not_author_client,
                                                 delete_page_url,
                                                 comment,
                                                 ):
    """
    Тест: неавторизованный пользователь
    не может удалять комментарии.
    """
    response = not_author_client.post(delete_page_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    comment_after_delete = Comment.objects.get(id=comment.id)
    assert Comment.objects.count() == 1
    assert comment_after_delete.news == comment.news
    assert comment_after_delete.text == comment.text
    assert comment_after_delete.author == comment.author


def test_user_cant_edit_comment_another_user(not_author_client,
                                             edit_page_url,
                                             comment,
                                             ):
    """Пользователи не могут редактировать не свои комментарии"""
    response = not_author_client.post(
        edit_page_url,
        data=comment_form_data
    )
    new_comment = Comment.objects.get(id=comment.id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert new_comment.author == comment.author
    assert new_comment.news == comment.news
    assert new_comment.text == comment.text
