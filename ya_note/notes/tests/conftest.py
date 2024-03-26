from django.contrib.auth import get_user_model
from django.test import Client, TestCase

from notes.models import Note

User = get_user_model()


class NotesTestCase(TestCase):

    TITLE = 'testTitle'
    TEXT = 'testText'
    TEST_USER_NAME = 'testUser'
    TEST_AUTHOR_NAME = 'testAuthor'

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username=cls.TEST_USER_NAME)
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.author = User.objects.create(username=cls.TEST_AUTHOR_NAME)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title=cls.TITLE,
            text=cls.TEXT,
            author=cls.author,
        )
