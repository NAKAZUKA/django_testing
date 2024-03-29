from django.utils import timezone
from datetime import timedelta
import pytest
from django.test.client import Client
from django.urls import reverse

from news.models import News, Comment


FORM_DATA = {'text': 'Текст комментария'}
COUNT_OBJECTS_FOR_TESTING = 10
ROUTES_FOR_HOME_PAGE = 'news:home'
ROUTES_FOR_DETAIL_PAGE = 'news:detail'
ROUTES_FOR_DELETE_PAGE = 'news:delete'
ROUTES_FOR_EDIT_PAGE = 'news:edit'
ROUTES_FOR_USER_LOGIN_PAGE = 'users:login'
ROUTES_FOR_USER_LOGOUT_PAGE = 'users:logout'
ROUTES_FOR_USER_SIGNUP_PAGE = 'users:signup'


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
    for i in range(COUNT_OBJECTS_FOR_TESTING):
        News.objects.create(
            title=f'title {i}',
            text=f'text {i}',
        )
    return None


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
    for index in range(COUNT_OBJECTS_FOR_TESTING):
        comment = Comment.objects.create(
            news=news, author=author, text=f'Comment text{index}',
        )
        comment.created = now + timedelta(days=index)
        comment.save()
    return news_url
