import sys

from PySide6.QtWidgets import QApplication

from ui.main_window import MainWindow
from ui.theme import DARK_THEME

from database.schema import create_database


def main():
    # Создаём базу данных и таблицы, если их ещё нет
    create_database()

    # Создаём приложение Qt
    app = QApplication(sys.argv)

    # Применяем тёмную тему
    app.setStyleSheet(DARK_THEME)

    # Создаём главное окно
    window = MainWindow()

    # Показываем окно
    window.show()

    # Запускаем цикл обработки событий
    sys.exit(app.exec())


if __name__ == "__main__":
    main()