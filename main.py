import os
import sys
import threading

import psutil as psutil
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont, QKeyEvent
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel

from AudioManager import AudioManager
from CheckButton import CheckButton
from ColorPalette import ColorPalette
from IconButton import IconButton
from ShoppingList import ShoppingList
from ShoppingListItem import ShoppingListItem
from SqlDataBase import SqlDataBase
from VoiceManager import VoiceManager
from video.VideoManager import VideoManager


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.colorPalette = ColorPalette()
        self.voicemanager = VoiceManager()
        self.voiceThread = None
        self.videomanager = VideoManager()
        self.videoThread = None
        self.audiomanager = AudioManager()

        self.dataBase = SqlDataBase()

        self.centralWidget = QWidget(self)
        self.menuWidget = QWidget(self.centralWidget)

        self.shopping_list = ShoppingList(self.centralWidget)

        self.voiceCheckButton = CheckButton(self.menuWidget, "robot_off.svg", "robot_on.svg")
        self.videoCheckButton = CheckButton(self.menuWidget, "mouse_off.svg", "mouse_on.svg")
        self.addButton = IconButton(self.menuWidget, "plus.svg", "plus_hover.svg", "plus_hover.svg")
        self.audioCheckButton = CheckButton(self.menuWidget, "sound_off.svg", "sound_on.svg")

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Agenda")
        self.resize(1447, 845)
        self.setStyleSheet(f" background-color: {self.colorPalette.colors['primary_color_dark']}; border-radius: 20")
        self.setCentralWidget(self.centralWidget)

        self.menuWidget.setGeometry(24, 26, 63, 791)
        self.menuWidget.setStyleSheet(f" background-color: {self.colorPalette.colors['primary_color']};"
                                      f" border-radius: 20")

        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.voiceCheckButton.setGeometry(13, 102, 37, 37)
        self.voiceCheckButton.setIconSize(QSize(37, 37))
        self.voiceCheckButton.sound = f"state-change_confirm-down.wav"
        self.voiceCheckButton.check_signal.connect(self.voice_check_button_clicked)

        self.videoCheckButton.setGeometry(13, 238, 37, 37)
        self.videoCheckButton.setIconSize(QSize(37, 37))
        self.videoCheckButton.sound = f"state-change_confirm-down.wav"
        self.videoCheckButton.check_signal.connect(self.video_check_button_clicked)

        self.addButton.setGeometry(13, 374, 37, 37)
        self.addButton.setIconSize(QSize(37, 37))
        self.addButton.sound = f"ui_refresh-feed.wav"
        self.addButton.click_signal.connect(self.add_button_clicked)

        self.audioCheckButton.setGeometry(13, 510, 37, 37)
        self.audioCheckButton.setIconSize(QSize(37, 37))
        self.audioCheckButton.sound = f"state-change_confirm-down.wav"
        self.audioCheckButton.check_signal.connect(self.toggle_audio)

    def toggle_audio(self, state):
        self.audiomanager.is_on = state
        if state:
            self.audiomanager.play_sound("state-change_confirm-down.wav")

    def voice_check_button_clicked(self, state):
        if state:
            self.voiceThread = threading.Thread(target=self.voicemanager.start)
            self.voiceThread.start()
        else:
            self.voicemanager.quitFlag = False

    def video_check_button_clicked(self, state):
        if state:
            self.videoThread = threading.Thread(target=self.videomanager.start)
            self.videoThread.start()
        else:
            self.videomanager.quitFlag = False

    def add_button_clicked(self):
        self.shopping_list.addNewItem(ShoppingListItem())

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        super(MainWindow, self).keyReleaseEvent(event)

        if event.key() == QtCore.Qt.Key_Q:
            print("Q")
            threading.Thread(target=self.videomanager.start).start()


def kill_proc_tree(pid, including_parent=True):
    parent = psutil.Process(pid)
    if including_parent:
        parent.kill()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    agenda = MainWindow()

    agenda.show()
    returnValue = app.exec()
    if returnValue is not None:
        kill_proc_tree(os.getpid())
        sys.exit(returnValue)
