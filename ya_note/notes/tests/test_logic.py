from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from .conftest import NotesTestCase


class LogicTestCase(NotesTestCase):
    """Тесты логики приложения notes"""

    def test_auth_user_can_create_note(self):
        """Тест залогиненный пользователь может создать заметку"""
        response = self.user_client.post(
            self.ROUTE_FOR_THE_ADD_NOTE_PAGE,
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(Note.objects.count(), 1)

    def test_not_auth_user_cannot_create_note(self):
        """Тест незалогиненный пользователь не может создать заметку"""
        response = self.client.post(
            self.ROUTE_FOR_THE_ADD_NOTE_PAGE,
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)

    def test_cannot_create_note_with_same_url(self):
        """
        Тест нельзя добавить запись с одинаковым url в базу данных
        сравнивает состав заметки созданой пользователем и существующей в базе
        проверяет наличие предупреждения в context переданной в шаблон
        """
        existing_notes_before = list(Note.objects.all())
        response = self.user_client.post(
            self.ROUTE_FOR_THE_ADD_NOTE_PAGE, data=self.DATA
        )
        existing_notes_after = list(Note.objects.all())
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertListEqual(existing_notes_after, existing_notes_before)

    def test_autofill_url_in_form(self):
        """
        Тест проверяет что запись создается с автозаполненным slug
        и проверяет правильность остальных полей формы
        """
        response = self.user_client.post(
            self.ROUTE_FOR_THE_ADD_NOTE_PAGE, data=self.DATA)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        created_note = Note.objects.get(title=self.DATA['title'])
        self.assertEqual(created_note.slug, slugify(created_note.title))
        self.assertEqual(created_note.text, self.DATA['text'])
        self.assertEqual(created_note.title, self.DATA['title'])

    def test_author_can_edit_and_delete_note(self):
        """
        Тест проверяет возможность редактирования
        и удаления автором своей заметки через POST запросы
        """
        new_data = {
            'text': 'Updated text',
        }
        edit_response = self.author_client.post(
            self.ROUTE_FOR_THE_EDIT_NOTE_PAGE,
            data=new_data,
            follow=True
        )
        self.assertEqual(edit_response.status_code, HTTPStatus.OK)
        delete_response = self.author_client.post(
            self.ROUTE_FOR_THE_DELETE_NOTE_PAGE,
            follow=True
        )
        self.assertEqual(delete_response.status_code, HTTPStatus.OK)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_edit_delete_note(self):
        """
        Тест проверяет недоступность редактирования
        и удаления заметок других пользователей
        """
        edit_response = self.user_client.post(
            self.ROUTE_FOR_THE_EDIT_NOTE_PAGE,
            data=self.DATA
        )
        self.assertEqual(edit_response.status_code, HTTPStatus.NOT_FOUND)
        delete_response = self.user_client.post(
            self.ROUTE_FOR_THE_DELETE_NOTE_PAGE
        )
        self.assertEqual(delete_response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
