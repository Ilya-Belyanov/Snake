from PyQt5 import  QtCore, QtGui, QtWidgets
from SnakeWindow import Ui_MainWindow


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        """Connect main Window"""
        super(MyWindow,self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.speed = 120
        self.timerMove = QtCore.QBasicTimer()
        self.timerMove.start(self.speed, self)

        self.timerApple = QtCore.QBasicTimer()

        self.ui.frame.gameResult.connect(self.gameResult)
        self.ui.frame.lcdSignal.connect(lambda count: self.ui.lcdCount.display(count))
        self.ui.frame.lcdSignalLenSnake.connect(lambda length: self.ui.lcdLenSnake.display(length))
        self.ui.frame.AppleTimer.connect(lambda time: self.timerApple.start(time, self))
        self.ui.btMode1.clicked.connect(lambda : self.setMode(1))
        self.ui.btMode2.clicked.connect(lambda : self.setMode(2))
        self.ui.btMode3.clicked.connect(lambda: self.setMode(3))
        self.ui.btMode4.clicked.connect(lambda: self.setMode(4))
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
        self.ui.frame.reload()

    def setSizeWindows(self,app):
        W = app.desktop().screenGeometry().width()
        H = app.desktop().screenGeometry().height()
        print(W, ' X ', H)
        mainW = int(W*0.625)
        mainH =int(H*0.720)
        indentW =int( (W/2) - (mainW/2) )
        indentH = int( (H / 2) - (mainH / 2))

        self.move(indentW, indentH)
        self.setFixedSize(mainW, mainH)
        self.ui.frameLeft.setGeometry(QtCore.QRect(0, 25, int(mainW * 0.16),int (mainH/2) ))
        self.ui.frame.setGeometry(QtCore.QRect(int(mainW*0.16), 25, int(mainW*0.60),mainH - 50))
        self.ui.frameRight.setGeometry(QtCore.QRect(int(mainW*0.16) + int(mainW*0.60) + 25, 25, int(mainW*0.2), int (mainH/2)+25))

    def loadStyleSheets(self):
         style = "static/style.css"
         with open(style, "r") as f:
             self.setStyleSheet(f.read())

    def checkStateShadow(self):
        if self.ui.shadow.isChecked():
            self.ui.frame.snake.shadowExist = True
        else:
            self.ui.frame.snake.shadowExist = False


    def showSnakeColor(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.ui.frame.snake.color = color

    def showBorderColor(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.ui.frame.snake.border = color

    def showAppleColor(self):
        color = QtWidgets.QColorDialog.getColor()

        if color.isValid():
            self.ui.frame.apple.color = color

    def setMode(self, mode):
        self.ui.frame.currentMode = mode
        self.ui.lcdModeName.display(mode)
        self.gameRestart()

    def gameResult(self, text):
        self.ui.lbStatus.setText(text)
        self.timerMove.stop()
        self.timerApple.stop()
        self.stop = True

    def gameRestart(self):
        self.ui.lbStatus.setText('GO')
        self.timerApple.stop()
        self.ui.frame.reload()
        self.stop = False
        self.timerMove.start(self.speed , self)

    def timerEvent(self, event):
        if event.timerId() == self.timerMove.timerId():
            self.ui.frame.snakeMove()
            self.update()

        if event.timerId() == self.timerApple.timerId():
            self.timerApple.stop()
            self.ui.frame.createApple()

    def keyPressEvent(self, event):
        key = event.key()
        if key == QtCore.Qt.Key_Up:
            self.ui.frame.snake.changeMove(0,1)

        if key == QtCore.Qt.Key_Down:
            self.ui.frame.snake.changeMove(0, -1)

        if key == QtCore.Qt.Key_Left:
            self.ui.frame.snake.changeMove(-1,0)

        if key == QtCore.Qt.Key_Right:
            self.ui.frame.snake.changeMove(1,0)

        if key == QtCore.Qt.Key_Space:
            if self.stop:
                self.gameRestart()


    def setChildrenFocusPolicy(self, policy):
        """Focus on the main Window"""
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)

        recursiveSetChildFocusPolicy(self)

