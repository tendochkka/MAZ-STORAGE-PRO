from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        label = QLabel("⚙ Настройки")

        label.setAlignment(Qt.AlignCenter)

        label.setStyleSheet("""
            font-size:26px;
            font-weight:bold;
        """)

        layout.addStretch()
        layout.addWidget(label)
        layout.addStretch()