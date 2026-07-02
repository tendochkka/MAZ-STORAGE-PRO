import sys
import traceback
from database.seed import seed_database

from PySide6.QtWidgets import QApplication, QMessageBox

from database.schema import create_database
from services.logger import logger
from ui.main_window import MainWindow


def exception_hook(exc_type, exc_value, exc_traceback):

    error = "".join(
        traceback.format_exception(
            exc_type,
            exc_value,
            exc_traceback
        )
    )

    logger.error(error)

    QMessageBox.critical(
        None,
        "Ошибка",
        error
    )


sys.excepthook = exception_hook


def main():

    create_database()
    seed_database()

    app = QApplication(sys.argv)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()