
from PyQt5 import  QtCore,QtWidgets
import sys
from SnakeLogic import Ui_MainWindow

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        '''Создаем наше главное окно'''
        super(MyWindow,self).__init__()

        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)

        self.timerMove = QtCore.QBasicTimer()

        self.speed = 1200
        self.timerMove.start(self.speed, self)
        self.ui.frame.gameOverSignal.connect(self.gameOver)
        self.ui.frame.cointSignal[str].connect(self.ui.statusbar.showMessage)
        self.ui.frame.gameWinnerSignal.connect(self.gameWin)
        # Фокус на главное окно
        self.setChildrenFocusPolicy(QtCore.Qt.NoFocus)

        # Переменная остановки
        self.stop = False

        # Первоначальный счет
        self.ui.statusbar.showMessage('Coint - 0'+ ' Режим ' +str(self.ui.frame.currentMode))

    def gameOver(self):
        '''Останавливаем игру'''
        self.timerMove.stop()
        self.stop = True

    def gameWin(self):
        '''Победа'''
        self.timerMove.stop()
        self.stop = True

    def gameAgain(self):
        '''Возобновляем игру'''
        self.ui.frame.newSnake()
        self.ui.frame.Apple()
        self.stop = False
        self.timerMove.start(self.speed , self)


    def timerEvent(self, event):
        '''Чекаем время'''
        if event.timerId() == self.timerMove.timerId():
            self.ui.frame.snakeMove()
            self.update()



    def keyPressEvent(self, event):
        '''Обрабатываем нажатия'''
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
                self.gameAgain()


    def setChildrenFocusPolicy(self, policy):
        '''Фокусируем нажатие на кнопки в главном окне'''
        def recursiveSetChildFocusPolicy(parentQWidget):
            for childQWidget in parentQWidget.findChildren(QtWidgets.QWidget):
                childQWidget.setFocusPolicy(policy)
                recursiveSetChildFocusPolicy(childQWidget)

        recursiveSetChildFocusPolicy(self)

app = QtWidgets.QApplication([])
application = MyWindow()
application.show()
sys.exit(app.exec())