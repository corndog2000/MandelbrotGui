import sys, random, math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor
from multiprocessing import Process

xMin = -500
xMax = 500
yMin = -500
yMax = 500
zoomLevel = 4

class Mandelbrot(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 700)    #300, 190
        self.setWindowTitle('Julia')
        self.show()

    #Custom version of the range function that works with float numbers
    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    def linearMap(self, value, low, high, newLow, newHigh):
        return newLow + ((value - low) / (high - low)) * (newHigh - newLow)

    #Called whenever the window is resized or brought into focus
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        #Run the drawMandelbrot program
        self.drawMandelbrot(qp, xMin, xMax, yMin, yMax)
        qp.end()
    
    def mousePressEvent(self, event):
        global xMin
        global xMax
        global yMin
        global yMax
        
        size = self.size()
        windowWidth = size.width()
        windowHeight = size.height()

        xMouse = event.x()
        yMouse = event.y()

        xMouse = self.linearMap(xMouse, 0, windowWidth, xMin, xMax)
        yMouse = self.linearMap(yMouse, 0, windowHeight, yMax, yMin)

        #Make temporary variables to store the new x/y min/max so they aren't changed while the algorithms are still working
        xMinTemp = xMouse - ((xMax - xMin) / (zoomLevel * zoomLevel))
        xMaxTemp = xMouse + ((xMax - xMin) / (zoomLevel * zoomLevel))
        yMinTemp = yMouse - ((yMax - yMin) / (zoomLevel * zoomLevel))
        yMaxTemp = yMouse + ((yMax - yMin) / (zoomLevel * zoomLevel))

        xMin = xMinTemp
        xMax = xMaxTemp
        yMin = yMinTemp
        yMax = yMaxTemp

        #Update scale for the new zoomed in view
        #widthScale = widthScale / ((zoomLevel * zoomLevel) / 1.5)
        #heightScale = heightScale / ((zoomLevel * zoomLevel) / 1.5)

        widthScale = (xMax - xMin) / size.width()
        heightScale = (yMax - yMin) / size.height()

        self.repaint()

    def drawMandelbrot(self, qp, xMin, xMax, yMin, yMax):
        #Variables
        print("Started Calculations")
        size = self.size()
        maxIteration = 255
        C = -0.8
        D = 0.156
        
        widthScale = (xMax - xMin) / size.width()
        heightScale = (yMax - yMin) / size.height()

        #    widthScale = 6 / size.width()
        #    heightScale = 6 / size.height()

        for w in self.frange(xMin, xMax, widthScale):
            for h in self.frange(yMin, yMax, heightScale):

                x = (h - 32) / 100
                y = (w - 32) / 100
                iteration = 0

                while (iteration < maxIteration):
                    R = ((x * x) - (y * y)) + C
                    I = (2 * (x * y)) + D
                    
                    if (R * R > 500):
                        break
                    else:
                        x = R
                        y = I

                    iteration += 1

                if iteration != maxIteration:
                    qp.setPen(QColor.fromHsv(iteration, 255, 255))
                else:
                    qp.setPen(Qt.black)

                newW = self.linearMap(w, xMin, xMax, 0, size.width() - 1)
                newH = self.linearMap(h, yMin, yMax, size.height() - 1, 0)
                qp.drawPoint(newW, newH)


if __name__ == '__main__':
    app = QApplication([])
    ex = Mandelbrot()
    app.exec_()