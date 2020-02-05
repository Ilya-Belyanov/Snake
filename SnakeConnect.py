
from PyQt5 import  QtCore, QtGui, QtWidgets
from SnakeWindow import Ui_MainWindow
import sys

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        '''Connect main Window'''
        super(MyWindow,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        #screen = QtWidgets.QApplication(sys.argv)
        #print(screen.desktop().screenGeometry().width(),' X ',screen.desktop().screenGeometry().height())
        self.speed = 120
        self.timerMove = QtCore.QBasicTimer()
        self.timerMove.start(self.speed, self)

        self.ui.frame.gameOverSignal.connect(self.gameOver)
        self.ui.frame.gameWinnerSignal.connect(self.gameWin)
        self.ui.frame.lcdSignal.connect(self.changeLCD)
        self.ui.frame.lcdSignalMode.connect(self.changeLcdMode)
        self.ui.btMode1.clicked.connect(self.setModeOne)
        self.ui.btMode2.clicked.connect(self.setModeTwo)
        self.ui.btColor.clicked.connect(self.showSnakeColor)
        self.ui.btBorderColor.clicked.connect(self.showBorderColor)
        self.ui.btAppleColor.clicked.connect(self.showAppleColor)
        self.ui.shadow.toggled.connect(self.checkStateShadow)
        
        # First parameters
        self.ui.lcdModeName.display(self.ui.frame.currentMode)
        self.ui.lbStatus.setText('GO')

        # Focus on the main Window
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

        self.stop = False

        self.loadStyleSheets()

    def setSizeWindows(self,app):
        W = app.desktop().screenGeometry().width()
        H = app.desktop().screenGeometry().height()
        print(W, ' X ', H)
        mainW = int(W*0.625)
        mainH =int(H*0.720)
        indentW =int( (W/2) - (mainW/2) )
        indentH = int((H / 2) - (mainH / 2))

        self.move(indentW, indentH)
        self.setFixedSize(mainW, mainH)
        self.ui.frameLeft.setGeometry(QtCore.QRect(0, 25, int(mainW * 0.16),int (mainH/2) - 50))
        self.ui.frame.setGeometry(QtCore.QRect(int(mainW*0.16), 25, int(mainW*0.60),mainH - 50))
        self.ui.frameRight.setGeometry(QtCore.QRect(int(mainW*0.16) + int(mainW*0.60) + 25, 25, int(mainW*0.2), int (mainH/2)))

    def loadStyleSheets(self):
         style = "static/style.css"
         with open(style, "r") as f:
             self.setStyleSheet(f.read())

    def checkStateShadow(self):
        if self.ui.shadow.isChecked():
            self.ui.frame.shadowExist = True
        else:
            self.ui.frame.shadowExist = False


    def showSnakeColor(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.ui.frame.colorSnake = color

    def showBorderColor(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.ui.frame.borderSnake = color

    def showAppleColor(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.ui.frame.colorApple = color

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

