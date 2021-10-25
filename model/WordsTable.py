from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QLineEdit,
    QHBoxLayout, QVBoxLayout, QHeaderView, QTableWidget,
    QLabel, QMessageBox, QButtonGroup, QAbstractItemView,
    QTableView, QTableWidgetItem, QInputDialog
)
from PyQt5.QtCore import Qt

from QSSTool import QSSTool
from constants import WordsTableConstants as wtc


class TableWidget(QWidget):
    # store event signal
    delete_signal = pyqtSignal(str)
    update_signal = pyqtSignal(str, str)
    copy_signal = pyqtSignal(str)
    change_signal = pyqtSignal(str)

    def __init__(self, *args, **kwargs):

        # count: Total number of the data in the database
        # data: ten data from the database
        if kwargs.get('count') is not None:
            count = kwargs.pop('count')
        else:
            count = 0
        if kwargs.get('data') is not None:
            self.data = kwargs.pop('data')
        else:
            self.data = ()

        # When we have count, then we can calculate the total of pages
        if count and count % wtc.TABLE_DATA_SHOW_COUNT == 0:
            self.page = count // wtc.TABLE_DATA_SHOW_COUNT
        else:
            self.page = count // wtc.TABLE_DATA_SHOW_COUNT + 1

        super(TableWidget, self).__init__(*args, **kwargs)
        self.initUI()

    def initUI(self):
        self.setLayout(self.__layout())
        QSSTool.qss(self, wtc.TABLE_QSS_FILE_PATH)

    def __layout(self):
        """
        This is method different with Windows.py.
        it cover a QVBoxLayout that have table.

        :return: QVBoxLayout()
        """

        vbox = QVBoxLayout()

        # 8 * 3 table
        self.table = QTableWidget(wtc.TABLE_DEFAULT_ROW, wtc.TABLE_DEFAULT_COLUMN)
        # table header
        self.table.setHorizontalHeaderLabels(wtc.TABLE_HEADER_LIST)
        # auto resize mode to fill reminder space
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # config the height of table header
        self.table.horizontalHeader().setFixedHeight(wtc.TABLE_HEADER_HEIGHT)
        # only select one column
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        # nothing edit data
        self.table.setEditTriggers(QTableView.NoEditTriggers)
        # only column, nothing many column in time
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        for i in range(wtc.TABLE_DEFAULT_ROW):
            # config the height of column
            self.table.setRowHeight(i, wtc.TABLE_ROW_HEIGHT)

        self.data_show()

        vbox.addWidget(self.table)
        vbox.addLayout(self.page_layout())

        return vbox

    def page_layout(self):
        """
        Layout of table at the page tail and these are button about page.

        :return: QHBoxLayout()
        """

        hbox = QHBoxLayout()
        hbox.setSpacing(0)

        home_page = QPushButton("First")
        last_page = QPushButton("<Last")
        page1 = QPushButton("1")
        page2 = QPushButton("2")
        page3 = QPushButton("3")
        page4 = QPushButton("4")
        page5 = QPushButton("5")
        next_page = QPushButton("Next>")
        finally_page = QPushButton("End")
        self.total_page = QLabel("Total " + str(self.page) + " Pages")
        skip_to = QLabel("Jump to")
        self.skip_page = QLineEdit()
        skip_page_to = QLabel("Page")
        confirm = QPushButton("Confirm")

        # take these button into one group to convince operate
        self.group = QButtonGroup(self)
        btn_list = [page1, page2, page3, page4, page5]
        for b in btn_list:
            self.group.addButton(b)
            b.setCheckable(True)
            b.clicked.connect(self.changeTableContent)
        self.group.buttons()[0].setChecked(True)  # default state is 1

        btn_list += [
            home_page, last_page, finally_page, next_page,
            skip_to, confirm
        ]
        for b in btn_list:
            b.setCursor(Qt.PointingHandCursor)

        w_list = [
            home_page, last_page, page1, page2, page3, page4,
            page5, finally_page, next_page, self.total_page,
            skip_to, self.skip_page, skip_page_to, confirm
        ]

        objectname_list = [
            'home_page', 'last_page', 'page1', 'page2', 'page3',
            'page4', 'page5', 'finally_page', 'next_page', 'total_page',
            'skip_to', 'skip_page', 'skip_page_to', 'confirm'
        ]

        for w, objectname in zip(w_list, objectname_list):
            w.setObjectName(objectname)
            hbox.addWidget(w)

        # connect function and signal
        home_page.clicked.connect(self.__home_page)
        finally_page.clicked.connect(self.__finally_page)
        last_page.clicked.connect(self.__last_page)
        next_page.clicked.connect(self.__next_page)
        confirm.clicked.connect(self.__confirm_skip)

        return hbox

    def operate(self, row):

        w = QWidget()

        hbox = QHBoxLayout()
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(0)

        btn_name_list = ['Delete', 'Update', 'Copy']
        btn_click_event_list = [self.__delete, self.__update, self.__copy]

        for btn_name, btn_objname, btn_click_event in zip(btn_name_list,
                                                          btn_name_list,
                                                          btn_click_event_list):
            btn = QPushButton(btn_name)
            btn.setObjectName(btn_objname)
            btn.clicked.connect(btn_click_event)
            btn.setMinimumSize(50, 40)
            btn.setCursor(Qt.PointingHandCursor)
            btn.row = row

            hbox.addWidget(btn)

        w.setLayout(hbox)

        return w

    def __delete(self):
        """
        delete operator clicked event
        :return:
        """
        row = self.sender().row  # find which row send signal
        word = self.table.item(row, 0).text()
        self.delete_signal.emit(word)
        self.changeTableContent()

    def __update(self):
        """
        update operator clicked event
        :return:
        """
        row = self.sender().row  # find which row send signal
        word = self.table.item(row, 0).text()
        text, change_text = QInputDialog(self, 'update', 'input your update content: ',
                                         QLineEdit.Normal, "")
        if change_text and text:
            self.update_signal.emit(text, word)

        self.changeTableContent()

    def __copy(self):
        """
        Copy content into your clipboard.
        """
        row = self.sender().row
        clipboard = QApplication.clipboard()

        word = self.table.item(row, 0).text()
        translation = self.table.item(row, 1).text()
        text = word + ": " + translation

        clipboard.setText(text)
        self.copy_signal.emit(text)

    def data_show(self):
        """
        Show the data in per page.
        """

        self.table.clearContents()

        for r in range(wtc.TABLE_DATA_SHOW_COUNT):

            # if reminder the number of data less than max count, then break
            if r >= len(self.data):
                break

            word, translation = self.data[r]

            word_item = QTableWidgetItem(word)
            translation_item = QTableWidgetItem(translation)

            word_item.setTextAlignment(Qt.AlignCenter)
            translation_item.setTextAlignment(Qt.AlignCenter)

            self.table.setItem(r, 0, QTableWidgetItem(word_item))
            self.table.setItem(r, 1, QTableWidgetItem(translation))
            self.table.setCellWidget(r, 2, self.operate(r))

    def changeTableContent(self):
        """
        send signal that current content of the page table is update
        """
        btn = self.group.checkedButton()
        self.change_signal.emit(btn.text())

        self.data_show()

    def __home_page(self):
        """
        when click first button then send signal
        """

        buttons = self.group.buttons()

        for i in range(5):
            buttons[i].setText(str(i + 1))
        buttons[0].setChecked(True)

        self.changeTableContent()

    def __finally_page(self):

        total_page = self.total_page.text().split(' ')[1]
        buttons = self.group.buttons()

        if int(total_page) <= 5:
            p = range(1, 6)
        else:
            p = range(int(total_page) - 4, int(total_page) + 1)
        for i in range(5):
            buttons[i].setText(str(p[i]))
        buttons[-1].setChecked(True)

        self.changeTableContent()

    def __last_page(self):

        buttons = self.group.buttons()
        for b in buttons:
            if b.isChecked():
                page = b.text()
                index = buttons.index(b)
                break

        if page == '1':
            QMessageBox.information(self, 'tip', 'The current page is 1', QMessageBox.Yes)
            return

        if index == 0:
            p = range(int(page) - 1, int(page) + 4)

            for i in range(5):
                buttons[i].setText(str(p[i]))
            buttons[index].setChecked(True)
        else:
            buttons[index - 1].setChecked(True)

        self.changeTableContent()

    def __next_page(self):

        total_page = self.total_page.text().split(' ')[1]
        buttons = self.group.buttons()

        for b in buttons:
            if b.isChecked():
                page = b.text()
                index = buttons.index(b)
                break

        if page == total_page:
            QMessageBox.information(self, 'tip', "Have been end page", QMessageBox.Yes)
            return

        if index == 4 and int(total_page) > 5:
            p = range(int(page) - 3, int(page) + 2)
            for i in range(5):
                buttons[i].setText(str(p[i]))
            buttons[index].setChecked(True)
        else:
            buttons[index + 1].setChecked(True)

        self.changeTableContent()

    def __confirm_skip(self):

        total_page = self.total_page.text().split(' ')[1]
        buttons = self.group.buttons()

        page = self.skip_page.text()

        if not page:
            return

        self.skip_page.clear()

        if int(total_page) < int(page) or int(page) < 0:
            QMessageBox.information(self, 'tip', 'Your index is illegal', QMessageBox.Yes)
            return

        if int(page) + 5 > int(total_page):
            p = range(int(total_page) - 4, int(total_page) + 1)
            for i in range(5):
                buttons[i].setText(str(p[i]))
                if p[i] == int(page):
                    buttons[i].setChecked(True)


        else:

            p = range(int(page), int(page) + 5)

            for i in range(5):

                buttons[i].setText(str(p[i]))

                if str(p[i]) == page:
                    buttons[0].setChecked(True)

        self.changeTableContent()
