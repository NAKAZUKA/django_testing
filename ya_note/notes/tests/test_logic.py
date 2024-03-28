from http import HTTPStatus

from notes.forms import WARNING
from notes.models import Note
from pytils.translit import slugify

from .conftest import NotesTestCase
from .set_of_routes import (ROUTE_FOR_THE_ADD_NOTE_PAGE,
                            ROUTE_FOR_THE_EDIT_NOTE_PAGE)


class LogicTestCase(NotesTestCase):
    """Тесты логики приложения notes"""

    data = {
        'title': 'testTitle',
        'text': 'testText',
    }

    def test_auth_user_can_create_note(self):
        """Тест залогиненный пользователь может создать заметку"""
        response = self.user_client.post(
            self.reverse_method(ROUTE_FOR_THE_ADD_NOTE_PAGE),
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_not_auth_user_cannot_create_note(self):
        """Тест не залогиненный пользователь не может создать заметку"""
        response = self.client.post(
            self.reverse_method(ROUTE_FOR_THE_ADD_NOTE_PAGE),
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_cannot_create_note_with_same_url(self):
        """Тест нельзя добавить запись с одинаковым url в базу данных"""
        initial_count = Note.objects.count()
        response = self.user_client.post(
            self.reverse_method(ROUTE_FOR_THE_ADD_NOTE_PAGE), data=self.data)
        self.assertEqual(initial_count, Note.objects.count())
        self.assertContains(response, WARNING)

    def test_autofill_url_in_form(self):
        """Тест проверяет что запись создается с автозаполненным slug"""
        response = self.user_client.post(
            self.reverse_method(ROUTE_FOR_THE_ADD_NOTE_PAGE), data=self.data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(
            Note.objects.first().slug, slugify(self.data['title'])
        )

    def test_author_can_edit_delete_note(self):
        """
        Тест проверяет возможность редактирования
        и удаления автору своих заметок через POST запрос
        """
        response = self.author_client.post(
            self.reverse_method(ROUTE_FOR_THE_EDIT_NOTE_PAGE,
                                (self.note.slug,)
                                ),
            data=self.data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)

    def test_user_cannot_edit_delete_note(self):
        """
        Тест проверяет недоступность редактирования
        и удаления заметок других пользователей
        """
        response = self.user_client.post(
            self.reverse_method(ROUTE_FOR_THE_EDIT_NOTE_PAGE,
                                (self.note.slug,)
                                ),
            data=self.data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
