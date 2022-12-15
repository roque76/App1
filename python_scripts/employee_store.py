import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QHeaderView
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve,Qt,QPoint
from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUi

class Employee_store(QMainWindow):
    def __init__(self):
        super(Employee_store,self).__init__()
        loadUi('employee_store.ui',self)
        #Attach Buttons
        self.inventory_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.inventory_pag))
        self.sell_prod_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.sell_pag))
        self.anotation_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.anotation_pag))
        self.factura_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.facturas_pag))
        #Hide minimize button
        self.minimize.hide()
        self.maximize.clicked.connect(self.maximized)
        self.minimize.clicked.connect(self.minimized)
        self.hide.clicked.connect(self.hided)

        self.tit_f.mouseMoveEvent = self.moveWindow

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        
    def hided(self):
        self.showMinimized()

    def maximized(self):
        self.showMaximized()
        self.maximize.hide()
        self.minimize.show()
    
    def minimized (self):
        self.showNormal()
        self.minimize.hide()
        self.maximize.show()


    def mousePressEvent(self,event):        
        self.clicked_pos = event.globalPos()

    def moveWindow(self,event):
        delt = QPoint(event.globalPos() - self.clicked_pos)
        self.move(self.x()+delt.x(),self.y()+delt.y())
        self.clicked_pos = event.globalPos()
        if self.clicked_pos.y()<=10:
            self.maximized()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin = Employee_store()
    admin.show()
    sys.exit(app.exec_())