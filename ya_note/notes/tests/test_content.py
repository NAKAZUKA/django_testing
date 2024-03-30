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
            self.ROUTE_FOR_THE_LIST_PAGE
        )
        notes_list = response.context['object_list']
        self.assertIn(self.note, notes_list)
        for note in notes_list:
            if note == self.note:
                self.assertEqual(note.title, self.note.title)
                self.assertEqual(note.text, self.note.text)

    def test_authors_note_not_included_in_users_note_list(self):
        """Запись автора не отображается в списке заметок пользователя"""
        response = self.user_client.get(
            self.ROUTE_FOR_THE_LIST_PAGE
        )
        notes_list = response.context['object_list']
        self.assertNotIn(self.note, notes_list)

    def test_page_add_and_edit_includ_forms(self):
        """
        Страница создания и редактирования заметки
        включает в себя форму правильного типа
        """
        urls = (
            (self.ROUTE_FOR_THE_ADD_NOTE_PAGE),
            (self.ROUTE_FOR_THE_EDIT_NOTE_PAGE),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
