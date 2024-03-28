from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from notes.models import Note

User = get_user_model()


class NotesTestCase(TestCase):

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
        )

    @classmethod
    def reverse_method(cls, routs, args=None):
        return reverse(routs, args=args)
