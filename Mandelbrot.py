import sys, random, math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor

xMin = -3
xMax = 3
yMin = -3
yMax = 3
widthScale = 3
heightScale = 3
zoomLevel = 4
zoomedIn = False

class Mandelbrot(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 700)    #300, 190
        self.setWindowTitle('Mandelbrot')
        self.show()

        global widthScale
        global heightScale

        size = self.size()
        widthScale = (xMax - xMin) / size.width()
        heightScale = (yMax - yMin) / size.height()

    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    def linearMap(self, value, low, high, newLow, newHigh):
        return newLow + ((value - low) / (high - low)) * (newHigh - newLow)

    def mousePressEvent(self, event):
        global xMin
        global xMax
        global yMin
        global yMax
        global widthScale
        global heightScale
        global zoomedIn

        zoomedIn = True
        
        size = self.size()
        windowWidth = size.width()
        windowHeight = size.height()

        xMouse = event.x()
        yMouse = event.y()

        print("xMouse: ", xMouse)
        print("yMouse: ", yMouse)
        # print("Before Map - xMin: ", xMin)
        # print("Before Map - yMin: ", yMin)
        # print("Before Map - xMax: ", xMax)
        # print("Before Map - yMax: ", yMax)

        xMouse = self.linearMap(xMouse, 0, windowWidth, xMin, xMax)
        yMouse = self.linearMap(yMouse, 0, windowHeight, yMax, yMin)

        print("xMouse: ", xMouse)
        print("yMouse: ", yMouse)

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
        print("Done zooming in.")
        print("New xMin: ", xMin)
        print("New xMax: ", xMax)
        print("New yMin: ", yMin)
        print("New yMax: ", yMax)
        print("New widthScale: ", widthScale)
        print("New heightScale: ", heightScale)

        #print(x)
        #print(y)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        #self.drawPoints(qp)
        #Run the draw program
        self.drawMandelbrot(qp, xMin, xMax, yMin, yMax, widthScale, heightScale)
        qp.end()

    def drawMandelbrot(self, qp, xMin, xMax, yMin, yMax, widthScale, heightScale):
        #Variables
        size = self.size()
        maxIteration = 100
        
        #if zoomedIn is False:
        widthScale = (xMax - xMin) / size.width()
        heightScale = (yMax - yMin) / size.height()


        #    widthScale = 6 / size.width()
        #    heightScale = 6 / size.height()

        for w in self.frange(xMin, xMax, widthScale):
            for h in self.frange(yMin, yMax, heightScale):

                x = 0
                y = 0
                iteration = 0

                while (x*x + y*y <= 4) and (iteration < maxIteration):
                    xtemp = (x*x - y*y) + w
                    y = ((2*x) * y) + h
                    x = xtemp
                    iteration += 1
                '''    
                if iteration != maxIteration:
                    if iteration <= 33:
                        qp.setPen(QColor(self.linearMap(iteration, 0, 33, 0, 255), 255, 255))  #Red is based on iteration
                        #qp.setPen(Qt.red)
                    elif iteration > 33 and iteration <= 66:
                        qp.setPen(QColor(255, self.linearMap(iteration, 33, 66, 0, 255), 255))  #Green is based on iteration
                        #qp.setPen(Qt.green)
                    else:
                        qp.setPen(QColor(255, 255, self.linearMap(iteration, 67, maxIteration, 0, 255)))  #Blue is based on iteration
                        #qp.setPen(Qt.blue)
                else:
                    qp.setPen(Qt.black)
                '''

                if iteration != maxIteration:
                    qp.setPen(QColor.fromHsv(self.linearMap(iteration, 0, 100, 0, 255), 255, 255))
                else:
                    qp.setPen(Qt.black)

                newW = self.linearMap(w, xMin, xMax, 0, size.width() - 1)
                newH = self.linearMap(h, yMin, yMax, size.height() - 1, 0)
                qp.drawPoint(newW, newH)

def main():
    app = QApplication([])
    ex = Mandelbrot()
    app.exec_()

if __name__ == '__main__':
    main()