from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class NotesTestCase(TestCase):

    SLUG = 'testtitle'
    HOME_URL = reverse('notes:home')
    LIST_URL = reverse('notes:list')
    ADD_URL = reverse('notes:add')
    SUCCES_URL = reverse('notes:success')
    EDIT_URL = reverse('notes:edit', args=(SLUG,))
    USER_LOGIN_URL = reverse('users:login')
    USER_SIGNUP_URL = reverse('users:signup')
    USER_LOGOUT_URL = reverse('users:logout')
    DETAIL_URL = reverse('notes:detail', args=(SLUG,))
    DELETE_URL = reverse('notes:delete', args=(SLUG,))

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
            slug=cls.SLUG
        )
        cls.form_data = {
            'title': 'testformTitle',
            'text': 'testformText',
            'slug': 'testformtitle',
        }
        cls.new_form_data = {
            'title': 'newtestTitle',
            'text': 'newtestText',
            'slug': 'newtestSlug',
        }
