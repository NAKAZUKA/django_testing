from http import HTTPStatus

from pytils.translit import slugify

from notes.models import Note
from .conftest import NotesTestCase
from notes.forms import WARNING


class LogicTestCase(NotesTestCase):
    """Тесты логики приложения notes"""

    def test_auth_user_can_create_note(self):
        """Тест залогиненный пользователь может создать заметку"""
        Note.objects.all().delete()
        response = self.author_client.post(
            self.ADD_URL,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.title, self.form_data['title'])
        self.assertEqual(note.text, self.form_data['text'])
        self.assertEqual(note.slug, self.form_data['slug'])
        self.assertEqual(note.author, self.author)

    def test_not_auth_user_cannot_create_note(self):
        """Тест незалогиненный пользователь не может создать заметку"""
        existing_notes_before = set(Note.objects.all())
        response = self.client.post(
            self.ADD_URL,
            data=self.form_data
        )
        existing_notes_after = set(Note.objects.all())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(existing_notes_after, existing_notes_before)
        self.assertEqual(len(existing_notes_after - existing_notes_before), 0)

    def test_cannot_create_note_with_same_url(self):
        """
        Тест нельзя добавить запись с одинаковым url в базу данных
        сравнивает состав заметки созданой пользователем и существующей в базе
        проверяет наличие предупреждения в context переданной в шаблон
        """
        self.form_data['slug'] = self.SLUG
        existing_notes_before = set(Note.objects.all())
        response = self.author_client.post(
            self.ADD_URL,
            data=self.form_data
        )
        self.assertFormError(
            response,
            'form',
            'slug',
            errors=(self.note.slug + WARNING)
        )
        existing_notes_after = set(Note.objects.all())
        self.assertEqual(existing_notes_before, existing_notes_after)

    def test_autofill_url_in_form(self):
        """
        Тест проверяет, что запись создается с автозаполненным slug
        и проверяет правильность остальных полей формы
        """
        Note.objects.all().delete()
        self.form_data.pop('slug')
        response = self.user_client.post(
            self.ADD_URL, data=self.form_data
        )
        self.assertRedirects(response, self.SUCCES_URL)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.author, self.user)

    def test_author_can_edit_note(self):
        """Автор может редактировать свою заметку"""
        note_before_edit = self.note
        response = self.author_client.post(
            self.EDIT_URL,
            data=self.new_form_data
        )
        self.assertRedirects(response, self.SUCCES_URL)
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, self.new_form_data['title'])
        self.assertEqual(note.text, self.new_form_data['text'])
        self.assertEqual(note.slug, self.new_form_data['slug'])
        self.assertEqual(note.author, note_before_edit.author)

    def test_author_can_delete_note(self):
        """Автор может удалить свою заметку"""
        response = self.author_client.delete(self.DELETE_URL)
        self.assertRedirects(response, self.SUCCES_URL)
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk=self.note.pk)

    def test_user_cannot_edit_note(self):
        """
        Тест проверяет недоступность редактирования
        заметок других пользователей
        """
        note_befor_edit = self.note
        response = self.user_client.post(
            self.EDIT_URL,
            data=self.new_form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_after_edit = Note.objects.get(id=self.note.id)
        self.assertEqual(note_befor_edit.title, note_after_edit.title)
        self.assertEqual(note_befor_edit.text, note_after_edit.text)
        self.assertEqual(note_befor_edit.author, note_after_edit.author)
        self.assertEqual(note_befor_edit.slug, note_after_edit.slug)

    def test_user_cannot_delete_note(self):
        """
        Тест проверяет недоступность
        удаления заметок других пользователей
        """
        notes_before_delete = set(Note.objects.values_list('id', flat=True))
        response = self.user_client.delete(self.DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        notes_after_delete = set(Note.objects.values_list('id', flat=True))
        self.assertEqual(notes_after_delete, notes_before_delete)
