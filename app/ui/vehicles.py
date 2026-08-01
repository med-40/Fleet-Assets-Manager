from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
)


class VehiclesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setLayoutDirection(Qt.RightToLeft)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(15)

        # العنوان
        title = QLabel("السيارات")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(title)

        # البحث والفلاتر
        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("بحث عن سيارة...")
        self.search_box.setMinimumHeight(40)

        self.status_filter = QComboBox()
        self.status_filter.addItems([
            "كل الحالات",
            "متاحة",
            "في مهمة",
            "في الصيانة",
            "متوقفة",
        ])
        self.status_filter.setMinimumHeight(40)

        self.type_filter = QComboBox()
        self.type_filter.addItems([
            "كل أنواع العتاد",
            "سيارة",
            "شاحنة",
            "حافلة",
            "مركبة أخرى",
        ])
        self.type_filter.setMinimumHeight(40)

        self.department_filter = QComboBox()
        self.department_filter.addItem("كل المصالح")
        self.department_filter.setMinimumHeight(40)

        filters_layout.addWidget(self.search_box, 2)
        filters_layout.addWidget(self.status_filter, 1)
        filters_layout.addWidget(self.type_filter, 1)
        filters_layout.addWidget(self.department_filter, 1)

        main_layout.addLayout(filters_layout)

        # الأزرار
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        add_button = QPushButton("إضافة")
        edit_button = QPushButton("تعديل")
        archive_button = QPushButton("أرشفة")
        refresh_button = QPushButton("تحديث")

        for button in [
            add_button,
            edit_button,
            archive_button,
            refresh_button,
        ]:
            button.setMinimumHeight(40)

        add_button.clicked.connect(self.add_vehicle)
        edit_button.clicked.connect(self.edit_vehicle)
        archive_button.clicked.connect(self.archive_vehicle)
        refresh_button.clicked.connect(self.refresh_table)

        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(edit_button)
        buttons_layout.addWidget(archive_button)
        buttons_layout.addWidget(refresh_button)
        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        # جدول السيارات
        self.table = QTableWidget()

        self.columns = [
            "وثيقة الاستلام",
            "نوع العتاد",
            "العلامة",
            "الطراز",
            "رقم الهيكل",
            "رقم التسجيل",
            "نوع الوقود",
            "معدل الاستهلاك",
            "الحالة",
            "تاريخ آخر مراجعة",
            "المصلحة",
        ]

        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setSelectionMode(
            QTableWidget.SingleSelection
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.table)

        # عدد السيارات
        self.count_label = QLabel("عدد السيارات: 0")
        self.count_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(self.count_label)

        # بيانات تجريبية مؤقتة
        self.load_demo_data()

    def load_demo_data(self):
        """بيانات مؤقتة لاختبار شكل الصفحة."""

        data = [
            [
                "REC-001",
                "سيارة",
                "Toyota",
                "Hilux",
                "VIN000001",
                "000001-16-00",
                "ديزل",
                "10.5",
                "متاحة",
                "2026-07-15",
                "المصلحة 1",
            ],
            [
                "REC-002",
                "حافلة",
                "Higer",
                "KLQ",
                "VIN000002",
                "000002-16-00",
                "ديزل",
                "18.0",
                "في مهمة",
                "2026-07-10",
                "المصلحة 2",
            ],
        ]

        self.table.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for column_index, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(
                    row_index,
                    column_index,
                    item,
                )

        self.update_count()

    def update_count(self):
        count = self.table.rowCount()
        self.count_label.setText(
            f"عدد السيارات: {count}"
        )

    def add_vehicle(self):
        QMessageBox.information(
            self,
            "إضافة سيارة",
            "نافذة إضافة السيارة سيتم تجهيزها في الخطوة التالية.",
        )

    def edit_vehicle(self):
        current_row = self.table.currentRow()

        if current_row < 0:
            QMessageBox.warning(
                self,
                "تنبيه",
                "اختر سيارة أولًا.",
            )
            return

        QMessageBox.information(
            self,
            "تعديل سيارة",
            "نافذة تعديل السيارة سيتم تجهيزها لاحقًا.",
        )

    def archive_vehicle(self):
        current_row = self.table.currentRow()

        if current_row < 0:
            QMessageBox.warning(
                self,
                "تنبيه",
                "اختر سيارة أولًا.",
            )
            return

        QMessageBox.information(
            self,
            "أرشفة",
            "نظام الأرشفة سيتم ربطه بقاعدة البيانات لاحقًا.",
        )

    def refresh_table(self):
        self.load_demo_data()
