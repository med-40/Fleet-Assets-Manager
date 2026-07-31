import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QVBoxLayout,
    QWidget,
)


class FleetAssetsManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("نظام تسيير الحضيرة")
        self.resize(1100, 700)

        # الاتجاه من اليمين إلى اليسار
        self.setLayoutDirection(Qt.RightToLeft)

        central_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("نظام تسيير الحضيرة")
        title.setAlignment(Qt.AlignRight)
        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            padding: 20px;
        """)

        subtitle = QLabel(
            "إدارة السيارات والصيانة والوقود والمهمات"
        )
        subtitle.setAlignment(Qt.AlignRight)
        subtitle.setStyleSheet("""
            font-size: 18px;
            padding: 10px 20px;
        """)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.RightToLeft)

    window = FleetAssetsManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
