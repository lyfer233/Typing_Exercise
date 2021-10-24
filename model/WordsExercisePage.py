from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (
    QHBoxLayout, QVBoxLayout, QLabel, QToolButton, QTableWidget, QTableWidgetItem, QGridLayout
)

from QSSTool import QSSTool
from model import Window
from slot import QueryWord
from constants import WordsExercisePageConstants as wepc

data_count = 0
data = ()


class WordsExercisePage(Window):

    __timer = 0
    __input_number = 0
    __speed = 0
    __correct = 0
    __accuracy = 0
    __calc = QTimer()
    sum_str_len = []

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.receive_data()
        self.__calc.timeout.connect(self.calc_data)
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

    def word_show(self):
        self.word_area = QVBoxLayout()

        self.word = InputWord("start")
        self.word.setObjectName("inputword")
        self.word.setAlignment(Qt.AlignCenter)
        self.translation = QLabel('input "start" to start')
        self.translation.setObjectName("translation")
        self.translation.setAlignment(Qt.AlignCenter)
        self.word_area.addStretch()
        self.word_area.addWidget(self.word)
        self.word_area.addSpacing(20)
        self.word_area.addWidget(self.translation)
        self.word_area.addStretch()

        return self.word_area

    def statistic_information(self):
        self.grid = QGridLayout()
        names = ['time', 'input number', 'speed', 'correct', 'accuracy',]
        positions = [(0, i) for i in range(5)]

        for positions, name in zip(positions, names):
            label = QLabel(name)
            self.grid.addWidget(label, *positions)

        self.update_grid_data()
        return self.grid

    def right_layout(self):
        vbox = QVBoxLayout()

        vbox.addLayout(self.top_bar())
        vbox.addLayout(self.word_show())
        vbox.addLayout(self.statistic_information())

        # divide these into 1/6, 1/2, 1/3 size
        vbox.setStretch(1, 2)
        vbox.setStretch(2, 1)
        vbox.setStretch(3, 2)

        return vbox

    def change_btn_state(self):
        global data_count
        if self.start_and_stop_btn.isChecked():
            self.start_and_stop_btn.setIcon(QIcon(wepc.WORDS_EXERCISE_PAGE_QSS_FILE_START_ICON_PATH))
            self.start_and_stop_btn.setChecked(True)
            self.__calc.start(wepc.TIME_INTERVAL)
            self.word.recovery_status()
            self.grabKeyboard()
        else:
            self.start_and_stop_btn.setIcon(QIcon(wepc.WORDS_EXERCISE_PAGE_QSS_FILE_PAUSE_ICON_PATH))
            self.start_and_stop_btn.setChecked(False)
            self.__calc.stop()
            self.word.save_status()
            self.releaseKeyboard()

    def receive_data(self):
        global data
        data = QueryWord.from_db(self.conn)
        self.sum_str_len.append(0)
        for i in range(len(data)):
            self.sum_str_len.append(self.sum_str_len[i] + len(data[i][0]))

    def keyPressEvent(self, QKeyEvent) -> None:
        self.__input_number += 1
        self.word.receive_key(QKeyEvent.key(), translation=self.translation, my_timer=self.__calc)

    def calc_data(self):
        self.__timer += wepc.TIME_INTERVAL
        self.__correct += self.sum_str_len[data_count]
        self.__accuracy = self.__correct / self.__input_number
        self.__speed = self.__correct / (self.__timer / 1000)

    def update_grid_data(self):
        self.grid.addWidget(QLabel("{}s".format(self.__timer // 1000)), 1, 0)
        self.grid.addWidget(QLabel(str(self.__input_number)), 1, 1)
        self.grid.addWidget(QLabel(str(self.__speed)), 1, 2)
        self.grid.addWidget(QLabel(str(self.__correct)), 1, 3)
        self.grid.addWidget(QLabel(str(self.__accuracy)), 1, 4)


class InputWord(QLabel):
    pos = 0
    tmp_text = ""

    def __init__(self, input_word):
        super().__init__()
        self.__raw_text = input_word
        self.setText("<font color=gray>{}</font>".format(input_word))
        self.setStyleSheet("font: 400 80px Cascadia Mono ExtraLight")
        self.show()

    def receive_key(self, key, translation, my_timer):
        if 65 <= key <= 90 or 97 <= key <= 122:
            if chr(key).lower() == self.__raw_text[self.pos]:
                self.correct_char()
                self.pos += 1
            else:
                self.incorrect_char(chr(key).lower())
        else:
            return

        if self.pos >= len(self.__raw_text):
            if not my_timer.isActive():
                my_timer.start(wepc.TIME_INTERVAL)
            global data_count
            if data_count >= len(data):
                self.close()
                return
            self.pos = 0
            self.__raw_text = data[data_count][0]
            self.setText("<font color=gray>{}</font>".format(data[data_count][0]))
            translation.setText(data[data_count][1])
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

    def save_status(self):
        self.tmp_text = self.text()
        self.setText("")
        self.setPixmap(QPixmap(wepc.WORDS_EXERCISE_PAGE_QSS_FILE_CURTAIN_ICON_PATH))

    def recovery_status(self):
        print(self.tmp_text)
        self.setText(self.tmp_text)
