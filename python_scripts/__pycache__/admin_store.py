import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QHeaderView,QMessageBox
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve,Qt,QPoint
from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUi
from sqlite_conection import Conect

class Admin_store(QMainWindow):
    def __init__(self):
        super(Admin_store,self).__init__()
        loadUi('admin_store.ui',self)
        #Comunicación con db
        self.men_bt.clicked.connect(self.move_men)
        self.data_base = Conect()

        #Hide Minimize button
        self.minimize.hide()
        #conncect buttons from pages
        #Show elements from inventario
        self.refresh_bt.clicked.connect(self.show_products)
        #Show elements from facturas
        self.refresh_fact.clicked.connect(self.show_facts)
        #Show elements from condensado
        self.refresh_cond.clicked.connect(self.show_condensado)
        #Modify page setup
        self.updte_bt.clicked.connect(self.modify_products)
        self.search_bt.clicked.connect(self.search_name_updt)
        self.reg_pag_bt.clicked.connect(self.register_products)
        #Control for deletion page
        self.search_del_bt.clicked.connect(self.select_deletion)
        self.pagdel_bt.clicked.connect(self.delete_products)
        self.del_show.clicked.connect(self.show_del_prod)
        #Control title bar
        self.maximize.clicked.connect(self.maximized)
        self.minimize.clicked.connect(self.minimized)
        self.clos.clicked.connect(lambda:self.close())
        self.hide.clicked.connect(self.hided)
        #Opacity hide title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Move UI
        self.tit_f.mouseMoveEvent = self.move_window
        #Control frame attatchement
        #Selection page
        self.base_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.select_pag))
        #Registration of product
        self.regist_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.regist_pag))
        #Update pag
        self.updt_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.updat_pag))
        self.delete_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.delet_pag))
      
        #Set selection page
        self.base_bt_2.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.base_pag))
        self.fact_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.fact_pag))
        self.condens_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.pag_cone))
      
        #Search for base combo box in Inevtario table
        self.search_db.clicked.connect(self.election_db)
        #Search for bills in combo box In Facturas table
        self.search_fact.clicked.connect(self.election_fact)
        #Search options in cond
        self.search_cond.clicked.connect(self.select_cond)


    
    
    def hided(self):
        self.showMinimized()
    def minimized(self):
        self.showNormal()
        self.minimize.hide()
        self.maximize.show()
    def maximized(self):
        self.showMaximized()
        self.maximize.hide()
        self.minimize.show()
    
    def mousePressEvent(self, event):
        self.clicked_pos = event.globalPos()

    def move_window (self, event):  
        delt = QPoint(event.globalPos() - self.clicked_pos)
        self.move(self.x()+delt.x(),self.y()+delt.y())
        self.clicked_pos = event.globalPos()
        if self.clicked_pos.y()<=10:
            self.maximized()
        
    
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

    def show_products(self):
        data = self.data_base.show_inv()
        self.prodc_table.clear()
        self.prodc_table.setRowCount(len(data))
        self.prodc_table.setColumnCount(len(data[0]))
        columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
        self.prodc_table.setHorizontalHeaderLabels(columnas)

        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.prodc_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))

    def show_facts(self):
        data = self.data_base.show_fact()
        self.prodc_table_3.setRowCount(len(data))
        self.prodc_table_3.setColumnCount(len(data[0]))
        
        for i, row in enumerate(data):
            for j,column in enumerate(row):
                self.prodc_table_3.setItem(i,j, QtWidgets.QTableWidgetItem(str(column)))

    def show_condensado(self):
        data = self.data_base.show_cond()
        self.cond_table.setRowCount(len(data))
        self.cond_table.setColumnCount(len(data[0]))
        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.cond_table.setItem(i,j, QtWidgets.QTableWidgetItem(str(column)))
    
    
    def register_products(self):
        ref = self.ref_line.text().upper()
        name = self.name_line.text().upper()
        mat = self.mat_line.text().upper()
        cantidad = self.cant_line.text().upper()
        prec = self.prec_line.text().upper()
        compra = self.compr_line.text().upper()
        group = self.group_line.text().upper()

        if ref != ''and name!=''and mat!='' and cantidad!= ''and prec!=''and compra!=''and group!='':
            self.data_base.register(ref,name,mat,cantidad,prec,compra,group)
            self.compr_line.clear()
            self.name_line.clear()
            self.mat_line.clear()
            self.cant_line.clear()
            self.ref_line.clear()
            self.prec_line.clear()
            self.group_line.clear()
            msg = QMessageBox()
            msg.setWindowTitle('Exito')
            msg.setText('Producto registrado con exito')
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()    
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campos Vacios')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()    
    def search_name_updt(self):
        name_prod = self.name_sear_line.text().upper()
        self.producto = self.data_base.search(name_prod)
        if len(self.producto) !=0:
            self.id = self.producto[0][0]
            self.id_updt_lab.setText(str(self.id))
            self.ref_updt_line.setText(self.producto[0][1])
            self.name_updt_line.setText(self.producto[0][2])
            self.mat_updt_line.setText(self.producto[0][3])
            self.prec_updt_line.setText(str(self.producto[0][4]))
            self.compr_updt_line.setText(str(self.producto[0][5]))
            self.cant_updt_line.setText(str(self.producto[0][7]))
            self.gr_updt_line.setText(str(self.producto[0][8]))
            self.indic_upd.setText('Producto encontrado')
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Producto no encontrado')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
        
    def modify_products(self):
        name_prod = self.name_sear_line.text().upper()
        if name_prod !="":
            self.producto = self.data_base.search(name_prod)
            if self.producto!= '':
                id_=self.id_updt_lab.text().upper()
                ref = self.ref_updt_line.text().upper()
                name = self.name_updt_line.text().upper()
                mat = self.mat_updt_line.text().upper()
                cantidad = self.cant_updt_line.text().upper()
                prec = self.prec_updt_line.text().upper()
                compra = self.compr_updt_line.text().upper()
                grupo = self.gr_updt_line.text().upper()
                action = self.data_base.update(id_,ref,name,mat,prec,compra,cantidad,grupo)
            

            if action ==1:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Producto Actualizado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
                self.ref_line.clear()
                self.name_line.clear()
                self.mat_line.clear()
                self.cant_line.clear()
                self.prec_line.clear()
                self.compr_line.clear()
                self.name_sear_line.setText("")
                self.id_updt_lab.setText("")
            
            elif action == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Producto no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campos Vacios')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
        
    def del_name(self):
        name_del = self.nam_sear_del_line.text().upper()
        
        if name_del!='':
            data = self.data_base.name_db(name_del)

            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Producto no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
                    
            else:
                self.del_table_prod.setRowCount(len(data))
                self.del_table_prod.setColumnCount(len(data[0]))
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
                self.del_table_prod.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.del_table_prod.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campo Vacio')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def show_del_prod(self):
        data = self.data_base.show_inv()
        # tablerow=0
        self.del_table_prod.clear()
        self.del_table_prod.setRowCount(len(data))
        self.del_table_prod.setColumnCount(len(data[0]))
        columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
        self.del_table_prod.setHorizontalHeaderLabels(columnas)

        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.del_table_prod.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))

    def del_ref(self):
        ref_del=self.nam_sear_del_line.text().upper()

        if ref_del!="":
            data = self.data_base.ref_db(ref_del)

            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Producto no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
                    
            else:
                self.del_table_prod.setRowCount(len(data))
                self.del_table_prod.setColumnCount(len(data[0]))
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
                self.del_table_prod.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.del_table_prod.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campo Vacio')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def del_mat(self):
        mat_del =self.nam_sear_del_line.text().upper()
        if mat_del!="":
            data = self.data_base.mat_db(mat_del)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Producto no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
                    
            else:
                self.del_table_prod.setRowCount(len(data))
                self.del_table_prod.setColumnCount(len(data[0]))
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
                self.del_table_prod.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.del_table_prod.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campo Vacio')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def del_prec(self):
        prec_del = self.nam_sear_del_line.text().upper()
        if prec_del!="":
            data = self.data_base.prec_db(prec_del)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Producto no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
                    
            else:
                self.del_table_prod.setRowCount(len(data))
                self.del_table_prod.setColumnCount(len(data[0]))
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
                self.del_table_prod.setHorizontalHeaderLabels(columnas)

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.del_table_prod.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Campo Vacio')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def delete_products(self):
        row = self.del_table_prod.currentRow()
        item  = self.del_table_prod.item(row,2)
        data = item.text()
        
        if row >= 0:
            self.del_table_prod.removeRow(row)
            self.data_base.delete(data)
            self.nam_sear_del_line.setText('')
            msg = QMessageBox()
            msg.setWindowTitle('Exito')
            msg.setText('Producto eliminado con exito')
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def select_deletion(self):
        option = self.comboBox.currentText()
        if option == "NOMBRE":
            self.del_name()
        elif option == "REFERENCIA":
            self.del_ref()
        elif option == "MATERIAL":  
            self.del_mat()
        elif option == "PRECIO":
            self.del_prec()
    
    def gr_datab(self):
        group = self.combo_line.text().upper()

        if group!='':
            data = self.data_base.gr_db(group)
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
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
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

    def ref_datab(self):
        ref = self.combo_line.text().upper()

        if ref!='':
            data = self.data_base.ref_db(ref)
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
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
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
    
    def name_datab(self):
        name = self.combo_line.text().upper()

        if name!='':
            data = self.data_base.name_db(name)
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
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
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
    
    def mat_datab(self):
        mat = self.combo_line.text().upper()

        if mat!='':
            data = self.data_base.mat_db(mat)
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
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
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
    
    def buyed_datab(self):
        buyed = self.combo_line.text().upper()

        if buyed!='':
            data = self.data_base.buyed_db(buyed)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Precio de compra no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table.setRowCount(len(data))
                self.prodc_table.setColumnCount(len(data[0]))
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
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
    
    def utils_datab(self):
        utils = self.combo_line.text().upper()

        if utils!='':
            data = self.data_base.utils_db(utils)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Utilidad no encontrada')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table.setRowCount(len(data))
                self.prodc_table.setColumnCount(len(data[0]))
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
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
    
    def cant_datab(self):
        cant = self.combo_line.text().upper()

        if cant!='':
            data = self.data_base.cant_db(cant)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Cantidad no encontrada')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table.setRowCount(len(data))
                self.prodc_table.setColumnCount(len(data[0]))
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
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
    
    def prec_datab(self):
        prec = self.combo_line.text().upper()

        if prec!='':
            data = self.data_base.prec_db(prec)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Precio no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table.setRowCount(len(data))
                self.prodc_table.setColumnCount(len(data[0]))
                columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
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
        
    def election_db(self):
        option = self.combo.currentText()

        if option == "GRUPO":
            self.gr_datab()
        elif option == "NOMBRE":
            self.name_datab()
        elif option == "PRECIO":
            self.prec_datab()
        elif option == "REFERENCIA":
            self.ref_datab()
        elif option == "CANTIDAD":
            self.cant_datab()
        elif option == "UTILIDAD":
            self.utils_datab()
        elif option == "MATERIAL":
            self.mat_datab()
        elif option == "PRECIO DE COMPRA":
            self.buyed_datab()
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Opcion invalida')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
            
    
    def election_fact(self):
        option = self.combo_3.currentText()

        if option == "ID":
            self.Id_fact()
        elif option == "REF":
            self.Ref_fact()
        elif option == "NOMBRE":
            self.Name_fact()
        elif option == "MATERIAL":
            self.Mat_fact()
        elif option == "GRUPO":
            self.Group_fact()
        elif option == "PRECIO VENTA":
            self.Price_fact()
        elif option == "CANTIDAD":
            self.Cant_fact()
        elif option == "VALOR TOTAL":
            self.Tot_fact()
        elif option == "IVA":
            self.Iva_fact()
        elif option == "NUM_FACT":
            self.Num_fact()
        elif option == "FECHA":
            self.Date_fact()
        elif option == "TIEMPO":
            self.Time_fact()
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Opcion invalida')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Id_fact(self):
        ids= self.combo_line_3.text().upper()

        if ids!='':
            data = self.data_base.id_fact(ids)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('ID no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Ref_fact(self):
        ref= self.combo_line_3.text().upper()

        if ref!='':
            data = self.data_base.ref_fact(ref)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Referencia no encontrada')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Name_fact(self):
        name= self.combo_line_3.text().upper()

        if name!='':
            data = self.data_base.name_fact(name)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Nombre no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Mat_fact(self):
        mat= self.combo_line_3.text().upper()

        if mat!='':
            data = self.data_base.mat_fact(mat)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Material no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def Group_fact(self):
        gr= self.combo_line_3.text().upper()

        if gr!='':
            data = self.data_base.group_fact(gr)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Grupo no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Price_fact(self):
        price= self.combo_line_3.text().upper()

        if price!='':
            data = self.data_base.price_fact(price)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Grupo no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def Cant_fact(self):
        cant= self.combo_line_3.text().upper()

        if cant!='':
            data = self.data_base.cant_fact(cant)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Cantidad no encontrada')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Tot_fact(self):
        tot= self.combo_line_3.text().upper()

        if tot!='':
            data = self.data_base.tot_fact(tot)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Valor total no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Iva_fact(self):
        iva= self.combo_line_3.text().upper()

        if iva!='':
            data = self.data_base.iva_fact(iva)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Valor de iva no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Num_fact(self):
        num= self.combo_line_3.text().upper()

        if num!='':
            data = self.data_base.num_fact(num)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Numero de factura no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Date_fact(self):
        date= self.combo_line_3.text().upper()

        if date!='':
            data = self.data_base.date_fact(date)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Fecha no encontrada')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def Time_fact(self):
        time= self.combo_line_3.text().upper()

        if time!='':
            data = self.data_base.time_fact(time)
            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Tiempo no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
            else:

                self.prodc_table_3.setRowCount(len(data))
                self.prodc_table_3.setColumnCount(len(data[0]))

                for i, row in enumerate(data):
                    for j, column in enumerate(row):
                        self.prodc_table_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def id_cond(self):
        id = self.combo_line_4.text().upper()

        if id!="":
            data = self.data_base.id_cond(id)
            if len(data)==0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("ID no encontrada")
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x= msg.exec_()
            else:
                self.cond_table.setRowCount(len(data))
                self.cond_table.setColumnCount(len(data[0]))
                
                for i,row in enumerate(data):
                    for j,column in enumerate(row):
                        self.cond_table.setItem(i,j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()

    def valtot_cond(self):
        val = self.combo_line_4.text().upper()

        if val!="":
            data = self.data_base.valtot_connd(val)
            if len(data)==0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Valor no encontrado")
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x= msg.exec_()
            else:
                self.cond_table.setRowCount(len(data))
                self.cond_table.setColumnCount(len(data[0]))
                
                for i,row in enumerate(data):
                    for j,column in enumerate(row):
                        self.cond_table.setItem(i,j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def numfact_cond(self):
        num = self.combo_line_4.text().upper()

        if num!="":
            data = self.data_base.numfact_cond(num)
            if len(data)==0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Numero no encontrado")
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x= msg.exec_()
            else:
                self.cond_table.setRowCount(len(data))
                self.cond_table.setColumnCount(len(data[0]))
                
                for i,row in enumerate(data):
                    for j,column in enumerate(row):
                        self.cond_table.setItem(i,j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def cant_cond(self):
        cant = self.combo_line_4.text().upper()

        if id!="":
            data = self.data_base.cant_cond(cant)
            if len(data)==0:
                msg = QMessageBox()
                msg.setWindowTitle("Error")
                msg.setText("Producto no encontrado")
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x= msg.exec_()
            else:
                self.cond_table.setRowCount(len(data))
                self.cond_table.setColumnCount(len(data[0]))
                
                for i,row in enumerate(data):
                    for j,column in enumerate(row):
                        self.cond_table.setItem(i,j, QtWidgets.QTableWidgetItem(str(column)))
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Rellene el campo')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            x = msg.exec_()
    
    def select_cond(self):
        option = self.combo_4.currentText()

        if option== "ID":
            self.id_cond()
        elif option=="VALOR_TOTAL":
            self.valtot_cond()
        elif option=="NUM_FACT":
            self.numfact_cond()
        elif option =="CANTIDAD":
            self.cant_cond()
    



if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin = Admin_store()
    admin.show()
    sys.exit(app.exec_())



