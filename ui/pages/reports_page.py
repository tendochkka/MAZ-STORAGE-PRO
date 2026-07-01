from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class ReportsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("📊 Отчёты")

        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()