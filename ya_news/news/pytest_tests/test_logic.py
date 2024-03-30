from http import HTTPStatus

from pytest_django.asserts import assertFormError

from news.forms import BAD_WORDS, WARNING
from news.models import Comment

FORM_DATA = {'text': 'Текст комментария'}


def test_client_cannot_create_comment(client,
                                      detail_page_url
                                      ):
    """Тест: клиент не может комментировать новость."""
    url = detail_page_url
    response = client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_client_user_can_add_comment(not_author_client,
                                     detail_page_url
                                     ):
    """Тест: авторизованный пользователь может комментировать новость."""
    url = detail_page_url
    response = not_author_client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 1
    assert Comment.objects.first().text == FORM_DATA['text']
    assert Comment.objects.first().news_id is not None
    assert Comment.objects.first().author_id is not None


def test_bad_wards_in_comment(not_author_client, detail_page_url):
    """Тест: нельзя комментировать новость с запрещёнными словами."""
    FORM_DATA['text'] = ' '.join(BAD_WORDS)
    print(FORM_DATA)
    url = detail_page_url
    response = not_author_client.post(url, data=FORM_DATA)
    assertFormError(response, form='form', field='text', errors=WARNING)
    assert Comment.objects.count() == 0


def test_author_client_can_edit_comment(author_client,
                                        edit_page_url
                                        ):
    """
    Тест: авторизованный пользователь
    может редактировать комментарии.
    """
    text_comment_before = Comment.objects.first().text
    url = edit_page_url
    response = author_client.post(url,
                                  data={'text': 'Новый текст комментария'}
                                  )
    assert response.status_code == HTTPStatus.FOUND
    assert text_comment_before != 'Новый текст комментария'


def test_author_client_can_delete_comment(author_client,
                                          delete_page_url
                                          ):
    """
    Тест: авторизованный пользователь
    может удалять комментарии.
    """
    url = delete_page_url
    response = author_client.post(url)
    assert response.status_code == HTTPStatus.FOUND
    assert Comment.objects.count() == 0


def test_not_author_client_cannot_delete_comment(not_author_client,
                                                 delete_page_url
                                                 ):
    """
    Тест: неавторизованный пользователь
    не может удалять комментарии.
    """
    before_delete = Comment.objects.all()
    url = delete_page_url
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    after_delete = Comment.objects.all()
    assert before_delete[0].text == after_delete[0].text


def test_not_author_client_cannot_edit_comment(not_author_client,
                                               edit_page_url
                                               ):
    """
    Тест: не авторизованный пользователь
    не может редактировать комментарии.
    """
    assert Comment.objects.count() == 1
    comment_before = Comment.objects.first()
    url = edit_page_url
    response = not_author_client.post(url, data=FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment_before.text != FORM_DATA['text']
