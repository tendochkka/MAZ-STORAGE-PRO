from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
)

from services.repair_service import RepairService
from services.transaction_service import TransactionService


class RepairViewDialog(QDialog):

    def __init__(self, repair, parent=None):
        super().__init__(parent)

        self.repair = repair
        self.service = RepairService()
        self.transaction_service = TransactionService()

        self.setWindowTitle("Карточка ремонта")
        self.setMinimumWidth(950)
        self.setMinimumHeight(700)

        self.build_ui()
        self.load_data()

    def build_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.vehicle = QLineEdit()
        self.vehicle.setReadOnly(True)
        self.date = QLineEdit()
        self.date.setReadOnly(True)
        self.mileage = QLineEdit()
        self.mileage.setReadOnly(True)
        self.repair_type = QLineEdit()
        self.repair_type.setReadOnly(True)
        self.mechanic = QLineEdit()
        self.mechanic.setReadOnly(True)
        self.status = QLineEdit()
        self.status.setReadOnly(True)
        self.cost = QLineEdit()
        self.cost.setReadOnly(True)

        self.reason = QTextEdit()
        self.reason.setReadOnly(True)
        self.reason.setFixedHeight(70)
        self.work_description = QTextEdit()
        self.work_description.setReadOnly(True)
        self.work_description.setFixedHeight(90)
        self.comment = QTextEdit()
        self.comment.setReadOnly(True)
        self.comment.setFixedHeight(70)

        form.addRow("Автобус", self.vehicle)
        form.addRow("Дата", self.date)
        form.addRow("Пробег", self.mileage)
        form.addRow("Тип ремонта", self.repair_type)
        form.addRow("Механик", self.mechanic)
        form.addRow("Статус", self.status)
        form.addRow("Стоимость ремонта", self.cost)
        form.addRow("Причина обращения", self.reason)
        form.addRow("Выполненные работы", self.work_description)
        form.addRow("Комментарий", self.comment)
        layout.addLayout(form)

        self.parts_table = QTableWidget()
        self.parts_table.setColumnCount(8)
        self.parts_table.setHorizontalHeaderLabels([
            "Артикул",
            "Запчасть",
            "Нужно",
            "Выдано",
            "Осталось",
            "Ед.",
            "Цена",
            "Сумма",
        ])
        self.parts_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.parts_table.verticalHeader().setVisible(False)
        self.parts_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        layout.addWidget(self.parts_table)

        totals = QHBoxLayout()
        self.parts_total_label = QLabel("Стоимость запчастей: 0.00")
        self.total_cost_label = QLabel("Общая стоимость: 0.00")
        totals.addWidget(self.parts_total_label)
        totals.addStretch()
        totals.addWidget(self.total_cost_label)
        layout.addLayout(totals)

        buttons = QHBoxLayout()
        self.issue_button = QPushButton("Выдать запчасти")
        self.close_button = QPushButton("Закрыть")
        buttons.addWidget(self.issue_button)
        buttons.addStretch()
        buttons.addWidget(self.close_button)
        layout.addLayout(buttons)

        self.issue_button.clicked.connect(self.issue_parts)
        self.close_button.clicked.connect(self.accept)

    def load_data(self):
        self.vehicle.setText(
            f"{self.repair.vehicle_plate} — {self.repair.vehicle_model}"
        )
        self.date.setText(self.repair.date)
        self.mileage.setText(str(self.repair.mileage))
        self.repair_type.setText(self.repair.repair_type)
        self.mechanic.setText(self.repair.mechanic_name or "Не указан")
        self.status.setText(self.repair.status)
        self.cost.setText(f"{self.repair.cost:.2f}")
        self.reason.setPlainText(self.repair.reason)
        self.work_description.setPlainText(self.repair.work_description)
        self.comment.setPlainText(self.repair.comment)

        parts = self.service.get_repair_parts(self.repair.id)
        self.parts_table.setRowCount(len(parts))
        can_issue = False
        parts_total = 0.0

        for row, item in enumerate(parts):
            quantity = int(item["quantity"] or 0)
            issued = int(item["issued_quantity"] or 0)
            remaining = max(quantity - issued, 0)
            price = float(item["price"] or 0.0)
            total = quantity * price
            parts_total += total

            if remaining > 0:
                can_issue = True

            values = [
                item["article"] or "",
                item["name"] or "",
                str(quantity),
                str(issued),
                str(remaining),
                item["unit"] or "",
                f"{price:.2f}",
                f"{total:.2f}",
            ]

            for column, value in enumerate(values):
                self.parts_table.setItem(row, column, QTableWidgetItem(value))

        self.issue_button.setEnabled(can_issue and bool(parts))
        self.parts_table.resizeColumnsToContents()

        self.parts_total = parts_total
        self.parts_total_label.setText(
            f"Стоимость запчастей: {parts_total:,.2f}"
        )
        self.total_cost_label.setText(
            f"Общая стоимость: {(float(self.repair.cost or 0) + parts_total):,.2f}"
        )

    def issue_parts(self):
        parts = self.service.get_repair_parts(self.repair.id)

        try:
            count = self.transaction_service.issue_repair_parts(
                self.repair.id,
                self.repair.vehicle_id,
                self.repair.mechanic_id,
                parts,
            )
        except ValueError as exc:
            QMessageBox.warning(self, "Выдача запчастей", str(exc))
            return
        except Exception as exc:
            QMessageBox.critical(
                self,
                "Ошибка",
                f"Не удалось выдать запчасти:\n{exc}",
            )
            return

        if count == 0:
            QMessageBox.information(
                self,
                "Выдача запчастей",
                "Все запчасти по этому ремонту уже выданы.",
            )
        else:
            QMessageBox.information(
                self,
                "Выдача запчастей",
                f"Выдано единиц запчастей: {count}.",
            )

        self.load_data()
