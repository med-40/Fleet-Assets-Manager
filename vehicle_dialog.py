from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QComboBox,
    QDoubleSpinBox,
    QDateEdit,
    QTextEdit,
    QPushButton,
    QMessageBox,
)


class VehicleDialog(QDialog):
    def __init__(self, parent=None, vehicle_data=None):
        super().__init__(parent)

        self.vehicle_data = vehicle_data or {}

        self.setWindowTitle(
            "إضافة سيارة" if not vehicle_data else "تعديل سيارة"
        )

        self.resize(650, 600)
        self.setLayoutDirection(Qt.RightToLeft)

        layout = QFormLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(12)

        # وثيقة الاستلام
        self.receipt_document = QLineEdit()
        self.receipt_document.setPlaceholderText(
            "رقم أو مرجع وثيقة الاستلام"
        )
        layout.addRow("وثيقة الاستلام:", self.receipt_document)

        # نوع العتاد
        self.vehicle_type = QComboBox()
        self.vehicle_type.addItems([
            "سيارة",
            "شاحنة",
            "حافلة",
            "مركبة أخرى",
        ])
        layout.addRow("نوع العتاد:", self.vehicle_type)

        # العلامة
        self.brand = QLineEdit()
        self.brand.setPlaceholderText("مثال: Toyota")
        layout.addRow("العلامة:", self.brand)

        # الطراز
        self.model = QLineEdit()
        self.model.setPlaceholderText("مثال: Hilux")
        layout.addRow("الطراز:", self.model)

        # رقم الهيكل ورقم التسجيل في نفس السطر
        identity_layout = QHBoxLayout()

        self.vin = QLineEdit()
        self.vin.setPlaceholderText("رقم الهيكل VIN")

        self.registration_number = QLineEdit()
        self.registration_number.setPlaceholderText(
            "رقم التسجيل"
        )

        identity_layout.addWidget(self.vin)
        identity_layout.addWidget(self.registration_number)

        layout.addRow(
            "التعريف:",
            identity_layout
        )

        # نوع الوقود
        self.fuel_type = QComboBox()
        self.fuel_type.addItems([
            "ديزل",
            "بنزين",
            "كهرباء",
            "هجين",
            "أخرى",
        ])
        layout.addRow("نوع الوقود:", self.fuel_type)

        # معدل الاستهلاك
        self.fuel_consumption = QDoubleSpinBox()
        self.fuel_consumption.setRange(0, 999.99)
        self.fuel_consumption.setDecimals(2)
        self.fuel_consumption.setSuffix(" لتر/100 كم")

        layout.addRow(
            "معدل الاستهلاك:",
            self.fuel_consumption
        )

        # الحالة
        self.status = QComboBox()
        self.status.addItems([
            "متاحة",
            "في مهمة",
            "في الصيانة",
            "متوقفة",
        ])
        layout.addRow("الحالة:", self.status)

        # تاريخ آخر مراجعة
        self.last_review_date = QDateEdit()
        self.last_review_date.setCalendarPopup(True)
        self.last_review_date.setDisplayFormat("yyyy-MM-dd")

        layout.addRow(
            "تاريخ آخر مراجعة:",
            self.last_review_date
        )

        # المصلحة
        self.department = QLineEdit()
        self.department.setPlaceholderText(
            "المصلحة أو الوحدة التابعة لها السيارة"
        )
        layout.addRow("المصلحة:", self.department)

        # الملاحظات
        self.notes = QTextEdit()
        self.notes.setPlaceholderText(
            "ملاحظات إضافية..."
        )
        self.notes.setMinimumHeight(90)

        layout.addRow("ملاحظات:", self.notes)

        # أزرار الحفظ والإلغاء
        buttons_layout = QHBoxLayout()

        save_button = QPushButton("حفظ")
        cancel_button = QPushButton("إلغاء")

        save_button.setMinimumHeight(40)
        cancel_button.setMinimumHeight(40)

        save_button.clicked.connect(self.validate_and_accept)
        cancel_button.clicked.connect(self.reject)

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        layout.addRow("", buttons_layout)

        self.setLayout(layout)

        # تحميل البيانات إذا كانت نافذة تعديل
        if vehicle_data:
            self.load_vehicle_data(vehicle_data)

    def validate_and_accept(self):
        """التحقق من البيانات قبل الحفظ."""

        if not self.receipt_document.text().strip():
            QMessageBox.warning(
                self,
                "بيانات ناقصة",
                "يرجى إدخال وثيقة الاستلام.",
            )
            self.receipt_document.setFocus()
            return

        if not self.brand.text().strip():
            QMessageBox.warning(
                self,
                "بيانات ناقصة",
                "يرجى إدخال العلامة.",
            )
            self.brand.setFocus()
            return

        if not self.model.text().strip():
            QMessageBox.warning(
                self,
                "بيانات ناقصة",
                "يرجى إدخال الطراز.",
            )
            self.model.setFocus()
            return

        if not self.vin.text().strip():
            QMessageBox.warning(
                self,
                "بيانات ناقصة",
                "يرجى إدخال رقم الهيكل.",
            )
            self.vin.setFocus()
            return

        if not self.registration_number.text().strip():
            QMessageBox.warning(
                self,
                "بيانات ناقصة",
                "يرجى إدخال رقم التسجيل.",
            )
            self.registration_number.setFocus()
            return

        self.accept()

    def get_data(self):
        """إرجاع بيانات السيارة."""

        return {
            "receipt_document":
                self.receipt_document.text().strip(),

            "vehicle_type":
                self.vehicle_type.currentText(),

            "brand":
                self.brand.text().strip(),

            "model":
                self.model.text().strip(),

            "vin":
                self.vin.text().strip(),

            "registration_number":
                self.registration_number.text().strip(),

            "fuel_type":
                self.fuel_type.currentText(),

            "fuel_consumption":
                self.fuel_consumption.value(),

            "status":
                self.status.currentText(),

            "last_review_date":
                self.last_review_date.date().toString(
                    "yyyy-MM-dd"
                ),

            "department":
                self.department.text().strip(),

            "notes":
                self.notes.toPlainText().strip(),
        }

    def load_vehicle_data(self, data):
        """تحميل بيانات سيارة موجودة للتعديل."""

        self.receipt_document.setText(
            data.get("receipt_document", "")
        )

        self.vehicle_type.setCurrentText(
            data.get("vehicle_type", "سيارة")
        )

        self.brand.setText(
            data.get("brand", "")
        )

        self.model.setText(
            data.get("model", "")
        )

        self.vin.setText(
            data.get("vin", "")
        )

        self.registration_number.setText(
            data.get("registration_number", "")
        )

        self.fuel_type.setCurrentText(
            data.get("fuel_type", "ديزل")
        )

        self.fuel_consumption.setValue(
            float(data.get("fuel_consumption", 0))
        )

        self.status.setCurrentText(
            data.get("status", "متاحة")
        )

        self.department.setText(
            data.get("department", "")
        )

        self.notes.setPlainText(
            data.get("notes", "")
      )
