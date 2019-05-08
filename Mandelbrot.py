import sys, random
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class Mandelbrot(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 190)
        self.setWindowTitle('Mandelbrot')
        self.show()

    def frange(self, start, stop, step):
        i = start
        while i < stop:
            yield i
            i += step

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        #self.drawPoints(qp)
        self.drawMandelbrot(qp)
        qp.end()

    #Not used
    #def drawPoints(self, qp):
    #    size = self.size()

    #    for x in range(0, size.width() - 1):
    #        for y in range(0, size.height() - 1):
    #            qp.setPen(Qt.blue)
    #            qp.drawPoint(x, y)

    def drawMandelbrot(self, qp):
        #Variables
        size = self.size()
        maxIteration = 25

        for w in self.frange(-3.0, 3.0, 0.1):
            for h in self.frange(-3.0, 3.0, 0.1):

                x = 0
                y = 0
                iteration = 0

                while (x*x + y*y <= 4) and (iteration < maxIteration):
                    xtemp = (x*x - y*y) + w
                    y = ((2*x) * y) + h
                    x = xtemp
                    iteration += 1
                    
                if iteration != maxIteration:
                    qp.setPen(Qt.cyan)
                else:
                    qp.setPen(Qt.black)

                qp.drawPoint(w, h)

if __name__ == '__main__':
    app = QApplication([])
    ex = Mandelbrot()
    app.exec_()