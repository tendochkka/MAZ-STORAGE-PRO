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
    QHeaderView,
)

from services.vehicle_service import VehicleService
from services.repair_service import RepairService
from ui.dialogs.vehicle_dialog import VehicleDialog
from ui.pages.vehicle_history_page import VehicleHistoryPage


class VehiclesPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = VehicleService()
        self.repair_service = RepairService()

        self.build_ui()
        self.load_data()

    def build_ui(self):
        layout = QVBoxLayout(self)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск по гос. номеру, модели, VIN...")
        layout.addWidget(self.search)

        buttons = QHBoxLayout()
        self.add_button = QPushButton("Добавить")
        self.edit_button = QPushButton("Изменить")
        self.delete_button = QPushButton("Удалить")
        self.history_button = QPushButton("История ремонта")
        self.refresh_button = QPushButton("Обновить")

        buttons.addWidget(self.add_button)
        buttons.addWidget(self.edit_button)
        buttons.addWidget(self.delete_button)
        buttons.addWidget(self.history_button)
        buttons.addStretch()
        buttons.addWidget(self.refresh_button)
        layout.addLayout(buttons)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Гос. номер",
            "Модель",
            "Гаражный №",
            "VIN",
            "Пробег",
            "Комментарий",
            "ID",
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.search.textChanged.connect(self.filter_table)
        self.add_button.clicked.connect(self.add_vehicle)
        self.edit_button.clicked.connect(self.edit_vehicle)
        self.delete_button.clicked.connect(self.delete_vehicle)
        self.history_button.clicked.connect(self.open_history)
        self.refresh_button.clicked.connect(self.load_data)
        self.table.cellDoubleClicked.connect(lambda *_: self.open_history())

    def load_data(self):
        self.vehicles = self.service.get_all_vehicles()
        self.fill_table(self.vehicles)

    def fill_table(self, vehicles):
        self.table.setRowCount(len(vehicles))

        for row, vehicle in enumerate(vehicles):
            values = [
                vehicle.plate_number,
                vehicle.model,
                vehicle.garage_number,
                vehicle.vin,
                str(vehicle.mileage),
                vehicle.comment,
                str(vehicle.id),
            ]

            for column, value in enumerate(values):
                self.table.setItem(row, column, QTableWidgetItem(value))

        self.table.resizeColumnsToContents()

    def filter_table(self):
        text = self.search.text().lower().strip()

        for row in range(self.table.rowCount()):
            visible = False
            for column in range(self.table.columnCount()):
                item = self.table.item(row, column)
                if item and text in item.text().lower():
                    visible = True
                    break
            self.table.setRowHidden(row, not visible)

    def current_vehicle(self):
        row = self.table.currentRow()
        if row < 0:
            return None

        visible_vehicles = [
            vehicle for vehicle in self.vehicles
            if not self.table.isRowHidden(self.vehicles.index(vehicle))
        ]

        item = self.table.item(row, 6)
        if item is None:
            return None

        vehicle_id = int(item.text())
        return next(
            (vehicle for vehicle in self.vehicles if vehicle.id == vehicle_id),
            None,
        )

    def add_vehicle(self):
        dialog = VehicleDialog(parent=self)
        if dialog.exec():
            self.service.add_vehicle(dialog.get_vehicle())
            self.load_data()

    def edit_vehicle(self):
        vehicle = self.current_vehicle()
        if vehicle is None:
            return

        dialog = VehicleDialog(vehicle, self)
        if dialog.exec():
            self.service.update_vehicle(dialog.get_vehicle())
            self.load_data()

    def delete_vehicle(self):
        vehicle = self.current_vehicle()
        if vehicle is None:
            return

        answer = QMessageBox.question(
            self,
            "Удаление",
            f"Удалить автобус {vehicle.plate_number}?",
        )

        if answer == QMessageBox.Yes:
            self.service.delete_vehicle(vehicle.id)
            self.load_data()

    def open_history(self):
        vehicle = self.current_vehicle()
        if vehicle is None:
            return

        self.history_window = VehicleHistoryPage(vehicle, self)
        self.history_window.show()
