from PyQt5 import QtWidgets
from SnakeConnect import MyWindow
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()
    application.setSizeWindows(app)
    sys.exit(app.exec())