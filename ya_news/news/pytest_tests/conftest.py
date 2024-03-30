from datetime import timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News


COUNT_NEWS_COMMENTS_FOR_TESTING = 10
ROUTES_FOR_DETAIL_PAGE = 'news:detail'
ROUTES_FOR_DELETE_PAGE = 'news:delete'
ROUTES_FOR_EDIT_PAGE = 'news:edit'


@pytest.fixture
def detail_page_url(news):
    return reverse(ROUTES_FOR_DETAIL_PAGE, args=(news.pk,))


@pytest.fixture
def delete_page_url(comment):
    return reverse(ROUTES_FOR_DELETE_PAGE, args=(comment.pk,))


@pytest.fixture
def edit_page_url(comment):
    return reverse(ROUTES_FOR_EDIT_PAGE, args=(comment.pk,))


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create_user(
        username='author',
    )


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create_user(
        username='not_author',
    )


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def news(author):
    return News.objects.create(
        title='Заголовок',
        text='Текст',
    )


@pytest.fixture
def create_news_objects():
    news_objects = [
        News(title=f'title {i}', text=f'text {i}')
        for i in range(COUNT_NEWS_COMMENTS_FOR_TESTING)
    ]
    News.objects.bulk_create(news_objects)


@pytest.fixture
def get_url_news_detail():
    def _get_url_news_detail(news):
        return (news.id,)
    return _get_url_news_detail


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def create_comment_objects(author, news):
    news_url = reverse('news:detail', kwargs={'pk': news.pk},)
    now = timezone.now()
    for index in range(COUNT_NEWS_COMMENTS_FOR_TESTING):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Comment text{index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return news_url
