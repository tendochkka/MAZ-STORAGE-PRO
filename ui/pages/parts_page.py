from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
)

from services.part_service import PartService
from ui.dialogs.part_dialog import PartDialog


class PartsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = PartService()

        layout = QVBoxLayout(self)

        title = QLabel("📦 Каталог запчастей")
        title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        layout.addWidget(title)

        top = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Поиск по артикулу или названию..."
        )

        self.add_button = QPushButton("➕ Добавить")

        top.addWidget(self.search)
        top.addWidget(self.add_button)

        layout.addLayout(top)

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels([
            "Артикул",
            "Название",
            "Остаток",
            "Место",
            "Цена",
            "ID"
        ])

        self.table.hideColumn(5)

        layout.addWidget(self.table)

        self.add_button.clicked.connect(self.open_add_dialog)

        self.load_data()

    def load_data(self):

        parts = self.service.get_all_parts()

        self.table.setRowCount(len(parts))

        for row, part in enumerate(parts):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(part["article"])
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(part["name"])
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(str(part["quantity"]))
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(part["location"])
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(str(part["price"]))
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(str(part["id"]))
            )

        self.table.resizeColumnsToContents()

    def open_add_dialog(self):

        dialog = PartDialog(self)

        dialog.exec()