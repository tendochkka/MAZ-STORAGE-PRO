from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QMessageBox,
)

from services.repair_service import RepairService
from ui.dialogs.repair_dialog import RepairDialog
from ui.dialogs.repair_view_dialog import RepairViewDialog


class RepairsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.service = RepairService()

        self.build_ui()
        self.load_data()

    def build_ui(self):
        layout = QVBoxLayout(self)

        filters = QHBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Поиск по автобусу, причине, работам, механику...")
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
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "Дата",
            "Автобус",
            "Модель",
            "Пробег",
            "Тип ремонта",
            "Причина",
            "Механик",
            "Статус",
            "Стоимость",
        ])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
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
        self.repairs = self.service.get_all_repairs()
        self.fill_table(self.repairs)

    def fill_table(self, repairs):
        self.table.setRowCount(len(repairs))

        for row, repair in enumerate(repairs):
            values = [
                repair.date,
                repair.vehicle_plate,
                repair.vehicle_model,
                str(repair.mileage),
                repair.repair_type,
                repair.reason,
                repair.mechanic_name,
                repair.status,
                f"{repair.cost:.2f}",
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)
                if column == 0:
                    item.setData(Qt.UserRole, repair.id)
                self.table.setItem(row, column, item)

        self.table.resizeColumnsToContents()

    def filter_table(self):
        text = self.search.text().lower().strip()
        selected_status = self.status_filter.currentText()

        for row in range(self.table.rowCount()):
            text_match = not text
            if text:
                for column in range(self.table.columnCount()):
                    item = self.table.item(row, column)
                    if item and text in item.text().lower():
                        text_match = True
                        break

            status_item = self.table.item(row, 7)
            status_match = (
                selected_status == "Все статусы"
                or (status_item is not None and status_item.text() == selected_status)
            )

            self.table.setRowHidden(row, not (text_match and status_match))

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
                QMessageBox.warning(self, "Изменение ремонта", str(exc))
                return
            self.load_data()

    def delete_repair(self):
        repair = self.current_repair()
        if repair is None:
            return

        from PySide6.QtWidgets import QMessageBox

        answer = QMessageBox.question(
            self,
            "Удаление",
            f"Удалить ремонт от {repair.date} для {repair.vehicle_plate}?",
        )

        if answer == QMessageBox.Yes:
            try:
                self.service.delete_repair(repair.id)
            except ValueError as exc:
                QMessageBox.warning(self, "Удаление ремонта", str(exc))
                return
            self.load_data()
