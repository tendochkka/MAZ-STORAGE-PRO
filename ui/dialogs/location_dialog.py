from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)

from models.location import Location


class LocationDialog(QDialog):

    def __init__(self, location=None, parent=None):
        super().__init__(parent)

        self.location = location

        self.setWindowTitle("Место хранения")
        self.setMinimumWidth(420)

        self.create_ui()
        self.load_data()

    def create_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.zone_edit = QLineEdit()
        self.rack_edit = QLineEdit()
        self.shelf_edit = QLineEdit()
        self.cell_edit = QLineEdit()
        self.description_edit = QLineEdit()

        self.code_label = QLabel("-")

        form.addRow("Зона", self.zone_edit)
        form.addRow("Стеллаж", self.rack_edit)
        form.addRow("Полка", self.shelf_edit)
        form.addRow("Ячейка", self.cell_edit)
        form.addRow("Описание", self.description_edit)
        form.addRow("Код", self.code_label)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")

        buttons.addStretch()
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.cancel_button)

        layout.addLayout(buttons)

        self.zone_edit.textChanged.connect(self.update_code)
        self.rack_edit.textChanged.connect(self.update_code)
        self.shelf_edit.textChanged.connect(self.update_code)
        self.cell_edit.textChanged.connect(self.update_code)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def load_data(self):

        if self.location is None:
            return

        self.zone_edit.setText(self.location.zone)
        self.rack_edit.setText(self.location.rack)
        self.shelf_edit.setText(self.location.shelf)
        self.cell_edit.setText(self.location.cell)
        self.description_edit.setText(self.location.description)

        self.update_code()

    def update_code(self):

        zone = self.zone_edit.text().strip()
        rack = self.rack_edit.text().strip()
        shelf = self.shelf_edit.text().strip()
        cell = self.cell_edit.text().strip()

        code = f"{zone}-{rack}-{shelf}-{cell}"

        self.code_label.setText(code)

    def get_location(self):

        if self.location is None:
            location = Location()
        else:
            location = self.location

        location.zone = self.zone_edit.text().strip()
        location.rack = self.rack_edit.text().strip()
        location.shelf = self.shelf_edit.text().strip()
        location.cell = self.cell_edit.text().strip()
        location.description = self.description_edit.text().strip()

        return location