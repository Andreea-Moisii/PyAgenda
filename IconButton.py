import os

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QIcon, QCursor
from PyQt5.QtWidgets import QLabel, QPushButton

from AudioManager import AudioManager
from ColorPalette import ColorPalette


class IconButton(QPushButton):
    click_signal = pyqtSignal()

    def __init__(self, parent, iconUnClicked=None, iconClicked=None, iconHover=None):
        super(IconButton, self).__init__(parent)
        self.clickedIcon = None
        self.unClickedIcon = None
        self.hoverIcon = None


        self.audio = AudioManager()
        self.sound = None

        self.colorPalette = ColorPalette()

        if iconClicked:
            self.clickedIcon = QIcon("Icons\\" + iconClicked)

        if iconUnClicked:
            self.unClickedIcon = QIcon("Icons\\" + iconUnClicked)
        if iconHover:
            self.hoverIcon = QIcon("Icons\\" + iconHover)

        self.onTop = False
        self.setupUi()

    def setupUi(self):
        self.setText("")
        if self.unClickedIcon:
            self.setIcon(self.unClickedIcon)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mousePressEvent(self, e):
        super(IconButton, self).mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            if self.sound:
                self.audio.play_sound(self.sound)
            else:
                self.audio.play_sound("navigation_hover-tap.wav")
            if self.clickedIcon:
                self.setIcon(self.clickedIcon)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.onTop:
                if self.hoverIcon:
                    self.setIcon(self.hoverIcon)
            else:
                if self.unClickedIcon:
                    self.setIcon(self.unClickedIcon)
            self.click_signal.emit()

    def enterEvent(self, e):
        super(IconButton, self).enterEvent(e)
        self.onTop = True
        if self.hoverIcon:
            self.setIcon(self.hoverIcon)
        self.setStyleSheet(f"background-color: {self.colorPalette.colors['accent_color_darker']}; "
                        f"border-radius: 15")


    def leaveEvent(self, e):
        super(IconButton, self).enterEvent(e)
        self.onTop = False
        if self.unClickedIcon:
            self.setIcon(self.unClickedIcon)
        self.setStyleSheet(f"background-color: {self.colorPalette.colors['primary_color']}; "
                        f"border-radius: 15")