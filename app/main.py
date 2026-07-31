import sys

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

        self.setWindowTitle("Fleet Assets Manager")
        self.resize(1000, 650)

        central_widget = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Fleet Assets Manager")
        title.setStyleSheet(
            "font-size: 28px; font-weight: bold;"
        )

        welcome = QLabel(
            "Welcome to Fleet Assets Manager"
        )

        layout.addWidget(title)
        layout.addWidget(welcome)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


def main():

    app = QApplication(sys.argv)

    window = FleetAssetsManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
