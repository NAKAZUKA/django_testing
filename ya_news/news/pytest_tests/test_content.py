import pytest
from django.urls import reverse


pytestmark = pytest.mark.django_db
ROUTES_FOR_HOME_PAGE = reverse('news:home')


def test_main_home_news_count(client, create_news_objects):
    """Тест проверяет количество новостей на главной странице"""
    assert len(
        client.get(ROUTES_FOR_HOME_PAGE).context['object_list']
    ) == 10


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


def test_comment_ordering(client, create_comment_objects, detail_page_url):
    """Тест проверяет правильность сортировки комментариев"""
    response = client.get(detail_page_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps
