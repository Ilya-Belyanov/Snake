from PyQt5 import QtCore, QtWidgets
from SnakeLogic import FormPaint
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1000, 1000)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.frame = FormPaint(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.dopFrame()

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def dopFrame(self):
        self.frameLeft = QtWidgets.QFrame(self.centralwidget)
        self.frameRight = QtWidgets.QFrame(self.centralwidget)
        self.frameRight.setObjectName("frameRight")
        self.lbModeChoice = QtWidgets.QLabel('Walls')
        self.btMode1 = QtWidgets.QPushButton('1. On')
        self.btMode2 = QtWidgets.QPushButton('2. Off')
        self.lbCharact = QtWidgets.QLabel('Characteristic \n Color')
        self.btColor = QtWidgets.QPushButton('Snake')
        self.btBorderColor = QtWidgets.QPushButton('Shadow Snake')
        self.btAppleColor = QtWidgets.QPushButton('Apple')
        self.shadow = QtWidgets.QRadioButton('State Shadow')
        self.shadow.setChecked(True)

        self.lbCount = QtWidgets.QLabel('Count of apple')
        self.lcdCount = QtWidgets.QLCDNumber()

        self.lbModeName = QtWidgets.QLabel('State Walls')
        self.lcdModeName = QtWidgets.QLCDNumber()

        self.lbStatus = QtWidgets.QLabel()

        self.vboxLeft = QtWidgets.QVBoxLayout(self.frameLeft)
        self.vboxLeft.setSpacing(5)
        self.vboxLeft.addWidget(self.lbCount)
        self.vboxLeft.addWidget(self.lcdCount)
        self.vboxLeft.addWidget(self.lbModeName)
        self.vboxLeft.addWidget(self.lcdModeName)
        self.vboxLeft.addWidget(self.lbStatus)

        self.vboxRight = QtWidgets.QVBoxLayout(self.frameRight)
        self.vboxRight.setSpacing(10)
        self.vboxRight.addWidget(self.lbModeChoice)
        self.vboxRight.addWidget(self.btMode1)
        self.vboxRight.addWidget(self.btMode2)
        self.vboxRight.addWidget(self.lbCharact)
        self.vboxRight.addWidget(self.btColor)
        self.vboxRight.addWidget(self.btBorderColor)
        self.vboxRight.addWidget(self.btAppleColor)
        self.vboxRight.addWidget(self.shadow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Snake"))