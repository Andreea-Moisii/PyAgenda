import os
import sys
import threading

import psutil as psutil
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QLabel

from ColorPalette import ColorPalette
from IconButton import IconButton
from ShoppingList import ShoppingList
from ShoppingListItem import ShoppingListItem
from VoiceManager import VoiceManager


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.colorPalette = ColorPalette()
        self.voice = VoiceManager()
        self.vThread = threading.Thread(target=self.voice.start)
        self.vThread.start()

        self.centralWidget = QWidget(self)
        self.menuWidget = QWidget(self.centralWidget)

        self.shopping_list = ShoppingList(self.centralWidget)

        # self.contentWidget = QWidget()
        # self.titleWidget = QWidget(self.contentWidget)
        # self.taskWidget = QWidget(self.contentWidget)
        self.list1Widget = ShoppingListItem()
        self.list2Widget = ShoppingListItem()
        self.list3Widget = ShoppingListItem()
        self.list4Widget = ShoppingListItem()

        self.shopping_list.addWidget(self.list1Widget)
        self.shopping_list.addWidget(self.list2Widget)
        self.shopping_list.addWidget(self.list3Widget)
        self.shopping_list.addWidget(self.list4Widget)

        self.searchWidget = IconButton(self.menuWidget, "search.png", "search_selected.png", "search_selected.png")
        self.listWidget = IconButton(self.menuWidget, "list.png", "list_selected.png", "list_selected.png")
        self.agendaWidget = IconButton(self.menuWidget, "agenda.png", "agenda_selected.png", "agenda_selected.png")
        self.recorderWidget = IconButton(self.menuWidget, "recorder.png", "recorder_selected.png", "recorder_selected.png")
        self.settingsWidget = IconButton(self.menuWidget, "settings.png", "settings_selected.png", "settings_selected.png")

        # self.titleLabel = QLabel(self.titleWidget)
        # self.tasksLabel = QLabel(self.taskWidget)

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

        # self.titleWidget.setGeometry(27, 61, 1255, 95)
        # self.titleWidget.setStyleSheet(f" background-color: {self.colorPalette.colors['secondary_color']};"
        #                                f" border-radius: 10")
        # self.titleLabel.setGeometry(33, 22, 95, 52)
        # self.titleLabel.setText("Title :")
        # self.titleLabel.setFont(font)
        #
        # self.taskWidget.setGeometry(27, 198, 1255, 565)
        # self.taskWidget.setStyleSheet(f" background-color: {self.colorPalette.colors['secondary_color']};"
        #                               f" border-radius: 10")
        # self.tasksLabel.setGeometry(28, 27, 99, 39)
        # self.tasksLabel.setText("Tasks :")
        # self.tasksLabel.setFont(font)


        self.searchWidget.setGeometry(13, 102, 37, 37)
        self.searchWidget.setIconSize(QSize(37, 37))
        self.searchWidget.sound = f"ui_tap-variant-01.wav"

        self.listWidget.setGeometry(13, 238, 37, 37)
        self.listWidget.setIconSize(QSize(37, 37))
        self.listWidget.sound = f"ui_unlock.wav"

        self.agendaWidget.setGeometry(13, 374, 37, 37)
        self.agendaWidget.setIconSize(QSize(37, 37))
        self.agendaWidget.sound = f"ui_refresh-feed.wav"

        self.recorderWidget.setGeometry(13, 510, 37, 37)
        self.recorderWidget.setIconSize(QSize(37, 37))
        self.listWidget.sound = f"state-change_confirm-down.wav"

        self.settingsWidget.setGeometry(13, 646, 37, 37)
        self.settingsWidget.setIconSize(QSize(37, 37))
        self.settingsWidget.sound = f"alert_error-03.wav"

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