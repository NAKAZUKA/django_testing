from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from .conftest import NotesTestCase


class LogicTestCase(NotesTestCase):
    """Тесты логики приложения notes"""

    def test_auth_user_can_create_note(self):
        """Тест залогиненный пользователь может создать заметку"""
        response = self.author_client.post(
            self.ADD_URL,
            data=self.DATA
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 2)

    def test_not_auth_user_cannot_create_note(self):
        """Тест незалогиненный пользователь не может создать заметку"""
        existing_notes_before = set(Note.objects.all())
        response = self.client.post(
            self.ADD_URL,
            data=self.DATA
        )
        existing_notes_after = set(Note.objects.all())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertSetEqual(existing_notes_after, existing_notes_before)

    def test_cannot_create_note_with_same_url(self):
        """
        Тест нельзя добавить запись с одинаковым url в базу данных
        сравнивает состав заметки созданой пользователем и существующей в базе
        проверяет наличие предупреждения в context переданной в шаблон
        """
        existing_note_before = Note.objects.first()
        response = self.author_client.post(
            self.ADD_URL, data=self.DATA
        )
        existing_note_after = Note.objects.first()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(existing_note_after, existing_note_before)

    def test_autofill_url_in_form(self):
        """
        Тест проверяет, что запись создается с автозаполненным slug
        и проверяет правильность остальных полей формы
        """
        response = self.user_client.post(
            self.ADD_URL, data=self.DATA
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        created_note = Note.objects.latest('id')
        self.assertEqual(created_note.slug, slugify(self.DATA['title']))
        self.assertEqual(created_note.text, self.DATA['text'])
        self.assertEqual(created_note.title, self.DATA['title'])
        self.assertEqual(created_note.author, self.user)

    def test_author_can_edit_and_delete_note(self):
        """
        Тест проверяет возможность редактирования
        и удаления автором своей заметки через POST запросы
        """
        new_data = {
            'title': 'Updated title',
            'text': 'Updated text',
            'slug': self.note.slug,
        }
        edit_response = self.author_client.post(
            self.EDIT_URL,
            data=new_data,
            follow=True
        )
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(edit_response.status_code, HTTPStatus.OK)
        self.assertEqual(updated_note.title, new_data['title'])
        self.assertEqual(updated_note.text, new_data['text'])
        self.assertEqual(updated_note.slug, new_data['slug'])
        delete_response = self.author_client.post(
            self.DELETE_URL,
            follow=True
        )
        self.assertEqual(delete_response.status_code, HTTPStatus.OK)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_cannot_edit_note(self):
        """
        Тест проверяет недоступность редактирования
        заметок других пользователей
        """
        original_note = Note.objects.get(id=self.note.id)
        response = self.user_client.post(
            self.EDIT_URL,
            data=self.DATA
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        updated_note = Note.objects.get(id=self.note.id)
        self.assertEqual(original_note.title, updated_note.title)
        self.assertEqual(original_note.text, updated_note.text)

    def test_user_cannot_delete_note(self):
        """
        Тест проверяет недоступность
        удаления заметок других пользователей
        """
        notes_before = list(Note.objects.all())
        response = self.user_client.post(
            self.DELETE_URL
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after = list(Note.objects.all())
        self.assertListEqual(notes_after, notes_before)
