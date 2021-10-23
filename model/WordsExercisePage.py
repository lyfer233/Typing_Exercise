from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton,
    QDesktopWidget, QHBoxLayout, QVBoxLayout, QAction,
    QButtonGroup, qApp, QLabel, QToolButton
)

from QSSTool import QSSTool
from model import Window
from constants import WordsExercisePageConstants as wepc

class WordsExercisePage(Window):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.initUI()

    def initUI(self):
        super(WordsExercisePage, self).initUI()
        QSSTool.qss(self, wepc.WORDS_EXERCISE_PAGE_QSS_FILE_PATH)
        self.show()

    def top_bar(self):
        hbox = QHBoxLayout()

        self.start_and_stop_btn = QToolButton()
        self.start_and_stop_btn.setIcon(QIcon(wepc.WORDS_EXERCISE_PAGE_QSS_FILE_PAUSE_ICON_PATH))
        self.setObjectName('start_and_stop_btn')
        self.start_and_stop_btn.setCheckable(True)
        self.start_and_stop_btn.setChecked(True)
        self.start_and_stop_btn.setIconSize(QtCore.QSize(60, 60))
        self.start_and_stop_btn.clicked.connect(self.change_btn_state)

        hbox.addStretch()
        hbox.addWidget(self.start_and_stop_btn)
        hbox.addStretch()

        return hbox

    def stop_show(self):
        ...

    def word_show(self):
        vbox = QVBoxLayout()

        word = QLabel("ADD")
        translation = QLabel("加")
        vbox.addStretch()
        vbox.addWidget(word)
        vbox.addWidget(translation)
        vbox.addStretch()

        return vbox

    def statistic_information(self):
        hbox = QHBoxLayout()

        hbox.addWidget(QLabel("PlaceHolder"))

        return hbox


    def right_layout(self):
        vbox = QVBoxLayout()

        vbox.addLayout(self.top_bar())
        vbox.addLayout(self.word_show())
        vbox.addLayout(self.statistic_information())

        # divide these into 1/6, 1/2, 1/3 size
        # vbox.setStretch(1, 1)
        # vbox.setStretch(2, 3)
        # vbox.setStretch(3, 2)

        return vbox

    def change_btn_state(self):
        if self.start_and_stop_btn.isChecked():
            self.start_and_stop_btn.setIcon(QIcon(wepc.WORDS_EXERCISE_PAGE_QSS_FILE_START_ICON_PATH))
            self.start_and_stop_btn.setChecked(True)
        else:
            self.start_and_stop_btn.setIcon(QIcon(wepc.WORDS_EXERCISE_PAGE_QSS_FILE_PAUSE_ICON_PATH))
            self.start_and_stop_btn.setChecked(False)
