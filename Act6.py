import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFrame
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QRect

class ImageThread(QThread):
    positionChanged = pyqtSignal(int, int)
    def __init__(self, x, y, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
    
    def run(self):
        while True:
            if self.direction == 'R':
                self.x += 1
                if self.x == 650:
                    self.direction = 'L'
            elif self.direction == 'L':
                self.x -= 1
                if self.x == 0:
                    self.direction = 'R'

            if self.direction == 'D':
                self.y += 1
                if self.y == 650:
                    self.direction = 'U'
            elif self.direction == 'U':
                self.y -= 1
                if self.y ==0:
                    self.direction = 'D'

            self.positionChanged.emit(self.x, self.y)
            self.msleep(5)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('ACT6 - HILOS')
        self.setWindowIcon(QIcon(str('AppIcon.ico')))
        self.setFixedSize(800, 800)

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

        pixmap1 = QPixmap('Cora.png').scaled(200, 200)
        self.label1.setPixmap(pixmap1)

        pixmap2 = QPixmap('Eno.png').scaled(200, 200)
        self.label2.setPixmap(pixmap2)

        self.thread1 = ImageThread(0, 300, 'R')
        self.thread1.positionChanged.connect(self.UdatePosition1)
        self.thread1.start()

        self.thread2 = ImageThread(300, 0, 'D')
        self.thread2.positionChanged.connect(self.UdatePosition2)
        self.thread2.start()

    def UdatePosition1(self, x, y):
        self.label1.move(x, y)

    def UdatePosition2(self, x, y):
        self.label2.move(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())