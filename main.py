import json
import uuid      # Для генерации уникальных ID для заметок
import os        # Для работы с файловой системой (проверка наличия файла и т.д.)

FILE_NAME = "notes.json"

# Класс Note — описывает одну заметку
class Note:
    def __init__(self, title, content, tags=None, note_id=None):
        self.id = note_id or str(uuid.uuid4())[:8]  # Генерируем уникальный ID (8 символов)
        self.title = title                          # Заголовок заметки
        self.content = content                      # Содержимое заметки
        self.tags = tags if tags else []            # Теги (если не переданы — создаём пустой список)

    # Преобразование заметки в словарь для сохранения в JSON
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "tags": self.tags
        }

    # Создание заметки из словаря
    @staticmethod
    def from_dict(data):
        return Note(data["title"], data["content"], data["tags"], data["id"])

    # Метод отображения заметки в консоли
    def display(self):
        print("=" * 50)
        print(f"[{self.id}] {self.title.upper()}")  # Показываем заголовок заглавными буквами
        print("-" * 50)
        print(self.content)                         # Показываем содержание
        if self.tags:                               # Если есть теги — показываем их
            print(f"📌 Теги: {', '.join(self.tags)}")
        print("=" * 50)

# Класс NoteApp — управление заметками и логикой приложения
class NoteApp:
    def __init__(self):
        self.notes = []        # Список всех заметок
        self.load_notes()      # Загружаем заметки из файла при запуске

    # Сохранение всех заметок в JSON-файл
    def save_notes(self):
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            json.dump([note.to_dict() for note in self.notes], f, indent=4, ensure_ascii=False)

    # Загрузка заметок из JSON-файла
    def load_notes(self):
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.notes = [Note.from_dict(d) for d in data]

    # Создание новой заметки через ввод пользователя
    def create_note(self):
        title = input("Заголовок: ")
        print("Введите текст заметки (в конце введите 'END' на новой строке):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        content = "\n".join(lines)  # Собираем все строки в одну строку с переводами строк
        tags = input("Теги (через запятую): ").split(",")
        tags = [tag.strip() for tag in tags if tag.strip()]  # Очищаем пробелы и пустые значения
        note = Note(title, content, tags)  # Создаём заметку
        self.notes.append(note)           # Добавляем в список
        self.save_notes()                 # Сохраняем в файл
        print("✅ Заметка создана.")

    # Показать все заметки
    def list_notes(self):
        if not self.notes:
            print("Нет заметок.")
            return
        for note in self.notes:
            note.display()

    # Поиск заметки по ID
    def find_note_by_id(self, note_id):
        for note in self.notes:
            if note.id == note_id:
                return note
        return None

    # Редактирование заметки
    def edit_note(self):
        note_id = input("Введите ID заметки: ")
        note = self.find_note_by_id(note_id)
        if not note:
            print("Заметка не найдена.")
            return
        new_title = input(f"Новый заголовок (оставьте пустым чтобы не менять): ")
        print("Новый текст (введите 'END' чтобы закончить):")
        lines = []
        while True:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        new_content = "\n".join(lines)
        new_tags = input("Новые теги (через запятую): ")

        # Применяем изменения только если пользователь что-то ввёл
        if new_title:
            note.title = new_title
        if new_content:
            note.content = new_content
        if new_tags:
            note.tags = [tag.strip() for tag in new_tags.split(",") if tag.strip()]

        self.save_notes()
        print("✏️ Заметка обновлена.")

    # Удаление заметки по ID
    def delete_note(self):
        note_id = input("Введите ID для удаления: ")
        note = self.find_note_by_id(note_id)
        if not note:
            print("Заметка не найдена.")
            return
        self.notes.remove(note)
        self.save_notes()
        print("🗑️ Заметка удалена.")

    # Поиск заметок по ключевому слову
    def search_notes(self):
        keyword = input("Введите слово для поиска: ").lower()
        found = [n for n in self.notes if
                 keyword in n.title.lower() or
                 keyword in n.content.lower() or
                 any(keyword in tag.lower() for tag in n.tags)]
        if found:
            print(f"🔍 Найдено {len(found)} заметок:")
            for note in found:
                note.display()
        else:
            print("Ничего не найдено.")

    def run(self):
        while True:
            print("\n📝 Меню:")
            print("1. ➕ Создать заметку")
            print("2. 📋 Показать все заметки")
            print("3. ✏️ Редактировать заметку")
            print("4. 🗑️ Удалить заметку")
            print("5. 🔍 Поиск по заметкам")
            print("0. 🚪 Выход")

            choice = input("Выбор: ")

            if choice == '1':
                self.create_note()
            elif choice == '2':
                self.list_notes()
            elif choice == '3':
                self.edit_note()
            elif choice == '4':
                self.delete_note()
            elif choice == '5':
                self.search_notes()
            elif choice == '0':
                print("Выход из приложения...")
                break
            else:
                print("❌ Неверный выбор!")

if __name__ == "__main__":
    app = NoteApp()
    app.run()
