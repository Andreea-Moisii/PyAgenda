from PyQt5.QtWidgets import QScrollArea, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QFrame, QLayout

from ColorPalette import ColorPalette


class ShoppingList(QScrollArea):
    def __init__(self, parent=None):
        super(ShoppingList, self).__init__(parent=parent)

        self.scrollAreaWidgetContents = QWidget()
        self.orizontalLayout = QHBoxLayout(self.scrollAreaWidgetContents)
        self.spacerItem = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(108, 24, 1309, 791)
        self.colorPalette = ColorPalette()
        self.setStyleSheet(f" background-color: {self.colorPalette.colors['primary_color']};"
                                         f" border-radius: 20")

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())

        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(1309, 791)
        self.setFrameShape(QFrame.NoFrame)
        self.setLineWidth(0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignCenter)

        self.scrollAreaWidgetContents.setGeometry(0, 0, 1309, 791)

        self.orizontalLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.orizontalLayout.setContentsMargins(30, 30, 30, 30)
        self.orizontalLayout.setSpacing(50)

        self.orizontalLayout.addSpacerItem(self.spacerItem)

        self.setWidget(self.scrollAreaWidgetContents)

    def addWidget(self, widget):
        self.orizontalLayout.removeItem(self.spacerItem)
        self.orizontalLayout.addWidget(widget)
        self.orizontalLayout.addItem(self.spacerItem)
