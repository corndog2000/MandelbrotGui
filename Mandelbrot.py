import sys, random, math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QColor

class Mandelbrot(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 700, 443.33)    #300, 190
        self.setWindowTitle('Mandelbrot')
        self.show()

    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    def linearInter(self, value, low, high, newLow, newHigh):
        return ((value - low) / (high - low)) * (newHigh - newLow)

    def mousePressEvent(self, event):
        x = event.x()
        y = event.y()
        
        print(x)
        print(y)

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        #self.drawPoints(qp)
        self.drawMandelbrot(qp, 3, 3)
        qp.end()

    #Not used
    #def drawPoints(self, qp):
    #    size = self.size()

    #    for x in range(0, size.width() - 1):
    #        for y in range(0, size.height() - 1):
    #            qp.setPen(Qt.blue)
    #            qp.drawPoint(x, y)

    def drawMandelbrot(self, qp, xMinMax, yMinMax):
        #Variables
        size = self.size()
        maxIteration = 25

        for w in self.frange(-xMinMax, xMinMax, 6 / size.width()):
            for h in self.frange(-yMinMax, yMinMax, 6 / size.height()):

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
                        qp.setPen(QColor(self.linearInter(iteration, 0, 8, 0, 255), 255, 255))  #Red is based on iteration
                        #qp.setPen(Qt.red)
                    elif iteration > 8 and iteration <= 16:
                        qp.setPen(QColor(255, self.linearInter(iteration, 9, 16, 0, 255), 255))  #Green is based on iteration
                        #qp.setPen(Qt.green)
                    else:
                        qp.setPen(QColor(255, 255, self.linearInter(iteration, 17, 25, 0, 255)))  #Blue is based on iteration
                        #qp.setPen(Qt.blue)
                else:
                    qp.setPen(Qt.black)

                newW = self.linearInter(w, -3.0, 3.0, 0, size.width() - 1)
                newH = self.linearInter(h, -3.0, 3.0, 0, size.height() - 1)
                qp.drawPoint(newW, newH)

def main():
    app = QApplication([])
    ex = Mandelbrot()
    app.exec_()

if __name__ == '__main__':
    main()