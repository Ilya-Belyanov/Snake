
from PyQt5 import  QtCore, QtGui, QtWidgets
from SnakeWindow import Ui_MainWindow

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        '''Connect main Window'''
        super(MyWindow,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.speed = 120
        self.timerMove = QtCore.QBasicTimer()
        self.timerMove.start(self.speed, self)

        self.ui.frame.gameOverSignal.connect(self.gameOver)
        self.ui.frame.gameWinnerSignal.connect(self.gameWin)
        self.ui.frame.lcdSignal.connect(self.changeLCD)
        self.ui.frame.lcdSignalMode.connect(self.changeLcdMode)
        self.ui.btMode1.clicked.connect(self.setModeOne)
        self.ui.btMode2.clicked.connect(self.setModeTwo)
        
        # First parameters
        self.ui.lcdModeName.display(self.ui.frame.currentMode)
        self.ui.lbStatus.setText('GO')

        # Focus on the main Window
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

        self.stop = False

        self.windowStyle()

    def windowStyle(self):
        self.ui.frame.setGeometry(QtCore.QRect(200, 25, 800, 800))
        self.ui.frameRight.setGeometry(QtCore.QRect(1025, 25, 100, 350))
        self.ui.frameLeft.setGeometry(QtCore.QRect(0, 25, 200, 300))

        self.ui.frame.setStyleSheet('background-color: rgb(120,120,120)')
        self.ui.frameRight.setStyleSheet('background-color: rgb(170,170,170)')
        self.ui.frameLeft.setStyleSheet('background-color: rgb(220,220,220)')
        self.ui.centralwidget.setStyleSheet('background-color: rgb(220,220,220)')
        self.ui.statusbar.setStyleSheet('background-color: rgb(200,200,200)')

        self.ui.lbModeChoice.setFont(QtGui.QFont('Lucida Bright', 7))
        self.ui.lbModeChoice.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignTop)

        self.ui.lbCount.setFont(QtGui.QFont('Lucida Bright', 7))
        self.ui.lbCount.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

        self.ui.lbModeName.setFont(QtGui.QFont('Lucida Bright', 7))
        self.ui.lbModeName.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

        self.ui.lbStatus.setFont(QtGui.QFont('Lucida Bright', 12))
        self.ui.lbStatus.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignCenter)

    def changeLcdMode(self,mode):
        self.ui.lcdModeName.display(mode)

    def changeLCD(self,count):
        self.ui.lcdCount.display(count)

    def setModeOne(self):
        self.ui.frame.currentMode = 1
        self.gameRestart()

    def setModeTwo(self):
        self.ui.frame.currentMode = 2
        self.gameRestart()

    def gameOver(self):
        self.ui.lbStatus.setText('GAME OVER...\nPress Space')
        self.timerMove.stop()
        self.stop = True

    def gameWin(self):
        self.ui.lbStatus.setText('Respect for you...\nPress Space')
        self.timerMove.stop()
        self.stop = True

    def gameRestart(self):
        self.ui.lbStatus.setText('GO')
        self.ui.frame.newSnake()
        self.ui.frame.createApple()
        self.stop = False
        self.timerMove.start(self.speed , self)


    def timerEvent(self, event):
        if event.timerId() == self.timerMove.timerId():
            self.ui.frame.snakeMove()
            self.update()


    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Up:
            self.ui.frame.changeMove(0,1)

        if key == QtCore.Qt.Key_Down:
            self.ui.frame.changeMove(0, -1)

        if key == QtCore.Qt.Key_Left:
            self.ui.frame.changeMove(-1,0)

        if key == QtCore.Qt.Key_Right:
            self.ui.frame.changeMove(1,0)

        if key == QtCore.Qt.Key_Space:
            if self.stop:
                self.gameRestart()


    def setChildrenFocusPolicy(self, policy):
        '''Focus on the main Window'''
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)

        recursiveSetChildFocusPolicy(self)

