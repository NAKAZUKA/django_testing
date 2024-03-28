from notes.forms import NoteForm

from .conftest import NotesTestCase
from .set_of_routes import (ROUTE_FOR_THE_ADD_NOTE_PAGE,
                            ROUTE_FOR_THE_EDIT_NOTE_PAGE,
                            ROUTE_FOR_THE_LIST_PAGE)


class ContentTestCase(NotesTestCase):
    """Тесты содержания заметок"""

    def test_note_in_context_of_notes_list(self):
        """
        отдельная заметка передается на страницу сосписком
        заметок и присутствует в списке object_list в контексте
        """
        response = self.author_client.get(
            self.reverse_method(ROUTE_FOR_THE_LIST_PAGE)
        )
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    def test_authors_note_not_included_in_users_note_list(self):
        """Запись автора не отображается в списке заметок пользователя"""
        response = self.user_client.get(
            self.reverse_method(ROUTE_FOR_THE_LIST_PAGE)
        )
        object_list = response.context['object_list']
        self.assertNotIn(self.note, object_list)

    def test_page_add_and_edit_includ_forms(self):
        """
        Страница создания и редактирования заметки
        включает в себя форму правильного типа
        """
        urls = (
            (ROUTE_FOR_THE_ADD_NOTE_PAGE, None),
            (ROUTE_FOR_THE_EDIT_NOTE_PAGE, (self.note.slug,)),
        )
        for url, args in urls:
            with self.subTest(url=url):
                response = self.author_client.get(
                    self.reverse_method(url, args)
                )
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
