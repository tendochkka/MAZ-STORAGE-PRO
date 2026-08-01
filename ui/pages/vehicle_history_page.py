from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QAbstractItemView,
    QHeaderView,
)

from services.repair_service import RepairService
from services.vehicle_service import VehicleService
from ui.dialogs.repair_dialog import RepairDialog
from ui.dialogs.repair_view_dialog import RepairViewDialog


class VehicleHistoryPage(QWidget):

    def __init__(self, vehicle, parent=None):
        super().__init__(parent)

        self.vehicle = vehicle
        self.service = RepairService()
        self.vehicle_service = VehicleService()

        self.setWindowTitle(
            f"История ремонта — {vehicle.plate_number}"
        )
        self.resize(1100, 650)

        self.build_ui()
        self.load_data()

    def build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel(
            f"🚌 {self.vehicle.plate_number} — "
            f"{self.vehicle.model} | VIN: {self.vehicle.vin}"
        )
        title.setStyleSheet("font-size:20px;font-weight:bold;")
        layout.addWidget(title)

        self.summary = QLabel()
        self.summary.setStyleSheet("font-size:14px;")
        layout.addWidget(self.summary)

        buttons = QHBoxLayout()
        self.add_button = QPushButton("Добавить ремонт")
        self.view_button = QPushButton("Просмотр")
        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")
        self.refresh_button = QPushButton("Обновить")

        buttons.addWidget(self.add_button)
        buttons.addWidget(self.view_button)
        buttons.addWidget(self.edit_button)
        buttons.addWidget(self.delete_button)
        buttons.addStretch()
        buttons.addWidget(self.refresh_button)
        layout.addLayout(buttons)

        self.table = QTableWidget()
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels([
            "Дата",
            "Пробег",
            "Тип ремонта",
            "Причина",
            "Работы",
            "Механик",
            "Статус",
            "Стоимость",
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.add_button.clicked.connect(self.add_repair)
        self.view_button.clicked.connect(self.view_repair)
        self.edit_button.clicked.connect(self.edit_repair)
        self.table.cellDoubleClicked.connect(lambda *_: self.view_repair())
        self.delete_button.clicked.connect(self.delete_repair)
        self.refresh_button.clicked.connect(self.load_data)

    def load_data(self):
        self.repairs = self.service.get_repairs_by_vehicle(self.vehicle.id)
        total_cost = sum(float(repair.cost or 0) for repair in self.repairs)
        self.summary.setText(
            f"Текущий пробег: {self.vehicle.mileage:,} км  |  "
            f"Количество ремонтов: {len(self.repairs)}  |  "
            f"Стоимость ремонтов: {total_cost:,.2f}"
        )
        self.table.setRowCount(len(self.repairs))

        for row, repair in enumerate(self.repairs):
            values = [
                repair.date,
                str(repair.mileage),
                repair.repair_type,
                repair.reason,
                repair.work_description,
                repair.mechanic_name,
                repair.status,
                f"{repair.cost:.2f}",
            ]

            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()

    def current_repair(self):
        row = self.table.currentRow()
        if row < 0 or row >= len(self.repairs):
            return None
        return self.repairs[row]

    def add_repair(self):
        dialog = RepairDialog(parent=self)

        index = dialog.vehicle.findData(self.vehicle.id)
        if index >= 0:
            dialog.vehicle.setCurrentIndex(index)
            dialog.vehicle.setEnabled(False)

        dialog.mileage.setValue(self.vehicle.mileage)

        if dialog.exec():
            self.service.add_repair_with_parts(
                dialog.get_repair(),
                dialog.get_repair_parts(),
            )
            updated_vehicle = self.vehicle_service.get_vehicle_by_id(self.vehicle.id) if hasattr(self, "vehicle_service") else None
            if updated_vehicle is not None:
                self.vehicle = updated_vehicle
            self.load_data()


    def view_repair(self):
        repair = self.current_repair()
        if repair is None:
            return

        dialog = RepairViewDialog(repair, self)
        dialog.exec()

    def edit_repair(self):
        repair = self.current_repair()
        if repair is None:
            return

        dialog = RepairDialog(repair, self)
        if dialog.exec():
            repair_data = dialog.get_repair()
            try:
                self.service.update_repair(repair_data)
                self.service.replace_repair_parts(
                    repair_data.id,
                    dialog.get_repair_parts(),
                )
            except ValueError as exc:
                QMessageBox.warning(self, "Изменение ремонта", str(exc))
                return
            self.load_data()

    def delete_repair(self):
        repair = self.current_repair()
        if repair is None:
            return

        answer = QMessageBox.question(
            self,
            "Удаление",
            f"Удалить ремонт от {repair.date}?",
        )

        if answer == QMessageBox.Yes:
            try:
                self.service.delete_repair(repair.id)
            except ValueError as exc:
                QMessageBox.warning(self, "Удаление ремонта", str(exc))
                return
            self.load_data()
