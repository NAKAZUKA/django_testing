from django.urls import reverse

from .conftest import NotesTestCase


class ContentTestCase(NotesTestCase):
    """Тесты содержания заметок"""

    def test_note_and_user_lists_in_context(self):
        """
        Отдельная заметка передаётся на страницу со
        списком заметок в списке object_list в словаре context, и
        заметка автора не отображается в списке заметок пользователя
        """
        clients = (
            (self.user_client, self.note, False),
            (self.author_client, self.note, True),
        )
        for client, note, expected_in_list in clients:
            with self.subTest(client=client, note=note):
                response = client.get(reverse('notes:list'))
                object_list = response.context['object_list']
                if expected_in_list:
                    assert note in object_list
                else:
                    assert note not in object_list

    def test_page_add_and_edit_includ_forms(self):
        """
        Страница создания и редактирования заметки
        включает в себя форму
        """
        urls = (
            ('notes:add', None),
            ('notes:edit', (self.note.slug,)),
        )
        for url, args in urls:
            with self.subTest(url=url):
                response = self.author_client.get(reverse(url, args=args))
                self.assertIn('form', response.context)
