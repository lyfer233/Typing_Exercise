from PyQt5 import QtCore
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QMainWindow, QPushButton,
    QDesktopWidget, QHBoxLayout, QVBoxLayout, QAction,
    QButtonGroup, qApp, QLabel, QToolButton
)

from QSSTool import QSSTool
from model import Window
from slot import QueryWord
from constants import WordsExercisePageConstants as wepc

data_count = 0
data = ()

class WordsExercisePage(Window):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.receive_data()
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

        word = InputWord("start")
        translation = QLabel("输入start以开始")
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

    def receive_data(self):
        global data
        data = QueryWord.from_db(self.conn)

    def keyPressEvent(self, QKeyEvent) -> None:
        pass

class InputWord(QLabel):
    pos = 0
    def __init__(self, input_word):
        super().__init__()
        self.__raw_text = input_word
        self.setText("<font color=gray>{}</font>".format(input_word))
        self.setStyleSheet("font: 400 60px Cascadia Mono ExtraLight")
        self.show()

    def keyPressEvent(self, QKeyEvent):
        if str.isalpha(chr(QKeyEvent.key())):
            if chr(QKeyEvent.key()).lower() == self.__raw_text[self.pos]:
                self.correct_char()
                self.pos += 1
            else:
                self.incorrect_char(chr(QKeyEvent.key()).lower())

        if self.pos >= len(self.__raw_text):
            global data_count
            if data_count >= len(data):
                self.close()
                return
            self.pos = 0
            self.__raw_text = data[data_count][0]
            self.setText("<font color=gray>{}</font>".format(data[data_count][0]))
            data_count += 1

            # next_word(want_delete=self)


    def correct_char(self):
        self.setText(
            "<font color=green>{}</font>"
            "<font color=gray>{}</font>".format(
                self.__raw_text[0:self.pos + 1], self.__raw_text[self.pos + 1:]
            )
        )

    def incorrect_char(self, error_char):
        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.setSingleShot(True)
        self.timer.start(200)
        self.setText('<font color=green>{}</font>'
                     '<font color=red>{}</font>'
                     '<font color=gray>{}</font>'.format(
            self.__raw_text[0:self.pos], error_char,
            self.__raw_text[self.pos + 1:]
        ))
        self.pos = 0

    def refresh(self):
        self.setText("<font color=gray>{}</font>".format(self.__raw_text))