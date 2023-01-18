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
        self.regist_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.regist_pag))
        #Hide minimize button
        self.minimize.hide()
        #Title control
        self.maximize.clicked.connect(self.maximized)
        self.minimize.clicked.connect(self.minimized)
        self.hide.clicked.connect(self.hided)
        self.clos.clicked.connect(lambda:self.close())
        self.men_bt.clicked.connect(self.move_men)
        #Move Window when pressed
        self.tit_f.mouseMoveEvent = self.moveWindow
        #Frameless window
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Iventory page set up
        self.refresh_bt.clicked.connect(self.show_inv)
        self.search_inv.clicked.connect(self.select_inv)
        #Sell page set up
        self.search_ref.clicked.connect(self.show_data_ref)  
        self.sell_pag_bt.clicked.connect(self.new_fact)
        self.strt_fact.clicked.connect(self.new_bill)
        self.close_bill.clicked.connect(self.closed_bill)
        self.sell_pag_bt.hide()
        self.close_bill.hide()
        #Bills page
        self.updt_fact.clicked.connect(self.show_fact) 
        self.gr_sells.clicked.connect(self.select_fact)
        #Anotation pag
        self.search_bt.clicked.connect(self.select_nt)
        self.note_bt.clicked.connect(self.new_note)
        #Animation for the menu button.
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
    #Title buttons control
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
    #Opens a bill, linked to back
    def new_bill (self):
        self.data_base.new_fact()
        
        msg = QMessageBox()
        msg.setWindowTitle('NUEVA FACTURA')
        msg.setText('Factura abierta')
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()
        self.close_bill.show()
        self.sell_pag_bt.show()
        self.strt_fact.hide()
    #Moves window when pressed
    def mousePressEvent(self,event):        
        self.clicked_pos = event.globalPos()

    def moveWindow(self,event):
        delt = QPoint(event.globalPos() - self.clicked_pos)
        self.move(self.x()+delt.x(),self.y()+delt.y())
        self.clicked_pos = event.globalPos()
        if self.clicked_pos.y()<=10:
            self.maximized()
    #Closes an open bill, linked to back
    def closed_bill(self):
        self.data_base.close_bill()
        msg = QMessageBox()
        msg.setWindowTitle("FACTURA CERRADA")
        msg.setText('Factura cerrada')
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()
        self.close_bill.hide()
        self.sell_pag_bt.hide()
        self.strt_fact.show()
    #Shows the complete inventory, linked to back
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
    #Filters for the showing of the inventory
    def show_inv_group(self):
        group = self.combo_line_inv.text().upper()
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
    
    def show_inv_ref(self):
        ref = self.combo_line_inv.text().upper()
        if ref !='':
            data = self.data_base.ref_inv(ref)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Referencia no encontrada')
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
    
    def show_inv_name(self):
        name = self.combo_line_inv.text().upper()
        if name !='':
            data = self.data_base.name_inv(name)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Nombre no encontrado')
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
    
    def show_inv_mat(self):
        mat = self.combo_line_inv.text().upper()
        if mat !='':
            data = self.data_base.mat_inv(mat)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Material no encontrado')
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

    def show_inv_prec(self):
        prec = self.combo_line_inv.text().upper()
        if prec !='':
            data = self.data_base.prec_inv(prec)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Material no encontrado')
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
    # Selection of the filters 
    def select_inv(self):
        option = self.combo_inv.currentText().upper()
        if option == "REFERENCIA":
            self.show_inv_ref()
        elif option == "NOMBRE":
            self.show_inv_name()
        elif option == "GRUPO":
            self.show_inv_group()
        elif option == "MATERIAL":
            self.show_inv_mat()
        elif option == "PRECIO":
            self.show_inv_prec()
    #Shows info of product before adding to the cart
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
        elif len(self.producto)==0:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Articulo no encontrado')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    # Shows the complete table of bills, sorted by items
    def show_fact(self):
        data = self.data_base.show_fact()
        self.fact_table.clear()
        self.fact_table.setRowCount(len(data))
        self.fact_table.setColumnCount(len(data[0]))
        columnas=['REF.','NOMBRE','MATERIAL','GRUPO','PRECIO','CANTIDAD','VALOR_TOTAL','IVA','FECHA','NUM_FACT']
        self.fact_table.setHorizontalHeaderLabels(columnas)

        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.fact_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
    #Inserts the info of the product selled to the Bills table.
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
    #Filters to the Bills table
    def show_fact_num(self):
        num = self.combo_line.text().upper()
        if num !='':
            data = self.data_base.fact_num_fact(num)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Numero de factura no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:
                self.fact_table.setRowCount(len(data))
                self.fact_table.setColumnCount(len(data[0]))
                columnas=['REF.','NOMBRE','MATERIAL','GRUPO','PRECIO','CANTIDAD','VALOR_TOTAL','IVA','FECHA','NUM_FACT']
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

    def show_fact_gr(self):
        gr = self.combo_line.text().upper()
        if gr != '':
            data = self.data_base.fact_gr(gr)
            if len(data)==0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Grupo no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:
                self.fact_table.setRowCount(len(data))
                self.fact_table.setColumnCount(len(data[0]))
                columnas=['REF.','NOMBRE','MATERIAL','GRUPO','PRECIO','CANTIDAD','VALOR_TOTAL','IVA','FECHA','NUM_FACT']
                self.fact_table.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.fact_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Grupo no encontrado')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def show_fact_name(self):
        name = self.combo_line.text().upper()
        if name != '':
            data = self.data_base.fact_name(name)
            if len(data)==0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Nombre no encontrado no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:
                self.fact_table.setRowCount(len(data))
                self.fact_table.setColumnCount(len(data[0]))
                columnas=['REF.','NOMBRE','MATERIAL','GRUPO','PRECIO','CANTIDAD','VALOR_TOTAL','IVA','FECHA','NUM_FACT']
                self.fact_table.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.fact_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campo vacío')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def show_fact_mat(self):
        mat = self.combo_line.text().upper()
        if mat !='':
            data = self.data_base.fact_mat(mat)
            if len(data)==0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Material no encontrado no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:
                self.fact_table.setRowCount(len(data))
                self.fact_table.setColumnCount(len(data[0]))
                columnas=['REF.','NOMBRE','MATERIAL','GRUPO','PRECIO','CANTIDAD','VALOR_TOTAL','IVA','FECHA','NUM_FACT']
                self.fact_table.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.fact_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campo vacío')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def show_fact_prec(self):
        prec = self.combo_line.text().upper()
        if prec !='':
            data = self.data_base.fact_prec(prec)
            if len(data)==0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Articulo no encontrado no encontrado no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:
                self.fact_table.setRowCount(len(data))
                self.fact_table.setColumnCount(len(data[0]))
                columnas=['REF.','NOMBRE','MATERIAL','GRUPO','PRECIO','CANTIDAD','VALOR_TOTAL','IVA','FECHA','NUM_FACT']
                self.fact_table.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.fact_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campo vacío')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    #Selection to the filters
    def select_fact(self):
        option = self.combo_fact.currentText().upper()
        if option == "GRUPO":
            self.show_fact_gr()
        elif option == "NUMERO":
            self.show_fact_num()
        elif option == 'NOMBRE':
            self.show_fact_name()
        elif option == "MATERIAL":
            self.show_fact_mat()
        elif option == "PRECIO":
            self.show_fact_prec()

    #Anotation set up.
    #Filters for notes.
    def ref_note(self):
        ref = self.combo_nt_line.text().upper()
        self.producto = self.data_base.ref_inv(ref)
        if len(self.producto) !=0:
            self.ref_nt_lab.setText(self.producto[0][0])
            self.name_nt_lab.setText(self.producto[0][1])
            self.mat_nt_lab.setText(str(self.producto[0][2]))
            self.prec_nt_lab.setText(str(self.producto[0][3]))
            self.cant_nt_lab.setText(str(self.producto[0][4]))
            self.group_nt_lab.setText(str(self.producto[0][5]))
        elif len(self.producto)==0:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Articulo no encontrado')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def name_note(self):
        name = self.combo_nt_line.text().upper()
        self.producto = self.data_base.name_inv(name)
        if len(self.producto) !=0:
            self.ref_nt_lab.setText(self.producto[0][0])
            self.name_nt_lab.setText(self.producto[0][1])
            self.mat_nt_lab.setText(str(self.producto[0][2]))
            self.prec_nt_lab.setText(str(self.producto[0][3]))
            self.cant_nt_lab.setText(str(self.producto[0][4]))
            self.group_nt_lab.setText(str(self.producto[0][5]))
        elif len(self.producto)==0:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Articulo no encontrado')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    #Selection of filters
    def select_nt(self):
        option = self.combo_nts.currentText().upper()
        if option == "NOMBRE":
            self.name_note()
        elif option == "REFERENCIA":
            self.ref_note()
    def new_note(self):
        note = self.nt_line.text()
        name = self.name_nt_lab.text()
        mat = self.mat_nt_lab.text()
        cant = self.cant_nt_lab.text()
        group = self.group_nt_lab.text()
        prec = self.prec_nt_lab.text()
        try:
            with open("Notes.txt", "a") as f:
                f.write(f"\n-.-.-.-.-.-.-.-.-.-\n Nombre: {name}\n Material: {mat}\n Grupo:{group}\n Cantidad: {cant}\nPrecio:{prec}\nNota:{note}\n-.-.-.-.-.-.-.-.-.-")
                self.ref_nt_lab.clear()
                self.name_nt_lab.clear()
                self.mat_nt_lab.clear()
                self.prec_nt_lab.clear()
                self.cant_nt_lab.clear()
                self.group_nt_lab.clear()
                self.nt_line.clear()
                msg = QMessageBox()
                msg.setWindowTitle('Exito')
                msg.setText('Anotación realizada con exito')
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()

        except FileNotFoundError:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Archivo no encontrado ó eliminado')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin = Employee_store()
    admin.show()
    sys.exit(app.exec_())