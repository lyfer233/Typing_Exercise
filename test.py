import sys

from PyQt5.QtWidgets import QApplication

from model.MainPage import MainPage
from model.WordsExercisePage import WordsExercisePage
from slot import QueryWord

if __name__ == "__main__":
    app = QApplication(sys.argv)
    e = WordsExercisePage()
    e.show()
    print(QueryWord.from_db())
    sys.exit(app.exec_())