from notes.forms import NoteForm
from .conftest import NotesTestCase


class ContentTestCase(NotesTestCase):
    """Тесты содержания заметок"""

    def test_note_in_context_of_notes_list(self):
        """
        отдельная заметка передается на страницу сосписком
        заметок и присутствует в списке object_list в контексте
        """
        response = self.author_client.get(
            self.LIST_URL
        )
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        for note in notes:
            self.assertEqual(note.title, self.note.title)
            self.assertEqual(note.text, self.note.text)
            self.assertEqual(note.slug, self.note.slug)
            self.assertEqual(note.author, self.author)

    def test_authors_note_not_included_in_users_note_list(self):
        """Запись автора не отображается в списке заметок пользователя"""
        response = self.user_client.get(
            self.LIST_URL
        )
        notes = response.context['object_list']
        self.assertNotIn(self.note, notes)

    def test_page_add_and_edit_includ_forms(self):
        """
        Страница создания и редактирования заметки
        включает в себя форму правильного типа
        """
        urls = (
            (self.ADD_URL),
            (self.EDIT_URL),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
