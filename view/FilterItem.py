from PyQt6 import QtCore
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QFrame,
    QLabel,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
)

from view.Icon import Icon


class FilterItem(QFrame):
    def __init__(self, title) -> None:
        super().__init__()
        self.horizontalLayout = QHBoxLayout(self)
        self.title = title
        self.ItemName = QLabel()
        self.ItemName.setObjectName("ItemName")
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.horizontalLayout.addWidget(self.ItemName)
        self.ItemName.setText(title)
        self.horizontalLayout.addItem(self.horizontalSpacer)
        self.applyButton = QPushButton()
        self.applyButton.setObjectName("applyButton")
        showIcon = Icon("icons/filter.svg")
        self.applyButton.setIcon(showIcon)
        self.applyButton.setIconSize(QtCore.QSize(15, 15))
        self.applyButton.setFixedSize(25, 25)
        self.horizontalLayout.addWidget(self.applyButton)
