from PyQt5 import  QtGui

class Snake:
    def __init__(self, length):
        self.lenSnake = length
        self.color = QtGui.QColor.fromRgb(0, 250, 0, 255)
        self.border = QtGui.QColor.fromRgb(0, 200, 0, 255)
        self.shadowExist = True
        self.deleted = False

    def createNew(self, x, y):
        self.coords = []
        self.deleted = False
        self.startCoord = [x, y]
        self.coords.append(self.startCoord)
        self.currentDirect = (0, 1)
        for i in range(self.lenSnake - 1):
            x -=1
            coord = [x, y]
            self.coords.append(coord)

    def checkMinLen(self, apple):
        if self.getLen() - apple < 0:
            return False
        return True

    def move(self, apple, Newx, Newy, cut):
        if not self.deleted:
            oldCoord = self.coords
            self.coords = []
            NewCoords = [Newx, Newy]
            self.coords.append(NewCoords)
            for i in range(len(oldCoord) - apple - cut):
                NewCoords = [oldCoord[i][0], oldCoord[i][1]]
                self.coords.append(NewCoords)

    def changeMove(self, x, y):
        if len(self.coords) != 1:
            NewX = self.coords[0][0] + x
            NewY = self.coords[0][1] + y
            if NewX != self.coords[1][0] and NewY != self.coords[1][1]:
                self.currentDirect = (x, y)
        else:
            self.currentDirect = (x, y)

    def eatApple(self,Newx, Newy, coordApple):
        NewCoords = [Newx, Newy]
        if NewCoords == coordApple:
            return True
        else:
            return False

    def collision(self, coords):
        if coords in self.coords:
            return True
        return False

    def deleteMe(self):
        self.coords = []
        self.deleted = True

    def getLen(self):
        return len(self.coords)

class Apple:
    def __init__(self, coord):
        self.color = QtGui.QColor.fromRgb(200, 0, 0, 255)
        self.coords = coord

    def __str__(self):
        return "Good"

    def effect(self):
        return 0

class BadApple(Apple):
    def __init__(self, coord):
        super().__init__(coord)
        self.color = QtGui.QColor.fromRgb(0, 0, 0, 255)

    def __str__(self):
        return "Bad"

    def effect(self):
        return 2

