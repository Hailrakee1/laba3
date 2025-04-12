import unittest
from unittest.mock import patch, mock_open
import json
from main import Note, NoteApp

class NoteTests(unittest.TestCase):

    def test_note_creation(self):
        note = Note("Title", "Some content", tags=["tag1", "tag2"])
        self.assertEqual(note.title, "Title")
        self.assertEqual(note.content, "Some content")
        self.assertEqual(note.tags, ["tag1", "tag2"])
        self.assertTrue(len(note.id) == 8)

    def test_note_serialization(self):
        note = Note("Test", "Body", ["tag"])
        data = note.to_dict()
        restored_note = Note.from_dict(data)
        self.assertEqual(restored_note.title, "Test")
        self.assertEqual(restored_note.content, "Body")
        self.assertEqual(restored_note.tags, ["tag"])
        self.assertEqual(restored_note.id, note.id)


class NoteAppTests(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists", return_value=False)
    def test_load_notes_file_not_exist(self, mock_exists, mock_file):
        app = NoteApp()
        self.assertEqual(app.notes, [])

    @patch("builtins.open", new_callable=mock_open)
    def test_save_and_load_notes(self, mock_file):
        note = Note("Test", "Text", ["tag1"])
        app = NoteApp()
        app.notes = [note]

        # Сохраняем
        app.save_notes()

     # Собираем всё, что было записано в файл
        written_data = ''.join(call.args[0] for call in mock_file().write.call_args_list)

        expected_data = json.dumps([note.to_dict()], indent=4, ensure_ascii=False)
        self.assertEqual(written_data, expected_data)

    # Подменяем read
        mock_file().read.return_value = expected_data
        with patch("os.path.exists", return_value=True):
            app2 = NoteApp()
            self.assertEqual(len(app2.notes), 1)
            self.assertEqual(app2.notes[0].title, "Test")

    def test_find_note_by_id(self):
        note = Note("Test", "Some text", ["tag"])
        app = NoteApp()
        app.notes = [note]
        found = app.find_note_by_id(note.id)
        self.assertIsNotNone(found)
        self.assertEqual(found.title, "Test")

    def test_delete_note(self):
        note = Note("Test", "Delete me")
        app = NoteApp()
        app.notes = [note]
        app.notes.remove(note)
        self.assertNotIn(note, app.notes)

    def test_search_notes(self):
        n1 = Note("Shopping list", "Buy milk and eggs", ["groceries"])
        n2 = Note("Workout", "Pushups and squats", ["health"])
        app = NoteApp()
        app.notes = [n1, n2]

        result = [n for n in app.notes if "milk" in n.content.lower()]
        self.assertEqual(result[0], n1)

