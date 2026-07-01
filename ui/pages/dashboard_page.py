from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        title = QLabel("🚍 MAZ Storage Pro")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size:30px;
            font-weight:bold;
            padding-top:40px;
        """)

        subtitle = QLabel("Добро пожаловать!")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size:18px;
            color:#BBBBBB;
        """)

        info = QLabel(
            "Система управления складом запчастей\n"
            "для автобусов МАЗ-203 и МАЗ-206"
        )

        info.setAlignment(Qt.AlignCenter)
        info.setStyleSheet("""
            font-size:16px;
            color:#AAAAAA;
            padding:25px;
        """)

        layout.addStretch()

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(info)

        layout.addStretch()