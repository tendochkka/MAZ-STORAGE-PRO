from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QSpinBox,
    QPushButton,
)

from models.vehicle import Vehicle


class VehicleDialog(QDialog):

    def __init__(self, vehicle=None, parent=None):
        super().__init__(parent)

        self.vehicle = vehicle

        self.setWindowTitle("Автобус")
        self.setMinimumWidth(500)

        self.build_ui()
        self.load_data()

    def build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.plate_number = QLineEdit()
        self.model = QLineEdit()
        self.garage_number = QLineEdit()
        self.vin = QLineEdit()
        self.mileage = QSpinBox()
        self.mileage.setMaximum(10_000_000)
        self.comment = QLineEdit()

        form.addRow("Гос. номер", self.plate_number)
        form.addRow("Модель", self.model)
        form.addRow("Гаражный номер", self.garage_number)
        form.addRow("VIN", self.vin)
        form.addRow("Пробег", self.mileage)
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

    def load_data(self):
        if self.vehicle is None:
            return

        self.plate_number.setText(self.vehicle.plate_number)
        self.model.setText(self.vehicle.model)
        self.garage_number.setText(self.vehicle.garage_number)
        self.vin.setText(self.vehicle.vin)
        self.mileage.setValue(self.vehicle.mileage)
        self.comment.setText(self.vehicle.comment)

    def get_vehicle(self):
        vehicle = self.vehicle or Vehicle()

        vehicle.plate_number = self.plate_number.text().strip().upper()
        vehicle.model = self.model.text().strip()
        vehicle.garage_number = self.garage_number.text().strip()
        vehicle.vin = self.vin.text().strip().upper()
        vehicle.mileage = self.mileage.value()
        vehicle.comment = self.comment.text().strip()

        return vehicle
