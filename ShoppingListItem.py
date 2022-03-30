from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QTextEdit, QLineEdit, QSizePolicy

from ColorPalette import ColorPalette


class ShoppingListItem(QFrame):

    def __init__(self, parent = None):
        super(ShoppingListItem, self).__init__(parent)
        self.title = QLineEdit(self)
        self.content = QTextEdit(self)

        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(41, 29, 255, 725)
        self.colorPalette = ColorPalette()
        self.setStyleSheet(f" background-color: {self.colorPalette.colors['secondary_color']};"
                           f" border-radius: 20")

        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.title.setGeometry(19, 12, 212, 39)
        self.title.setPlaceholderText("List title:")
        self.title.setFont(font)

        font.setBold(False)
        self.content.setGeometry(11, 62, 234, 651)
        self.content.setPlaceholderText("List content:")
        self.content.setFont(font)

        self.setMinimumSize(QSize(255, 725))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)