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
        self.refresh_bt.clicked.connect(self.show_products)
        self.updte_bt.clicked.connect(self.modify_products)
        self.search_bt.clicked.connect(self.search_name_updt)
        self.reg_pag_bt.clicked.connect(self.register_products)
        self.search_del_bt.clicked.connect(self.search_del_name)
        self.pagdel_bt.clicked.connect(self.delete_products)
        #Control title bar
        self.close.clicked.connect(lambda: self.close)
        self.maximize.clicked.connect(self.maximized)
        self.minimize.clicked.connect(self.minimized)
        self.hide.clicked.connect(self.hided)
        #Opacity hide title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Move UI
        self.tit_f.mouseMoveEvent = self.move_window
        #Control frame attatchement
        self.base_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.base_pag))
        self.regist_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.regist_pag))
        self.updt_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.updat_pag))
        self.delete_bt.clicked.connect(lambda:self.stackedWidget.setCurrentWidget(self.delet_pag))
        self.base_bt.clicked.connect(self.clear)
        self.regist_bt.clicked.connect(self.clear)
        self.updt_bt.clicked.connect(self.clear)
        self.delete_bt.clicked.connect(self.clear)
        
        self.prodc_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.del_table_prod.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.search_db.clicked.connect(self.gr_datab)
    def clear(self):
        self.indic_upd.setText("")
        self.indic_reg.setText("")
        self.indic_del.setText("")
    
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
        # tablerow=0
        self.prodc_table.clear()
        self.prodc_table.setRowCount(len(data))
        self.prodc_table.setColumnCount(len(data[0]))
        columnas=['ID_DB','REF.','NOMBRE','MATERIAL','PRECIO','COMPRADO','UTILIDAD','CANTIDAD','GRUPO']
        self.prodc_table.setHorizontalHeaderLabels(columnas)

        for i, row in enumerate(data):
            for j, column in enumerate(row):
                self.prodc_table.setItem(i, j, QtWidgets.QTableWidgetItem(str(column)))

          
    
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
            self.indic_reg.setText('Producto Registrado')
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
        self.indic_upd.setText("")
        self.indic_reg.setText("")
        self.indic_del.setText("")
        name_prod = self.name_sear_line.text().upper()
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
            self.indic_upd.setText("Producto Actualizado")
            self.ref_line.clear()
            self.name_line.clear()
            self.mat_line.clear()
            self.cant_line.clear()
            self.prec_line.clear()
            self.compr_line.clear()
            self.name_sear_line.setText("")
            self.id_updt_lab.setText("")
        
        elif action == 0:
            self.indic_upd.setText("Error")
        else:
            self.indic_upd.setText('Campos Vacios')
    
    def search_del_name(self):
        name_del = str(self.nam_sear_del_line.text().upper())
    
        if name_del!='':
            data = self.data_base.search(name_del)

            if len(data) == 0:
                msg = QMessageBox()
                msg.setWindowTitle('Error')
                msg.setText('Producto no encontrado')
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok)
                x = msg.exec_()
                
            else:
                self.indic_del.setText('Producto Encontrado')
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
        self.row_flag = self.del_table_prod.currentRow()
        if self.row_flag == 0:
            self.del_table_prod.removeRow(0)
            self.data_base.delete(self.product_name)
            self.indic_del.setText('Producto Eliminado')
            self.nam_sear_del_line.setText('')
    
    def gr_datab(self):
        group = self.gr_line.text().upper()

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

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    admin = Admin_store()
    admin.show()
    sys.exit(app.exec_())



