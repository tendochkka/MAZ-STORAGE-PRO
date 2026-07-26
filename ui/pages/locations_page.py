from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
)

from services.location_service import LocationService
from ui.dialogs.location_dialog import LocationDialog


class LocationsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = LocationService()

        self.create_ui()
        self.load_data()

    def create_ui(self):

        layout = QVBoxLayout(self)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск...")

        layout.addWidget(self.search_edit)

        buttons = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")
        self.refresh_button = QPushButton("Обновить")

        buttons.addWidget(self.add_button)
        buttons.addWidget(self.edit_button)
        buttons.addWidget(self.delete_button)
        buttons.addStretch()
        buttons.addWidget(self.refresh_button)

        layout.addLayout(buttons)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Код",
            "Зона",
            "Стеллаж",
            "Полка",
            "Ячейка",
            "Описание",
        ])

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)

        layout.addWidget(self.table)

        self.search_edit.textChanged.connect(self.filter_table)

        self.add_button.clicked.connect(self.add_location)
        self.edit_button.clicked.connect(self.edit_location)
        self.delete_button.clicked.connect(self.delete_location)
        self.refresh_button.clicked.connect(self.load_data)

    def load_data(self):

        self.locations = self.service.get_all_locations()

        self.table.setRowCount(len(self.locations))

        for row, location in enumerate(self.locations):

            self.table.setItem(row, 0, QTableWidgetItem(location.code))
            self.table.setItem(row, 1, QTableWidgetItem(location.zone))
            self.table.setItem(row, 2, QTableWidgetItem(location.rack))
            self.table.setItem(row, 3, QTableWidgetItem(location.shelf))
            self.table.setItem(row, 4, QTableWidgetItem(location.cell))
            self.table.setItem(row, 5, QTableWidgetItem(location.description))

        self.table.resizeColumnsToContents()

    def filter_table(self):

        text = self.search_edit.text().lower()

        for row in range(self.table.rowCount()):

            visible = False

            for column in range(self.table.columnCount()):

                item = self.table.item(row, column)

                if item and text in item.text().lower():
                    visible = True
                    break

            self.table.setRowHidden(row, not visible)

    def current_location(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return self.locations[row]

    def add_location(self):

        dialog = LocationDialog(parent=self)

        if dialog.exec():

            location = dialog.get_location()

            self.service.add_location(
                location.zone,
                location.rack,
                location.shelf,
                location.cell,
                location.description,
            )

            self.load_data()

    def edit_location(self):

        location = self.current_location()

        if location is None:
            return

        dialog = LocationDialog(location, self)

        if dialog.exec():

            self.service.update_location(
                dialog.get_location()
            )

            self.load_data()

    def delete_location(self):

        location = self.current_location()

        if location is None:
            return

        answer = QMessageBox.question(
            self,
            "Удаление",
            f"Удалить место хранения {location.code}?"
        )

        if answer == QMessageBox.Yes:

            self.service.delete_location(location.id)

            self.load_data()