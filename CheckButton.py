from PyQt5.QtCore import pyqtSignal, Qt, QEvent
from PyQt5.QtGui import QIcon, QCursor, QMouseEvent
from PyQt5.QtWidgets import QPushButton

from AudioManager import AudioManager


class CheckButton(QPushButton):
    check_signal = pyqtSignal(bool)

    def __init__(self, container, iconUnselect=None, iconSelect=None, iconHover=None):
        super(CheckButton, self).__init__(container)
        self.settings = None

        self.iconSelect = QIcon("icons\\" + iconSelect) if iconSelect else None
        self.iconUnselect = QIcon("icons\\" + iconUnselect) if iconUnselect else None
        self.iconHover = QIcon("icons\\" + iconHover) if iconHover else None

        self.audio = AudioManager()
        self.sound = None

        self.active = False
        self.onTop = False
        self.setupUi()

    def setupUi(self):
        self.setText("")
        self.setIcon(self.iconUnselect)
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def check(self):
        if self.iconSelect:
            self.setIcon(self.iconSelect)
        self.active = True

        # play audio if found or default tap sound
        if self.sound:
            self.audio.play_sound(self.sound)


    def uncheck(self):
        if self.iconUnselect:
            self.setIcon(self.iconUnselect)
        self.active = False

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        if e.button() == Qt.LeftButton:
            if self.active:
                self.uncheck()
            else:
                self.check()
            self.check_signal.emit(self.active)

    def enterEvent(self, e: QEvent) -> None:
        self.onTop = True
        super(CheckButton, self).enterEvent(e)

    def leaveEvent(self, e: QEvent) -> None:
        self.onTop = False
        super(CheckButton, self).enterEvent(e)
