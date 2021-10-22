import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QApplication, QPushButton, QLineEdit,
    QTextEdit, QHBoxLayout, QVBoxLayout, QLabel,
)

from model import Window
from QSSTool import QSSTool
from constants import MainPageConstants as mpc

class MainPage(Window):

    def __init__(self, parent = None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        super(MainPage, self).initUI()
        QSSTool.qss(self, mpc.MAINPAGE_QSS_FILE_PATH)
        self.show()

    def right_layout(self):

        vbox = QVBoxLayout()

        welcome_label = QLabel(mpc.MAINPAGE_WELCOME)
        welcome_label.setObjectName('welcome')
        vbox.addWidget(welcome_label, 0, Qt.AlignCenter | Qt.AlignVCenter)

        return vbox