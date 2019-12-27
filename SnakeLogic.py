from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget
import random


class FormPaint(QtWidgets.QFrame):
    '''Окно отображения'''
    gameOverSignal = QtCore.pyqtSignal() # Для подтверждения проигрыша
    gameWinnerSignal = QtCore.pyqtSignal()  # Для подтверждения выигрыша
    cointSignal = QtCore.pyqtSignal(str) # Для отправки счета
    def __init__(self, parent):
        '''Задает начальные параметры'''
        super().__init__(parent)
        self.Width = 30
        self.Height = 30

        self.newSnake()
        self.Apple()


    def newSnake(self):
        '''Новая змея'''
        self.cointApple = 0
        self.currentDirect = (0, 1)
        self.snakeCoords = []
        x = int(self.Width/2)

        y = 1
        coord = [x,y]
        self.snakeCoords.append(coord)


        for i in range(0,4):
            x -=1
            coord = [x, y]

            self.snakeCoords.append(coord)
        self.cointSignal.emit('Coint - ' + str(self.cointApple))


    def Apple(self):
        '''Создает яблоко'''
        while True:
            x = random.randint(0,self.Width-1)
            y = random.randint(1,self.Height)
            coords = [x,y]
            if coords not in self.snakeCoords:
                break

        self.appleCoords = coords

    def snakeMove(self):
        '''Движение змеи'''

        oldCoord = self.snakeCoords

        Newx =  oldCoord[0][0] + self.currentDirect[0]
        Newy =  oldCoord[0][1] + self.currentDirect[1]

        # Отвечает за столкновение с яблоком
        apple = 1

        if not self.checkPosition(Newx,Newy):
            self.gameOverSignal.emit()
            self.cointSignal.emit('GAMEOVER Press Space for return')
        else:
            if self.checkCollision(Newx, Newy):
                self.cointApple+=1
                self.cointSignal.emit('Coint - '+str(self.cointApple))
                apple = 0
                self.Apple()

            self.snakeCoords = []
            NewCoords = [Newx,Newy]
            self.snakeCoords.append(NewCoords)

            for i in range(0,len(oldCoord)-apple):
                NewCoords = [oldCoord[i][0],oldCoord[i][1]]
                self.snakeCoords.append(NewCoords)

        #Проверяем на победу
        self.checkWIN()

    def checkPosition(self,Newx,Newy):
        '''Проверяем на выход за рамки и не пересекая себя же'''
        NewCoords = [Newx, Newy]
        if Newx > self.Width - 1 or Newy > self.Height or Newx < 0 or Newy < 1:
            return False

        elif NewCoords in self.snakeCoords:
            return False

        else:
            return True

    def checkCollision(self,Newx,Newy):
        '''Проверяет на столкновение с яблоком'''
        NewCoords = [Newx, Newy]

        if NewCoords == self.appleCoords:
            return True
        else:
            return False

    def changeMove(self,x,y):
        '''Меняем направление'''
        if self.currentDirect[0] != -x or self.currentDirect[1] != -y:
            self.currentDirect = (x, y)

    def checkWIN(self):
        '''Проверяем на выигрыш'''
        if len(self.snakeCoords) == self.Width*self.Height:
            self.gameWinnerSignal.emit()
            self.cointSignal.emit('WIN!!! Respect For you. Press Space for return')
    def paintEvent(self, event):
        ''' Рисуем все элементы'''
        qp = QtGui.QPainter()
        size = self.size()
        qp.begin(self)
        self.drawGrid(qp,size)
        self.drawSnake(qp,size)
        self.drawApple(qp,size)
        qp.end()

    def drawGrid(self,qp,size):
        ''' Рисуем сетку'''
        color = QtGui.QColor.fromRgb(0, 0, 0, 255)
        pen = QtGui.QPen(color,0.1, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        for j in range(self.Height+1):
                y = j * (size.height() / self.Height)
                qp.drawLine(0,y,size.width(),y)

        for i in range(self.Width+1):
                x = i * (size.width() / self.Width)
                qp.drawLine(x,0,x,size.height())

    def drawSnake(self,qp,size):
        '''Рисуем змею'''
        color = QtGui.QColor.fromRgb(0, 0, 0, 255)
        pen = QtGui.QPen(color, 0.5, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        for i in self.snakeCoords:
            x = i[0] * (size.width() / self.Width)
            y = (self.Height-i[1]) * (size.height() / self.Height)
            qp.fillRect(x +1, y+1, (size.width() / self.Width) - 2, (size.height() / self.Height) - 2,
                        color)

    def drawApple(self,qp,size):
        '''Рисуем яблоко'''
        color = QtGui.QColor.fromRgb(100, 0, 0, 255)
        pen = QtGui.QPen(color, 0.5, QtCore.Qt.SolidLine)
        qp.setPen(pen)


        x = self.appleCoords[0] * (size.width() / self.Width)
        y = (self.Height-self.appleCoords[1]) * (size.height() / self.Height)
        qp.fillRect(x +1, y+1, (size.width() / self.Width) - 2, (size.height() / self.Height) - 2,
                        color)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.frame = FormPaint(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

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
        MainWindow.setWindowTitle(_translate("MainWindow", "Etching"))

