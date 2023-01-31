import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QHeaderView,QMessageBox
from PyQt5.QtCore import QPropertyAnimation,QEasingCurve,Qt,QPoint
from PyQt5 import QtCore,QtWidgets
from PyQt5.uic import loadUi
from sqlite_conection_employee import Conexion
from employee_store import Employee_store
from admin_store import Admin_store

class Login(QMainWindow):
    def __init__(self):
        super(Login,self).__init__()
        loadUi('login.ui',self)
        #Pages set up
        self.emp_bt.clicked.connect(lambda:self.pagWidget.setCurrentWidget(self.emp))
        self.admn_bt.clicked.connect(lambda:self.pagWidget.setCurrentWidget(self.adm))
        self.ps_emp_chng.clicked.connect(lambda:self.pagWidget.setCurrentWidget(self.emp_change))
        self.back_emp.clicked.connect(lambda:self.pagWidget.setCurrentWidget(self.emp))
        #Set menu bar
        self.clos.clicked.connect(lambda:self.close())
        #Set movement for ui
        self.super_f.mouseMoveEvent = self.moveWindow
        #Frameless window
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setWindowOpacity(1)
        #Incorporate admin and employee view
        self.admin = Admin_store()
        self.employee = Employee_store()
        #Link buttons to respective functions
        self.log_adm.clicked.connect(self.admin_log)
        self.log_emp.clicked.connect(self.employee_log)

        self.ps_emp_chng.clicked.connect(self.pas_change_emp)
        #Set parameters
        self.emp_pass = "Test"
        self.emp_user = "empleado"

        self.adm_pass = "AdminTest"
        self.adm_user = "admin"
        #Set Functions
    def employee_log(self):
        print("Here")
        user = self.user_emp.text()
        passw = self.pass_emp.text()

        if user == self.emp_user and passw == self.emp_pass:
            self.employee.show()
            self.hide()
        

    def admin_log(self):
        print(1)
        user = self.user_adm_line_2.text()
        passw = self.pass_adm.text()
        if user == self.adm_user and passw == self.adm_pass:
            self.admin.show()
            self.hide()
        if user != self.adm_user and passw ==self.adm_pass:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Usuario incorrecto')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()
        elif passw != self.adm_pass and user==self.adm_user:
            msg = QMessageBox()
            msg.setWindowTitle('Error')
            msg.setText('Contrasena incorrecta')
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()               


    def pas_change_emp(self):
        print(1)

    def mousePressEvent(self,event):        
        self.clicked_pos = event.globalPos()

    def moveWindow(self,event):
        delt = QPoint(event.globalPos() - self.clicked_pos)
        self.move(self.x()+delt.x(),self.y()+delt.y())
        self.clicked_pos = event.globalPos()
        if self.clicked_pos.y()<=10:
            self.maximized()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    employee = Employee_store()
    login = Login()
    login.show()
    sys.exit(app.exec_())


