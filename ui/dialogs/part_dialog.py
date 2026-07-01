from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)


class PartDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Добавление запчасти")

        self.resize(550, 650)

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.article = QLineEdit()

        self.name = QLineEdit()

        self.manufacturer = QLineEdit()

        self.models = QComboBox()
        self.models.addItems([
            "МАЗ-203",
            "МАЗ-206",
            "МАЗ-203 / 206"
        ])

        self.unit = QComboBox()
        self.unit.addItems([
            "шт",
            "компл",
            "л",
            "м",
            "кг"
        ])

        self.quantity = QSpinBox()
        self.quantity.setMaximum(100000)

        self.min_quantity = QSpinBox()
        self.min_quantity.setMaximum(100000)

        self.price = QDoubleSpinBox()
        self.price.setMaximum(100000000)
        self.price.setDecimals(2)

        self.location = QComboBox()

        self.comment = QTextEdit()

        form.addRow("Артикул", self.article)
        form.addRow("Название", self.name)
        form.addRow("Производитель", self.manufacturer)
        form.addRow("Совместимость", self.models)
        form.addRow("Ед. изм.", self.unit)
        form.addRow("Количество", self.quantity)
        form.addRow("Мин. остаток", self.min_quantity)
        form.addRow("Цена", self.price)
        form.addRow("Место хранения", self.location)
        form.addRow("Комментарий", self.comment)

        layout.addLayout(form)

        buttons = QHBoxLayout()

        self.cancelButton = QPushButton("Отмена")

        self.saveButton = QPushButton("Сохранить")

        buttons.addStretch()

        buttons.addWidget(self.cancelButton)

        buttons.addWidget(self.saveButton)

        layout.addLayout(buttons)

        self.cancelButton.clicked.connect(self.reject)

        self.saveButton.clicked.connect(self.accept)