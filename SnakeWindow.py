from PyQt5 import QtCore, QtWidgets
from SnakeLogic import FormPaint

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(1150, 875)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")


        self.frame = FormPaint(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
 
        self.frameLeft = QtWidgets.QFrame(self.centralwidget)
        self.frameRight = QtWidgets.QFrame(self.centralwidget)

        self.lbModeChoice = QtWidgets.QLabel('Choise Mode')
        self.btMode1 = QtWidgets.QPushButton('Mode 1')
        self.btMode2 = QtWidgets.QPushButton('Mode 2')

        self.lbCount = QtWidgets.QLabel('Count of apple')
        self.lcdCount = QtWidgets.QLCDNumber()

        self.lbModeName = QtWidgets.QLabel('Current Mode')
        self.lcdModeName = QtWidgets.QLCDNumber()

        self.lbStatus = QtWidgets.QLabel()
        
        self.vboxLeft = QtWidgets.QVBoxLayout(self.frameLeft)
        self.vboxLeft.setSpacing(5)
        self.vboxLeft.addWidget(self.lbCount)
        self.vboxLeft.addWidget(self.lcdCount)
        self.vboxLeft.addWidget(self.lbModeName)
        self.vboxLeft.addWidget(self.lcdModeName)
        self.vboxLeft.addWidget(self.lbStatus)

        self.vbox = QtWidgets.QVBoxLayout(self.frameRight)
        self.vbox.setSpacing(10)
        self.vbox.addWidget(self.lbModeChoice)
        self.vbox.addWidget(self.btMode1)
        self.vbox.addWidget(self.btMode2)

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

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Snake"))