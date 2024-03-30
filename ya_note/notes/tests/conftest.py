from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from pytils.translit import slugify

from notes.models import Note

User = get_user_model()


class NotesTestCase(TestCase):

    NOTE_SLUG = slugify('testTitle')
    ROUTE_FOR_THE_HOME_PAGE = reverse('notes:home')
    ROUTE_FOR_THE_LIST_PAGE = reverse('notes:list')
    ROUTE_FOR_THE_ADD_NOTE_PAGE = reverse('notes:add')
    ROUTE_FOR_THE_SUCCESS_PAGE = reverse('notes:success')
    ROUTE_FOR_THE_EDIT_NOTE_PAGE = reverse('notes:edit', args=(NOTE_SLUG,))
    ROUTE_FOR_THE_USER_LOGIN_PAGE = reverse('users:login')
    ROUTE_FOR_THE_USER_SIGNUP_PAGE = reverse('users:signup')
    ROUTE_FOR_THE_USER_LOGOUT_PAGE = reverse('users:logout')
    ROUTE_FOR_THE_DETAIL_NOTE_PAGE = reverse('notes:detail', args=(NOTE_SLUG,))
    ROUTE_FOR_THE_DELETE_NOTE_PAGE = reverse('notes:delete', args=(NOTE_SLUG,))

    DATA = {
        'title': 'testTitle',
        'text': 'testText',
        'slug': NOTE_SLUG
    }

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='testUser')
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.author = User.objects.create(username='testAuthor')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title='testTitle',
            text='testText',
            author=cls.author,
            slug=cls.NOTE_SLUG
        )
