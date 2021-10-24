import sqlite3

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget, QMainWindow, QPushButton,
    QDesktopWidget, QHBoxLayout, QVBoxLayout, QButtonGroup, QMessageBox
)

from QSSTool import QSSTool
from constants import WindowConstants as wc


class Window(QMainWindow):
    # TODO(lyfer): Adding the Window class comment

    # pages switch signal
    main_page_signal = pyqtSignal()
    words_exercise_page = pyqtSignal()
    words_table_page = pyqtSignal()
    articles_exercise_page = pyqtSignal()
    pk_page = pyqtSignal()
    your_log_page = pyqtSignal()

    conn = sqlite3.connect(wc.WORDLIST_PATH)

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

    def initUI(self):
        """
        Configure your window UI

        :return: None
        """
        self.center()
        self.__layout()
        QSSTool.qss(self, wc.WINDOW_QSS_FILE_PATH)
        self.setWindowTitle(wc.WINDOW_TITLE)
        self.setWindowIcon(QIcon(wc.WINDOW_ICON_PATH))

    def center(self):
        """
        Take the windows into your center of screen

        :return: None
        """

        self.resize(wc.WINDOW_WIDTH, wc.WINDOW_HEIGHT)

        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()

        self.move(
            (screen.width() - size.width()) / 2,
            (screen.height() - size.height()) / 2,
        )

    def left_layout(self):
        """
        Main Window left bar layout

        :return: QVBoxLayout
        """
        btn_name_list = ['Main', 'Words Exercise', 'Words Table','Articles Exercise', 'PK', 'Your Log']
        btn_click_event_list = [
            self.__main_page, self.__words_exercise_page, self.__articles_exercise_page,
            self.__words_table_page, self.__pk_page, self.__your_log_page,
        ]

        vbox = QVBoxLayout()
        self.left_button_group = QButtonGroup()

        for name, btn_click_event in zip(btn_name_list, btn_click_event_list):
            now_button = QPushButton(name)
            now_button.setCursor(Qt.PointingHandCursor)  # take your shape of cursor from pointer to hand
            now_button.setObjectName('left_btn')  # set button id
            now_button.setChecked(True)
            now_button.clicked.connect(btn_click_event)

            self.left_button_group.addButton(now_button)
            vbox.addWidget(now_button)

        self.left_button_group.buttons()[0].setChecked(True)

        return vbox

    def right_layout(self):
        """
        Override the method by the child window

        :return: QVBoxLayout()
        """

        vbox = QVBoxLayout()
        return vbox

    def __layout(self):
        """
        Merge left and right layouts and set details

        :return: None
        """
        widget = QWidget()
        self.setCentralWidget(widget)

        vbox_left = self.left_layout()
        vbox_right = self.right_layout()

        hbox = QHBoxLayout()
        hbox.addLayout(vbox_left)
        hbox.addLayout(vbox_right)

        # left space is 1/8, right space is 7/8
        hbox.setStretch(1, 1)
        hbox.setStretch(2, 7)

        widget.setLayout(hbox)

    def closeEvent(self, event) -> None:
        reply = QMessageBox.question(self,
                                     'Exit',
                                     'Your app will exit, are you sure?',
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    '''
    These are signal function area
    '''

    def __main_page(self):  # send the main page signal
        self.main_page_signal.emit()

    def __words_exercise_page(self):  # send words exercise page signal
        self.words_exercise_page.emit()

    def __words_table_page(self): # send words table page signal
        self.words_table_page.emit()

    def __articles_exercise_page(self):  # send articles exercise page signal
        self.articles_exercise_page.emit()

    def __pk_page(self):  # send pk page signal
        self.pk_page.emit()

    def __your_log_page(self):  # send log page signal
        self.your_log_page.emit()

    def __del__(self):
        self.conn.close()
