from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)


class DashboardPage(QWidget):
    def __init__(self):
        super().__init__()

        self.setLayoutDirection(Qt.RightToLeft)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 25, 30, 25)
        main_layout.setSpacing(20)

        # عنوان الصفحة
        title = QLabel("لوحة التحكم")
        title.setStyleSheet("""
            QLabel {
                font-size: 28px;
                font-weight: bold;
            }
        """)

        subtitle = QLabel(
            "نظرة عامة على حالة الحضيرة والنشاطات الحالية"
        )
        subtitle.setStyleSheet("""
            QLabel {
                font-size: 15px;
            }
        """)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # بطاقات الإحصائيات
        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(15)

        cards_layout.addWidget(
            self.create_card("إجمالي السيارات", "0")
        )

        cards_layout.addWidget(
            self.create_card("السيارات المتاحة", "0")
        )

        cards_layout.addWidget(
            self.create_card("السيارات في مهمة", "0")
        )

        cards_layout.addWidget(
            self.create_card("السيارات في الصيانة", "0")
        )

        main_layout.addLayout(cards_layout)

        # التنبيهات
        alerts_frame = QFrame()
        alerts_frame.setFrameShape(QFrame.StyledPanel)

        alerts_layout = QVBoxLayout(alerts_frame)
        alerts_layout.setContentsMargins(20, 20, 20, 20)
        alerts_layout.setSpacing(10)

        alerts_title = QLabel("التنبيهات")
        alerts_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
        """)

        alerts_text = QLabel(
            "لا توجد تنبيهات حاليًا."
        )

        alerts_layout.addWidget(alerts_title)
        alerts_layout.addWidget(alerts_text)

        main_layout.addWidget(alerts_frame)

        # آخر النشاطات
        activity_frame = QFrame()
        activity_frame.setFrameShape(QFrame.StyledPanel)

        activity_layout = QVBoxLayout(activity_frame)
        activity_layout.setContentsMargins(20, 20, 20, 20)
        activity_layout.setSpacing(10)

        activity_title = QLabel("آخر النشاطات")
        activity_title.setStyleSheet("""
            QLabel {
                font-size: 20px;
                font-weight: bold;
            }
        """)

        activity_text = QLabel(
            "لا توجد نشاطات مسجلة بعد."
        )

        activity_layout.addWidget(activity_title)
        activity_layout.addWidget(activity_text)

        main_layout.addWidget(activity_frame)

        main_layout.addStretch()

    def create_card(self, title, value):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setMinimumHeight(120)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 15, 20, 15)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignRight)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignRight)

        value_label.setStyleSheet("""
            QLabel {
                font-size: 30px;
                font-weight: bold;
            }
        """)

        layout.addWidget(title_label)
        layout.addStretch()
        layout.addWidget(value_label)

        return card
