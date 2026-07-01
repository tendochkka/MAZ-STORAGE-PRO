from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QSplitter,
    QStackedWidget,
)

from ui.pages.dashboard_page import DashboardPage
from ui.pages.parts_page import PartsPage
from ui.pages.vehicles_page import VehiclesPage
from ui.pages.reports_page import ReportsPage
from ui.pages.settings_page import SettingsPage


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MAZ Storage Pro")

        self.resize(1400, 850)

        splitter = QSplitter()

        self.setCentralWidget(splitter)

        self.menu = QListWidget()

        self.menu.setMaximumWidth(220)

        pages = [
            "🏠 Главная",
            "📦 Склад",
            "🚌 Автобусы",
            "📊 Отчёты",
            "⚙ Настройки",
        ]

        for page in pages:
            QListWidgetItem(page, self.menu)

        splitter.addWidget(self.menu)

        self.stack = QStackedWidget()

        splitter.addWidget(self.stack)

        self.stack.addWidget(DashboardPage())
        self.stack.addWidget(PartsPage())
        self.stack.addWidget(VehiclesPage())
        self.stack.addWidget(ReportsPage())
        self.stack.addWidget(SettingsPage())

        splitter.setStretchFactor(1, 1)

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)

        self.menu.setCurrentRow(0)

        self.statusBar().showMessage("MAZ Storage Pro v0.1.0")