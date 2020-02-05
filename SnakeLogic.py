from PyQt5 import  QtCore, QtGui, QtWidgets
import random
import math


class FormPaint(QtWidgets.QFrame):
    '''Central frame'''
    gameOverSignal = QtCore.pyqtSignal() # Для подтверждения проигрыша
    gameWinnerSignal = QtCore.pyqtSignal()  # Для подтверждения выигрыша
    lcdSignal = QtCore.pyqtSignal(int) # Сигнал для дисплея count
    lcdSignalMode = QtCore.pyqtSignal(int) # Сигнал о текущем моде
    def __init__(self, parent):
        '''Set Start Parameters'''
        super().__init__(parent)
        self.Width = 30
        self.Height = 30

        self.currentMode = 1
        self.startSnake = 4
        self.colorSnake = QtGui.QColor.fromRgb(0, 250, 0, 255)
        self.borderSnake = QtGui.QColor.fromRgb(0, 200,0, 255)
        self.colorApple = QtGui.QColor.fromRgb(200, 0, 0, 255)
        self.newSnake()
        self.shadowExist = True
        self.createApple()


    def newSnake (self):
        self.cointApple = 0
        self.currentDirect = (0, 1)
        self.snakeCoords = []
        x = int(self.Width/2)

        y = 1
        coord = [x,y]
        self.snakeCoords.append(coord)


        for i in range(0,self.startSnake):
            x -=1
            coord = [x, y]            
            self.snakeCoords.append(coord)
            self.lcdSignal.emit(self.cointApple)
            self.lcdSignalMode.emit(self.currentMode)


    def createApple(self):
        '''Создает яблоко'''
        while True:
            x = random.randint(0,self.Width-1)
            y = random.randint(1,self.Height)
            coords = [x,y]
            if coords not in self.snakeCoords:
                break

        self.appleCoords = coords

    def snakeMove(self):
        oldCoord = self.snakeCoords

        Newx =  oldCoord[0][0] + self.currentDirect[0]
        Newy =  oldCoord[0][1] + self.currentDirect[1]

        # Отвечает за столкновение с яблоком
        apple = 1

        if not self.checkPosition(Newx,Newy):
            self.gameOverSignal.emit()

        else:
            if self.currentMode ==2:
                if Newx <0:
                    Newx+=self.Width
                elif Newx > self.Width -1 :
                    Newx -= self.Width
                elif Newy <1:
                    Newy+=self.Height
                elif Newy > self.Height:
                    Newy -= self.Height

            if self.checkCollision(Newx, Newy):
                self.cointApple += 1
                self.lcdSignal.emit(self.cointApple)
                apple = 0

            self.snakeCoords = []
            NewCoords = [Newx,Newy]
            self.snakeCoords.append(NewCoords)

            for i in range(0,len(oldCoord)-apple):
                NewCoords = [oldCoord[i][0],oldCoord[i][1]]
                self.snakeCoords.append(NewCoords)

            if apple ==0:
                self.checkWIN()


    def checkPosition(self,Newx,Newy):
        '''Проверяем на выход за рамки и не пересекая себя же'''
        NewCoords = [Newx, Newy]
        if Newx > self.Width - 1 or Newy > self.Height or Newx < 0 or Newy < 1:
            if self.currentMode ==1:
                return False
            elif self.currentMode ==2:
                return True

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
        '''Change direction of move'''
        if len(self.snakeCoords) > 1:
            NewX = self.snakeCoords[0][0] + x
            NewY = self.snakeCoords[0][1] + y

            if self.currentMode ==2:
                if NewX <0:
                    NewX+=self.Width
                elif NewX > self.Width -1 :
                    NewX -= self.Width
                elif NewY <1:
                    NewY+=self.Height
                elif NewY > self.Height:
                    NewY -= self.Height

            if NewX == self.snakeCoords[1][0] and NewY == self.snakeCoords[1][1]:
                pass
            else:
                self.currentDirect = (x, y)

        else:
            self.currentDirect = (x, y)

    def checkWIN(self):
        if len(self.snakeCoords) == self.Width*self.Height:
            self.gameWinnerSignal.emit()
        else:
            self.createApple()

    def paintEvent(self, event):
        ''' Draw all elements'''
        qp = QtGui.QPainter()
        size = self.size()
        qp.begin(self)
        self.drawGrid(qp,size)
        self.drawSnake(qp,size)
        self.drawApple(qp,size)
        qp.end()

    def drawGrid(self,qp,size):
        color = QtGui.QColor.fromRgb(0, 0, 0, 255)
        pen = QtGui.QPen(color,0.2, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        for j in range(self.Height+1):
                y = j * (size.height() / self.Height)
                qp.drawLine(0,y,size.width(),y)

        for i in range(self.Width+1):
                x = i * (size.width() / self.Width)
                qp.drawLine(x,0,x,size.height())

        pen = QtGui.QPen(color, 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.drawRect(0,0,size.height()-1,size.width()-1)

    def drawSnake(self,qp,size):
        color = self.colorSnake
        color_2 = self.borderSnake
        pen = QtGui.QPen(color, 0.5, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        for i in self.snakeCoords:
            if self.shadowExist:
                x = i[0] * (size.width() // self.Width)
                y = (self.Height-i[1]) * (size.height() // self.Height)
                qp.fillRect(x, y , (size.width() / self.Width) , (size.height() / self.Height) ,
                        color_2)
            x = i[0] * (size.width() / self.Width)
            y = (self.Height - i[1]) * (size.height() / self.Height)
            qp.fillRect(x +1, y+1, (size.width() / self.Width) - 2, (size.height() / self.Height) - 2,
                        color)

        x = self.snakeCoords[0][0] * (size.width() / self.Width)
        y = (self.Height - self.snakeCoords[0][1]) * (size.height() / self.Height)

        color_3 = QtGui.QColor.fromRgb(0, 10, 0, 255)
        pen = QtGui.QPen(color_3, 0.5, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(color_3)

        if self.currentDirect == (0,1):
            qp.drawEllipse(x+2, y+2, 6, 6)
            qp.drawEllipse(x+ (size.width() / self.Width) - 8, y + 2, 6, 6)

        elif self.currentDirect == (0, -1):
            qp.drawEllipse(x + 2, y + (size.width() / self.Width) - 8, 6,6)
            qp.drawEllipse(x + (size.width() / self.Width) - 8, y + (size.width() / self.Width) - 8, 6, 6)

        elif self.currentDirect == (-1,0):
            qp.drawEllipse(x+2, y+2, 6, 6)
            qp.drawEllipse(x+2,y + (size.width() / self.Width) - 8, 6, 6)

        elif self.currentDirect == (1,0):
            qp.drawEllipse(x+ (size.width() / self.Width) - 8, y + 2, 6, 6)
            qp.drawEllipse(x+ (size.width() / self.Width) - 8, y + (size.width() / self.Width) - 8, 6, 6)



    def drawApple(self,qp,size):
        if len(self.snakeCoords) != self.Width * self.Height:
            color = self.colorApple
            #color_2 = QtGui.QColor.fromRgb(255, 255, 255, 255)
            pen = QtGui.QPen(color, 0.5, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.setBrush(color)

            x = self.appleCoords[0] * (size.width() / self.Width)
            y = (self.Height-self.appleCoords[1]) * (size.height() / self.Height)
            #qp.fillRect(x, y, (size.width() / self.Width), (size.height() / self.Height),
                        #color_2)
            qp.drawEllipse(x , y, (size.width() / self.Width) , (size.height() / self.Height) )



