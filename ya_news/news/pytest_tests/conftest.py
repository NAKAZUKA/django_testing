from datetime import timedelta

import pytest
from django.test.client import Client
from django.urls import reverse
from django.utils import timezone

from news.models import Comment, News
from yanews.settings import NEWS_COUNT_ON_HOME_PAGE


@pytest.fixture
def detail_page_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture
def delete_page_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def edit_page_url(comment):
    return reverse('news:edit', args=(comment.pk,))


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
        for i in range(NEWS_COUNT_ON_HOME_PAGE)
    ]
    News.objects.bulk_create(news_objects)


@pytest.fixture
def comment(author, news):
    return Comment.objects.create(
        news=news,
        author=author,
        text='Текст комментария',
    )


@pytest.fixture
def create_comment_objects(author, news):
    now = timezone.now()
    for index in range(10):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Comment text{index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
def comment_form_data(news):
    return {
        'news': news,
        'text': 'Новый текст комментария'
    }
