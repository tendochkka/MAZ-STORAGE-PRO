from datetime import date

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QSpinBox,
    QDoubleSpinBox,
    QComboBox,
    QPushButton,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QMessageBox,
    QInputDialog,
)

from models.repair import Repair
from services.vehicle_service import VehicleService
from services.mechanic_service import MechanicService
from services.part_service import PartService
from services.repair_service import RepairService


class RepairDialog(QDialog):

    def __init__(self, repair=None, parent=None):
        super().__init__(parent)

        self.repair = repair
        self.vehicle_service = VehicleService()
        self.mechanic_service = MechanicService()
        self.part_service = PartService()
        self.repair_service = RepairService()

        self.setWindowTitle("Ремонт автобуса")
        self.setMinimumWidth(850)
        self.setMinimumHeight(700)

        self.build_ui()
        self.load_vehicles()
        self.load_mechanics()
        self.load_parts()
        self.load_data()

    def build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.vehicle = QComboBox()
        self.date = QLineEdit(date.today().isoformat())
        self.mileage = QSpinBox()
        self.mileage.setMaximum(10_000_000)
        self.repair_type = QLineEdit()
        self.reason = QTextEdit()
        self.reason.setFixedHeight(70)
        self.work_description = QTextEdit()
        self.work_description.setFixedHeight(90)
        self.mechanic = QComboBox()
        self.add_mechanic_button = QPushButton("Добавить механика")
        self.status = QComboBox()
        self.status.addItems([
            "В работе",
            "Выполнен",
            "В долгом ремонте",
            "Отменён",
        ])
        self.cost = QDoubleSpinBox()
        self.cost.setMaximum(1_000_000_000)
        self.cost.setDecimals(2)
        self.comment = QLineEdit()

        form.addRow("Автобус", self.vehicle)
        form.addRow("Дата", self.date)
        form.addRow("Пробег", self.mileage)
        form.addRow("Тип ремонта", self.repair_type)
        form.addRow("Причина обращения", self.reason)
        form.addRow("Выполненные работы", self.work_description)
        mechanic_layout = QHBoxLayout()
        mechanic_layout.addWidget(self.mechanic)
        mechanic_layout.addWidget(self.add_mechanic_button)
        form.addRow("Механик", mechanic_layout)
        form.addRow("Статус", self.status)
        form.addRow("Стоимость", self.cost)
        form.addRow("Комментарий", self.comment)
        layout.addLayout(form)

        parts_buttons = QHBoxLayout()
        parts_buttons.addWidget(QPushButton("Запчасти ремонта"))
        parts_buttons.addStretch()
        self.add_part_button = QPushButton("Добавить запчасть")
        self.remove_part_button = QPushButton("Удалить запчасть")
        parts_buttons.addWidget(self.add_part_button)
        parts_buttons.addWidget(self.remove_part_button)
        layout.addLayout(parts_buttons)

        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(4)
        self.parts_table.setHorizontalHeaderLabels([
            "Запчасть",
            "Количество",
            "Цена",
            "Комментарий",
        ])
        self.parts_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.parts_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.parts_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.parts_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        layout.addWidget(self.parts_table)

        buttons = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        buttons.addStretch()
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.cancel_button)
        layout.addLayout(buttons)

        self.add_mechanic_button.clicked.connect(self.add_mechanic)
        self.add_part_button.clicked.connect(self.add_part_row)
        self.remove_part_button.clicked.connect(self.remove_part_row)
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def load_vehicles(self):
        self.vehicle.clear()
        self.vehicles = self.vehicle_service.get_all_vehicles()

        for item in self.vehicles:
            self.vehicle.addItem(
                f"{item.plate_number} — {item.model}",
                item.id,
            )

    def load_mechanics(self):
        self.mechanic.clear()
        self.mechanic.addItem("Не указан", None)
        self.mechanics = self.mechanic_service.get_all_mechanics()

        for item in self.mechanics:
            self.mechanic.addItem(item.name, item.id)

    def load_parts(self):
        self.parts = self.part_service.get_all_parts()

    def add_mechanic(self):
        name, ok = QInputDialog.getText(
            self,
            "Добавить механика",
            "ФИО механика:",
        )

        if not ok:
            return

        name = name.strip()
        if not name:
            return

        try:
            self.mechanic_service.add_mechanic(name)
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось добавить механика:\n{exc}",
            )
            return

        current_name = name
        self.load_mechanics()
        index = self.mechanic.findText(current_name)
        if index >= 0:
            self.mechanic.setCurrentIndex(index)

    def load_data(self):
        if self.repair is None:
            return

        vehicle_index = self.vehicle.findData(self.repair.vehicle_id)
        if vehicle_index >= 0:
            self.vehicle.setCurrentIndex(vehicle_index)

        self.date.setText(self.repair.date)
        self.mileage.setValue(self.repair.mileage)
        self.repair_type.setText(self.repair.repair_type)
        self.reason.setPlainText(self.repair.reason)
        self.work_description.setPlainText(self.repair.work_description)

        mechanic_index = self.mechanic.findData(self.repair.mechanic_id)
        if mechanic_index >= 0:
            self.mechanic.setCurrentIndex(mechanic_index)

        status_index = self.status.findText(self.repair.status)
        if status_index >= 0:
            self.status.setCurrentIndex(status_index)

        self.cost.setValue(self.repair.cost)
        self.comment.setText(self.repair.comment)

        for item in self.repair_service.get_repair_parts(self.repair.id):
            self.add_part_row(
                part_id=item["part_id"],
                quantity=item["quantity"],
                price=item["price"],
                comment=item["comment"] or "",
            )

    def add_part_row(self, part_id=None, quantity=1, price=None, comment=""):
        row = self.parts_table.rowCount()
        self.parts_table.insertRow(row)

        combo = QComboBox()
        for part in self.parts:
            combo.addItem(
                f"{part.article} — {part.name}",
                part.id,
            )

        if part_id is not None:
            index = combo.findData(part_id)
            if index >= 0:
                combo.setCurrentIndex(index)

        spin = QSpinBox()
        spin.setMinimum(1)
        spin.setMaximum(1_000_000)
        spin.setValue(quantity)

        price_spin = QDoubleSpinBox()
        price_spin.setMaximum(1_000_000_000)
        price_spin.setDecimals(2)

        if price is None:
            current_part = combo.currentData()
            part = next((p for p in self.parts if p.id == current_part), None)
            price_spin.setValue(part.price if part else 0)
        else:
            price_spin.setValue(price)

        comment_edit = QLineEdit(comment)

        combo.currentIndexChanged.connect(
            lambda: self.update_part_price(combo, price_spin)
        )

        self.parts_table.setCellWidget(row, 0, combo)
        self.parts_table.setCellWidget(row, 1, spin)
        self.parts_table.setCellWidget(row, 2, price_spin)
        self.parts_table.setCellWidget(row, 3, comment_edit)

    def update_part_price(self, combo, price_spin):
        part = next(
            (p for p in self.parts if p.id == combo.currentData()),
            None,
        )
        if part:
            price_spin.setValue(part.price)

    def remove_part_row(self):
        row = self.parts_table.currentRow()
        if row >= 0:
            self.parts_table.removeRow(row)

    def get_repair(self):
        repair = self.repair or Repair()

        repair.vehicle_id = self.vehicle.currentData()
        repair.date = self.date.text().strip()
        repair.mileage = self.mileage.value()
        repair.repair_type = self.repair_type.text().strip()
        repair.reason = self.reason.toPlainText().strip()
        repair.work_description = self.work_description.toPlainText().strip()
        repair.mechanic_id = self.mechanic.currentData()
        repair.status = self.status.currentText()
        repair.cost = self.cost.value()
        repair.comment = self.comment.text().strip()

        return repair

    def get_repair_parts(self):
        result = []

        for row in range(self.parts_table.rowCount()):
            combo = self.parts_table.cellWidget(row, 0)
            quantity = self.parts_table.cellWidget(row, 1)
            price = self.parts_table.cellWidget(row, 2)
            comment = self.parts_table.cellWidget(row, 3)

            if combo is None:
                continue

            result.append({
                "part_id": combo.currentData(),
                "quantity": quantity.value(),
                "price": price.value(),
                "comment": comment.text().strip(),
            })

        return result
