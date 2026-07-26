from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QHeaderView
)

from services.part_service import PartService
from services.search_service import SearchService
from ui.dialogs.part_dialog import PartDialog


class PartsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = PartService()
        self.search_service = SearchService()

        self.build_ui()
        self.load_data()

    def build_ui(self):

        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск...")

        layout.addWidget(self.search)

        buttons = QHBoxLayout()

        self.add_btn = QPushButton("Добавить")
        self.edit_btn = QPushButton("Изменить")
        self.delete_btn = QPushButton("Удалить")
        self.refresh_btn = QPushButton("Обновить")

        buttons.addWidget(self.add_btn)
        buttons.addWidget(self.edit_btn)
        buttons.addWidget(self.delete_btn)

        buttons.addStretch()

        buttons.addWidget(self.refresh_btn)

        layout.addLayout(buttons)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Артикул",
            "Наименование",
            "Количество",
            "Место хранения",
            "Цена",
            "ID"
        ])

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        self.search.textChanged.connect(
            self.search_parts
        )

        self.refresh_btn.clicked.connect(
            self.load_data
        )

        self.add_btn.clicked.connect(
            self.add_part
        )

        self.edit_btn.clicked.connect(
            self.edit_part
        )

        self.delete_btn.clicked.connect(
            self.delete_part
        )

    def load_data(self):

        self.parts = self.service.get_all_parts()

        self.fill_table(self.parts)

    def fill_table(self, parts):

        self.table.setRowCount(len(parts))

        for row, part in enumerate(parts):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(part.article)
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(part.name)
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(str(part.quantity))
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(part.location_code)
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(f"{part.price:.2f}")
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(str(part.id))
            )

        self.table.resizeColumnsToContents()

    def search_parts(self):

        text = self.search.text()

        self.parts = self.search_service.search_parts(text)

        self.fill_table(self.parts)

    def current_part(self):

        row = self.table.currentRow()

        if row < 0:
            return None

        return self.parts[row]

    def add_part(self):

        dialog = PartDialog(parent=self)

        if dialog.exec():

            self.service.add_part(
                dialog.get_part()
            )

            self.load_data()

    def edit_part(self):

        part = self.current_part()

        if part is None:
            return

        dialog = PartDialog(part, self)

        if dialog.exec():

            self.service.update_part(
                dialog.get_part()
            )

            self.load_data()

    def delete_part(self):

        part = self.current_part()

        if part is None:
            return

        answer = QMessageBox.question(
            self,
            "Удаление",
            f"Удалить запчасть\n\n{part.article}\n{part.name}?"
        )

        if answer == QMessageBox.Yes:

            self.service.delete_part(
                part.id
            )

            self.load_data()