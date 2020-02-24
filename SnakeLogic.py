from PyQt5 import  QtCore, QtGui, QtWidgets
from SnakeElements import Snake, Apple, BadApple
import random

class FormPaint(QtWidgets.QFrame):
    """Central frame"""
    gameResult = QtCore.pyqtSignal(str) # Для подтверждения проигрыша или выигрыша
    lcdSignal = QtCore.pyqtSignal(int) # Сигнал для дисплея count
    lcdSignalMode = QtCore.pyqtSignal(int) # Сигнал о текущем моде
    AppleTimer = QtCore.pyqtSignal(int) # Сигнал при плохом яблоке
    lcdSignalLenSnake = QtCore.pyqtSignal(int)
    def __init__(self, parent):
        """Set Start Parameters"""
        super().__init__(parent)
        self.Width = 30
        self.Height = 30
        self.currentMode = 1
        self.snake = Snake(4)
        self.reload()

    def reload (self):
        self.cointApple = 0
        self.snake.createNew(x=int(self.Width/2), y=1)
        self.lcdSignal.emit(self.cointApple)
        self.lcdSignalMode.emit(self.currentMode)
        self.lcdSignalLenSnake.emit(self.snake.getLen())
        self.createApple()

    def createApple(self):
        """Создает яблоко"""
        coords = self.createAppleCoord()
        ap = random.randint(1,10)
        if ap <= 9:
            self.apple = Apple(coords)
        else:
            self.apple = BadApple(coords)
            self.AppleTimer.emit(3000)

    def createAppleCoord(self):
        while True:
            x = random.randint(0,self.Width-1)
            y = random.randint(1,self.Height)
            coords = [x,y]
            if not self.snake.collision(coords):
                break
        return coords

    def createGoodApple(self):
        self.apple = Apple(self.apple.coords)

    def snakeMove(self):
        Newx =  self.snake.coords[0][0] + self.snake.currentDirect[0]
        Newy =  self.snake.coords[0][1] + self.snake.currentDirect[1]
        Newx, Newy, cut = self.checkMode(Newx, Newy)
        # Отвечает за столкновение с яблоком
        __apple = 1

        if not self.checkBorder(Newx,Newy) or not self.checkCollision(Newx,Newy):
            self.gameResult.emit("GAME OVER...\nPress Space")
        else:
            if self.snake.eatApple(Newx, Newy, self.apple.coords):
                self.cointApple += 1
                self.lcdSignal.emit(self.cointApple)
                __apple = self.apple.effect()
                if not self.snake.checkMinLen(__apple):
                    self.gameResult.emit("GAME OVER...\nPress Space")
                    self.snake.deleteMe()
                self.checkWIN()
            self.snake.move(__apple, Newx, Newy, cut)
            self.lcdSignalLenSnake.emit(self.snake.getLen())

    def checkMode(self, Newx, Newy):
        cut = 0
        if self.currentMode == 2:
            Newx, Newy = self.modeTwo(Newx, Newy)
        elif self.currentMode == 3:
            cut = self.modeThree(Newx, Newy)
        return Newx, Newy, cut

    def modeTwo(self, Newx, Newy):
        if Newx < 0: Newx += self.Width
        elif Newx > self.Width - 1: Newx -= self.Width
        elif Newy < 1: Newy += self.Height
        elif Newy > self.Height: Newy -= self.Height

        return Newx, Newy

    def modeThree(self, Newx, Newy):
        if self.snake.collision([Newx, Newy]):
            return self.snake.getLen() - self.snake.coords.index([Newx, Newy])
        return 0

    def checkBorder(self, Newx, Newy):
        """Проверяем на выход за рамки и не пересекая себя же"""
        if Newx > self.Width - 1 or Newy > self.Height or Newx < 0 or Newy < 1:
            if self.currentMode ==1 or self.currentMode ==3:
                return False
        return True

    def checkCollision(self, Newx, Newy):
        NewCoords = [Newx, Newy]
        if self.snake.collision(NewCoords):
            if self.currentMode !=3:
                return False
        return True

    def checkWIN(self):
        if self.snake.getLen() == self.Width*self.Height:
            self.gameResult.emit("Respect for you...\nPress Space")
        else:
            self.createApple()

    def paintEvent(self, event):
        """ Draw all elements"""
        qp = QtGui.QPainter()
        size = self.size()
        qp.begin(self)
        self.drawGrid(qp,size)
        if not self.snake.deleted:
            self.drawSnake(qp, size)
            self.drawEyes(qp, size)
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

    def drawSnake(self,qp,size):
        color = self.snake.color
        color_2 = self.snake.border
        pen = QtGui.QPen(color, 0.5, QtCore.Qt.SolidLine)
        qp.setPen(pen)

        for i in self.snake.coords:
            if self.snake.shadowExist:
                x = i[0] * (size.width() // self.Width)
                y = (self.Height-i[1]) * (size.height() // self.Height)
                qp.fillRect(x, y , (size.width() / self.Width) , (size.height() / self.Height) ,
                        color_2)
            x = i[0] * (size.width() / self.Width)
            y = (self.Height - i[1]) * (size.height() / self.Height)
            qp.fillRect(x +1, y+1, (size.width() / self.Width) - 2, (size.height() / self.Height) - 2,
                        color)


    def drawEyes(self,qp, size):
        color = QtGui.QColor.fromRgb(0, 10, 0, 255)
        pen = QtGui.QPen(color, 0.5, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        qp.setBrush(color)

        x = self.snake.coords[0][0] * (size.width() / self.Width)
        y = (self.Height - self.snake.coords[0][1]) * (size.height() / self.Height)

        if self.snake.currentDirect == (0,1):
            qp.drawEllipse(x+2, y+2, 6, 6)
            qp.drawEllipse(x+ (size.width() / self.Width) - 8, y + 2, 6, 6)

        elif self.snake.currentDirect == (0, -1):
            qp.drawEllipse(x + 2, y + (size.width() / self.Width) - 8, 6,6)
            qp.drawEllipse(x + (size.width() / self.Width) - 8, y + (size.width() / self.Width) - 8, 6, 6)

        elif self.snake.currentDirect == (-1,0):
            qp.drawEllipse(x+2, y+2, 6, 6)
            qp.drawEllipse(x+2,y + (size.width() / self.Width) - 8, 6, 6)

        elif self.snake.currentDirect == (1,0):
            qp.drawEllipse(x+ (size.width() / self.Width) - 8, y + 2, 6, 6)
            qp.drawEllipse(x+ (size.width() / self.Width) - 8, y + (size.width() / self.Width) - 8, 6, 6)



    def drawApple(self,qp,size):
        if self.snake.getLen() != self.Width*self.Height:
            color = self.apple.color
            pen = QtGui.QPen(color, 0.5, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.setBrush(color)

            x = self.apple.coords[0] * (size.width() / self.Width)
            y = (self.Height-self.apple.coords[1]) * (size.height() / self.Height)
            qp.drawEllipse(x , y, (size.width() / self.Width) , (size.height() / self.Height) )



