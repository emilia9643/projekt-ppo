import sys
from PyQt5.QtWidgets import QApplication
from mainUi import Ui

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()