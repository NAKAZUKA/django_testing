import pytest
from django.urls import reverse
# from news.models import Comment


COUNT_OBJECT_ON_DIFFERENT_PAGE = 10


@pytest.mark.django_db
def test_main_home_news_count(client, create_news_objects):
    """Тест проверяет количество новостей на главной странице"""
    create_news_objects(COUNT_OBJECT_ON_DIFFERENT_PAGE)
    url = reverse('news:home')
    response = client.get(url)
    assert len(
        response.context['object_list']
    ) == COUNT_OBJECT_ON_DIFFERENT_PAGE


@pytest.mark.django_db
def test_order_news_on_home_page(client, create_news_objects):
    """Тест проверяет правильность сортировки новостей на главной странице"""
    create_news_objects(COUNT_OBJECT_ON_DIFFERENT_PAGE)
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    all_dates = [news.date for news in object_list]
    sorted_dates = sorted(all_dates, reverse=True)
    assert all_dates == sorted_dates


@pytest.mark.django_db
def test_comment_form_availability(client, news, get_url_news_detail):
    """
    Тест проверяет доступность формы для отправки
    комментария на странице новости анонимному пользователю
    """
    url = reverse('news:detail', args=get_url_news_detail(news))
    response = client.get(url)
    assert 'comment_form' not in response.context


@pytest.mark.django_db
def test_comment_ordering(client, create_comment_objects):
    response = client.get(create_comment_objects)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert all_timestamps == sorted_timestamps
