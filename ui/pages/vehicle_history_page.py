from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QComboBox,
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
        self.resize(1200, 720)

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

        filters = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Поиск по типу ремонта, причине, работам, механику..."
        )
        filters.addWidget(self.search)

        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "Все статусы",
            "В работе",
            "Выполнен",
            "В долгом ремонте",
            "Отменён",
        ])
        self.status_filter.setMinimumWidth(180)
        filters.addWidget(self.status_filter)

        self.reset_filter_button = QPushButton("Сбросить")
        filters.addWidget(self.reset_filter_button)

        layout.addLayout(filters)

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
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.search.textChanged.connect(self.filter_table)
        self.status_filter.currentIndexChanged.connect(self.filter_table)
        self.reset_filter_button.clicked.connect(self.reset_filters)
        self.add_button.clicked.connect(self.add_repair)
        self.view_button.clicked.connect(self.view_repair)
        self.edit_button.clicked.connect(self.edit_repair)
        self.table.cellDoubleClicked.connect(lambda *_: self.view_repair())
        self.delete_button.clicked.connect(self.delete_repair)
        self.refresh_button.clicked.connect(self.load_data)

    def load_data(self):
        self.vehicle = self.vehicle_service.get_vehicle_by_id(self.vehicle.id)

        self.repairs = self.service.get_repairs_by_vehicle(self.vehicle.id)

        total_cost = 0.0
        for repair in self.repairs:
            total_cost += float(repair.cost or 0)
            for item in self.service.get_repair_parts(repair.id):
                total_cost += float(item["quantity"] or 0) * float(item["price"] or 0)

        self.summary.setText(
            f"Текущий пробег: {self.vehicle.mileage:,} км  |  "
            f"Количество ремонтов: {len(self.repairs)}  |  "
            f"Общая стоимость: {total_cost:,.2f}"
        )

        self.fill_table(self.repairs)

    def fill_table(self, repairs):
        self.table.setRowCount(len(repairs))

        for row, repair in enumerate(repairs):
            repair_total = float(repair.cost or 0)
            for item in self.service.get_repair_parts(repair.id):
                repair_total += (
                    float(item["quantity"] or 0)
                    * float(item["price"] or 0)
                )

            values = [
                repair.date,
                str(repair.mileage),
                repair.repair_type,
                repair.reason,
                repair.work_description,
                repair.mechanic_name,
                repair.status,
                f"{repair_total:,.2f}",
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column == 0:
                    item.setData(Qt.UserRole, repair.id)
                self.table.setItem(row, column, item)

        self.table.resizeColumnsToContents()
        self.filter_table()

    def filter_table(self):
        text = self.search.text().lower().strip()
        selected_status = self.status_filter.currentText()

        for row in range(self.table.rowCount()):
            text_match = not text

            if text:
                for column in range(1, 7):
                    item = self.table.item(row, column)
                    if item and text in item.text().lower():
                        text_match = True
                        break

            status_item = self.table.item(row, 6)
            status_match = (
                selected_status == "Все статусы"
                or (
                    status_item is not None
                    and status_item.text() == selected_status
                )
            )

            self.table.setRowHidden(
                row,
                not (text_match and status_match),
            )

    def reset_filters(self):
        self.search.clear()
        self.status_filter.setCurrentIndex(0)

    def current_repair(self):
        row = self.table.currentRow()
        if row < 0:
            return None

        item = self.table.item(row, 0)
        if item is None:
            return None

        repair_id = item.data(Qt.UserRole)

        return next(
            (repair for repair in self.repairs if repair.id == repair_id),
            None,
        )

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
                QMessageBox.warning(
                    self,
                    "Изменение ремонта",
                    str(exc),
                )
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
                QMessageBox.warning(
                    self,
                    "Удаление ремонта",
                    str(exc),
                )
                return

            self.load_data()
