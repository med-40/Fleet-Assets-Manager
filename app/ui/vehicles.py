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

from ui.vehicle_dialog import VehicleDialog


class VehiclesPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setLayoutDirection(Qt.RightToLeft)

        self.vehicles = []

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(15)

        # =========================
        # العنوان
        # =========================

        title = QLabel("السيارات")

        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(title)

        # =========================
        # البحث والفلاتر
        # =========================

        filters_layout = QHBoxLayout()
        filters_layout.setSpacing(10)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText(
            "بحث برقم التسجيل، رقم الهيكل، العلامة أو الطراز..."
        )
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

        # =========================
        # الأزرار
        # =========================

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(8)

        self.add_button = QPushButton("إضافة")
        self.edit_button = QPushButton("تعديل")
        self.archive_button = QPushButton("أرشفة")
        self.refresh_button = QPushButton("تحديث")

        for button in [
            self.add_button,
            self.edit_button,
            self.archive_button,
            self.refresh_button,
        ]:
            button.setMinimumHeight(40)

        buttons_layout.addWidget(self.add_button)
        buttons_layout.addWidget(self.edit_button)
        buttons_layout.addWidget(self.archive_button)
        buttons_layout.addWidget(self.refresh_button)

        buttons_layout.addStretch()

        main_layout.addLayout(buttons_layout)

        # =========================
        # جدول السيارات
        # =========================

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

        self.table.setAlternatingRowColors(True)

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        self.table.horizontalHeader().setStretchLastSection(True)

        main_layout.addWidget(self.table)

        # =========================
        # عدد السيارات
        # =========================

        self.count_label = QLabel(
            "عدد السيارات: 0"
        )

        self.count_label.setStyleSheet("""
            QLabel {
                font-size: 15px;
                font-weight: bold;
            }
        """)

        main_layout.addWidget(self.count_label)

        # =========================
        # ربط الأزرار
        # =========================

        self.add_button.clicked.connect(
            self.add_vehicle
        )

        self.edit_button.clicked.connect(
            self.edit_vehicle
        )

        self.archive_button.clicked.connect(
            self.archive_vehicle
        )

        self.refresh_button.clicked.connect(
            self.refresh_table
        )

        self.search_box.textChanged.connect(
            self.apply_filters
        )

        self.status_filter.currentTextChanged.connect(
            self.apply_filters
        )

        self.type_filter.currentTextChanged.connect(
            self.apply_filters
        )

        self.department_filter.currentTextChanged.connect(
            self.apply_filters
        )

        # =========================
        # بيانات مؤقتة للاختبار
        # =========================

        self.load_demo_data()

    # ==================================================
    # بيانات تجريبية
    # ==================================================

    def load_demo_data(self):

        self.vehicles = [
            {
                "receipt_document": "REC-001",
                "vehicle_type": "سيارة",
                "brand": "Toyota",
                "model": "Hilux",
                "vin": "VIN000001",
                "registration_number": "001-16-0001",
                "fuel_type": "ديزل",
                "fuel_consumption": 10.5,
                "status": "متاحة",
                "last_review_date": "2026-07-15",
                "department": "المصلحة 1",
                "notes": "",
            },
            {
                "receipt_document": "REC-002",
                "vehicle_type": "حافلة",
                "brand": "Higer",
                "model": "KLQ",
                "vin": "VIN000002",
                "registration_number": "002-16-0002",
                "fuel_type": "ديزل",
                "fuel_consumption": 18.0,
                "status": "في مهمة",
                "last_review_date": "2026-07-10",
                "department": "المصلحة 2",
                "notes": "",
            },
        ]

        self.refresh_table()

    # ==================================================
    # عرض البيانات
    # ==================================================

    def refresh_table(self):

        self.table.setRowCount(0)

        for vehicle in self.vehicles:

            row = self.table.rowCount()

            self.table.insertRow(row)

            values = [
                vehicle.get("receipt_document", ""),
                vehicle.get("vehicle_type", ""),
                vehicle.get("brand", ""),
                vehicle.get("model", ""),
                vehicle.get("vin", ""),
                vehicle.get("registration_number", ""),
                vehicle.get("fuel_type", ""),
                str(vehicle.get("fuel_consumption", "")),
                vehicle.get("status", ""),
                vehicle.get("last_review_date", ""),
                vehicle.get("department", ""),
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(str(value))

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

        self.update_count()

        self.apply_filters()

    # ==================================================
    # إضافة سيارة
    # ==================================================

    def add_vehicle(self):

        dialog = VehicleDialog(self)

        if dialog.exec():

            vehicle_data = dialog.get_data()

            self.vehicles.append(
                vehicle_data
            )

            self.refresh_table()

            QMessageBox.information(
                self,
                "تم الحفظ",
                "تمت إضافة السيارة بنجاح.",
            )

    # ==================================================
    # تعديل سيارة
    # ==================================================

    def edit_vehicle(self):

        current_row = self.table.currentRow()

        if current_row < 0:

            QMessageBox.warning(
                self,
                "تنبيه",
                "اختر سيارة أولًا.",
            )

            return

        vehicle = self.get_visible_vehicle(
            current_row
        )

        if vehicle is None:

            QMessageBox.warning(
                self,
                "خطأ",
                "تعذر تحديد السيارة.",
            )

            return

        dialog = VehicleDialog(
            self,
            vehicle
        )

        if dialog.exec():

            updated_data = dialog.get_data()

            original_index = self.vehicles.index(
                vehicle
            )

            self.vehicles[
                original_index
            ] = updated_data

            self.refresh_table()

            QMessageBox.information(
                self,
                "تم التعديل",
                "تم تعديل بيانات السيارة بنجاح.",
            )

    # ==================================================
    # أرشفة سيارة
    # ==================================================

    def archive_vehicle(self):

        current_row = self.table.currentRow()

        if current_row < 0:

            QMessageBox.warning(
                self,
                "تنبيه",
                "اختر سيارة أولًا.",
            )

            return

        vehicle = self.get_visible_vehicle(
            current_row
        )

        if vehicle is None:
            return

        reply = QMessageBox.question(
            self,
            "تأكيد الأرشفة",
            "هل تريد أرشفة السيارة المحددة؟",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply == QMessageBox.Yes:

            original_index = self.vehicles.index(
                vehicle
            )

            self.vehicles.pop(
                original_index
            )

            self.refresh_table()

            QMessageBox.information(
                self,
                "تمت الأرشفة",
                "تمت أرشفة السيارة.",
            )

    # ==================================================
    # البحث والفلاتر
    # ==================================================

    def apply_filters(self):

        search_text = (
            self.search_box.text()
            .strip()
            .lower()
        )

        selected_status = (
            self.status_filter.currentText()
        )

        selected_type = (
            self.type_filter.currentText()
        )

        selected_department = (
            self.department_filter.currentText()
        )

        visible_vehicles = []

        for vehicle in self.vehicles:

            searchable_text = " ".join([
                str(vehicle.get("receipt_document", "")),
                str(vehicle.get("brand", "")),
                str(vehicle.get("model", "")),
                str(vehicle.get("vin", "")),
                str(vehicle.get("registration_number", "")),
            ]).lower()

            if (
                search_text
                and search_text not in searchable_text
            ):
                continue

            if (
                selected_status != "كل الحالات"
                and vehicle.get("status")
                != selected_status
            ):
                continue

            if (
                selected_type != "كل أنواع العتاد"
                and vehicle.get("vehicle_type")
                != selected_type
            ):
                continue

            if (
                selected_department != "كل المصالح"
                and vehicle.get("department")
                != selected_department
            ):
                continue

            visible_vehicles.append(
                vehicle
            )

        self.display_vehicles(
            visible_vehicles
        )

    # ==================================================
    # عرض السيارات بعد الفلترة
    # ==================================================

    def display_vehicles(self, vehicles):

        self.table.setRowCount(0)

        departments = set()

        for vehicle in self.vehicles:

            department = vehicle.get(
                "department",
                ""
            )

            if department:
                departments.add(
                    department
                )

        current_department = (
            self.department_filter.currentText()
        )

        self.department_filter.blockSignals(True)

        self.department_filter.clear()

        self.department_filter.addItem(
            "كل المصالح"
        )

        for department in sorted(
            departments
        ):
            self.department_filter.addItem(
                department
            )

        self.department_filter.setCurrentText(
            current_department
        )

        self.department_filter.blockSignals(
            False
        )

        for vehicle in vehicles:

            row = self.table.rowCount()

            self.table.insertRow(row)

            values = [
                vehicle.get("receipt_document", ""),
                vehicle.get("vehicle_type", ""),
                vehicle.get("brand", ""),
                vehicle.get("model", ""),
                vehicle.get("vin", ""),
                vehicle.get("registration_number", ""),
                vehicle.get("fuel_type", ""),
                str(vehicle.get("fuel_consumption", "")),
                vehicle.get("status", ""),
                vehicle.get("last_review_date", ""),
                vehicle.get("department", ""),
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(
                    str(value)
                )

                item.setTextAlignment(
                    Qt.AlignCenter
                )

                self.table.setItem(
                    row,
                    column,
                    item
                )

        self.update_count()

    # ==================================================
    # تحديد السيارة الظاهرة
    # ==================================================

    def get_visible_vehicle(self, row):

        search_text = (
            self.search_box.text()
            .strip()
            .lower()
        )

        selected_status = (
            self.status_filter.currentText()
        )

        selected_type = (
            self.type_filter.currentText()
        )

        selected_department = (
            self.department_filter.currentText()
        )

        visible_vehicles = []

        for vehicle in self.vehicles:

            searchable_text = " ".join([
                str(vehicle.get("receipt_document", "")),
                str(vehicle.get("brand", "")),
                str(vehicle.get("model", "")),
                str(vehicle.get("vin", "")),
                str(vehicle.get("registration_number", "")),
            ]).lower()

            if (
                search_text
                and search_text not in searchable_text
            ):
                continue

            if (
                selected_status != "كل الحالات"
                and vehicle.get("status")
                != selected_status
            ):
                continue

            if (
                selected_type != "كل أنواع العتاد"
                and vehicle.get("vehicle_type")
                != selected_type
            ):
                continue

            if (
                selected_department != "كل المصالح"
                and vehicle.get("department")
                != selected_department
            ):
                continue

            visible_vehicles.append(
                vehicle
            )

        if 0 <= row < len(visible_vehicles):

            return visible_vehicles[row]

        return None

    # ==================================================
    # عدد السيارات
    # ==================================================

    def update_count(self):

        count = self.table.rowCount()

        self.count_label.setText(
            f"عدد السيارات: {count}"
            )
