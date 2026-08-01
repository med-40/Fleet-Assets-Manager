from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QGridLayout,
    QVBoxLayout,
    QFrame,
)


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setLayoutDirection(Qt.RightToLeft)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # عنوان Dashboard
        title = QLabel("لوحة التحكم")
        title.setAlignment(Qt.AlignRight)
        title.setStyleSheet("""
            font-size: 30px;
            font-weight: bold;
            padding: 10px;
        """)

        subtitle = QLabel(
            "نظرة عامة على حالة الحضيرة"
        )
        subtitle.setAlignment(Qt.AlignRight)
        subtitle.setStyleSheet("""
            font-size: 16px;
            padding: 5px 10px 15px 10px;
        """)

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # شبكة البطاقات
        cards_layout = QGridLayout()
        cards_layout.setSpacing(18)

        cards = [
            ("🚗", "السيارات والعتاد", "0"),
            ("🚙", "السيارات في مهمة", "0"),
            ("🔧", "الصيانة المستحقة", "0"),
            ("⛽", "استهلاك الوقود", "0"),
            ("🪪", "رخص السير القريبة من الانتهاء", "0"),
            ("🛠️", "الأعطال والإصلاحات", "0"),
            ("🔋", "البطاريات", "0"),
            ("🛞", "الإطارات", "0"),
        ]

        for index, (icon, name, value) in enumerate(cards):

            card = self.create_card(icon, name, value)

            row = index // 4
            column = index % 4

            cards_layout.addWidget(card, row, column)

        main_layout.addLayout(cards_layout)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def create_card(self, icon, name, value):

        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)

        card.setMinimumHeight(150)

        card.setStyleSheet("""
            QFrame {
                border: 1px solid #cccccc;
                border-radius: 12px;
                background-color: #f7f7f7;
            }

            QLabel {
                border: none;
                background: transparent;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)

        icon_label = QLabel(icon)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("""
            font-size: 30px;
        """)

        name_label = QLabel(name)
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
        """)

        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
        """)

        layout.addWidget(icon_label)
        layout.addWidget(name_label)
        layout.addWidget(value_label)

        card.setLayout(layout)

        return card
