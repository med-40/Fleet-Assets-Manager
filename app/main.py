import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
    QFrame,
)

from ui.dashboard import DashboardPage


class FleetAssetsManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("نظام تسيير الحضيرة")
        self.resize(1200, 750)

        self.setLayoutDirection(Qt.RightToLeft)

        # الصفحة الرئيسية
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # القائمة الجانبية
        sidebar = QFrame()
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(15, 25, 15, 25)
        sidebar_layout.setSpacing(8)

        logo = QLabel("نظام تسيير الحضيرة")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
                padding: 15px;
            }
        """)

        sidebar_layout.addWidget(logo)

        self.dashboard_button = self.create_menu_button("لوحة التحكم")
        self.vehicles_button = self.create_menu_button("السيارات")
        self.drivers_button = self.create_menu_button("السائقون")
        self.missions_button = self.create_menu_button("المهمات")
        self.fuel_button = self.create_menu_button("الوقود")
        self.maintenance_button = self.create_menu_button("الصيانة")
        self.faults_button = self.create_menu_button("الأعطال")
        self.batteries_button = self.create_menu_button("البطاريات")
        self.tires_button = self.create_menu_button("الإطارات")
        self.reports_button = self.create_menu_button("التقارير")
        self.settings_button = self.create_menu_button("الإعدادات")

        sidebar_layout.addWidget(self.dashboard_button)
        sidebar_layout.addWidget(self.vehicles_button)
        sidebar_layout.addWidget(self.drivers_button)
        sidebar_layout.addWidget(self.missions_button)
        sidebar_layout.addWidget(self.fuel_button)
        sidebar_layout.addWidget(self.maintenance_button)
        sidebar_layout.addWidget(self.faults_button)
        sidebar_layout.addWidget(self.batteries_button)
        sidebar_layout.addWidget(self.tires_button)
        sidebar_layout.addWidget(self.reports_button)
        sidebar_layout.addWidget(self.settings_button)

        sidebar_layout.addStretch()

        version = QLabel("الإصدار 0.2")
        version.setAlignment(Qt.AlignCenter)

        sidebar_layout.addWidget(version)

        # منطقة الصفحات
        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.pages.addWidget(self.dashboard_page)

        # الصفحة المؤقتة لبقية الأقسام
        self.placeholder_page = self.create_placeholder_page(
            "السيارات"
        )
        self.pages.addWidget(self.placeholder_page)

        # الربط
        self.dashboard_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.vehicles_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        # التخطيط الرئيسي
        main_layout.addWidget(sidebar)
        main_layout.addWidget(self.pages)

        # فتح Dashboard عند التشغيل
        self.pages.setCurrentIndex(0)

    def create_menu_button(self, text):
        button = QPushButton(text)
        button.setMinimumHeight(45)

        button.setStyleSheet("""
            QPushButton {
                text-align: right;
                padding: 8px 15px;
                border: none;
                border-radius: 6px;
                font-size: 15px;
            }

            QPushButton:hover {
                background-color: #e8e8e8;
            }
        """)

        return button

    def create_placeholder_page(self, title):
        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 30, 30, 30)

        label = QLabel(title)
        label.setAlignment(Qt.AlignRight)

        label.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
            }
        """)

        layout.addWidget(label)
        layout.addStretch()

        return page


def main():
    app = QApplication(sys.argv)

    app.setLayoutDirection(Qt.RightToLeft)

    window = FleetAssetsManager()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
