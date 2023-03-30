import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QThread, pyqtSignal

class ImageThread(QThread):
    positionChanged = pyqtSignal(int, int)
    def __init__(self, x, y, direction):
        super().__init__()
        self.x = x
        self.y = y
        self.direction = direction
    
    def run(self):
        while True:
#           SI LA DIRECCION RECIBIDA ES R=RIGHT ENTONCES VA AVANZANDO HASTA LLEGAR AL MIMITE DE LA VENTANA
            if self.direction == 'R':
                self.x += 1
#               AL LLEGAR AL LIMITE DE LA VENTANA CAMBIA EL ATRIBUTO A L=LEFT Y CAMBIA DE DIRECCION EL MOVIMIENTO
                if self.x == 650:
                    self.direction = 'L'
#           Y AHORA CON LA NUEVA DIRECCION DE MOVIMIENTO AVANZA EN DIRECCION CONTRARIA HASTA LLEGAR AL ORIGEN
            elif self.direction == 'L':
                self.x -= 1
#               AL LLEGAR AL ORIGEN VUELVE A CAMBIAR LA DIRECCION DEL MOVIMIENTO
                if self.x == 0:
                    self.direction = 'R'

#           HACEMOS LO MISMO QUE ARRIBA SOLO QUE AHORA CON LAS POSICIONES EN VERTICAL ARRIBA Y ABAJO RESPECTIVAMENTE 
            if self.direction == 'D':
                self.y += 1
                if self.y == 650:
                    self.direction = 'U'
            elif self.direction == 'U':
                self.y -= 1
                if self.y ==0:
                    self.direction = 'D'

#           SE REGRESA EN CADA PASO LA NUEVA POSICION Y SE APLICA UN SLEEP DE UN MILISEGUNDO
            self.positionChanged.emit(self.x, self.y)
            self.msleep(1)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

#       DECLARACION DE LA VENTANA PRINCIPAL
        self.setWindowTitle('ACT6 - HILOS')
        self.setWindowIcon(QIcon(str('AppIcon.ico')))
        self.setFixedSize(800, 800)

#       DECLARACION DE 2 LABELS QUE CONTENDRAN LAS IMAGENES
        self.label1 = QLabel(self)
        self.label2 = QLabel(self)

#       SE DECLARAN LAS 2 IMAGENES Y SE LE ASIGNAN A LOS LABELS
        pixmap1 = QPixmap('Cora.png').scaled(200, 200)
        self.label1.setPixmap(pixmap1)

        pixmap2 = QPixmap('Eno.png').scaled(200, 200)
        self.label2.setPixmap(pixmap2)

#       SE DECLARAN LOS 2 HILOS DEL TIPO CLASE imagethread     
        self.thread1 = ImageThread(0, 300, 'R')
        self.thread1.positionChanged.connect(self.UdatePosition1)
        self.thread1.start()

        self.thread2 = ImageThread(300, 0, 'D')
        self.thread2.positionChanged.connect(self.UdatePosition2)
        self.thread2.start()

#   CON LAS NUEVAS POSICIONES RECIBIDAS SE REALIZA EL MOVIMIENTO EN CADA LABEL/IMAGEN
    def UdatePosition1(self, x, y):
        self.label1.move(x, y)

    def UdatePosition2(self, x, y):
        self.label2.move(x, y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())