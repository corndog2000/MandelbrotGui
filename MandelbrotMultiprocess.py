import sys, random, math, time
#import array as arrPoints
import threading
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor


xMin = -3
xMax = 3
yMin = -3
yMax = 3
zoomLevel = 4
arrPoints = []  #At the beginning set the array to be empty

class GuiApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(50, 50, 1600, 900)    #300, 190
        self.setWindowTitle('Mandelbrot')
        self.show()
        #self.showFullScreen()

    #Called whenever the window is resized or brought into focus
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        #Run the drawMandelbrot program
        self.drawMandelbrot(qp, arrPoints)
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

        xMouse = linearMap(xMouse, 0, windowWidth, xMin, xMax)
        yMouse = linearMap(yMouse, 0, windowHeight, yMax, yMin)

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

    def drawMandelbrot(self, qp, points):
        size = self.size()
        
        #print("draw mandelbrot ", len(points))
        if len(points) > 0:
            
            for Point in points:
                #print(Point)
                newW = linearMap(Point.x, xMin, xMax, 0, size.width() - 1)
                newH = linearMap(Point.y, yMin, yMax, size.height() - 1, 0)

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
            #qp.setPen(Qt.gray)
            qp.fillRect(0, 0, size.width(), size.height(), Qt.gray)
        
class Point(object):
    def __init__(self, x=0, y=0, color=0):
        self.x = x
        self.y = y
        self.color = color

#Custom version of the range function that works with float numbers
def frange(start, stop, step):
    i = start
    while i < stop:
        yield i
        i += step

def linearMap(value, low, high, newLow, newHigh):
    return newLow + ((value - low) / (high - low)) * (newHigh - newLow)

class MandelbrotCalculate(threading.Thread):
    def __init__(self, size, xMin, xMax, yMin, yMax, points, widthScale, heightScale):
        threading.Thread.__init__(self)
        self.size = size
        self.xMin = xMin
        self.xMax = xMax
        self.yMin = yMin
        self.yMax = yMax
        self.points = points
        self.widthScale = widthScale
        self.heightScale = heightScale

    def run(self):
        #size = guiApp.size()
        maxIteration = 255

        #print("xMin ", self.xMin)
        #print("xMax ", self.xMax)
        #print("yMin ", self.yMin)
        #print("yMax ", self.yMax)
        #print(widthScale)
        #print(heightScale)
        #print(size)

        for w in frange(self.xMin, self.xMax, self.widthScale):
            for h in frange(self.yMin, self.yMax, self.heightScale):

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
                    #self.points.append(pointToAdd)
                    #print("appended colered pixel. Iteration: ", iteration)
                else:
                    #qp.setPen(Qt.black)
                    pointToAdd = Point(x=w, y=h, color=-1)
                    #self.points.append(pointToAdd)
                    #print("appended black pixel")
        
        #print("mandel calc done ", len(self.points))

def runMultiprocessing(guiApp):
    size = guiApp.size()
    threadPool = []
    
    #numberOfThreads = threading.cpu_count()
    numberOfThreads = 1
    #print(numberOfThreads)

    totalLength = abs(xMin) + abs(xMax)
    pieceLength = totalLength / numberOfThreads
    #print(totalLength)
    #print(pieceLength)

    widthScale = (xMax - xMin) / size.width()
    heightScale = (yMax - yMin) / size.height()

    time1 = time.time()

    for i in range(numberOfThreads):
        #xMinNew = xMin + (pieceLength * i)
        #xMaxNew = xMin + (pieceLength * (i + 1))

        yMinNew = yMin + (pieceLength * i)
        yMaxNew = yMin + (pieceLength * (i + 1))

        #print("Thread ", i, " started.")
        #print(xMinNew)
        #print(xMaxNew)
        t = MandelbrotCalculate(guiApp.size(), xMin, xMax, yMinNew, yMaxNew, arrPoints, widthScale, heightScale)
        #calculateMandelbrot(guiApp.size(), xMinNew, xMaxNew, yMin, yMax,arrPoints)
        t.start()
        threadPool.append(t)
    
    for t in threadPool:
        t.join()
    
    time2 = time.time()
    print('computation took %0.3f ms' % ((time2-time1)*1000.0))

    guiApp.repaint()
    #print("join done ", len(arrPoints))

def main():
    app = QApplication([])
    guiApp = GuiApp()
    runMultiprocessing(guiApp)
    app.exec_()

if __name__ == '__main__':
    main()