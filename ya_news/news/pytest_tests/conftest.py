from django.utils import timezone
from datetime import timedelta
import pytest
from django.test.client import Client
from django.urls import reverse

from news.models import News, Comment


COUNT_COMMENTS_FOR_TESTING = 5


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
    def _create_news_objects(count):
        for i in range(count):
            News.objects.create(
                title=f'title {i}',
                text=f'text {i}',
            )
    return _create_news_objects


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
    for index in range(COUNT_COMMENTS_FOR_TESTING):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Comment text{index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return news_url


@pytest.fixture
def form_data():
    return {'text': 'Текст комментария'}


@pytest.fixture
def form_data_with_bad_wards():
    return {'text': 'редиска'}
