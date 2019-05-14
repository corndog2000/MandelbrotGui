import sys, random, math
import array as arrPoints
import multiprocessing
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor


xMin = -3
xMax = 3
yMin = -3
yMax = 3
zoomLevel = 4
arrPoints = []  #At the beginning set the array to be emptyc

class GuiApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 700)    #300, 190
        self.setWindowTitle('Mandelbrot')
        self.show()
        #self.showFullScreen()

    #Called whenever the window is resized or brought into focus
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        #Run the drawMandelbrot program
        self.drawMandelbrot(qp, xMin, xMax, yMin, yMax, arrPoints)
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

        #print("xMouse: ", xMouse)
        #print("yMouse: ", yMouse)
        #print("Before Map - xMin: ", xMin)
        #print("Before Map - yMin: ", yMin)
        #print("Before Map - xMax: ", xMax)
        #print("Before Map - yMax: ", yMax)

        xMouse = self.linearMap(xMouse, 0, windowWidth, xMin, xMax)
        yMouse = self.linearMap(yMouse, 0, windowHeight, yMax, yMin)

        #print("xMouse: ", xMouse)
        #print("yMouse: ", yMouse)

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
        #print("Done zooming in.")
        #print("New xMin: ", xMin)
        #print("New xMax: ", xMax)
        #print("New yMin: ", yMin)
        #print("New yMax: ", yMax)
        #print("New widthScale: ", widthScale)
        #print("New heightScale: ", heightScale)

        #print(x)
        #print(y)

    def drawMandelbrot(self, qp, arrPoints):
        size = self.size()
        
        if 0 > len(arrPoints):
            
            for Point in arrPoints:
                newW = self.linearMap(Point.x, xMin, xMax, 0, size.width() - 1)
                newH = self.linearMap(Point.y, yMin, yMax, size.height() - 1, 0)

                #Grab the color from the current Point object
                color = Point.color

                #The calculateMandelbrot will set color to -1 if the iterations are infinite else set the color based on iterations
                if color != -1:
                    qp.setPen(QColor.fromHsv(color, 255, 255))
                else:
                    qp.setPen(Qt.black)

                #draw the point on the canvas
                qp.drawPoint(newW, newH)
        else:
            qp.setPen(Qt.gray)
            qp.fillRect(size.width(), size.height())
        
class Point(object):
    def __init__(self, x=0, y=0, color=0):
        self.x = x
        self.y = y
        self.color = color

#Custom version of the range function that works with float numbers
def frange(self, start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

def linearMap(self, value, low, high, newLow, newHigh):
    return newLow + ((value - low) / (high - low)) * (newHigh - newLow)

def calculateMandelbrot(guiApp, xMin, xMax, yMin, yMax):
    size = guiApp.size()
    maxIteration = 255
    arrPoints = []  #Clear the array. This get's rid of the old data points

    widthScale = (xMax - xMin) / size.width()
    heightScale = (yMax - yMin) / size.height()

    for w in frange(xMin, xMax, widthScale):
        for h in frange(yMin, yMax, heightScale):

            x = 0
            y = 0
            iteration = 0

            while (x*x + y*y <= 4) and (iteration < maxIteration):
                xtemp = (x*x - y*y) + w
                y = ((2*x) * y) + h
                x = xtemp
                iteration += 1
        
        if iteration != maxIteration:
            #qp.setPen(QColor.fromHsv(iteration, 255, 255))
            pointToAdd = Point(x=w, y=h, color=iteration)
            arrPoints.append(pointToAdd)
        else:
            #qp.setPen(Qt.black)
            pointToAdd = Point(x=w, y=h, color=-1)
            arrPoints.append(pointToAdd)

def runMultiprocessing(self, guiApp):
    numberOfThreads = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(numberOfThreads)

    totalLength = abs(xMin) + abs(xMax)
    pieceLength = totalLength / numberOfThreads

    for i in range(numberOfThreads):
        xMinNew = xMin + (pieceLength * i)
        xMaxNew = xMin + (pieceLength * (i + 1))

        print("Process ", i, " started.")
        p = multiprocessing.Process(target=calculateMandelbrot, args=(guiApp, xMinNew, xMaxNew, yMin, yMax))
        p.start()
    
    p.join()
    guiApp.repaint()

def main():
    app = QApplication([])
    guiApp = GuiApp()
    runMultiprocessing()
    app.exec_()

if __name__ == '__main__':
    main()