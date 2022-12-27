import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QHeaderView,QMessageBox
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
        self.sell_pag_bt.clicked.connect(self.new_fact)
        #Bills page
        self.updt_fact.clicked.connect(self.show_fact) 
        self.gr_sells.clicked.connect(self.show_fact_gr)
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
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Grupo no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:
                self.prodc_table.setRowCount(len(data))
                self.prodc_table.setColumnCount(len(data[0]))
                columnas=['REF.','NOMBRE','MATERIAL','PRECIO','CANTIDAD','GRUPO']
                self.prodc_table.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def show_data_ref(self):
        ref_prod = self.ref_line_sell.text().upper()
        self.producto = self.data_base.ref_inv(ref_prod)
        if len(self.producto) !=0:
            self.ref_lab_3.setText(self.producto[0][0])
            self.name_lab_3.setText(self.producto[0][1])
            self.mat_lab_2.setText(str(self.producto[0][2]))
            self.group_lab.setText(str(self.producto[0][3]))
            self.prec_line.setText(str(self.producto[0][4]))
            self.cant_lab.setText(str(self.producto[0][5]))
    
    def show_fact(self):
        data = self.data_base.show_fact()
        self.fact_table.clear()
        self.fact_table.setRowCount(len(data))
        self.fact_table.setColumnCount(len(data[0]))
        columnas=['REF.','NOMBRE','MATERIAL','GRUPO','PRECIO','CANTIDAD','VALOR_TOTAL','IVA']
        self.fact_table.setHorizontalHeaderLabels(columnas)

        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.fact_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
    def new_fact(self):
        ref = self.ref_lab_3.text().upper()
        name = self.name_lab_3.text().upper()
        mat = self.mat_lab_2.text().upper()
        gr = self.group_lab.text().upper()
        price = self.prec_line.text().upper()
        cant = self.cant_line.text().upper()
        if ref != '' and name !='' and mat != '' and gr!= '' and price!='' and cant!= '':
            self.data_base.fact_inv(ref,name,mat,gr,price,cant)
            self.ref_lab_3.clear()
            self.name_lab_3.clear()
            self.mat_lab_2.clear()
            self.group_lab.clear()
            self.prec_line.clear()
            self.cant_line.clear()
            self.cant_lab.clear()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene todos los espacios')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def show_fact_gr(self):
        group = self.group_line_sell.text().upper()
        if group !='':
            data = self.data_base.fact_group(group)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Grupo no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:
                self.fact_table.setRowCount(len(data))
                self.fact_table.setColumnCount(len(data[0]))
                columnas=['REF.','NOMBRE','MATERIAL','GRUPO','PRECIO','CANTIDAD','VALOR_TOTAL','IVA']
                self.fact_table.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.fact_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin = Employee_store()
    admin.show()
    sys.exit(app.exec_())