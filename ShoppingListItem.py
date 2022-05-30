import threading

from PyQt5.QtCore import QSize, pyqtSignal, QEvent
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QFrame, QTextEdit, QLineEdit, QSizePolicy

from ColorPalette import ColorPalette
from IconButton import IconButton
from SqlDataBase import SqlDataBase
import smtplib


class CustomQLineEdit(QLineEdit):
    exit_signal = pyqtSignal()

    def leaveEvent(self, a0: QEvent):
        self.exit_signal.emit()
        super().leaveEvent(a0)


class CustomQTextEdit(QTextEdit):
    exit_signal = pyqtSignal()

    def leaveEvent(self, a0: QEvent):
        self.exit_signal.emit()
        super().leaveEvent(a0)


class ShoppingListItem(QFrame):
    delete_signal = pyqtSignal()

    def __init__(self, parent=None, data=None):
        super(ShoppingListItem, self).__init__(parent)

        self.sql = SqlDataBase()

        self.pannel = QFrame(self)
        self.title = CustomQLineEdit(self.pannel)
        self.content = CustomQTextEdit(self.pannel)

        self.sendButton = IconButton(self)
        self.titleButton = QLineEdit(self.sendButton)

        self.deleteButton = IconButton(self, "close.svg", None, "close_hover.svg")

        self.colorPalette = ColorPalette()
        self.data = {"id": "", "title": "", "description": "", "date_added": ""} if data is None else data
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(41, 29, 255, 725)
        self.setStyleSheet(f" background-color: {self.colorPalette.colors['secondary_color']};"
                           f" border-radius: 20")
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)

        self.pannel.setGeometry(0, 0, 255, 623)

        self.sendButton.setGeometry(0, 685, 255, 48)
        self.sendButton.setStyleSheet(f" background-color: {self.colorPalette.colors['warning_color_darker']};"
                                      f" border-radius: 10")
        self.sendButton.setText("Send")
        self.sendButton.setFont(font)
        self.sendButton.click_signal.connect(self.send_email)

        self.title.setGeometry(19, 12, 212, 39)
        self.title.setPlaceholderText("List title:")
        self.title.setText(self.data["title"])
        self.title.setFont(font)

        font.setBold(False)
        self.content.setGeometry(11, 62, 234, 651)
        self.content.setPlaceholderText("List content:")
        self.content.setText(self.data["description"])
        self.content.setFont(font)

        self.setMinimumSize(QSize(255, 725))
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)

        self.title.exit_signal.connect(self.exit_title)
        self.content.exit_signal.connect(self.exit_content)

        self.deleteButton.setGeometry(224, 6, 24, 24)
        self.deleteButton.click_signal.connect(self.onDelete)

    def exit_title(self):
        self.data["title"] = self.title.text()
        self.sql.update_item(self.data)

    def exit_content(self):
        self.data["description"] = self.content.toPlainText()
        self.sql.update_item(self.data)

    def onDelete(self):
        self.sql.delete_item(self.data)
        self.delete_signal.emit()

    def send_email(self):
        threading.Thread(target=self.onSend()).start()

    def onSend(self):
        receiver = "moisii.andreea98@gmail.com"

        message = f"""From: From Person <shoppingListApp>
        To: To Person <moisii.andreea98@gmail.com>
        Subject: {self.title.text()}

        {self.content.toPlainText()}
        """

        try:
            smtpObj = smtplib.SMTP("smtp.gmail.com", 587)
            smtpObj.ehlo()
            smtpObj.starttls()
            smtpObj.login("rebelrewards99@gmail.com", "Rewards99")
            smtpObj.sendmail("rebelrewards99@gmail.com", receiver, message)
            print("Successfully sent email")
            smtpObj.quit()
        except smtplib.SMTPException as e:
            print(e)
            print("Error: unable to send email")



