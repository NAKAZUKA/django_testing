from http import HTTPStatus

from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Текст комментария'}
NEW_TEXT_DATA = {'text': 'Новый текст комментария'}


def test_client_cannot_create_comment(client,
                                      detail_page_url
                                      ):
    """Тест: клиент не может комментировать новость."""
    response = client.post(detail_page_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_client_user_can_add_comment(not_author_client,
                                     detail_page_url,
                                     news,
                                     not_author
                                     ):
    """Тест: авторизованный пользователь может комментировать новость."""
    response = not_author_client.post(detail_page_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 1
    new_comment = Comment.objects.first()
    assert new_comment.text == FORM_DATA['text']
    assert new_comment.news_id == news.pk
    assert new_comment.author_id == not_author.id


def test_bad_words_in_comment(not_author_client, detail_page_url):
    """Тест: нельзя комментировать новость с запрещёнными словами."""
    for word in BAD_WORDS:
        FORM_DATA['text'] = word
        response = not_author_client.post(detail_page_url, data=FORM_DATA)
        assertFormError(response, form='form', field='text', errors=WARNING)
        assert Comment.objects.count() == 0


def test_author_client_can_edit_comment(author_client,
                                        edit_page_url,
                                        author,
                                        news
                                        ):
    """
    Тест: авторизованный пользователь
    может редактировать комментарии.
    """
    text_comment_before = Comment.objects.first()
    response = author_client.post(edit_page_url,
                                  data=NEW_TEXT_DATA
                                  )
    assert response.status_code == HTTPStatus.FOUND
    assert text_comment_before.text != NEW_TEXT_DATA['text']
    assert text_comment_before.author_id == author.id
    assert text_comment_before.news_id == news.id


def test_author_client_can_delete_comment(author_client,
                                          delete_page_url
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
                                                 news,
                                                 not_author
                                                 ):
    """
    Тест: неавторизованный пользователь
    не может удалять комментарии.
    """
    response = not_author_client.post(delete_page_url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Comment.objects.count() == 1
    assert comment.news_id == news.pk
    assert comment.author_id != not_author.id


def test_not_author_client_cannot_edit_comment(not_author_client,
                                               edit_page_url,
                                               comment
                                               ):
    """
    Тест: не авторизованный пользователь
    не может редактировать комментарии.
    """
    assert Comment.objects.count() == 1
    comment_before = comment
    response = not_author_client.post(edit_page_url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment_before.text == comment.text
    assert comment_before.author_id == comment.author_id
    assert comment_before.news_id == comment.news_id
