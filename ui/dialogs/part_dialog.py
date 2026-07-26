from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QPushButton
)

from models.part import Part
from services.location_service import LocationService


class PartDialog(QDialog):

    def __init__(self, part=None, parent=None):
        super().__init__(parent)

        self.part = part

        self.location_service = LocationService()

        self.setWindowTitle("Запчасть")
        self.setMinimumWidth(500)

        self.build_ui()
        self.load_locations()
        self.load_data()

    def build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.article = QLineEdit()
        self.name = QLineEdit()

        self.quantity = QSpinBox()
        self.quantity.setMaximum(1000000)

        self.min_quantity = QSpinBox()
        self.min_quantity.setMaximum(1000000)

        self.price = QDoubleSpinBox()
        self.price.setMaximum(100000000)
        self.price.setDecimals(2)

        self.manufacturer = QLineEdit()

        self.compatible_models = QLineEdit()

        self.unit = QLineEdit()

        self.comment = QLineEdit()

        self.location = QComboBox()

        form.addRow("Артикул", self.article)
        form.addRow("Наименование", self.name)
        form.addRow("Количество", self.quantity)
        form.addRow("Мин. остаток", self.min_quantity)
        form.addRow("Цена", self.price)
        form.addRow("Производитель", self.manufacturer)
        form.addRow("Совместимость", self.compatible_models)
        form.addRow("Ед. измерения", self.unit)
        form.addRow("Место хранения", self.location)
        form.addRow("Комментарий", self.comment)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")

        buttons.addStretch()
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.cancel_button)

        layout.addLayout(buttons)

        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def load_locations(self):

        self.location.clear()

        self.location.addItem("", None)

        self.locations = self.location_service.get_all_locations()

        for location in self.locations:
            self.location.addItem(
                location.code,
                location.id
            )

    def load_data(self):

        if self.part is None:
            return

        self.article.setText(self.part.article)
        self.name.setText(self.part.name)

        self.quantity.setValue(self.part.quantity)
        self.min_quantity.setValue(self.part.min_quantity)

        self.price.setValue(self.part.price)

        self.manufacturer.setText(self.part.manufacturer)
        self.compatible_models.setText(self.part.compatible_models)
        self.unit.setText(self.part.unit)
        self.comment.setText(self.part.comment)

        index = self.location.findData(
            self.part.location_id
        )

        if index >= 0:
            self.location.setCurrentIndex(index)

    def get_part(self):

        part = self.part or Part()

        part.article = self.article.text().strip()
        part.name = self.name.text().strip()

        part.quantity = self.quantity.value()
        part.min_quantity = self.min_quantity.value()

        part.price = self.price.value()

        part.manufacturer = self.manufacturer.text().strip()
        part.compatible_models = self.compatible_models.text().strip()
        part.unit = self.unit.text().strip()
        part.comment = self.comment.text().strip()

        part.location_id = self.location.currentData()

        return part