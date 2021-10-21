import sys

from PyQt5.QtWidgets import QApplication

from model.MainPage import MainPage

if __name__ == "__main__":
    app = QApplication(sys.argv)
    e = MainPage()
    e.show()
    sys.exit(app.exec_())