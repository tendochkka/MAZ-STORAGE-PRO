from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QHBoxLayout,
    QStackedWidget,
)

from ui.pages.parts_page import PartsPage
from ui.pages.locations_page import LocationsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MAZ Storage Pro")
        self.resize(1400, 800)

        self.create_ui()

    def create_ui(self):

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)

        self.menu = QListWidget()
        self.menu.setFixedWidth(220)

        self.menu.addItem("📦 Запчасти")
        self.menu.addItem("📍 Места хранения")

        layout.addWidget(self.menu)

        self.stack = QStackedWidget()

        self.parts_page = PartsPage()
        self.locations_page = LocationsPage()

        self.stack.addWidget(self.parts_page)
        self.stack.addWidget(self.locations_page)

        layout.addWidget(self.stack)

        self.menu.currentRowChanged.connect(
            self.stack.setCurrentIndex
        )

        self.menu.setCurrentRow(0)