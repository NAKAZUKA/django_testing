import pytest
from django.urls import reverse

from .conftest import (COUNT_OBJECTS_FOR_TESTING,
                       ROUTES_FOR_DETAIL_PAGE,
                       ROUTES_FOR_HOME_PAGE
                       )

pytestmark = pytest.mark.django_db


def test_main_home_news_count(client, create_news_objects):
    """Тест проверяет количество новостей на главной странице"""
    url = reverse(ROUTES_FOR_HOME_PAGE)
    response = client.get(url)
    assert len(
        response.context['object_list']
    ) == COUNT_OBJECTS_FOR_TESTING


def test_order_news_on_home_page(client, create_news_objects):
    """Тест проверяет правильность сортировки новостей на главной странице"""
    url = reverse(ROUTES_FOR_HOME_PAGE)
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


def test_comment_form_availability(client, news, get_url_news_detail):
    """
    Тест проверяет доступность формы для отправки
    комментария на странице новости анонимному пользователю
    """
    url = reverse(ROUTES_FOR_DETAIL_PAGE, args=get_url_news_detail(news))
    response = client.get(url)
    assert 'comment_form' not in response.context


def test_comment_ordering(client, create_comment_objects):
    """Тест проверяет правильность сортировки комментариев"""
    response = client.get(create_comment_objects)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps
