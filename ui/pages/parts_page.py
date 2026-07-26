from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
)


from services.part_service import PartService


class PartsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = PartService()

        self.build_ui()
        self.load_data()

    def build_ui(self):

        layout = QVBoxLayout(self)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Поиск запчастей...")

        layout.addWidget(self.search_edit)

        button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")
        self.refresh_button = QPushButton("Обновить")

        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)

        button_layout.addStretch()

        button_layout.addWidget(self.refresh_button)

        layout.addLayout(button_layout)

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

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.verticalHeader().setVisible(False)

        self.table.horizontalHeader().setStretchLastSection(False)

        self.table.horizontalHeader().setSectionResizeMode(
            1,
            QHeaderView.Stretch
        )

        layout.addWidget(self.table)

        self.search_edit.textChanged.connect(
            self.filter_table
        )

        self.refresh_button.clicked.connect(
            self.load_data
        )

    def load_data(self):

        self.parts = self.service.get_all_parts()

        self.table.setRowCount(len(self.parts))

        for row, part in enumerate(self.parts):

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

    def filter_table(self):

        text = self.search_edit.text().lower()

        for row in range(self.table.rowCount()):

            visible = False

            for column in range(self.table.columnCount()):

                item = self.table.item(row, column)

                if item and text in item.text().lower():
                    visible = True
                    break

            self.table.setRowHidden(
                row,
                not visible
            )