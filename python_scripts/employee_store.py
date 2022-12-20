import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QHeaderView
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve,Qt,QPoint
from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUi
from sqlite_conection_employee import Conexion

class Employee_store(QMainWindow):
    def __init__(self):
        super(Employee_store,self).__init__()
        loadUi('employee_store.ui',self)
        #sqlite conection
        self.data_base = Conexion()
        #Attach Buttons
        self.inventory_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.inventory_pag))
        self.sell_prod_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.sell_pag))
        self.anotation_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.anotation_pag))
        self.factura_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.facturas_pag))
        #Hide minimize button
        self.minimize.hide()
        #Title control
        self.maximize.clicked.connect(self.maximized)
        self.minimize.clicked.connect(self.minimized)
        self.hide.clicked.connect(self.hided)
        self.men_bt.clicked.connect(self.move_men)
        #Move Window when pressed
        self.tit_f.mouseMoveEvent = self.moveWindow
        #Frameless window
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Iventory page set up
        self.refresh_bt.clicked.connect(self.show_inv)
        self.search_inv.clicked.connect(self.show_inv_group)
        #Sell page set up
        self.search_ref.clicked.connect(self.show_data_ref)                                
    def move_men(self): 
        if True:
            width = self.control_f.width()
            normal =0
            if width == 0:
                extend = 200
            else:
                extend = normal
            self.animate =QPropertyAnimation(self.control_f, b'minimumWidth')
            self.animate.setDuration(250)
            self.animate.setStartValue(width)
            self.animate.setEndValue(extend)
            self.animate.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animate.start()
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

    def show_inv(self):
        data = self.data_base.show_inv()
        self.prodc_table.clear()
        self.prodc_table.setRowCount(len(data))
        self.prodc_table.setColumnCount(len(data[0]))
        columnas=['REF.','NOMBRE','MATERIAL','PRECIO','CANTIDAD','GRUPO']
        self.prodc_table.setHorizontalHeaderLabels(columnas)

        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.prodc_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
    
    def show_inv_group(self):
        group = self.group_line_inv.text().upper()
        if group !='':
            data = self.data_base.group_inv(group)
            self.prodc_table.setRowCount(len(data))
            self.prodc_table.setColumnCount(len(data[0]))
            columnas=['REF.','NOMBRE','MATERIAL','PRECIO','CANTIDAD','GRUPO']
            self.prodc_table.setHorizontalHeaderLabels(columnas)

            for i, row in enumerate(data):
                for j, column in enumerate(row):
                    self.prodc_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            print(0)
    
    def show_data_ref(self):
        ref_prod = self.ref_line_sell.text().upper()
        self.producto = self.data_base.ref_inv(ref_prod)
        if len(self.producto) !=0:
            self.id = self.producto[0][0]
            self.id_updt_lab.setText(str(self.id))
            self.ref_updt_line.setText(self.producto[0][1])
            self.name_updt_line.setText(self.producto[0][2])
            self.mat_updt_line.setText(self.producto[0][3])
            self.prec_updt_line.setText(self.producto[0][4])
            self.compr_updt_line.setText(self.producto[0][5])
            self.cant_updt_line.setText(self.producto[0][7])
            self.indic_reg.setText('Producto encontrado')
        else:
            self.indic_reg.setText("No existe el producto")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin = Employee_store()
    admin.show()
    sys.exit(app.exec_())