from PySide6.QtWidgets import (
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("MAZ Storage Pro")

        self.resize(1400, 850)

        central = QWidget()

        self.setCentralWidget(central)

        layout = QVBoxLayout()

        title = QLabel("🚍 MAZ Storage Pro")

        title.setStyleSheet("""

            font-size:32px;

            font-weight:bold;

            padding:25px;

        """)

        layout.addWidget(title)

        buttons = [

            "📦 Склад",

            "🚌 Автобусы",

            "📤 Выдача",

            "📥 Приемка",

            "📊 Отчеты",

            "⚙ Настройки"

        ]

        for text in buttons:

            button = QPushButton(text)

            button.setMinimumHeight(55)

            layout.addWidget(button)

        central.setLayout(layout)

        self.statusBar().showMessage("MAZ Storage Pro 1.0 Alpha")




