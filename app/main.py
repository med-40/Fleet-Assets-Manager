import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)

from dashboard import Dashboard


class FleetAssetsManager(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("نظام تسيير الحضيرة")
        self.resize(1200, 750)

        # الاتجاه من اليمين إلى اليسار
        self.setLayoutDirection(Qt.RightToLeft)

        # عرض لوحة التحكم
        self.dashboard = Dashboard()
        self.setCentralWidget(self.dashboard)


def main():

    app = QApplication(sys.argv)

    app.setLayoutDirection(Qt.RightToLeft)

    window = FleetAssetsManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
