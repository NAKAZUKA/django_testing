import pytest
from django.urls import reverse

from news.forms import CommentForm
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


pytestmark = pytest.mark.django_db
ROUTES_FOR_HOME_PAGE = reverse('news:home')


def test_main_home_news_count(client, create_news_objects):
    """Тест проверяет количество новостей на главной странице"""
    assert len(
        client.get(ROUTES_FOR_HOME_PAGE).context['object_list']
    ) == NEWS_COUNT_ON_HOME_PAGE


def test_order_news_on_home_page(client, create_news_objects):
    """Тест проверяет правильность сортировки новостей на главной странице"""
    all_dates = [
        news.date for news in client.get(
            ROUTES_FOR_HOME_PAGE
        ).context['object_list']
    ]
    assert all_dates == sorted(all_dates, reverse=True)


def test_comment_form_availability(client, detail_page_url):
    """
    Тест проверяет недоступность формы для отправки
    комментария на странице новости анонимному пользователю
    """
    response = client.get(detail_page_url)
    assert 'form' not in response.context


def test_comment_form_availability_for_auth_user(not_author_client,
                                                 detail_page_url
                                                 ):
    """
    Тест проверяет доступность формы для отправки
    комментария на странице новости авторизованным пользователем
    и её тип.
    """
    response = not_author_client.get(detail_page_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)


def test_comment_ordering(client, create_comment_objects, detail_page_url):
    """Тест проверяет правильность сортировки комментариев"""
    response = client.get(detail_page_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps
