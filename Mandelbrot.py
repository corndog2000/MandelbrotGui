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
zoomLevel = 2
zoomedIn = False

class Mandelbrot(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 443.33)    #300, 190
        self.setWindowTitle('Mandelbrot')
        self.show()

        global widthScale
        global heightScale

        size = self.size()
        widthScale = 6 / size.width()
        heightScale = 6 / size.height()

    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    def linearMap(self, value, low, high, newLow, newHigh):
        return ((value - low) / (high - low)) * (newHigh - newLow)

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
        
        xMouse = self.linearMap(xMouse, -(windowWidth / 2), (windowWidth / 2), xMin, xMax)
        yMouse = self.linearMap(yMouse, -(windowHeight / 2), (windowHeight / 2), yMin, yMax)

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
        widthScale = widthScale / ((zoomLevel * zoomLevel) / 1.5)
        heightScale = heightScale / ((zoomLevel * zoomLevel) / 1.5)

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
        maxIteration = 25
        
        if zoomedIn is False:
            widthScale = 6 / size.width()
            heightScale = 6 / size.height()

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
                    
                if iteration != maxIteration:
                    if iteration <= 8:
                        qp.setPen(QColor(self.linearMap(iteration, 0, 8, 0, 255), 255, 255))  #Red is based on iteration
                        #qp.setPen(Qt.red)
                    elif iteration > 8 and iteration <= 16:
                        qp.setPen(QColor(255, self.linearMap(iteration, 9, 16, 0, 255), 255))  #Green is based on iteration
                        #qp.setPen(Qt.green)
                    else:
                        qp.setPen(QColor(255, 255, self.linearMap(iteration, 17, 25, 0, 255)))  #Blue is based on iteration
                        #qp.setPen(Qt.blue)
                else:
                    qp.setPen(Qt.black)

                newW = self.linearMap(w, xMin, xMax, 0, size.width() - 1)
                newH = self.linearMap(h, yMin, yMax, 0, size.height() - 1)
                qp.drawPoint(newW, newH)

def main():
    app = QApplication([])
    ex = Mandelbrot()
    app.exec_()

if __name__ == '__main__':
    main()