import sys

from PyQt5.QtWidgets import QApplication

from model.MainPage import MainPage
from model.WordsExercisePage import WordsExercisePage
from model.WordsTable import TableWidget
from slot import QueryWord

if __name__ == "__main__":
    app = QApplication(sys.argv)
    e = TableWidget()
    e.show()
    sys.exit(app.exec_())